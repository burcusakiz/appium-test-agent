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

    def is_username_field_visible(self) -> bool:
        """Check if username field is visible"""
        try:
            element = self.driver.find_element(*self.USERNAME_FIELD)
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

    def login_with_error_check(self, username: str, password: str) -> tuple[bool, str]:
        """
        Perform login and return (success, error_message)

        Returns:
            tuple: (login_success, error_message_or_empty)
        """
        self.login(username, password)

        if self.is_logged_in():
            return True, ""
        else:
            error_msg = self.get_error_message()
            return False, error_msg

    def wait_for_error_message(self, timeout: int = 5) -> str:
        """Wait for error message to appear"""
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        wait = WebDriverWait(self.driver, timeout)
        try:
            element = wait.until(
                EC.visibility_of_element_located(self.ERROR_MESSAGE)
            )
            return element.text
        except:
            return ""

    def clear_fields(self) -> None:
        """Clear all input fields"""
        self.driver.find_element(*self.USERNAME_FIELD).clear()
        self.driver.find_element(*self.PASSWORD_FIELD).clear()

    def click_register(self) -> None:
        """Click register link"""
        self.driver.find_element(*self.REGISTER_LINK).click()

    def is_register_link_visible(self) -> bool:
        """Check if register link is visible"""
        try:
            return self.driver.find_element(*self.REGISTER_LINK).is_displayed()
        except:
            return False
