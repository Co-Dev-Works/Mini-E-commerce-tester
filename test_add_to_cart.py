import pytest
from pages.login_page import LoginPage
from pages.home_page import HomePage
from pages.cart_page import CartPage
from utils.logger import Logger

logger = Logger.get_logger(__name__)

class TestAddToCart:
    """Test cases for add to cart functionality"""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """Login before each test"""
        login_page = LoginPage(driver)
        login_page.login("standard_user", "secret_sauce")
    
    def test_add_single_product_to_cart(self, driver):
        """Test adding a single product to cart"""
        logger.info("Starting test: test_add_single_product_to_cart")
        
        home_page = HomePage(driver)
        home_page.add_product_to_cart_by_name("Sauce Labs Backpack")
        
        # Verify cart badge shows 1 item
        cart_count = home_page.get_cart_badge_count()
        assert cart_count == "1", f"Expected 1 item in cart, got {cart_count}"
        
        # Go to cart and verify
        home_page.click_shopping_cart()
        cart_page = CartPage(driver)
        assert cart_page.get_cart_item_count() == 1, "Cart should have 1 item"
        
        cart_items = cart_page.get_cart_item_names()
        assert "Sauce Labs Backpack" in cart_items, "Product not found in cart"
        
        logger.info("Test passed: test_add_single_product_to_cart")
    
    def test_add_multiple_products_to_cart(self, driver):
        """Test adding multiple products to cart"""
        logger.info("Starting test: test_add_multiple_products_to_cart")
        
        home_page = HomePage(driver)
        products = ["Sauce Labs Backpack", "Sauce Labs Bike Light", "Sauce Labs Bolt T-Shirt"]
        
        for product in products:
            home_page.add_product_to_cart_by_name(product)
        
        # Verify cart badge
        cart_count = home_page.get_cart_badge_count()
        assert cart_count == "3", f"Expected 3 items in cart, got {cart_count}"
        
        # Go to cart and verify
        home_page.click_shopping_cart()
        cart_page = CartPage(driver)
        assert cart_page.get_cart_item_count() == 3, "Cart should have 3 items"
        
        cart_items = cart_page.get_cart_item_names()
        for product in products:
            assert product in cart_items, f"{product} not found in cart"
        
        logger.info("Test passed: test_add_multiple_products_to_cart")
    
    def test_remove_product_from_cart(self, driver):
        """Test removing product from cart"""
        logger.info("Starting test: test_remove_product_from_cart")
        
        home_page = HomePage(driver)
        home_page.add_product_to_cart_by_name("Sauce Labs Backpack")
        home_page.add_product_to_cart_by_name("Sauce Labs Bike Light")
        
        home_page.click_shopping_cart()
        cart_page = CartPage(driver)
        
        # Remove one product
        cart_page.remove_item_by_name("Sauce Labs Backpack")
        
        # Verify count
        assert cart_page.get_cart_item_count() == 1, "Cart should have 1 item after removal"
        
        cart_items = cart_page.get_cart_item_names()
        assert "Sauce Labs Backpack" not in cart_items, "Removed product still in cart"
        assert "Sauce Labs Bike Light" in cart_items, "Remaining product not in cart"
        
        logger.info("Test passed: test_remove_product_from_cart")
    
    def test_cart_persists_across_pages(self, driver):
        """Test that cart items persist when navigating"""
        logger.info("Starting test: test_cart_persists_across_pages")
        
        home_page = HomePage(driver)
        home_page.add_product_to_cart_by_name("Sauce Labs Backpack")
        
        initial_count = home_page.get_cart_badge_count()
        
        # Navigate to cart and back
        home_page.click_shopping_cart()
        cart_page = CartPage(driver)
        cart_page.click_continue_shopping()
        
        # Verify cart count persists
        final_count = home_page.get_cart_badge_count()
        assert initial_count == final_count, "Cart count changed after navigation"
        
        logger.info("Test passed: test_cart_persists_across_pages")
    
    def test_empty_cart_message(self, driver):
        """Test empty cart displays correctly"""
        logger.info("Starting test: test_empty_cart_message")
        
        home_page = HomePage(driver)
        home_page.click_shopping_cart()
        
        cart_page = CartPage(driver)
        assert cart_page.get_cart_item_count() == 0, "Cart should be empty"
        
        # Verify no badge when cart is empty
        cart_page.click_continue_shopping()
        cart_count = home_page.get_cart_badge_count()
        assert cart_count == "0", "Badge should not show when cart is empty"
        
        logger.info("Test passed: test_empty_cart_message")
    
    def test_product_prices_in_cart(self, driver):
        """Test that product prices are displayed correctly in cart"""
        logger.info("Starting test: test_product_prices_in_cart")
        
        home_page = HomePage(driver)
        
        # Get price on home page
        home_prices = home_page.get_product_prices()
        backpack_price = home_prices[0]  # First product
        
        home_page.add_product_to_cart_by_name("Sauce Labs Backpack")
        home_page.click_shopping_cart()
        
        cart_page = CartPage(driver)
        cart_prices = cart_page.get_cart_item_prices()
        
        assert backpack_price in cart_prices, "Product price doesn't match in cart"
        
        logger.info("Test passed: test_product_prices_in_cart")