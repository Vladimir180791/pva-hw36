from selenium.webdriver.common.by import By
from src.pages.base_page import BasePage


class ProductPage(BasePage):
    """Page Object для страницы товара OpenCart"""
    
    # Locators
    PRODUCT_NAME = (By.CSS_SELECTOR, "h1")
    PRODUCT_PRICE = (By.CSS_SELECTOR, "li h2")
    ADD_TO_CART_BUTTON = (By.ID, "button-cart")
    QUANTITY_INPUT = (By.ID, "input-quantity")
    PRODUCT_IMAGES = (By.CSS_SELECTOR, "ul.thumbnails img")
    DESCRIPTION_TAB = (By.CSS_SELECTOR, "a[href='#tab-description']")
    SPECIFICATION_TAB = (By.CSS_SELECTOR, "a[href='#tab-specification']")
    REVIEWS_TAB = (By.CSS_SELECTOR, "a[href='#tab-review']")
    ALERT_SUCCESS = (By.CSS_SELECTOR, "div.alert-success")
    
    def get_product_name(self) -> str:
        """Получить название товара"""
        return self.get_text(self.PRODUCT_NAME)
    
    def get_product_price(self) -> str:
        """Получить цену товара"""
        return self.get_text(self.PRODUCT_PRICE)
    
    def set_quantity(self, quantity: int):
        """Установить количество товара"""
        self.fill_field(self.QUANTITY_INPUT, str(quantity))
    
    def add_to_cart(self, quantity: int = 1):
        """Добавить товар в корзину"""
        if quantity != 1:
            self.set_quantity(quantity)
        self.click_element(self.ADD_TO_CART_BUTTON)
    
    def is_add_to_cart_success(self) -> bool:
        """Проверить успешность добавления в корзину"""
        return self.is_element_present(self.ALERT_SUCCESS)
    
    def get_success_message(self) -> str:
        """Получить сообщение об успешном добавлении"""
        if self.is_add_to_cart_success():
            return self.get_text(self.ALERT_SUCCESS)
        return ""
    
    def switch_to_description_tab(self):
        """Переключиться на вкладку описания"""
        self.click_element(self.DESCRIPTION_TAB)
    
    def switch_to_specification_tab(self):
        """Переключиться на вкладку характеристик"""
        self.click_element(self.SPECIFICATION_TAB)
    
    def switch_to_reviews_tab(self):
        """Переключиться на вкладку отзывов"""
        self.click_element(self.REVIEWS_TAB)
    
    def get_product_images_count(self) -> int:
        """Получить количество изображений товара"""
        images = self.driver.find_elements(*self.PRODUCT_IMAGES)
        return len(images)
    
    def is_product_available(self) -> bool:
        """Проверить доступность товара (кнопка Add to Cart активна)"""
        add_button = self.driver.find_element(*self.ADD_TO_CART_BUTTON)
        return add_button.is_enabled()