# API Testing Guide

**Purpose**: REST and SOAP API testing for backend service validation

**When to use**: When testing API endpoints, verifying request/response behavior, or validating data exchange formats

---

## Overview

### REST vs SOAP Comparison

| Feature | REST | SOAP |
|---------|------|------|
| Protocol | HTTP/HTTPS | HTTP/HTTPS/SMTP/etc |
| Data Format | JSON (preferred), XML | XML only |
| Style | Resource-based, URI-based | Action-based, WSDL-defined |
| Complexity | Simple, lightweight | Complex, enterprise |
| Caching | Supports caching | No built-in caching |
| Security | OAuth, JWT | WS-Security (enterprise grade) |
| Documentation | OpenAPI/Swagger | WSDL |

---

## REST API Testing

### Basic Request Patterns

#### GET Request
```python
import requests

BASE_URL = "http://localhost:8080/api/v1"

def test_get_user_profile():
    """Test GET /users/{id} endpoint"""
    user_id = 12345
    response = requests.get(f"{BASE_URL}/users/{user_id}")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["id"] == user_id
    assert "name" in data
    assert "email" in data
```

#### POST Request (Create)
```python
def test_create_user():
    """Test POST /users endpoint"""
    payload = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "role": "user"
    }
    
    response = requests.post(
        f"{BASE_URL}/users",
        json=payload
    )
    
    assert response.status_code == 201
    data = response.json()
    
    assert data["name"] == payload["name"]
    assert "id" in data
    return data["id"]  # Return created ID for other tests
```

#### PUT/PATCH Request (Update)
```python
def test_update_user():
    """Test PUT /users/{id} endpoint"""
    user_id = 12345
    payload = {
        "name": "John Doe Updated",
        "role": "admin"
    }
    
    response = requests.put(
        f"{BASE_URL}/users/{user_id}",
        json=payload
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == payload["name"]
```

#### DELETE Request
```python
def test_delete_user():
    """Test DELETE /users/{id} endpoint"""
    user_id = 12345
    
    response = requests.delete(f"{BASE_URL}/users/{user_id}")
    
    assert response.status_code == 204
    
    # Verify deletion
    get_response = requests.get(f"{BASE_URL}/users/{user_id}")
    assert get_response.status_code == 404
```

### Headers and Authentication

#### Bearer Token Authentication
```python
def test_authenticated_request():
    """Test request with Bearer token"""
    # Login first
    login_response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"username": "testuser", "password": "password123"}
    )
    token = login_response.json()["token"]
    
    # Use token in subsequent requests
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(
        f"{BASE_URL}/users/profile",
        headers=headers
    )
    
    assert response.status_code == 200
```

#### Custom Headers
```python
def test_request_with_custom_headers():
    """Test request with API key and version headers"""
    headers = {
        "X-API-Key": "your-api-key",
        "X-API-Version": "v1",
        "Accept": "application/json"
    }
    
    response = requests.get(
        f"{BASE_URL}/products",
        headers=headers
    )
    
    assert response.status_code == 200
```

---

## Request Validation

### Status Code Categories
```python
import requests

# 2xx Success
assert response.status_code == 200  # OK
assert response.status_code == 201  # Created
assert response.status_code == 204  # No Content

# 4xx Client Error
assert response.status_code == 400  # Bad Request
assert response.status_code == 401  # Unauthorized
assert response.status_code == 403  # Forbidden
assert response.status_code == 404  # Not Found

# 5xx Server Error
assert response.status_code == 500  # Internal Server Error
assert response.status_code == 503  # Service Unavailable
```

### JSON Response Validation
```python
def validate_user_response(data: dict):
    """Validate user response structure"""
    required_fields = ["id", "name", "email", "created_at"]
    
    for field in required_fields:
        assert field in data, f"Missing required field: {field}"
    
    # Type validation
    assert isinstance(data["id"], int), "ID should be integer"
    assert isinstance(data["name"], str), "Name should be string"
    assert isinstance(data["email"], str), "Email should be string"
    
    # Format validation
    assert "@" in data["email"], "Invalid email format"
```

### Response Schema Validation (using jsonschema)
```python
from jsonschema import validate, ValidationError

USER_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string", "minLength": 1},
        "email": {"type": "string", "format": "email"},
        "role": {"type": "string", "enum": ["user", "admin", "moderator"]},
        "created_at": {"type": "string", "format": "date-time"}
    },
    "required": ["id", "name", "email", "role"]
}

def test_response_schema():
    """Validate response against JSON schema"""
    response = requests.get(f"{BASE_URL}/users/123")
    data = response.json()
    
    validate(instance=data, schema=USER_SCHEMA)
```

---

## API Testing Patterns

