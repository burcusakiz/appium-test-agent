"""
REST API Login Tests
Tests the login endpoint via HTTP requests to the mock API server.
"""

import pytest
import requests

BASE_URL = "http://127.0.0.1:8080"


class TestLoginAPI:
    """Test cases for REST API login endpoint"""

    @pytest.mark.api
    @pytest.mark.login
    def test_login_valid_credentials(self):
        """
        Verify that the login endpoint returns success
        with valid credentials.
        """
        payload = {
            "username": "testuser",
            "password": "password123"
        }

        response = requests.post(
            f"{BASE_URL}/api/login",
            json=payload,
            timeout=5
        )

        assert response.status_code == 200
        data = response.json()
        assert data.get("success") is True
        assert "token" in data
        assert "user" in data
        assert data["user"]["username"] == "testuser"

    @pytest.mark.api
    @pytest.mark.login
    def test_login_invalid_username(self):
        """
        Verify that login fails with appropriate error
        for non-existent username.
        """
        payload = {
            "username": "invaliduser123",
            "password": "password123"
        }

        response = requests.post(f"{BASE_URL}/api/login", json=payload, timeout=5)

        assert response.status_code == 401
        data = response.json()
        assert data.get("success") is False
        assert "Invalid" in data.get("message", "") or "invalid" in data.get("message", "").lower()

    @pytest.mark.api
    @pytest.mark.login
    def test_login_invalid_password(self):
        """
        Verify that login fails with appropriate error
        for wrong password.
        """
        payload = {
            "username": "testuser",
            "password": "wrongpassword"
        }

        response = requests.post(f"{BASE_URL}/api/login", json=payload, timeout=5)

        assert response.status_code == 401
        data = response.json()
        assert data.get("success") is False

    @pytest.mark.api
    @pytest.mark.login
    def test_login_empty_json_object(self):
        """
        Verify that login fails with empty JSON object.
        """
        response = requests.post(f"{BASE_URL}/api/login", json={}, timeout=5)

        # Empty JSON object gets 401 since username/password are empty strings
        assert response.status_code in [400, 401]
        data = response.json()
        assert data.get("success") is False

    @pytest.mark.api
    @pytest.mark.login
    def test_login_empty_body(self):
        """
        Verify that login fails with empty request body (no JSON).
        """
        response = requests.post(f"{BASE_URL}/api/login", data="", timeout=5)

        # Empty body gets 400 for missing request body
        assert response.status_code == 400

    @pytest.mark.api
    @pytest.mark.login
    def test_login_missing_fields(self):
        """
        Verify that login fails when required fields are missing.
        """
        payload = {"username": "testuser"}  # missing password

        response = requests.post(f"{BASE_URL}/api/login", json=payload, timeout=5)

        # Mock API returns 401 for missing/empty password
        assert response.status_code == 401
        data = response.json()
        assert data.get("success") is False

    @pytest.mark.api
    def test_api_health_check(self):
        """
        Verify the mock API server is running and healthy.
        """
        response = requests.get(f"{BASE_URL}/api/health", timeout=5)

        assert response.status_code == 200
        data = response.json()
        assert data.get("status") == "ok"
        assert data.get("service") == "LoginMockAPI"
