# Appium Test Writing Guide

**Purpose**: Mobile application testing (Android/iOS) using Appium framework

**When to use**: When automating mobile app UI tests for functional, regression, or smoke testing

---

## Core Concepts

### Appium Architecture
```
┌─────────────────────────────────────────────────────────┐
│                    Test Code                            │
│              (Python/Java/JS/...)                       │
└───────────────┬─────────────────────────────────────────┘
                │ HTTP Protocol (W3C WebDriver)
                ▼
┌─────────────────────────────────────────────────────────┐
│              Appium Server                              │
│          - Receives commands                            │
│          - Translates to native protocols               │
└───────────────┬─────────────────────────────────────────┘
                │
        ┌───────┴───────┐
        ▼               ▼
┌─────────────────┐ ┌─────────────────┐
│  AndroidDriver  │ │  IOSDriver      │
│  (UiAutomator2) │ │  (XCUITest)     │
└─────────────────┘ └─────────────────┘
        │               │
        ▼               ▼
┌─────────────────┐ ┌─────────────────┐
│  Android Device │ │  iOS Device     │
│  / Emulator     │ │  / Simulator    │
└─────────────────┘ └─────────────────┘
```

### WebDriver Protocol Commands
| Command | Android | iOS |
|---------|---------|-----|
| `findElement` | ID, XPath, Accessibility ID | ID, XPath, Class Chain |
| `click` | ✅ | ✅ |
| `sendKeys` | ✅ | ✅ |
| `tap` | ✅ | ✅ |
| `swipe` | ✅ | ✅ |
| `scroll` | ✅ | ✅ |

---

## Page Object Model (POM) Pattern

### Why POM?
1. **Maintainability** - Changes in UI only affect one place
2. **Readability** - Tests read like business logic
3. **Reusability** - Common actions centralized
4. **Test Isolation** - Each test focuses on one scenario

### Basic Structure
```
tests/
├── page_objects/
│   ├── __init__.py
│   ├── login_page.py      # Login screen interactions
│   ├── home_page.py       # Home screen interactions
│   └── profile_page.py    # Profile screen interactions
├── test_login.py          # Tests using POM
└── conftest.py            # Fixtures
```

### Page Object Implementation

#### Python - Login Page
```python
"""
login_page.py - Page Object for Login Screen
"""

from appium.webdriver.webdriver import WebDriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException


class LoginPage:
    """Page object encapsulating login screen elements and actions"""
    
    # Locators - use unique, stable identifiers
    USERNAME_FIELD = (AppiumBy.ID, "com.myapp:id/editTextUsername")
    PASSWORD_FIELD = (AppiumBy.ID, "com.myapp:id/editTextPassword")
    LOGIN_BUTTON = (AppiumBy.ID, "com.myapp:id/buttonLogin")
    ERROR_MESSAGE = (AppiumBy.ID, "com.myapp:id/textViewError")
    FORGOT_PASSWORD_LINK = (AppiumBy.ID, "com.myapp:id/linkForgotPassword")
    REGISTER_LINK = (AppiumBy.ID, "com.myapp:id/linkRegister")
    
    def __init__(self, driver: WebDriver):
        self.driver = driver
    
    # Action methods - what user can do
    def enter_username(self, username: str) -> 'LoginPage':
        """Enter username into the username field"""
        self._find_element(self.USERNAME_FIELD).clear()
        self._find_element(self.USERNAME_FIELD).send_keys(username)
        return self  # Enable method chaining
    
    def enter_password(self, password: str) -> 'LoginPage':
        """Enter password into the password field"""
        self._find_element(self.PASSWORD_FIELD).clear()
        self._find_element(self.PASSWORD_FIELD).send_keys(password)
        return self
    
    def click_login(self) -> 'LoginPage':
        """Click the login button"""
        self._find_element(self.LOGIN_BUTTON).click()
        return self
    
    def tap_forgot_password(self) -> 'LoginPage':
        """Tap forgot password link"""
        self._find_element(self.FORGOT_PASSWORD_LINK).click()
        return self
    
    # Assertion methods - what to verify
    def is_username_field_visible(self) -> bool:
        """Check if username field is visible"""
        return self._is_element_visible(self.USERNAME_FIELD)
    
    def is_error_visible(self) -> bool:
        """Check if error message is displayed"""
        return self._is_element_visible(self.ERROR_MESSAGE)
    
    def get_error_message(self) -> str:
        """Get the error message text"""
        try:
            return self._find_element(self.ERROR_MESSAGE).text
        except NoSuchElementException:
            return ""
    
    def is_logged_in(self) -> bool:
        """Check if user is logged in by verifying home screen elements"""
        try:
            self.driver.find_element(AppiumBy.ID, "com.myapp:id/home_section")
            return True
        except NoSuchElementException:
            return False
    
    # Helper methods
    def _find_element(self, locator: tuple) -> WebDriver.WebElement:
        """Find element with wait"""
        return self.driver.find_element(*locator)
    
    def _is_element_visible(self, locator: tuple) -> bool:
        """Check if element is visible"""
        try:
            return self._find_element(locator).is_displayed()
        except (NoSuchElementException, Exception):
            return False
    
    # Convenience method for complete login flow
    def login(self, username: str, password: str) -> 'LoginPage':
        """Perform complete login flow"""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
        return self
```

