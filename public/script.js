/**
 * HTTP Server Demo - Frontend JavaScript
 * 
 * This script demonstrates how to make HTTP requests from a web browser
 * using the Fetch API. It shows all four types of requests:
 * - GET: Retrieve data
 * - POST: Create new data
 * - PUT: Update existing data (not used in this demo)
 * - DELETE: Remove data (not used in this demo)
 */

// Base URL for API requests
const API_BASE = '/api';

/**
 * Helper function to display results in the UI
 * @param {string} elementId - ID of the element to display in
 * @param {object} data - Data to display
 * @param {boolean} isError - Whether this is an error response
 */
function displayResult(elementId, data, isError = false) {
    const element = document.getElementById(elementId);
    element.className = `result show ${isError ? 'error' : 'success'}`;
    element.innerHTML = `<pre><code>${JSON.stringify(data, null, 2)}</code></pre>`;
}

/**
 * Fetch current server time
 * Demonstrates a simple GET request
 */
async function fetchTime() {
    const resultElement = document.getElementById('time-result');
    const button = document.getElementById('btn-time');
    
    button.disabled = true;
    resultElement.innerHTML = '<p>Loading...</p>';
    resultElement.className = 'result show';
    
    try {
        // Make GET request to /api/time
        const response = await fetch(`${API_BASE}/time`);
        const data = await response.json();
        
        displayResult('time-result', data);
    } catch (error) {
        displayResult('time-result', { error: error.message }, true);
    } finally {
        button.disabled = false;
    }
}

/**
 * Fetch all users
 * Demonstrates GET request with array response
 */
async function fetchUsers() {
    const resultElement = document.getElementById('users-result');
    const button = document.getElementById('btn-users');
    
    button.disabled = true;
    resultElement.innerHTML = '<p>Loading...</p>';
    resultElement.className = 'result show';
    
    try {
        const response = await fetch(`${API_BASE}/users`);
        const data = await response.json();
        
        if (data.success && data.users) {
            // Create a nice table display
            let html = `
                <p><strong>Total users:</strong> ${data.count}</p>
                <table class="user-table">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Name</th>
                            <th>Email</th>
                            <th>Role</th>
                        </tr>
                    </thead>
                    <tbody>
            `;
            
            data.users.forEach(user => {
                html += `
                    <tr>
                        <td>${user.id}</td>
                        <td>${user.name}</td>
                        <td>${user.email}</td>
                        <td><span class="badge badge-${user.role === 'admin' ? 'error' : 'get'}">${user.role}</span></td>
                    </tr>
                `;
            });
            
            html += '</tbody></table>';
            resultElement.innerHTML = html;
            resultElement.className = 'result show success';
        } else {
            displayResult('users-result', data);
        }
    } catch (error) {
        displayResult('users-result', { error: error.message }, true);
    } finally {
        button.disabled = false;
    }
}

/**
 * Fetch a specific user by ID
 * Demonstrates GET request with path parameter
 */
async function fetchUserById() {
    const userId = document.getElementById('user-id').value;
    const resultElement = document.getElementById('user-result');
    const button = document.getElementById('btn-user');
    
    if (!userId) {
        displayResult('user-result', { error: 'Please enter a user ID' }, true);
        return;
    }
    
    button.disabled = true;
    resultElement.innerHTML = '<p>Loading...</p>';
    resultElement.className = 'result show';
    
    try {
        // GET request with path parameter /api/users/<id>
        const response = await fetch(`${API_BASE}/users/${userId}`);
        const data = await response.json();
        
        if (!response.ok) {
            displayResult('user-result', data, true);
        } else {
            displayResult('user-result', data);
        }
    } catch (error) {
        displayResult('user-result', { error: error.message }, true);
    } finally {
        button.disabled = false;
    }
}

/**
 * Create a new user
 * Demonstrates POST request with JSON body
 */
async function createUser(event) {
    event.preventDefault();
    
    const resultElement = document.getElementById('create-result');
    const name = document.getElementById('new-name').value;
    const email = document.getElementById('new-email').value;
    const role = document.getElementById('new-role').value;
    
    resultElement.innerHTML = '<p>Creating user...</p>';
    resultElement.className = 'result show';
    
    try {
        // POST request with JSON body
        const response = await fetch(`${API_BASE}/users`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: name,
                email: email,
                role: role
            })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            displayResult('create-result', data, true);
        } else {
            displayResult('create-result', data);
            // Clear the form
            document.getElementById('create-user-form').reset();
        }
    } catch (error) {
        displayResult('create-result', { error: error.message }, true);
    }
}

/**
 * Allow Enter key to trigger user lookup
 */
document.addEventListener('DOMContentLoaded', () => {
    const userIdInput = document.getElementById('user-id');
    if (userIdInput) {
        userIdInput.addEventListener('keypress', (event) => {
            if (event.key === 'Enter') {
                fetchUserById();
            }
        });
    }
    
    console.log('🌐 HTTP Server Demo loaded!');
    console.log('Available API endpoints:');
    console.log('  GET  /api/time      - Get server time');
    console.log('  GET  /api/users     - List all users');
    console.log('  GET  /api/users/:id - Get specific user');
    console.log('  POST /api/users     - Create new user');
});
