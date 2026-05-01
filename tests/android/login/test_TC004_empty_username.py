"""
Test Case: TC-0004 - Empty Username
App: com.demo.loginapp
Suite: TS-0001-LOGIN
Priority: Medium
Tags: regression, login, negative
"""

import pytest


class TestTC004EmptyUsername:
    """Test login fails with empty username"""

    VALID_PASSWORD = "password123"

    @pytest.mark.regression
    @pytest.mark.login
    @pytest.mark.negative
    def test_empty_username_only(self, driver):
        """
        Verify login fails with empty username but valid password.
        """
        from tests.page_objects.login_page import LoginPage

        login_page = LoginPage(driver)
        login_page.enter_password(self.VALID_PASSWORD)
        login_page.click_login()

        # Verify error message is displayed
        assert login_page.is_error_visible(), \
            "Error message should be displayed for empty username"

        # Verify user remains on login screen
        assert not login_page.is_logged_in(), \
            "User should remain on login screen with empty username"
