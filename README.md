# HTTP Server Demo - Networking Fundamentals

A simple educational HTTP server built with Python's standard library (`http.server`) demonstrating core networking concepts including request handling, REST APIs, JSON data exchange, and static file serving.

## 📚 How HTTP Works

HTTP (HyperText Transfer Protocol) is the foundation of data communication on the web. Here's a quick overview:

### The Request-Response Cycle

```
┌─────────────┐         HTTP Request          ┌─────────────┐
│   Client    │  ──────────────────────────▶  │   Server    │
│  (Browser)  │  GET /api/users HTTP/1.1      │             │
│             │  Host: localhost:8080         │             │
└─────────────┘                               │  Processes  │
                                              │   Request   │
┌─────────────┘         HTTP Response         │             │
│   Client    │  ◀──────────────────────────  │             │
│  (Browser)  │  HTTP/1.1 200 OK              │             │
│ Displays    │  Content-Type: application/json└─────────────┘
│   Result    │  { "users": [...] }
└─────────────┘
```

### HTTP Methods

| Method | Purpose | Example |
|--------|---------|---------|
| **GET** | Retrieve data | `GET /api/users` - List all users |
| **POST** | Create resource | `POST /api/users` - Create new user |
| **PUT** | Update resource | `PUT /api/users/1` - Update user |
| **DELETE** | Remove resource | `DELETE /api/users/1` - Delete user |
| **OPTIONS** | Preflight check | Used for CORS |

### HTTP Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created successfully |
| 400 | Bad Request | Invalid request syntax |
| 404 | Not Found | Resource doesn't exist |
| 405 | Method Not Allowed | HTTP method not supported |
| 500 | Internal Server Error | Server encountered an error |

## 🚀 How to Run the Server

### Prerequisites

- Python 3.7+ (standard library only, no external dependencies!)

### Starting the Server

```bash
# Navigate to the project directory
cd /Users/yoshikondo/network-projects/http-server

# Make the server executable (optional)
chmod +x server.py

# Run the server with default settings (localhost:8080)
python3 server.py

# Or run on a different port
PORT=9000 python3 server.py

# Or bind to all network interfaces (0.0.0.0)
HOST=0.0.0.0 PORT=8080 python3 server.py
```

### Access the Application

Once running, open your browser to:

```
http://localhost:8080
```

You'll see a web interface demonstrating all the API endpoints.

## 🧪 Testing the Endpoints

### Using curl

#### Get Server Time
```bash
# Request current server time
curl -X GET http://localhost:8080/api/time

# Expected response:
# {
#   "success": true,
#   "time": {
#     "iso": "2024-01-15T10:30:45.123456",
#     "timestamp": 1705317045.123,
#     "readable": "2024-01-15 10:30:45"
#   }
# }
```

#### List All Users
```bash
# Get all users
curl -X GET http://localhost:8080/api/users

# Expected response:
# {
#   "success": true,
#   "count": 3,
#   "users": [
#     {"id": 1, "name": "Alice Johnson", "email": "alice@example.com", "role": "admin"},
#     {"id": 2, "name": "Bob Smith", "email": "bob@example.com", "role": "user"},
#     {"id": 3, "name": "Carol White", "email": "carol@example.com", "role": "user"}
#   ]
# }
```

#### Get Specific User
```bash
# Get user with ID 1
curl -X GET http://localhost:8080/api/users/1

# Expected response:
# {
#   "success": true,
#   "user": {
#     "id": 1,
#     "name": "Alice Johnson",
#     "email": "alice@example.com",
#     "role": "admin"
#   }
# }

# Try a non-existent user (404 error)
curl -X GET http://localhost:8080/api/users/999
```

#### Create New User
```bash
# Create a new user (POST with JSON body)
curl -X POST http://localhost:8080/api/users \
  -H "Content-Type: application/json" \
  -d '{"name": "David Lee", "email": "david@example.com", "role": "user"}'

# Expected response:
# {
#   "success": true,
#   "message": "User created successfully",
#   "user": {
#     "id": 4,
#     "name": "David Lee",
#     "email": "david@example.com",
#     "role": "user"
#   }
# }
```

