"""
Test Case: TC-0001 - Valid Login
App: com.demo.loginapp
Suite: TS-0001-LOGIN
Priority: High
Tags: smoke, regression, login
"""

import pytest


class TestTC001ValidLogin:
    """Test valid login with correct credentials"""

    VALID_USERNAME = "testuser"
    VALID_PASSWORD = "password123"

    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.login
    def test_valid_login_shows_welcome_screen(self, driver):
        """
        Verify user can successfully login with valid credentials
        and is redirected to home screen.
        """
        from tests.page_objects.login_page import LoginPage
        from tests.page_objects.home_page import HomePage

        # Perform login
        login_page = LoginPage(driver)
        login_page.login(self.VALID_USERNAME, self.VALID_PASSWORD)

        # Verify home screen is displayed
        home_page = HomePage(driver)
        assert home_page.is_home_screen_visible(), \
            "Home screen should be visible after successful login"

        # Verify welcome message contains username
        welcome_msg = home_page.get_welcome_message()
        assert self.VALID_USERNAME in welcome_msg, \
            f"Welcome message '{welcome_msg}' should contain username '{self.VALID_USERNAME}'"

        # Verify logout button is visible
        assert home_page.is_logged_in(), \
            "Logout button should be visible after login"
