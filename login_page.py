from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class LoginPage(BasePage):
    """Page Object for Login Page"""
    
    # Locators
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "h3[data-test='error']")
    ERROR_BUTTON = (By.CLASS_NAME, "error-button")
    
    # URL
    URL = "https://www.saucedemo.com/"
    
    def __init__(self, driver):
        super().__init__(driver)
        self.driver.get(self.URL)
    
    def enter_username(self, username):
        """Enter username into username field"""
        self.enter_text(self.USERNAME_INPUT, username)
    
    def enter_password(self, password):
        """Enter password into password field"""
        self.enter_text(self.PASSWORD_INPUT, password)
    
    def click_login_button(self):
        """Click login button"""
        self.click(self.LOGIN_BUTTON)
    
    def login(self, username, password):
        """Complete login process"""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()
    
    def is_error_displayed(self):
        """Check if error message is displayed"""
        return self.is_displayed(self.ERROR_MESSAGE, timeout=5)
    
    def get_error_message(self):
        """Get error message text"""
        return self.get_text(self.ERROR_MESSAGE)
    
    def is_login_page_loaded(self):
        """Verify login page is loaded"""
        return self.is_displayed(self.LOGIN_BUTTON)