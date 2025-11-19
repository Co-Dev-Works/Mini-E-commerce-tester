import pytest
from utils.driver_setup import DriverSetup
from utils.logger import Logger
import os
from datetime import datetime

logger = Logger.get_logger(__name__)

@pytest.fixture(scope="function")
def driver(request):
    """
    Fixture to initialize and quit WebDriver for each test
    """
    logger.info(f"Initializing driver for test: {request.node.name}")
    
    # Initialize driver
    driver = DriverSetup.get_driver(headless=False)
    
    yield driver
    
    # Capture screenshot on failure
    if request.node.rep_call.failed:
        logger.error(f"Test failed: {request.node.name}")
        try:
            if not os.path.exists('screenshots'):
                os.makedirs('screenshots')
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            screenshot_name = f"screenshots/FAILED_{request.node.name}_{timestamp}.png"
            driver.save_screenshot(screenshot_name)
            logger.info(f"Screenshot saved: {screenshot_name}")
        except Exception as e:
            logger.error(f"Failed to capture screenshot: {e}")
    
    # Quit driver
    logger.info(f"Closing driver for test: {request.node.name}")
    driver.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to access test result and store in request object
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)

def pytest_configure(config):
    """
    Create necessary directories
    """
    directories = ['reports', 'screenshots', 'logs']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            logger.info(f"Created directory: {directory}")