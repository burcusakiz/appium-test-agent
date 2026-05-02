"""
Data-Driven Login Tests
Using pytest.mark.parametrize for comprehensive test coverage
"""

import pytest
from tests.page_objects.login_page import LoginPage
from tests.page_objects.home_page import HomePage
from tests.config.test_data import TestData, INVALID_CREDENTIALS


class TestDataDrivenLogin:
    """Data-driven test cases using pytest parametrize"""

    test_data = TestData()

    @pytest.mark.smoke
    @pytest.mark.login
    @pytest.mark.parametrize("username,password", [
        ("testuser", "password123"),
        ("demo_user", "demo123456"),
    ])
    def test_valid_login_variations(self, driver, username, password):
        """Test multiple valid credential combinations"""
        login_page = LoginPage(driver)
        login_page.login(username, password)

        assert HomePage(driver).is_home_screen_visible(), \
            f"Home screen should be visible for user: {username}"

        welcome_msg = HomePage(driver).get_welcome_message()
        assert username in welcome_msg, \
            f"Welcome message should contain username: {username}"

    @pytest.mark.regression
    @pytest.mark.negative
    @pytest.mark.parametrize("username,password,expected_error", [
        ("", "", "Please enter username and password"),
        ("testuser", "", "Please enter username and password"),
        ("", "password123", "Please enter username and password"),
        ("invaliduser", "wrongpass", "Invalid credentials"),
        ("testuser", "wrongpass", "Invalid credentials"),
    ])
    def test_invalid_credentials(self, driver, username, password, expected_error):
        """Test various invalid credential combinations"""
        login_page = LoginPage(driver)
        success, actual_error = login_page.login_with_error_check(username, password)

        assert not success, f"Login should fail for username: {username}"

        # Check error message (exact or contains)
        if expected_error:
            assert expected_error.lower() in actual_error.lower() or \
                   actual_error.lower() in expected_error.lower(), \
                f"Expected error to contain: '{expected_error}', got: '{actual_error}'"

    @pytest.mark.regression
    @pytest.mark.parametrize("field_to_clear", [
        "username",
        "password",
        "both",
    ])
    def test_empty_field_combinations(self, driver, field_to_clear):
        """Test empty field combinations"""
        login_page = LoginPage(driver)

        if field_to_clear != "password":
            login_page.enter_username("testuser")
        if field_to_clear != "username":
            login_page.enter_password("password123")

        success, error = login_page.login_with_error_check("", "")

        assert not success, "Login should fail when empty fields are provided"
        assert login_page.is_error_visible(), "Error should be visible"

    @pytest.mark.regression
    @pytest.mark.parametrize("test_data", [
        {"username": "testuser", "password": "password123"},
        {"username": "testuser", "password": "wrongpass"},
        {"username": "", "password": ""},
    ])
    def test_dynamic_credentials(self, driver, test_data):
        """Test with dynamic credential dictionary"""
        login_page = LoginPage(driver)
        success, error = login_page.login_with_error_check(
            test_data["username"],
            test_data["password"]
        )

        if test_data["username"] == "testuser" and test_data["password"] == "password123":
            assert success, "Valid credentials should succeed"
        else:
            assert not success, "Invalid credentials should fail"

    @pytest.mark.smoke
    @pytest.mark.login
    def test_login_logout_flow(self, driver):
        """Test complete login -> logout flow"""
        login_page = LoginPage(driver)
        home_page = HomePage(driver)

        # Login
        login_page.login(
            self.test_data.valid_username,
            self.test_data.valid_password
        )
        assert home_page.is_home_screen_visible(), "Should land on home screen"

        # Logout
        home_page.click_logout()
        assert login_page.is_username_field_visible(), "Should return to login screen"


@pytest.mark.regression
@pytest.mark.login
@pytest.mark.parametrize("username,password,expected", [
    ("testuser", "password123", True),
    ("testuser", "wrongpass", False),
    ("wronguser", "password123", False),
    ("", "password123", False),
    ("testuser", "", False),
    ("", "", False),
])
def test_login_with_fixture(driver, username, password, expected):
    """Simple parametrized test using driver fixture"""
    login_page = LoginPage(driver)
    success, _ = login_page.login_with_error_check(username, password)

    assert success == expected, \
        f"Login should {'succeed' if expected else 'fail'} for user: {username}"