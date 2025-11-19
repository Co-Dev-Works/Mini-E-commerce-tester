from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CartPage(BasePage):
    """Page Object for Shopping Cart Page"""
    
    # Locators
    PAGE_TITLE = (By.CLASS_NAME, "title")
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    CART_ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    CART_ITEM_PRICES = (By.CLASS_NAME, "inventory_item_price")
    CONTINUE_SHOPPING = (By.ID, "continue-shopping")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    REMOVE_BUTTONS = (By.CSS_SELECTOR, "button[id^='remove']")
    CART_QUANTITY = (By.CLASS_NAME, "cart_quantity")
    
    # Checkout Form Locators
    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    POSTAL_CODE = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    CANCEL_BUTTON = (By.ID, "cancel")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "h3[data-test='error']")
    
    # Checkout Overview Locators
    SUBTOTAL = (By.CLASS_NAME, "summary_subtotal_label")
    TAX = (By.CLASS_NAME, "summary_tax_label")
    TOTAL = (By.CLASS_NAME, "summary_total_label")
    FINISH_BUTTON = (By.ID, "finish")
    
    # Checkout Complete Locators
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")
    COMPLETE_TEXT = (By.CLASS_NAME, "complete-text")
    BACK_HOME_BUTTON = (By.ID, "back-to-products")
    
    def is_cart_page_loaded(self):
        """Verify cart page is loaded"""
        return self.is_displayed(self.PAGE_TITLE)
    
    def get_cart_item_count(self):
        """Get number of items in cart"""
        try:
            items = self.find_elements(self.CART_ITEMS)
            return len(items)
        except:
            return 0
    
    def get_cart_item_names(self):
        """Get list of item names in cart"""
        items = self.find_elements(self.CART_ITEM_NAMES)
        return [item.text for item in items]
    
    def get_cart_item_prices(self):
        """Get list of item prices in cart"""
        prices = self.find_elements(self.CART_ITEM_PRICES)
        return [price.text for price in prices]
    
    def remove_item_by_name(self, product_name):
        """Remove specific item from cart"""
        remove_button = (By.XPATH, f"//div[text()='{product_name}']/ancestor::div[@class='cart_item']//button")
        self.click(remove_button)
    
    def click_continue_shopping(self):
        """Click continue shopping button"""
        self.click(self.CONTINUE_SHOPPING)
    
    def click_checkout(self):
        """Click checkout button"""
        self.click(self.CHECKOUT_BUTTON)
    
    def fill_checkout_information(self, first_name, last_name, postal_code):
        """Fill checkout information form"""
        self.enter_text(self.FIRST_NAME, first_name)
        self.enter_text(self.LAST_NAME, last_name)
        self.enter_text(self.POSTAL_CODE, postal_code)
    
    def click_continue_checkout(self):
        """Click continue button on checkout form"""
        self.click(self.CONTINUE_BUTTON)
    
    def get_checkout_error_message(self):
        """Get checkout form error message"""
        return self.get_text(self.ERROR_MESSAGE)
    
    def get_subtotal(self):
        """Get subtotal from checkout overview"""
        return self.get_text(self.SUBTOTAL)
    
    def get_tax(self):
        """Get tax from checkout overview"""
        return self.get_text(self.TAX)
    
    def get_total(self):
        """Get total from checkout overview"""
        return self.get_text(self.TOTAL)
    
    def click_finish(self):
        """Click finish button"""
        self.click(self.FINISH_BUTTON)
    
    def is_checkout_complete(self):
        """Check if order is complete"""
        return self.is_displayed(self.COMPLETE_HEADER)
    
    def get_complete_header_text(self):
        """Get checkout complete header text"""
        return self.get_text(self.COMPLETE_HEADER)
    
    def get_complete_message_text(self):
        """Get checkout complete message text"""
        return self.get_text(self.COMPLETE_TEXT)
    
    def click_back_home(self):
        """Click back home button"""
        self.click(self.BACK_HOME_BUTTON)