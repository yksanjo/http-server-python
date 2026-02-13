#!/usr/bin/env python3
"""
Simple HTTP Server - Networking Fundamentals Demonstration
===========================================================

This server demonstrates core HTTP concepts using Python's standard library.
It handles static file serving and REST API endpoints.

Key Networking Concepts Demonstrated:
- HTTP request/response cycle
- RESTful API design
- JSON data exchange
- Status codes and error handling
- Request logging
"""

import json
import logging
import os
import time
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# Configure logging to see all incoming requests
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# In-memory "database" for demonstration purposes
# In production, this would be a real database
USERS = [
    {"id": 1, "name": "Alice Johnson", "email": "alice@example.com", "role": "admin"},
    {"id": 2, "name": "Bob Smith", "email": "bob@example.com", "role": "user"},
    {"id": 3, "name": "Carol White", "email": "carol@example.com", "role": "user"},
]

# Track the next ID for new users
NEXT_USER_ID = 4


class HTTPRequestHandler(BaseHTTPRequestHandler):
    """
    Custom request handler that routes requests to appropriate handlers.
    
    This class demonstrates how HTTP servers process different types of requests.
    Each HTTP method (GET, POST, etc.) has a corresponding do_METHOD handler.
    """

    def log_message(self, format, *args):
        """
        Override default logging to use our custom logger.
        Logs every request with timestamp, method, and path.
        """
        logger.info(f"{self.command} {self.path} - {self.client_address[0]}")

    def send_json_response(self, data, status_code=200):
        """
        Helper method to send JSON responses.
        
        Args:
            data: Python object to serialize to JSON
            status_code: HTTP status code (200=OK, 404=Not Found, etc.)
        """
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        # CORS headers - allow requests from any origin (for development)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        # Convert Python object to JSON bytes
        response_body = json.dumps(data, indent=2).encode('utf-8')
        self.wfile.write(response_body)

    def send_error_response(self, status_code, message):
        """
        Send a structured error response in JSON format.
        
        Args:
            status_code: HTTP error code
            message: Human-readable error message
        """
        error_data = {
            "error": True,
            "status_code": status_code,
            "message": message
        }
        self.send_json_response(error_data, status_code)

    def read_json_body(self):
        """
        Read and parse JSON from request body.
        
        Returns:
            Parsed JSON as Python object, or None if invalid
        """
        try:
            # Get content length from headers
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                return None
            
            # Read the request body
            body = self.rfile.read(content_length)
            # Parse JSON
            return json.loads(body.decode('utf-8'))
        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"Failed to parse JSON body: {e}")
            return None

    def serve_static_file(self, filepath):
        """
        Serve a static file from the public directory.
        
        Security note: This prevents directory traversal attacks by
        ensuring the resolved path stays within the public directory.
        
        Args:
            filepath: Requested file path
        """
        # Security: Prevent directory traversal
        # Resolve to absolute path and ensure it's within public directory
        public_dir = os.path.abspath('public')
        requested_path = os.path.abspath(os.path.join(public_dir, filepath))
        
        if not requested_path.startswith(public_dir):
            logger.warning(f"Directory traversal attempt blocked: {filepath}")
            self.send_error_response(403, "Access denied")
            return

        # Default to index.html if directory is requested
        if os.path.isdir(requested_path):
            requested_path = os.path.join(requested_path, 'index.html')

        if not os.path.exists(requested_path):
            self.send_error_response(404, f"File not found: {filepath}")
            return

        # Determine content type based on file extension
        content_types = {
            '.html': 'text/html',
            '.css': 'text/css',
            '.js': 'application/javascript',
            '.json': 'application/json',
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.gif': 'image/gif',
            '.svg': 'image/svg+xml',
        }
        ext = os.path.splitext(requested_path)[1].lower()
        content_type = content_types.get(ext, 'application/octet-stream')

        try:
            with open(requested_path, 'rb') as f:
                content = f.read()
            
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
            
        except Exception as e:
            logger.error(f"Error serving file {filepath}: {e}")
            self.send_error_response(500, "Internal server error")

    def do_GET(self):
        """
        Handle GET requests.
        
        GET requests are used to retrieve data from the server.
        They should not have side effects (read-only operations).
        """
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        # Route to appropriate handler based on path
        if path.startswith('/api/'):
            self.handle_api_get(path)
        else:
            # Serve static files
            # Remove leading slash and default to index.html
            filepath = path.lstrip('/')
            if not filepath:
                filepath = 'index.html'
            self.serve_static_file(filepath)

    def do_POST(self):
        """
        Handle POST requests.
        
        POST requests are used to create new resources or submit data.
        They typically include a request body with the data to be created.
        """
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path.startswith('/api/'):
            self.handle_api_post(path)
        else:
            self.send_error_response(405, "Method not allowed for this path")

    def do_OPTIONS(self):
        """
        Handle OPTIONS requests for CORS preflight.
        
        Browsers send OPTIONS before cross-origin POST/PUT/DELETE requests.
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def handle_api_get(self, path):
        """
        Route API GET requests to appropriate handlers.
        
        REST API endpoints:
        - GET /api/users        -> List all users
        - GET /api/users/<id>   -> Get specific user
        - GET /api/time         -> Get server time
        """
        global USERS

        # GET /api/users - List all users
        if path == '/api/users':
            self.send_json_response({
                "success": True,
                "count": len(USERS),
                "users": USERS
            })
            return

        # GET /api/users/<id> - Get specific user
        if path.startswith('/api/users/'):
            try:
                user_id = int(path.split('/')[-1])
                user = next((u for u in USERS if u['id'] == user_id), None)
                
                if user:
                    self.send_json_response({"success": True, "user": user})
                else:
                    self.send_error_response(404, f"User with ID {user_id} not found")
            except ValueError:
                self.send_error_response(400, "Invalid user ID format")
            return

        # GET /api/time - Get current server time
        if path == '/api/time':
            self.send_json_response({
                "success": True,
                "time": {
                    "iso": datetime.now().isoformat(),
                    "timestamp": time.time(),
                    "readable": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            })
            return

        # Unknown API endpoint
        self.send_error_response(404, f"API endpoint not found: {path}")

    def handle_api_post(self, path):
        """
        Handle API POST requests.
        
        REST API endpoints:
        - POST /api/users - Create a new user
        """
        global USERS, NEXT_USER_ID

        # POST /api/users - Create new user
        if path == '/api/users':
            data = self.read_json_body()
            
            if data is None:
                self.send_error_response(400, "Invalid JSON in request body")
                return

            # Validate required fields
            if 'name' not in data or 'email' not in data:
                self.send_error_response(400, "Missing required fields: name, email")
                return

            # Create new user
            new_user = {
                "id": NEXT_USER_ID,
                "name": data['name'],
                "email": data['email'],
                "role": data.get('role', 'user')  # Default role
            }
            
            USERS.append(new_user)
            NEXT_USER_ID += 1
            
            logger.info(f"Created new user: {new_user}")
            
            self.send_json_response({
                "success": True,
                "message": "User created successfully",
                "user": new_user
            }, status_code=201)  # 201 = Created
            return

        # Unknown API endpoint
        self.send_error_response(404, f"API endpoint not found: {path}")


def run_server(host='localhost', port=8080):
    """
    Start the HTTP server.
    
    Args:
        host: Hostname or IP to bind to (default: localhost)
        port: Port number to listen on (default: 8080)
    """
    server_address = (host, port)
    httpd = HTTPServer(server_address, HTTPRequestHandler)
    
    logger.info(f"=" * 50)
    logger.info(f"HTTP Server Starting...")
    logger.info(f"Server running at http://{host}:{port}")
    logger.info(f"Press Ctrl+C to stop")
    logger.info(f"=" * 50)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info("\nServer stopped by user")
        httpd.shutdown()


if __name__ == '__main__':
    # Allow port configuration via environment variable
    port = int(os.environ.get('PORT', 8080))
    host = os.environ.get('HOST', 'localhost')
    
    run_server(host=host, port=port)
