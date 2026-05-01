"""
Login Page Object Model for Appium Tests
"""

from appium.webdriver.webdriver import WebDriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException


class LoginPage:
    """Page object for the login screen"""

    # Locators
    USERNAME_FIELD = (AppiumBy.ID, "com.demo.loginapp:id/username_input")
    PASSWORD_FIELD = (AppiumBy.ID, "com.demo.loginapp:id/password_input")
    LOGIN_BUTTON = (AppiumBy.ID, "com.demo.loginapp:id/login_button")
    ERROR_MESSAGE = (AppiumBy.ID, "com.demo.loginapp:id/textViewError")
    REGISTER_LINK = (AppiumBy.ID, "com.demo.loginapp:id/linkRegister")

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def enter_username(self, username: str) -> None:
        """Enter username into the username field"""
        element = self.driver.find_element(*self.USERNAME_FIELD)
        element.clear()
        element.send_keys(username)

    def enter_password(self, password: str) -> None:
        """Enter password into the password field"""
        element = self.driver.find_element(*self.PASSWORD_FIELD)
        element.clear()
        element.send_keys(password)

    def click_login(self) -> None:
        """Click the login button"""
        self.driver.find_element(*self.LOGIN_BUTTON).click()

    def get_error_message(self) -> str:
        """Get the error message text"""
        try:
            element = self.driver.find_element(*self.ERROR_MESSAGE)
            return element.text
        except NoSuchElementException:
            return ""

    def is_error_visible(self) -> bool:
        """Check if error message is visible"""
        try:
            element = self.driver.find_element(*self.ERROR_MESSAGE)
            return element.is_displayed()
        except NoSuchElementException:
            return False

    def is_logged_in(self) -> bool:
        """Check if user is logged in by looking for home section elements"""
        try:
            self.driver.find_element(AppiumBy.ID, "com.demo.loginapp:id/home_section")
            return True
        except NoSuchElementException:
            return False

    def login(self, username: str, password: str) -> None:
        """Perform complete login flow"""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
