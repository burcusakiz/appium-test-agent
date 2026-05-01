#!/usr/bin/env python3
"""
Simple Python-based Mock REST API Server for Login Service
This serves as an alternative to SoapUI for environments where SoapUI is not available.
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import sys

VALID_USERNAME = "testuser"
VALID_PASSWORD = "password123"


class LoginAPIHandler(BaseHTTPRequestHandler):
    """Handler for the Login Mock API"""

    def log_message(self, format, *args):
        """Custom log message format"""
        print(f"[{self.log_date_time_string()}] {format % args}")

    def send_json_response(self, status_code, data):
        """Send a JSON response"""
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        """Handle POST requests"""
        if self.path == "/api/login":
            self.handle_login()
        else:
            self.send_json_response(404, {"error": "Not found"})

    def do_GET(self):
        """Handle GET requests"""
        if self.path == "/api/health":
            self.send_json_response(200, {"status": "ok", "service": "LoginMockAPI"})
        else:
            self.send_json_response(404, {"error": "Not found"})

    def handle_login(self):
        """Handle login request"""
        content_length = int(self.headers.get("Content-Length", 0))

        if content_length == 0:
            self.send_json_response(400, {
                "success": False,
                "message": "Request body is required"
            })
            return

        request_body = self.rfile.read(content_length).decode("utf-8")

        try:
            request_data = json.loads(request_body)
        except json.JSONDecodeError:
            self.send_json_response(400, {
                "success": False,
                "message": "Invalid JSON format"
            })
            return

        username = request_data.get("username", "")
        password = request_data.get("password", "")

        print(f"[Login Attempt] Username: {username}")

        if username == VALID_USERNAME and password == VALID_PASSWORD:
            # Successful login
            self.send_json_response(200, {
                "success": True,
                "message": "Login successful",
                "token": "mock_jwt_token_12345",
                "user": {
                    "username": username,
                    "email": "testuser@example.com",
                    "displayName": "Test User"
                }
            })
            print(f"[Login Success] User '{username}' logged in successfully")
        else:
            # Failed login
            self.send_json_response(401, {
                "success": False,
                "message": "Invalid username or password",
                "token": None,
                "error": "Unauthorized"
            })
            print(f"[Login Failed] Invalid credentials for user '{username}'")

    def do_PUT(self):
        """Handle PUT requests"""
        self.send_json_response(405, {"error": "Method not allowed"})

    def do_DELETE(self):
        """Handle DELETE requests"""
        self.send_json_response(405, {"error": "Method not allowed"})


def run_mock_server(host="127.0.0.1", port=8080):
    """Run the mock API server"""
    server_address = (host, port)
    httpd = HTTPServer(server_address, LoginAPIHandler)
    print(f"Mock API Server starting on http://{host}:{port}")
    print(f"Endpoint: http://{host}:{port}/api/login")
    print(f"Health check: http://{host}:{port}/api/health")
    print("")
    print("Press Ctrl+C to stop the server")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        httpd.server_close()


if __name__ == "__main__":
    HOST = "127.0.0.1"
    PORT = 8080

    if len(sys.argv) > 1:
        try:
            PORT = int(sys.argv[1])
        except ValueError:
            print(f"Invalid port number: {sys.argv[1]}")
            print("Usage: python mock_api_server.py [port]")
            sys.exit(1)

    run_mock_server(HOST, PORT)