#### Python - Home Page
```python
"""
home_page.py - Page Object for Home Screen
"""

from appium.webdriver.webdriver import WebDriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException


class HomePage:
    """Page object encapsulating home screen elements and actions"""
    
    # Locators
    WELCOME_TEXT = (AppiumBy.ID, "com.myapp:id/textViewWelcome")
    HOME_SECTION = (AppiumBy.ID, "com.myapp:id/home_section")
    NAVIGATION_DRAWER = (AppiumBy.ACCESSIBILITY_ID, "Open navigation drawer")
    PROFILE_BUTTON = (AppiumBy.ID, "com.myapp:id/buttonProfile")
    LOGOUT_BUTTON = (AppiumBy.ID, "com.myapp:id/buttonLogout")
    
    def __init__(self, driver: WebDriver):
        self.driver = driver
    
    def get_welcome_message(self) -> str:
        """Get welcome message text"""
        return self._find_element(self.WELCOME_TEXT).text
    
    def click_profile(self) -> 'HomePage':
        """Navigate to profile screen"""
        self._find_element(self.PROFILE_BUTTON).click()
        return self
    
    def click_logout(self) -> 'LoginPage':
        """Logout from application"""
        self._find_element(self.LOGOUT_BUTTON).click()
        # Return LoginPage since logout navigates there
        from tests.page_objects.login_page import LoginPage
        return LoginPage(self.driver)
    
    def open_navigation_drawer(self) -> 'HomePage':
        """Open the navigation drawer"""
        self._find_element(self.NAVIGATION_DRAWER).click()
        return self
    
    def is_home_screen_visible(self) -> bool:
        """Verify home screen is displayed"""
        return self._is_element_visible(self.HOME_SECTION)
    
    def get_username_from_header(self) -> str:
        """Extract username from home screen header"""
        welcome_text = self.get_welcome_message()
        # Expected format: "Hello, John Doe"
        return welcome_text.replace("Hello, ", "").strip()
    
    def _find_element(self, locator: tuple) -> WebDriver.WebElement:
        """Find element with wait"""
        return self.driver.find_element(*locator)
    
    def _is_element_visible(self, locator: tuple) -> bool:
        """Check if element is visible"""
        try:
            return self._find_element(locator).is_displayed()
        except (NoSuchElementException, Exception):
            return False
```

