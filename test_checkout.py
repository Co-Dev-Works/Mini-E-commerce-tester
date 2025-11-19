import pytest
from pages.login_page import LoginPage
from pages.home_page import HomePage
from pages.cart_page import CartPage
from utils.logger import Logger

logger = Logger.get_logger(__name__)

class TestCheckout:
    """Test cases for checkout functionality"""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """Login and add products before each test"""
        login_page = LoginPage(driver)
        login_page.login("standard_user", "secret_sauce")
        
        home_page = HomePage(driver)
        home_page.add_product_to_cart_by_name("Sauce Labs Backpack")
        home_page.click_shopping_cart()
    
    def test_successful_checkout(self, driver):
        """Test complete checkout process"""
        logger.info("Starting test: test_successful_checkout")
        
        cart_page = CartPage(driver)
        assert cart_page.get_cart_item_count() > 0, "Cart should have items"
        
        cart_page.click_checkout()
        
        # Fill checkout information
        cart_page.fill_checkout_information("John", "Doe", "12345")
        cart_page.click_continue_checkout()
        
        # Verify checkout overview page
        assert "Item total:" in cart_page.get_subtotal(), "Subtotal not displayed"
        assert "Tax:" in cart_page.get_tax(), "Tax not displayed"
        assert "Total:" in cart_page.get_total(), "Total not displayed"
        
        # Complete checkout
        cart_page.click_finish()
        
        # Verify success
        assert cart_page.is_checkout_complete(), "Checkout not completed"
        assert "Thank you for your order" in cart_page.get_complete_header_text(), "Success message not displayed"
        
        logger.info("Test passed: test_successful_checkout")
    
    def test_checkout_with_empty_first_name(self, driver):
        """Test checkout with missing first name"""
        logger.info("Starting test: test_checkout_with_empty_first_name")
        
        cart_page = CartPage(driver)
        cart_page.click_checkout()
        
        cart_page.fill_checkout_information("", "Doe", "12345")
        cart_page.click_continue_checkout()
        
        error_msg = cart_page.get_checkout_error_message()
        assert "First Name is required" in error_msg, f"Unexpected error: {error_msg}"
        
        logger.info("Test passed: test_checkout_with_empty_first_name")
    
    def test_checkout_with_empty_last_name(self, driver):
        """Test checkout with missing last name"""
        logger.info("Starting test: test_checkout_with_empty_last_name")
        
        cart_page = CartPage(driver)
        cart_page.click_checkout()
        
        cart_page.fill_checkout_information("John", "", "12345")
        cart_page.click_continue_checkout()
        
        error_msg = cart_page.get_checkout_error_message()
        assert "Last Name is required" in error_msg, f"Unexpected error: {error_msg}"
        
        logger.info("Test passed: test_checkout_with_empty_last_name")
    
    def test_checkout_with_empty_postal_code(self, driver):
        """Test checkout with missing postal code"""
        logger.info("Starting test: test_checkout_with_empty_postal_code")
        
        cart_page = CartPage(driver)
        cart_page.click_checkout()
        
        cart_page.fill_checkout_information("John", "Doe", "")
        cart_page.click_continue_checkout()
        
        error_msg = cart_page.get_checkout_error_message()
        assert "Postal Code is required" in error_msg, f"Unexpected error: {error_msg}"
        
        logger.info("Test passed: test_checkout_with_empty_postal_code")
    
    def test_checkout_with_multiple_items(self, driver):
        """Test checkout with multiple items"""
        logger.info("Starting test: test_checkout_with_multiple_items")
        
        # Add more items
        cart_page = CartPage(driver)
        cart_page.click_continue_shopping()
        
        home_page = HomePage(driver)
        home_page.add_product_to_cart_by_name("Sauce Labs Bike Light")
        home_page.click_shopping_cart()
        
        # Verify multiple items
        assert cart_page.get_cart_item_count() == 2, "Should have 2 items"
        
        # Proceed with checkout
        cart_page.click_checkout()
        cart_page.fill_checkout_information("John", "Doe", "12345")
        cart_page.click_continue_checkout()
        
        # Verify items on overview page
        items = cart_page.get_cart_item_names()
        assert len(items) == 2, "Overview should show 2 items"
        
        cart_page.click_finish()
        assert cart_page.is_checkout_complete(), "Checkout not completed"
        
        logger.info("Test passed: test_checkout_with_multiple_items")
    
    def test_return_to_home_after_checkout(self, driver):
        """Test returning to home page after successful checkout"""
        logger.info("Starting test: test_return_to_home_after_checkout")
        
        cart_page = CartPage(driver)
        cart_page.click_checkout()
        cart_page.fill_checkout_information("John", "Doe", "12345")
        cart_page.click_continue_checkout()
        cart_page.click_finish()
        
        assert cart_page.is_checkout_complete(), "Checkout not completed"
        
        # Click back home
        cart_page.click_back_home()
        
        home_page = HomePage(driver)
        assert home_page.is_home_page_loaded(), "Not redirected to home page"
        
        # Verify cart is empty
        cart_count = home_page.get_cart_badge_count()
        assert cart_count == "0", "Cart should be empty after checkout"
        
        logger.info("Test passed: test_return_to_home_after_checkout")
    
    def test_price_calculation_accuracy(self, driver):
        """Test that prices are calculated correctly"""
        logger.info("Starting test: test_price_calculation_accuracy")
        
        cart_page = CartPage(driver)
        cart_page.click_checkout()
        cart_page.fill_checkout_information("John", "Doe", "12345")
        cart_page.click_continue_checkout()
        
        # Get price details
        subtotal_text = cart_page.get_subtotal()
        tax_text = cart_page.get_tax()
        total_text = cart_page.get_total()
        
        # Verify all prices contain "$"
        assert "$" in subtotal_text, "Subtotal should contain currency"
        assert "$" in tax_text, "Tax should contain currency"
        assert "$" in total_text, "Total should contain currency"
        
        # Extract numeric values
        subtotal = float(subtotal_text.split("$")[1])
        tax = float(tax_text.split("$")[1])
        total = float(total_text.split("$")[1])
        
        # Verify calculation (with small tolerance for rounding)
        expected_total = round(subtotal + tax, 2)
        assert abs(total - expected_total) < 0.01, f"Total calculation incorrect: {total} != {expected_total}"
        
        logger.info("Test passed: test_price_calculation_accuracy")