### 1. Test Data Management
```python
import pytest

@pytest.fixture
def test_user_data():
    """Generate test user data"""
    import random
    import string
    
    def _generate_email():
        random_str = ''.join(random.choices(string.ascii_lowercase, k=8))
        return f"testuser_{random_str}@example.com"
    
    return {
        "name": "Test User",
        "email": _generate_email(),
        "password": "TestPassword123!"
    }

def test_create_user_with_fixture(test_user_data):
    response = requests.post(f"{BASE_URL}/users", json=test_user_data)
    assert response.status_code == 201
```

### 2. Test Data Cleanup
```python
@pytest.fixture
def create_and_cleanup_user():
    """Create user and cleanup after test"""
    created_ids = []
    
    def _create_user(data):
        response = requests.post(f"{BASE_URL}/users", json=data)
        user_id = response.json()["id"]
        created_ids.append(user_id)
        return response
    
    yield _create_user
    
    # Cleanup - delete all created users
    for user_id in created_ids:
        requests.delete(f"{BASE_URL}/users/{user_id}")

def test_create_user_with_cleanup(create_and_cleanup_user):
    response = create_and_cleanup_user({"name": "Cleanup Test", "email": "cleanup@example.com"})
    assert response.status_code == 201
```

### 3. Parametrized Testing
```python
import pytest

@pytest.mark.parametrize("username,password,expected_status", [
    ("valid_user", "valid_pass", 200),
    ("invalid_user", "valid_pass", 401),
    ("valid_user", "invalid_pass", 401),
    ("", "valid_pass", 400),
    ("valid_user", "", 400),
])
def test_login_endpoint(username, password, expected_status):
    payload = {"username": username, "password": password}
    response = requests.post(f"{BASE_URL}/auth/login", json=payload)
    assert response.status_code == expected_status
```

### 4. API Chain Testing
```python
def test_complete_user_journey():
    """Test complete user registration and login flow"""
    
    # Step 1: Register user
    user_data = {
        "name": "Chain Test User",
        "email": "chain_test@example.com",
        "password": "Password123!"
    }
    
    register_response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
    assert register_response.status_code == 201
    user_id = register_response.json()["id"]
    
    # Step 2: Login
    login_response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"email": user_data["email"], "password": user_data["password"]}
    )
    assert login_response.status_code == 200
    token = login_response.json()["token"]
    
    # Step 3: Get user profile
    headers = {"Authorization": f"Bearer {token}"}
    profile_response = requests.get(f"{BASE_URL}/users/profile", headers=headers)
    assert profile_response.status_code == 200
    
    # Step 4: Update profile
    update_response = requests.put(
        f"{BASE_URL}/users/profile",
        headers=headers,
        json={"bio": "Test bio"}
    )
    assert update_response.status_code == 200
    
    # Cleanup
    requests.delete(f"{BASE_URL}/users/{user_id}", headers=headers)
```

---

## SOAP API Testing

### SOAP Request Structure
```python
import requests
from zeep import Client
from lxml import etree

WSDL_URL = "http://localhost:8080/soap/login?wsdl"

def test_soap_login_with_zeep():
    """Test SOAP login using Zeep client"""
    client = Client(WSDL_URL)
    
    result = client.service.Login(
        username="testuser",
        password="password123"
    )
    
    assert result.success == True
    assert result.token is not None
    assert result.user is not None

def test_soap_login_raw():
    """Test SOAP login with raw XML"""
    soap_body = """<?xml version="1.0" encoding="UTF-8"?>
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" 
                      xmlns:login="http://api.example.com/login">
       <soapenv:Header/>
       <soapenv:Body>
          <login:Login>
             <login:username>testuser</login:username>
             <login:password>password123</login:password>
          </login:Login>
       </soapenv:Body>
    </soapenv:Envelope>"""
    
    headers = {
        "Content-Type": "text/xml; charset=utf-8",
        "SOAPAction": "http://api.example.com/login/Login"
    }
    
    response = requests.post(
        "http://localhost:8080/soap/login",
        data=soap_body,
        headers=headers
    )
    
    assert response.status_code == 200
    assert "success" in response.text
```

### SOAP WSDL Analysis
```python
def analyze_soap_service():
    """Analyze available SOAP operations"""
    client = Client(WSDL_URL)
    
    # List all services
    print("Services:", client.wsdl.services)
    
    # List operations for each port
    for service in client.wsdl.services.values():
        for port in service.ports.values():
            print(f"Operations in {port.name}:")
            for operation in port.binding.operations.values():
                print(f"  - {operation.name}")
```

---

## Mock API Server

### Flask Mock Server
```python
"""
mock_api_server.py - Simple REST API mock server
"""

from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory data store
users = {
    "testuser": {
        "id": 1,
        "name": "Test User",
        "email": "testuser@example.com",
        "password": "password123"
    }
}

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok", "service": "MockAPI"}), 200

@app.route('/api/login', methods=['POST'])
def login():
    """Login endpoint"""
    data = request.get_json()
    
    if not data:
        return jsonify({
            "success": False,
            "message": "Request body is required"
        }), 400
    
    username = data.get("username", "")
    password = data.get("password", "")
    
    if not username or not password:
        return jsonify({
            "success": False,
            "message": "Username and password are required"
        }), 400
    
    # Simple validation (in production, check database)
    if username in users and users[username]["password"] == password:
        return jsonify({
            "success": True,
            "token": "mock_jwt_token_12345",
            "user": {
                "id": users[username]["id"],
                "name": users[username]["name"],
                "email": users[username]["email"]
            }
        }), 200
    
    return jsonify({
        "success": False,
        "message": "Invalid username or password",
        "token": None
    }), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
```

