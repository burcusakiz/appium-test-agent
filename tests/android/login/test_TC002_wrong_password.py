"""
Test Case: TC-0002 - Wrong Password
App: com.demo.loginapp
Suite: TS-0001-LOGIN
Priority: High
Tags: regression, login, negative
"""

import pytest


class TestTC002WrongPassword:
    """Test login fails with incorrect password"""

    VALID_USERNAME = "testuser"
    INVALID_PASSWORD = "wrongpass"

    @pytest.mark.regression
    @pytest.mark.login
    @pytest.mark.negative
    def test_invalid_password_shows_error(self, driver):
        """
        Verify login fails with appropriate error for wrong password.
        """
        from tests.page_objects.login_page import LoginPage

        login_page = LoginPage(driver)
        login_page.login(self.VALID_USERNAME, self.INVALID_PASSWORD)

        # Verify error message is displayed
        assert login_page.is_error_visible(), \
            "Error message should be visible for invalid password"

        # Verify user remains on login screen
        assert not login_page.is_logged_in(), \
            "User should remain on login screen after failed login"
