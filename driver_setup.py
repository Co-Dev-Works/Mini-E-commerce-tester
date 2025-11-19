from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class DriverSetup:
    """Handles browser driver initialization and configuration"""
    
    @staticmethod
    def get_driver(headless=False):
        """
        Initialize and return Chrome WebDriver
        Args:
            headless (bool): Run browser in headless mode
        Returns:
            WebDriver: Configured Chrome WebDriver instance
        """
        chrome_options = Options()

        if headless:
            chrome_options.add_argument('--headless')

        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--start-maximized')

        chrome_options.add_experimental_option(
            'excludeSwitches',
            ['enable-logging']
        )

        # Selenium 4.20+ automatically downloads and manages the correct driver
        driver = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(10)
        return driver
