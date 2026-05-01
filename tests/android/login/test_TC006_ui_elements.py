"""
Test Case: TC-0006 - UI Elements Visible
App: com.demo.loginapp
Suite: TS-0001-LOGIN
Priority: Medium
Tags: smoke, regression, ui
"""

import pytest


class TestTC006UIElements:
    """Test all expected UI elements are visible on login screen"""

    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.ui
    def test_title_and_subtitle_visible(self, driver):
        """
        Verify all UI elements are visible on login screen.
        """
        from appium.webdriver.common.appiumby import AppiumBy

        # Verify Title - "Welcome Back"
        title = driver.find_element(AppiumBy.ID, "com.demo.loginapp:id/textViewTitle")
        assert title.is_displayed(), "Title should be visible"
        assert "Welcome" in title.text, "Title should contain 'Welcome'"

        # Verify Subtitle - contains "sign in" text
        subtitle = driver.find_element(AppiumBy.ID, "com.demo.loginapp:id/textViewSubtitle")
        assert subtitle.is_displayed(), "Subtitle should be visible"
        assert "sign in" in subtitle.text.lower(), "Subtitle should contain 'sign in'"

        # Verify Username Input
        username_input = driver.find_element(AppiumBy.ID, "com.demo.loginapp:id/username_input")
        assert username_input.is_displayed(), "Username input should be visible"
        assert username_input.is_enabled(), "Username input should be enabled"

        # Verify Password Input
        password_input = driver.find_element(AppiumBy.ID, "com.demo.loginapp:id/password_input")
        assert password_input.is_displayed(), "Password input should be visible"
        assert password_input.is_enabled(), "Password input should be enabled"

        # Verify Login Button
        login_button = driver.find_element(AppiumBy.ID, "com.demo.loginapp:id/login_button")
        assert login_button.is_displayed(), "Login button should be visible"
        assert login_button.text == "LOGIN", "Login button text should be 'LOGIN'"

        # Verify Register Link
        register_link = driver.find_element(AppiumBy.ID, "com.demo.loginapp:id/linkRegister")
        assert register_link.is_displayed(), "Register link should be visible"
        assert "register" in register_link.text.lower(), "Register link should contain 'register'"
