from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class HomePage(BasePage):
    """Page Object for Home/Products Page"""
    
    # Locators
    PAGE_TITLE = (By.CLASS_NAME, "title")
    PRODUCT_ITEMS = (By.CLASS_NAME, "inventory_item")
    SHOPPING_CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    SHOPPING_CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    HAMBURGER_MENU = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")
    PRODUCT_SORT = (By.CLASS_NAME, "product_sort_container")
    
    def is_home_page_loaded(self):
        """Verify home page is loaded"""
        return self.is_displayed(self.PAGE_TITLE)
    
    def get_page_title(self):
        """Get page title text"""
        return self.get_text(self.PAGE_TITLE)
    
    def get_product_count(self):
        """Get number of products displayed"""
        products = self.find_elements(self.PRODUCT_ITEMS)
        return len(products)
    
    def add_product_to_cart_by_name(self, product_name):
        """Add specific product to cart by name"""
        add_button = (By.XPATH, f"//div[text()='{product_name}']/ancestor::div[@class='inventory_item']//button")
        self.click(add_button)
    
    def get_cart_badge_count(self):
        """Get shopping cart item count"""
        try:
            return self.get_text(self.SHOPPING_CART_BADGE)
        except:
            return "0"
    
    def click_shopping_cart(self):
        """Click shopping cart icon"""
        self.click(self.SHOPPING_CART_LINK)
    
    def logout(self):
        """Logout from application"""
        self.click(self.HAMBURGER_MENU)
        self.click(self.LOGOUT_LINK)
    
    def get_product_names(self):
        """Get list of all product names"""
        products = self.find_elements((By.CLASS_NAME, "inventory_item_name"))
        return [product.text for product in products]
    
    def get_product_prices(self):
        """Get list of all product prices"""
        prices = self.find_elements((By.CLASS_NAME, "inventory_item_price"))
        return [price.text for price in prices]