### Test Implementation
```python
"""
test_login.py - Login test scenarios
"""

import pytest
from tests.page_objects.login_page import LoginPage
from tests.page_objects.home_page import HomePage


class TestLogin:
    """Test cases for login functionality"""
    
    VALID_USERNAME = "testuser"
    VALID_PASSWORD = "password123"
    INVALID_USERNAME = "invaliduser"
    INVALID_PASSWORD = "wrongpassword"
    
    @pytest.mark.smoke
    @pytest.mark.login
    def test_successful_login_with_valid_credentials(self, driver):
        """
        Verify user can successfully login with valid credentials
        and is redirected to home screen.
        
        Prerequisites:
        - User account exists
        - Valid credentials provided
        
        Steps:
        1. Enter valid username
        2. Enter valid password
        3. Click login button
        4. Verify home screen is displayed
        5. Verify welcome message contains username
        """
        login_page = LoginPage(driver)
        
        # Perform login
        login_page.login(self.VALID_USERNAME, self.VALID_PASSWORD)
        
        # Verify login success
        assert HomePage(driver).is_home_screen_visible(), \
            "Home screen should be visible after successful login"
        
        # Verify welcome message
        welcome_msg = HomePage(driver).get_welcome_message()
        assert self.VALID_USERNAME in welcome_msg, \
            "Welcome message should contain username"
    
    @pytest.mark.regression
    @pytest.mark.login
    def test_login_fails_with_invalid_password(self, driver):
        """
        Verify login fails with appropriate error for wrong password.
        """
        login_page = LoginPage(driver)
        
        login_page.login(self.VALID_USERNAME, self.INVALID_PASSWORD)
        
        assert login_page.is_error_visible(), \
            "Error message should be visible for invalid password"
        
        error_msg = login_page.get_error_message()
        assert "invalid" in error_msg.lower(), \
            "Error message should indicate invalid credentials"
        
        # Verify still on login screen
        assert login_page.is_username_field_visible(), \
            "Should remain on login screen after failed login"
    
    @pytest.mark.regression
    @pytest.mark.login
    def test_empty_credentials_display_error(self, driver):
        """
        Verify login fails with empty credentials.
        """
        login_page = LoginPage(driver)
        login_page.click_login()
        
        assert login_page.is_error_visible(), \
            "Error should be displayed for empty credentials"
    
    @pytest.mark.smoke
    @pytest.mark.login
    def test_logout_flow(self, driver):
        """
        Verify logout returns to login screen.
        """
        # First login
        login_page = LoginPage(driver)
        login_page.login(self.VALID_USERNAME, self.VALID_PASSWORD)
        
        # Navigate to home and logout
        home_page = HomePage(driver)
        home_page.click_logout()
        
        # Verify on login screen
        assert login_page.is_username_field_visible(), \
            "Should return to login screen after logout"
```

---

## Test Fixtures (conftest.py)

### Android Driver Fixture
```python
"""
conftest.py - Common fixtures for all tests
"""

import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from tests.page_objects.login_page import LoginPage


# Configuration constants
BASE_URL = "http://127.0.0.1:4723"
APP_PACKAGE = "com.myapp"
APP_ACTIVITY = "com.myapp.MainActivity"
PLATFORM_VERSION = "14.0"
DEVICE_NAME = "emulator-5554"


@pytest.fixture(scope="function")
def driver():
    """
    Create and manage Appium driver for each test.
    Scope: function = new driver for each test method.
    """
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.platform_version = PLATFORM_VERSION
    options.device_name = DEVICE_NAME
    options.app_package = APP_PACKAGE
    options.app_activity = APP_ACTIVITY
    options.no_reset = False  # Reset app state for each test
    options.auto_grant_permissions = True
    options.new_command_timeout = 300
    
    driver = webdriver.Remote(BASE_URL, options=options)
    driver.implicitly_wait(10)  # Implicit wait
    
    yield driver
    
    driver.quit()


@pytest.fixture(scope="function")
def logged_in_driver(driver):
    """
    Create a driver that is already logged in.
    Useful for tests that require authenticated state.
    """
    login_page = LoginPage(driver)
    login_page.login("testuser", "password123")
    yield driver
```

### iOS Driver Fixture
```python
@pytest.fixture(scope="function")
def ios_driver():
    """
    Create and manage Appium driver for iOS tests.
    """
    from appium.options.ios import XCUITestOptions
    
    options = XCUITestOptions()
    options.platform_name = "iOS"
    options.platform_version = "17.0"
    options.device_name = "iPhone 15"
    options.app = "/path/to/app.ipa"
    options.automation_name = "XCUITest"
    options.no_reset = False
    options.auto_grant_permissions = True
    
    driver = webdriver.Remote(BASE_URL, options=options)
    driver.implicitly_wait(10)
    
    yield driver
    driver.quit()
```

