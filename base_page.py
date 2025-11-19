from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
from datetime import datetime

class BasePage:
    """Base class for all page objects"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def find_element(self, locator):
        """Find and return element"""
        return self.wait.until(EC.presence_of_element_located(locator))
    
    def find_elements(self, locator):
        """Find and return multiple elements"""
        return self.wait.until(EC.presence_of_all_elements_located(locator))
    
    def click(self, locator):
        """Click on element"""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()
    
    def enter_text(self, locator, text):
        """Enter text into input field"""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
    
    def get_text(self, locator):
        """Get text from element"""
        return self.find_element(locator).text
    
    def is_displayed(self, locator, timeout=10):
        """Check if element is displayed"""
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    def take_screenshot(self, name):
        """Take screenshot and save to screenshots folder"""
        if not os.path.exists('screenshots'):
            os.makedirs('screenshots')
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'screenshots/{name}_{timestamp}.png'
        self.driver.save_screenshot(filename)
        return filename
    
    def get_current_url(self):
        """Return current page URL"""
        return self.driver.current_url
    
    def get_page_title(self):
        """Return page title"""
        return self.driver.title