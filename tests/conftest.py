"""
Appium Test Framework - Configuration and Fixtures
"""

import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
import os
from datetime import datetime
import pytest_html

# Test configuration
BASE_URL = "http://127.0.0.1:4723"
APP_PACKAGE = "com.demo.loginapp"
APP_ACTIVITY = ".LoginActivity"
PLATFORM_VERSION = "14.0"
DEVICE_NAME = "emulator-5554"


def get_appium_options():
    """Configure Appium capabilities for Android"""
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.platform_version = os.getenv("PLATFORM_VERSION", PLATFORM_VERSION)
    options.device_name = os.getenv("DEVICE_NAME", DEVICE_NAME)
    options.app_package = APP_PACKAGE
    options.app_activity = APP_ACTIVITY
    options.no_reset = False
    options.auto_grant_permissions = True
    options.new_command_timeout = 300
    return options


@pytest.fixture(scope="function")
def driver():
    """Create and manage Appium driver for each test"""
    options = get_appium_options()
    driver = webdriver.Remote(BASE_URL, options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def logged_in_driver(driver):
    """Create a driver that is already logged in"""
    from tests.page_objects.login_page import LoginPage

    login_page = LoginPage(driver)
    login_page.login("testuser", "password123")
    yield driver


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture screenshot on test failure and save to reports/YYYY-MM-DD/screenshots/"""
    outcome = yield
    rep = outcome.get_result()

    # Only capture screenshot on test failure (call phase)
    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get('driver')
        if driver:
            date_dir = datetime.now().strftime("%Y-%m-%d")
            base_dir = os.path.dirname(os.path.dirname(__file__))
            screenshots_dir = os.path.join(base_dir, "reports", date_dir, "screenshots")
            os.makedirs(screenshots_dir, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{item.name}_{timestamp}.png"
            filepath = os.path.join(screenshots_dir, filename)

            driver.save_screenshot(filepath)

            # Add screenshot to HTML report (for self-contained or linked)
            rep.extras = []
            if filepath and os.path.exists(filepath):
                rep.extras.append(pytest_html.extras.image(filepath))
