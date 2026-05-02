"""
Test Data Management - Centralized Configuration
"""

# Valid credentials for positive tests
VALID_USERS = [
    {"username": "testuser", "password": "password123"},
    {"username": "demo_user", "password": "demo123456"},
]

# Invalid credentials for negative tests
INVALID_CREDENTIALS = [
    {"username": "", "password": "", "error": "Please enter username and password"},
    {"username": "testuser", "password": "", "error": "Please enter username and password"},
    {"username": "", "password": "password123", "error": "Please enter username and password"},
    {"username": "invaliduser", "password": "wrongpass", "error": "Invalid credentials"},
    {"username": "testuser", "password": "wrongpass", "error": "Invalid credentials"},
]

# Test constants
TEST_DATA = {
    "app": {
        "package": "com.demo.loginapp",
        "activity": ".LoginActivity",
        "valid_username": "testuser",
        "valid_password": "password123",
    },
    "api": {
        "base_url": "http://127.0.0.1:8080",
        "login_endpoint": "/api/login",
    },
    "timeouts": {
        "implicit": 10,
        "explicit": 15,
        "page_load": 30,
    },
}


class TestData:
    """Test data class for better organization"""

    __test__ = False

    def __init__(self):
        self.valid_users = VALID_USERS
        self.invalid_credentials = INVALID_CREDENTIALS
        self.app_package = TEST_DATA["app"]["package"]
        self.app_activity = TEST_DATA["app"]["activity"]
        self.valid_username = TEST_DATA["app"]["valid_username"]
        self.valid_password = TEST_DATA["app"]["valid_password"]
        self.base_url = TEST_DATA["api"]["base_url"]
        self.implicit_timeout = TEST_DATA["timeouts"]["implicit"]
        self.explicit_timeout = TEST_DATA["timeouts"]["explicit"]

    def get_valid_user(self, index=0):
        """Get valid user by index"""
        return self.valid_users[index % len(self.valid_users)]

    def get_invalid_credential(self, index=0):
        """Get invalid credential by index"""
        return self.invalid_credentials[index % len(self.invalid_credentials)]

    def get_all_test_cases(self):
        """Get all test case configurations"""
        return {
            "valid_login": self.valid_users,
            "invalid_login": self.invalid_credentials,
        }