---

## Testing Patterns

### 1. Explicit Wait Pattern
```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(driver, 15)  # 15 second timeout

# Wait for element to be clickable
login_button = wait.until(
    EC.element_to_be_clickable((AppiumBy.ID, "com.myapp:id/buttonLogin"))
)
login_button.click()

# Wait for element to be visible
home_section = wait.until(
    EC.visibility_of_element_located((AppiumBy.ID, "com.myapp:id/home_section"))
)
assert home_section.is_displayed()

# Wait for element to be present
wait.until(
    EC.presence_of_element_located((AppiumBy.ID, "com.myapp:id/loadingIndicator"))
)
```

### 2. Scroll Pattern (for long lists)
```python
def scroll_to_element_by_text(driver, text):
    """Scroll until element with specific text is found"""
    from appium.webdriver.common.appiumby import AppiumBy
    
    scrollable = driver.find_element(AppiumBy.CLASS_NAME, "android.widget.ScrollView")
    
    while True:
        try:
            element = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 
                f'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text("{text}"))')
            return element
        except:
            # Get screen size for scroll
            size = scrollable.size
            start_y = size["height"] * 0.8
            end_y = size["height"] * 0.2
            
            driver.swipe(
                start_x=size["width"] * 0.5,
                start_y=start_y,
                end_x=size["width"] * 0.5,
                end_y=end_y,
                duration=500
            )
```

### 3. Handle Keyboard
```python
def hide_keyboard(driver):
    """Hide the software keyboard"""
    try:
        driver.hide_keyboard()
    except:
        # Keyboard might already be hidden
        pass

# Alternative: tap outside
driver.tap([(100, 50)])  # Tap outside the input field
```

### 4. Take Screenshot on Failure
```python
import pytest

@pytest.hookimpl(tryfirst=True)
def pytest_runtest_makereport(item, call):
    """Capture screenshot on test failure"""
    rep = yield
    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get('driver')
        if driver:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"reports/screenshot_{item.name}_{timestamp}.png"
            driver.save_screenshot(filename)
```

---

## Test Organization

### Test Tags/Markers
```python
# pytest.ini
[pytest]
markers =
    smoke: Smoke tests (quick, critical path)
    regression: Regression tests (full feature coverage)
    integration: Integration tests (multiple components)
    e2e: End-to-end tests (full user journeys)
    android: Android-specific tests
    ios: iOS-specific tests
    api: API-only tests (no UI)
```

### Running Tests
```bash
# Run smoke tests only
pytest -m smoke -v

# Run regression tests
pytest -m regression -v

# Run Android UI tests
pytest -m android -v

# Run with specific keyword
pytest -k "login and not logout" -v

# Generate HTML report
pytest --html=reports/report.html --self-contained-html

# Stop on first failure
pytest -x

# Show print statements
pytest -s
```

---

## Best Practices Summary

### ✅ DO
- Use unique, stable element locators (ID > Accessibility ID > XPath)
- Implement Page Object Pattern for maintainability
- Use explicit waits over implicit waits
- Create fixtures for common setup/teardown
- Name tests descriptively (test_<what>_<condition>_<expected>)
- Organize tests by feature
- Run tests on real devices when possible
- Take screenshots on failures

### ❌ DON'T
- Use absolute XPath expressions
- Rely on element position in DOM
- Mix test responsibilities
- Hardcode credentials in tests
- Use sleep() - use waits instead
- Share test data between tests
- Skip tests without valid reason
- Leave drivers open after tests

---

## References

- [Appium Documentation](https://appium.io/docs/)
- [W3C WebDriver Spec](https://www.w3.org/TR/webdriver/)
- [Page Object Pattern](https://martinfowler.com/bliki/PageObject.html)
- [Selenium Python Docs](https://selenium-python.readthedocs.io/)
