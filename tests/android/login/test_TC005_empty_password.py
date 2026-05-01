"""
Test Case: TC-0005 - Empty Password
App: com.demo.loginapp
Suite: TS-0001-LOGIN
Priority: Medium
Tags: regression, login, negative
"""

import pytest


class TestTC005EmptyPassword:
    """Test login fails with empty password"""

    VALID_USERNAME = "testuser"

    @pytest.mark.regression
    @pytest.mark.login
    @pytest.mark.negative
    def test_empty_password_only(self, driver):
        """
        Verify login fails with valid username but empty password.
        """
        from tests.page_objects.login_page import LoginPage

        login_page = LoginPage(driver)
        login_page.enter_username(self.VALID_USERNAME)
        login_page.click_login()

        # Verify error message is displayed
        assert login_page.is_error_visible(), \
            "Error message should be displayed for empty password"

        # Verify user remains on login screen
        assert not login_page.is_logged_in(), \
            "User should remain on login screen with empty password"