---

## Performance Testing

### Response Time Testing
```python
import time
import statistics

def test_response_time():
    """Test API response time meets SLA"""
    response_times = []
    iterations = 10
    
    for _ in range(iterations):
        start = time.time()
        response = requests.get(f"{BASE_URL}/products")
        end = time.time()
        response_times.append((end - start) * 1000)  # Convert to ms
    
    avg_time = statistics.mean(response_times)
    max_time = max(response_times)
    
    print(f"Average response time: {avg_time:.2f}ms")
    print(f"Max response time: {max_time:.2f}ms")
    
    # SLA check
    assert avg_time < 500, f"Average response time {avg_time}ms exceeds SLA of 500ms"
    assert max_time < 1000, f"Max response time {max_time}ms exceeds threshold"
```

### Load Testing (Basic)
```python
import threading
import queue
import time

def make_request(result_queue, url):
    """Make a single request and record result"""
    try:
        start = time.time()
        response = requests.get(url, timeout=10)
        elapsed = (time.time() - start) * 1000
        result_queue.put({
            "success": True,
            "status": response.status_code,
            "time_ms": elapsed
        })
    except Exception as e:
        result_queue.put({
            "success": False,
            "error": str(e)
        })

def test_concurrent_users():
    """Test API with multiple concurrent users"""
    url = f"{BASE_URL}/products"
    num_users = 20
    result_queue = queue.Queue()
    
    threads = []
    for _ in range(num_users):
        t = threading.Thread(target=make_request, args=(result_queue, url))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    # Analyze results
    results = []
    while not result_queue.empty():
        results.append(result_queue.get())
    
    successes = sum(1 for r in results if r["success"])
    print(f"Success rate: {successes}/{len(results)}")
    
    assert successes == len(results), "Some requests failed"
```

---

## Testing Best Practices

### ✅ DO
1. Test all HTTP methods (GET, POST, PUT, PATCH, DELETE)
2. Test success AND failure scenarios
3. Validate response status codes
4. Validate response body structure
5. Test edge cases (empty values, special characters, null values)
6. Use environment variables for URLs
7. Mock external dependencies
8. Run API tests in CI/CD pipeline
9. Keep tests independent (can run in any order)
10. Document API behavior alongside tests

### ❌ DON'T
1. Don't hardcode credentials
2. Don't skip assertions
3. Don't rely on test execution order
4. Don't test multiple things in one test
5. Don't use sleep() - use proper waits
6. Don't leave test data in production
7. Don't test implementation details, only behavior

---

## Pytest Configuration

### pytest.ini
```ini
[pytest]
# Test organization
testpaths = tests/api
python_files = test_*.py
python_classes = Test*
python_functions = test_*

# Markers
markers =
    smoke: Quick critical path tests
    regression: Full feature coverage tests
    integration: Tests involving multiple services
    performance: Performance testing tests

# Verbose output
addopts = -v --tb=short --strict-markers

# HTML report
htmlreport = reports/api_test_report.html
```

### run_api_tests.py
```python
#!/usr/bin/env python3
"""API Test Runner"""

import subprocess
import sys
import os
from datetime import datetime

def run_tests():
    """Run API tests with pytest"""
    os.environ["BASE_URL"] = "http://localhost:8080/api/v1"
    
    cmd = [
        "pytest",
        "tests/api/",
        "-v",
        "--html=reports/api_report.html",
        "--self-contained-html",
        "--tb=short"
    ]
    
    if len(sys.argv) > 1 and sys.argv[1] == "smoke":
        cmd.extend(["-m", "smoke"])
    
    result = subprocess.run(cmd)
    return result.returncode

if __name__ == "__main__":
    exit(run_tests())
```

---

## Common HTTP Status Codes Reference

| Code | Meaning | When to Expect |
|------|---------|----------------|
| 200 | OK | Successful GET/PUT/PATCH |
| 201 | Created | Successful POST |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Invalid request body |
| 401 | Unauthorized | Missing/invalid auth |
| 403 | Forbidden | Auth OK, no permission |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Duplicate resource |
| 422 | Unprocessable | Valid JSON, invalid data |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Server Error | Backend error |
| 503 | Service Unavailable | Service down |

---

## References

- [REST API Design Best Practices](https://restfulapi.net/)
- [HTTP Status Codes](https://httpstatusdogs.com/)
- [OpenAPI Specification](https://swagger.io/specification/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Requests Library Docs](https://requests.readthedocs.io/)
