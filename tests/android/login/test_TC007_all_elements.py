"""
Test Case: TC-0007 - All UI Elements Visible
App: com.demo.loginapp
Suite: TS-0001-LOGIN
Priority: Low
Tags: regression, ui, comprehensive
"""

import pytest


class TestTC007AllElements:
    """Test complete UI validation - all elements present and functional"""

    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.comprehensive
    def test_all_ui_elements_visible(self, driver):
        """
        Verify all 6 UI elements are present, enabled, and have correct text values.
        """
        from appium.webdriver.common.appiumby import AppiumBy

        # Collect all elements
        elements = {
            "Title": ("com.demo.loginapp:id/textViewTitle", lambda e: "Welcome" in e.text),
            "Subtitle": ("com.demo.loginapp:id/textViewSubtitle", lambda e: "sign in" in e.text.lower()),
            "Username Input": ("com.demo.loginapp:id/username_input", lambda e: e.is_enabled()),
            "Password Input": ("com.demo.loginapp:id/password_input", lambda e: e.is_enabled()),
            "Login Button": ("com.demo.loginapp:id/login_button", lambda e: e.text == "LOGIN"),
            "Register Link": ("com.demo.loginapp:id/linkRegister", lambda e: "register" in e.text.lower()),
        }

        visible_count = 0
        for name, (locator, check) in elements.items():
            element = driver.find_element(AppiumBy.ID, locator)
            assert element.is_displayed(), f"{name} should be visible"
            assert check(element), f"{name} should have correct value"
            visible_count += 1

        assert visible_count == 6, "All 6 UI elements should be visible"
