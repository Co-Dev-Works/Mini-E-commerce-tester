from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class ProductPage(BasePage):
    """Page Object for Individual Product Page"""
    
    # Locators
    PRODUCT_NAME = (By.CLASS_NAME, "inventory_details_name")
    PRODUCT_DESCRIPTION = (By.CLASS_NAME, "inventory_details_desc")
    PRODUCT_PRICE = (By.CLASS_NAME, "inventory_details_price")
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, "button[id^='add-to-cart']")
    REMOVE_BUTTON = (By.CSS_SELECTOR, "button[id^='remove']")
    BACK_TO_PRODUCTS = (By.ID, "back-to-products")
    PRODUCT_IMAGE = (By.CLASS_NAME, "inventory_details_img")
    
    def get_product_name(self):
        """Get product name"""
        return self.get_text(self.PRODUCT_NAME)
    
    def get_product_description(self):
        """Get product description"""
        return self.get_text(self.PRODUCT_DESCRIPTION)
    
    def get_product_price(self):
        """Get product price"""
        return self.get_text(self.PRODUCT_PRICE)
    
    def click_add_to_cart(self):
        """Add product to cart"""
        self.click(self.ADD_TO_CART_BUTTON)
    
    def click_remove(self):
        """Remove product from cart"""
        self.click(self.REMOVE_BUTTON)
    
    def is_remove_button_displayed(self):
        """Check if remove button is displayed"""
        return self.is_displayed(self.REMOVE_BUTTON, timeout=5)
    
    def click_back_to_products(self):
        """Click back to products button"""
        self.click(self.BACK_TO_PRODUCTS)
    
    def is_product_image_displayed(self):
        """Check if product image is displayed"""
        return self.is_displayed(self.PRODUCT_IMAGE)