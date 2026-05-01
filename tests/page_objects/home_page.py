"""
Home Page Object Model for Appium Tests
"""

from appium.webdriver.webdriver import WebDriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException


class HomePage:
    """Page object for the home screen"""

    # Locators
    WELCOME_TEXT = (AppiumBy.ID, "com.demo.loginapp:id/textViewWelcome")
    HOME_SECTION = (AppiumBy.ID, "com.demo.loginapp:id/home_section")
    LOGOUT_BUTTON = (AppiumBy.ID, "com.demo.loginapp:id/buttonLogout")
    NAVIGATION_DRAWER = (AppiumBy.ACCESSIBILITY_ID, "Open navigation drawer")

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def get_welcome_message(self) -> str:
        """Get welcome message text"""
        try:
            element = self.driver.find_element(*self.WELCOME_TEXT)
            return element.text
        except NoSuchElementException:
            return ""

    def click_logout(self) -> None:
        """Click the logout button"""
        self.driver.find_element(*self.LOGOUT_BUTTON).click()

    def is_home_screen_visible(self) -> bool:
        """Check if home screen is visible"""
        try:
            return self.driver.find_element(*self.HOME_SECTION).is_displayed()
        except NoSuchElementException:
            return False

    def get_username_from_welcome(self) -> str:
        """Extract username from welcome message"""
        message = self.get_welcome_message()
        if message:
            # Expected format: "Welcome testuser!" or "Hello, testuser"
            for prefix in ["Welcome ", "Hello, ", "Hello "]:
                if prefix in message:
                    return message.replace(prefix, "").rstrip("!")
        return ""

    def is_logged_in(self) -> bool:
        """Check if user is logged in"""
        return self.is_home_screen_visible()
