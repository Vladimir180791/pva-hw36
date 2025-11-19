from selenium.webdriver.common.by import By
from src.pages.base_page import BasePage


class CartPage(BasePage):
    """Page Object для страницы корзины OpenCart"""
    
    # Locators
    CART_ITEMS = (By.CSS_SELECTOR, "div.table-responsive tbody tr")
    ITEM_NAME = (By.CSS_SELECTOR, "td.text-left a")
    ITEM_QUANTITY = (By.CSS_SELECTOR, "input[name*='quantity']")
    ITEM_PRICE = (By.CSS_SELECTOR, "td:nth-child(5)")
    ITEM_TOTAL = (By.CSS_SELECTOR, "td:nth-child(6)")
    UPDATE_BUTTON = (By.CSS_SELECTOR, "button[data-original-title='Update']")
    REMOVE_BUTTON = (By.CSS_SELECTOR, "button[data-original-title='Remove']")
    CONTINUE_SHOPPING_BUTTON = (By.LINK_TEXT, "Continue Shopping")
    CHECKOUT_BUTTON = (By.LINK_TEXT, "Checkout")
    EMPTY_CART_MESSAGE = (By.CSS_SELECTOR, "div#content p")
    CART_TOTAL = (By.CSS_SELECTOR, "div.table-responsive tfoot tr:last-child td:last-child")
    
    def get_cart_items_count(self) -> int:
        """Получить количество товаров в корзине"""
        items = self.driver.find_elements(*self.CART_ITEMS)
        return len(items)
    
    def get_item_names(self) -> list:
        """Получить названия всех товаров в корзине"""
        items = self.driver.find_elements(*self.ITEM_NAME)
        return [item.text for item in items]
    
    def get_item_quantity(self, item_name: str) -> int:
        """Получить количество конкретного товара"""
        item_row = self._find_item_row(item_name)
        if item_row:
            quantity_input = item_row.find_element(*self.ITEM_QUANTITY)
            return int(quantity_input.get_attribute("value"))
        return 0
    
    def update_item_quantity(self, item_name: str, new_quantity: int):
        """Обновить количество товара"""
        item_row = self._find_item_row(item_name)
        if item_row:
            quantity_input = item_row.find_element(*self.ITEM_QUANTITY)
            quantity_input.clear()
            quantity_input.send_keys(str(new_quantity))
            
            update_btn = item_row.find_element(*self.UPDATE_BUTTON)
            update_btn.click()
    
    def remove_item(self, item_name: str):
        """Удалить товар из корзины"""
        item_row = self._find_item_row(item_name)
        if item_row:
            remove_btn = item_row.find_element(*self.REMOVE_BUTTON)
            remove_btn.click()
            # Ждем обновления корзины
            self.wait.until(lambda driver: self.get_cart_items_count() >= 0)
    
    def get_item_price(self, item_name: str) -> float:
        """Получить цену товара"""
        item_row = self._find_item_row(item_name)
        if item_row:
            price_text = item_row.find_element(*self.ITEM_PRICE).text
            return self._parse_price(price_text)
        return 0.0
    
    def get_item_total(self, item_name: str) -> float:
        """Получить общую стоимость товара"""
        item_row = self._find_item_row(item_name)
        if item_row:
            total_text = item_row.find_element(*self.ITEM_TOTAL).text
            return self._parse_price(total_text)
        return 0.0
    
    def get_cart_total(self) -> float:
        """Получить общую стоимость корзины"""
        if self.is_element_present(self.CART_TOTAL):
            total_text = self.get_text(self.CART_TOTAL)
            return self._parse_price(total_text)
        return 0.0
    
    def continue_shopping(self):
        """Продолжить покупки"""
        self.click_element(self.CONTINUE_SHOPPING_BUTTON)
    
    def proceed_to_checkout(self):
        """Перейти к оформлению заказа"""
        self.click_element(self.CHECKOUT_BUTTON)
    
    def is_cart_empty(self) -> bool:
        """Проверить пуста ли корзина"""
        return self.is_element_present(self.EMPTY_CART_MESSAGE)
    
    def get_empty_cart_message(self) -> str:
        """Получить сообщение о пустой корзине"""
        if self.is_cart_empty():
            return self.get_text(self.EMPTY_CART_MESSAGE)
        return ""
    
    def _find_item_row(self, item_name: str):
        """Найти строку товара по имени"""
        items = self.driver.find_elements(*self.CART_ITEMS)
        for item in items:
            name_element = item.find_element(*self.ITEM_NAME)
            if name_element.text == item_name:
                return item
        return None
    
    def _parse_price(self, price_text: str) -> float:
        """Парсить цену из текста"""
        import re
        # Удаляем все символы кроме цифр и точки
        cleaned = re.sub(r'[^\d.]', '', price_text)
        return float(cleaned) if cleaned else 0.0