#### Error Handling Test
```bash
# Invalid JSON (400 error)
curl -X POST http://localhost:8080/api/users \
  -H "Content-Type: application/json" \
  -d 'invalid json'

# Missing required fields (400 error)
curl -X POST http://localhost:8080/api/users \
  -H "Content-Type: application/json" \
  -d '{"name": "John"}'

# Invalid endpoint (404 error)
curl -X GET http://localhost:8080/api/invalid
```

### Using the Web Interface

Open `http://localhost:8080` in your browser and use the interactive demo:

1. **Server Time** - Click "Get Server Time" to see a simple GET request
2. **List Users** - View all users in a formatted table
3. **Get User** - Enter an ID and retrieve a specific user
4. **Create User** - Fill the form and submit to create a new user

## 🎓 Key Networking Concepts Demonstrated

### 1. HTTP Protocol Basics
- **Stateless Protocol**: Each request is independent; server doesn't remember previous requests
- **Text-Based**: Headers and (often) body are human-readable text
- **Request Line**: `METHOD /path HTTP/version`
- **Headers**: Key-value pairs with metadata about the request/response

### 2. REST API Design
REST (Representational State Transfer) is an architectural style:

```
GET    /api/users      → Collection: List all users
GET    /api/users/1    → Resource: Get user #1
POST   /api/users      → Collection: Create new user
```

### 3. JSON Data Exchange
JSON (JavaScript Object Notation) is the standard format for APIs:

```json
{
  "key": "value",
  "number": 42,
  "nested": {
    "array": [1, 2, 3]
  }
}
```

### 4. Static File Serving
The server demonstrates how web servers deliver files:
- HTML → Browser renders as a web page
- CSS → Browser applies styles
- JavaScript → Browser executes code

### 5. Request Logging
Every request is logged with:
- Timestamp
- HTTP method
- Request path
- Client IP address

```
2024-01-15 10:30:45 - GET /api/users - 127.0.0.1
```

### 6. Error Handling
Proper HTTP servers handle errors gracefully:
- Input validation
- Resource not found (404)
- Server errors (500)
- Structured error responses in JSON

### 7. Security Considerations
The server includes basic security measures:
- **Directory Traversal Protection**: Prevents `../../../etc/passwd` attacks
- **CORS Headers**: Controls cross-origin requests
- **Input Validation**: Validates JSON and required fields

## 📁 Project Structure

```
http-server/
├── server.py              # Main HTTP server (Python)
├── README.md              # This file
└── public/                # Static files directory
    ├── index.html         # Main web interface
    ├── style.css          # Styling
    └── script.js          # Frontend JavaScript
```

## 🔧 How It Works Under the Hood

### Python http.server Module

Python's built-in `http.server` provides:

1. **HTTPServer**: A socket server that listens for HTTP requests
2. **BaseHTTPRequestHandler**: A class to handle incoming requests

```python
# Create server instance
server = HTTPServer((host, port), RequestHandler)

# Start serving (blocks forever)
server.serve_forever()
```

### Request Handling Flow

```
1. Browser sends HTTP request
        ↓
2. HTTPServer receives the request
        ↓
3. BaseHTTPRequestHandler.do_GET() or do_POST() is called
        ↓
4. Our custom handler routes to appropriate method
        ↓
5. Response is sent back to browser
```

## 📝 Additional Notes

### In-Memory Data Store
This demo uses a simple Python list for users. In production, you would use:
- SQLite, PostgreSQL, or MySQL for persistence
- Redis for caching
- Proper data validation with libraries like Pydantic

### Scaling Considerations
This server is for educational purposes. For production:
- Use production WSGI servers (Gunicorn, uWSGI)
- Add rate limiting to prevent abuse
- Implement authentication/authorization
- Use HTTPS (TLS/SSL) for secure connections

## 📖 Resources

- [Python http.server Documentation](https://docs.python.org/3/library/http.server.html)
- [HTTP MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP)
- [REST API Tutorial](https://restfulapi.net/)
- [JSON Specification](https://www.json.org/)

## 🤝 License

This project is for educational purposes. Feel free to use and modify as needed.

---

**Happy Learning!** 🎓 Explore the code, experiment with the endpoints, and build your understanding of HTTP and web servers.
