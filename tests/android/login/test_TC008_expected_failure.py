"""
Test Case: TC-0008 - Expected Failure (Screenshot Testing)
App: com.demo.loginapp
Suite: TS-0001-LOGIN
Priority: Low
Tags: regression, login, negative

This test FAILS intentionally to demonstrate screenshot capture on failure.
The test expects home screen but login fails, triggering screenshot save.
"""

import pytest


class TestTC008ExpectedFailure:
    """Test that fails intentionally to show screenshot capture"""

    @pytest.mark.regression
    @pytest.mark.login
    @pytest.mark.negative
    def test_login_should_fail_but_capture_screenshot(self, driver):
        """
        INTENTIONALLY FAILING TEST - for screenshot demonstration.

        This test:
        1. Logs in with WRONG password (so login fails)
        2. Expects home screen (which won't be visible)
        3. Triggers failure hook that captures screenshot
        """
        from tests.page_objects.login_page import LoginPage
        from tests.page_objects.home_page import HomePage

        login_page = LoginPage(driver)
        login_page.login("testuser", "wrongpassword")

        # INTENTIONAL FAILURE: expect home screen but it won't be visible
        home_page = HomePage(driver)
        assert home_page.is_home_screen_visible(), \
            "INTENTIONAL FAILURE: Home screen should NOT be visible after wrong password"

        # This line never executes due to assertion failure above
        assert False, "Test failed intentionally to demonstrate screenshot capture"
