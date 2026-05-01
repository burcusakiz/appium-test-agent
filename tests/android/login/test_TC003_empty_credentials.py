"""
Test Case: TC-0003 - Empty Credentials
App: com.demo.loginapp
Suite: TS-0001-LOGIN
Priority: High
Tags: regression, login, negative
"""

import pytest


class TestTC003EmptyCredentials:
    """Test login fails with empty credentials"""

    @pytest.mark.regression
    @pytest.mark.login
    @pytest.mark.negative
    def test_empty_username_and_password_shows_error(self, driver):
        """
        Verify login fails with empty credentials.
        """
        from tests.page_objects.login_page import LoginPage

        login_page = LoginPage(driver)
        login_page.click_login()

        # Verify error message is displayed
        assert login_page.is_error_visible(), \
            "Error should be displayed for empty credentials"

        # Verify user remains on login screen
        assert not login_page.is_logged_in(), \
            "User should remain on login screen with empty credentials"
