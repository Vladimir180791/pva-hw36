from selenium.webdriver.common.by import By
from src.pages.base_page import BasePage


class MainPage(BasePage):
    """Page Object для главной страницы OpenCart"""
    
    # Locators
    LOGO = (By.CSS_SELECTOR, "#logo a")
    SEARCH_INPUT = (By.NAME, "search")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button.btn-light")
    CART_BUTTON = (By.CSS_SELECTOR, "div.btn-group button")
    NAVIGATION_MENU = (By.CSS_SELECTOR, "nav#menu")
    MENU_ITEMS = (By.CSS_SELECTOR, "nav#menu ul.nav > li")
    SLIDER = (By.CSS_SELECTOR, "div.swiper-viewport")
    FEATURED_PRODUCTS = (By.CSS_SELECTOR, "div.product-layout")
    PRODUCT_NAMES = (By.CSS_SELECTOR, "div.product-thumb h4 a")
    FOOTER = (By.TAG_NAME, "footer")
    
    def is_logo_visible(self) -> bool:
        """Проверить видимость логотипа"""
        return self.is_element_present(self.LOGO)
    
    def is_navigation_visible(self) -> bool:
        """Проверить видимость навигационного меню"""
        return self.is_element_present(self.NAVIGATION_MENU)
    
    def get_menu_items(self) -> list:
        """Получить список элементов меню"""
        items = self.driver.find_elements(*self.MENU_ITEMS)
        return [item.text for item in items if item.text]
    
    def search_for_product(self, product_name: str):
        """Выполнить поиск товара"""
        self.fill_field(self.SEARCH_INPUT, product_name)
        self.click_element(self.SEARCH_BUTTON)
    
    def is_search_results_visible(self) -> bool:
        """Проверить наличие результатов поиска"""
        results_locator = (By.CSS_SELECTOR, "div.product-thumb")
        return self.is_element_present(results_locator)
    
    def get_featured_products_count(self) -> int:
        """Получить количество товаров в блоке 'Featured'"""
        products = self.driver.find_elements(*self.FEATURED_PRODUCTS)
        return len(products)
    
    def get_featured_product_names(self) -> list:
        """Получить названия товаров в блоке 'Featured'"""
        products = self.driver.find_elements(*self.PRODUCT_NAMES)
        return [product.text for product in products if product.text]
    
    def click_featured_product(self, product_name: str):
        """Кликнуть на товар в блоке 'Featured'"""
        product_link = (By.LINK_TEXT, product_name)
        self.click_element(product_link)
    
    def open_cart(self):
        """Открыть корзину"""
        self.click_element(self.CART_BUTTON)
        cart_dropdown = (By.CSS_SELECTOR, "ul.dropdown-menu")
        self.wait.until(lambda driver: self.is_element_present(cart_dropdown))
    
    def get_cart_items_count(self) -> int:
        """Получить количество товаров в корзине (из бейджа)"""
        cart_count_locator = (By.CSS_SELECTOR, "span.cart-count")
        if self.is_element_present(cart_count_locator):
            count_text = self.get_text(cart_count_locator)
            return int(count_text) if count_text.isdigit() else 0
        return 0