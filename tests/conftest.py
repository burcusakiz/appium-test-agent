"""
Appium Test Framework - Configuration and Fixtures
"""

import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
import os
from datetime import datetime
import pytest_html
import subprocess
import time
import signal

# Test configuration
# Android
BASE_URL = "http://127.0.0.1:4723"
APP_PACKAGE = os.getenv("APP_PACKAGE", "com.demo.loginapp")
APP_ACTIVITY = os.getenv("APP_ACTIVITY", ".LoginActivity")
PLATFORM_VERSION = os.getenv("PLATFORM_VERSION", "14.0")
DEVICE_NAME = os.getenv("DEVICE_NAME", "emulator-5554")
APP_PATH = os.getenv("APP_PATH", None)

# Appium server state
appium_process = None

def start_appium_server():
    """Start Appium server if not running"""
    global appium_process

    # Check if Appium is already running
    try:
        result = subprocess.run(
            ["lsof", "-i", ":4723"],
            capture_output=True,
            timeout=5
        )
        if result.returncode == 0:
            print("Appium server is already running")
            return True
    except:
        pass

    # Start Appium server
    print("Starting Appium server...")
    try:
        appium_process = subprocess.Popen(
            ["appium", "--port", "4723", "--log-level", "error"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True
        )
        time.sleep(5)  # Wait for server to start
        print("Appium server started successfully")
        return True
    except Exception as e:
        print(f"Failed to start Appium server: {e}")
        return False

def stop_appium_server():
    """Stop Appium server"""
    global appium_process

    if appium_process:
        print("Stopping Appium server...")
        try:
            os.killpg(os.getpgid(appium_process.pid), signal.SIGTERM)
            time.sleep(2)
            appium_process.terminate()
        except:
            pass
        appium_process = None

def get_android_driver_options():
    """Configure Appium capabilities for Android"""
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.platform_version = os.getenv("PLATFORM_VERSION", PLATFORM_VERSION)
    options.device_name = os.getenv("DEVICE_NAME", DEVICE_NAME)
    options.app_package = os.getenv("APP_PACKAGE", APP_PACKAGE)
    options.app_activity = os.getenv("APP_ACTIVITY", APP_ACTIVITY)

    if APP_PATH and os.path.exists(APP_PATH):
        options.app = APP_PATH

    options.no_reset = False
    options.auto_grant_permissions = True
    options.new_command_timeout = 300
    return options


@pytest.fixture(scope="session")
def appium_session():
    """Manage Appium server lifecycle"""
    print("=" * 60)
    print("Appium Test Session Starting")
    print("=" * 60)

    start_appium_server()
    yield
    stop_appium_server()
    print("=" * 60)
    print("Appium Test Session Ended")
    print("=" * 60)


@pytest.fixture(scope="function")
def android_driver(appium_session):
    """Create and manage Appium driver for Android tests"""
    options = get_android_driver_options()
    driver = webdriver.Remote(BASE_URL, options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def driver(android_driver):
    """Default mobile driver used by Android tests."""
    yield android_driver


@pytest.fixture(scope="function")
def logged_in_android_driver(android_driver):
    """Create an Android driver that is already logged in"""
    from tests.page_objects.login_page import LoginPage

    login_page = LoginPage(android_driver)
    login_page.login("testuser", "password123")
    yield android_driver


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
