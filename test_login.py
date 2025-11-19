import pytest
from pages.login_page import LoginPage
from pages.home_page import HomePage
from utils.logger import Logger

logger = Logger.get_logger(__name__)

class TestLogin:
    """Test cases for login functionality"""
    
    def test_successful_login(self, driver):
        """Test login with valid credentials"""
        logger.info("Starting test: test_successful_login")
        
        login_page = LoginPage(driver)
        assert login_page.is_login_page_loaded(), "Login page not loaded"
        
        login_page.login("standard_user", "secret_sauce")
        
        home_page = HomePage(driver)
        assert home_page.is_home_page_loaded(), "Home page not loaded after login"
        assert home_page.get_page_title() == "Products", "Incorrect page title"
        
        logger.info("Test passed: test_successful_login")
    
    def test_login_with_invalid_username(self, driver):
        """Test login with invalid username"""
        logger.info("Starting test: test_login_with_invalid_username")
        
        login_page = LoginPage(driver)
        login_page.login("invalid_user", "secret_sauce")
        
        assert login_page.is_error_displayed(), "Error message not displayed"
        error_msg = login_page.get_error_message()
        assert "Username and password do not match" in error_msg, f"Unexpected error: {error_msg}"
        
        logger.info("Test passed: test_login_with_invalid_username")
    
    def test_login_with_invalid_password(self, driver):
        """Test login with invalid password"""
        logger.info("Starting test: test_login_with_invalid_password")
        
        login_page = LoginPage(driver)
        login_page.login("standard_user", "wrong_password")
        
        assert login_page.is_error_displayed(), "Error message not displayed"
        error_msg = login_page.get_error_message()
        assert "Username and password do not match" in error_msg, f"Unexpected error: {error_msg}"
        
        logger.info("Test passed: test_login_with_invalid_password")
    
    def test_login_with_empty_credentials(self, driver):
        """Test login with empty username and password"""
        logger.info("Starting test: test_login_with_empty_credentials")
        
        login_page = LoginPage(driver)
        login_page.click_login_button()
        
        assert login_page.is_error_displayed(), "Error message not displayed"
        error_msg = login_page.get_error_message()
        assert "Username is required" in error_msg, f"Unexpected error: {error_msg}"
        
        logger.info("Test passed: test_login_with_empty_credentials")
    
    def test_login_with_locked_user(self, driver):
        """Test login with locked out user"""
        logger.info("Starting test: test_login_with_locked_user")
        
        login_page = LoginPage(driver)
        login_page.login("locked_out_user", "secret_sauce")
        
        assert login_page.is_error_displayed(), "Error message not displayed"
        error_msg = login_page.get_error_message()
        assert "locked out" in error_msg.lower(), f"Unexpected error: {error_msg}"
        
        logger.info("Test passed: test_login_with_locked_user")
    
    def test_logout(self, driver):
        """Test logout functionality"""
        logger.info("Starting test: test_logout")
        
        login_page = LoginPage(driver)
        login_page.login("standard_user", "secret_sauce")
        
        home_page = HomePage(driver)
        assert home_page.is_home_page_loaded(), "Home page not loaded"
        
        home_page.logout()
        
        # Verify back on login page
        assert login_page.is_login_page_loaded(), "Not redirected to login page after logout"
        
        logger.info("Test passed: test_logout")