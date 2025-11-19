import pytest
import allure
from src.pages.main_page import MainPage
from src.pages.product_page import ProductPage
from src.pages.cart_page import CartPage


@allure.feature("Cart Management")
@allure.story("Shopping Cart Functionality")
class TestCart:
    """Тесты для функциональности корзины"""
    
    @allure.title("Добавление товара в корзину и проверка содержимого")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_add_item_to_cart_and_verify(self, driver):
        """Тест добавления товара и проверки корзины"""
        with allure.step("Добавить товар в корзину"):
            main_page = MainPage(driver)
            product_names = main_page.get_featured_product_names()
            main_page.click_featured_product(product_names[0])
            
            product_page = ProductPage(driver)
            product_page.add_to_cart()
            assert product_page.is_add_to_cart_success()
            
        with allure.step("Перейти в корзину"):
            main_page.open_cart()
            cart_page = CartPage(driver)
            
        with allure.step("Проверить содержимое корзины"):
            assert cart_page.get_cart_items_count() == 1
            assert product_names[0] in cart_page.get_item_names()
            assert cart_page.get_item_price(product_names[0]) > 0
            assert cart_page.get_item_total(product_names[0]) > 0
            assert cart_page.get_cart_total() > 0
    
    @allure.title("Обновление количества товара в корзине")
    @allure.severity(allure.severity_level.NORMAL)
    def test_update_item_quantity_in_cart(self, driver):
        """Тест обновления количества товара в корзине"""
        with allure.step("Добавить товар в корзину"):
            main_page = MainPage(driver)
            product_names = main_page.get_featured_product_names()
            main_page.click_featured_product(product_names[0])
            
            product_page = ProductPage(driver)
            product_page.add_to_cart()
            
        with allure.step("Перейти в корзину"):
            main_page.open_cart()
            cart_page = CartPage(driver)
            
        with allure.step("Обновить количество товара"):
            initial_total = cart_page.get_item_total(product_names[0])
            cart_page.update_item_quantity(product_names[0], 3)
            
        with allure.step("Проверить обновленную стоимость"):
            updated_total = cart_page.get_item_total(product_names[0])
            assert updated_total == initial_total * 3
    
    @allure.title("Удаление товара из корзины")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_remove_item_from_cart(self, driver):
        """Тест удаления товара из корзины"""
        with allure.step("Добавить товар в корзину"):
            main_page = MainPage(driver)
            product_names = main_page.get_featured_product_names()
            main_page.click_featured_product(product_names[0])
            
            product_page = ProductPage(driver)
            product_page.add_to_cart()
            
        with allure.step("Перейти в корзину"):
            main_page.open_cart()
            cart_page = CartPage(driver)
            assert cart_page.get_cart_items_count() == 1
            
        with allure.step("Удалить товар из корзины"):
            cart_page.remove_item(product_names[0])
            
        with allure.step("Проверить что корзина пуста"):
            assert cart_page.is_cart_empty()
            empty_message = cart_page.get_empty_cart_message()
            assert "empty" in empty_message.lower() or "пуста" in empty_message.lower()
    
    @allure.title("Добавление нескольких разных товаров в корзину")
    @allure.severity(allure.severity_level.NORMAL)
    def test_add_multiple_different_items_to_cart(self, driver):
        """Тест добавления нескольких разных товаров"""
        main_page = MainPage(driver)
        product_names = main_page.get_featured_product_names()
        
        with allure.step("Добавить первый товар"):
            main_page.click_featured_product(product_names[0])
            product_page = ProductPage(driver)
            product_page.add_to_cart()
            main_page = MainPage(driver)  # Возвращаемся на главную
            
        with allure.step("Добавить второй товар"):
            if len(product_names) > 1:
                main_page.click_featured_product(product_names[1])
                product_page = ProductPage(driver)
                product_page.add_to_cart()
                
        with allure.step("Проверить корзину"):
            main_page.open_cart()
            cart_page = CartPage(driver)
            
            if len(product_names) > 1:
                assert cart_page.get_cart_items_count() == 2
                all_items = cart_page.get_item_names()
                assert product_names[0] in all_items
                assert product_names[1] in all_items
            else:
                assert cart_page.get_cart_items_count() == 1
    
    @allure.title("Проверка общей стоимости корзины")
    @allure.severity(allure.severity_level.NORMAL)
    def test_cart_total_calculation(self, driver):
        """Тест расчета общей стоимости корзины"""
        main_page = MainPage(driver)
        product_names = main_page.get_featured_product_names()
        
        # Добавляем два товара
        for i in range(min(2, len(product_names))):
            main_page.click_featured_product(product_names[i])
            product_page = ProductPage(driver)
            product_page.add_to_cart()
            main_page = MainPage(driver)
            
        # Проверяем корзину
        main_page.open_cart()
        cart_page = CartPage(driver)
        
        total_expected = 0
        for i in range(min(2, len(product_names))):
            total_expected += cart_page.get_item_total(product_names[i])
            
        actual_total = cart_page.get_cart_total()
        assert abs(actual_total - total_expected) < 0.01  # Учитываем погрешность округления
    
    @pytest.mark.smoke
    @allure.title("Smoke test: базовая функциональность корзины")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_cart_smoke(self, driver):
        """Smoke test базовой функциональности корзины"""
        main_page = MainPage(driver)
        product_names = main_page.get_featured_product_names()
        
        # Добавляем товар
        main_page.click_featured_product(product_names[0])
        product_page = ProductPage(driver)
        product_page.add_to_cart()
        
        # Проверяем корзину
        main_page.open_cart()
        cart_page = CartPage(driver)
        
        # Базовые проверки
        assert cart_page.get_cart_items_count() > 0
        assert not cart_page.is_cart_empty()
        assert cart_page.get_cart_total() > 0
        
        # Очищаем корзину
        cart_page.remove_item(product_names[0])
        assert cart_page.is_cart_empty()