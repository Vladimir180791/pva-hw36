import pytest
import allure
from src.pages.main_page import MainPage
from src.pages.product_page import ProductPage


@allure.feature("Product Management")
@allure.story("Product Page Functionality")
class TestProduct:
    """Тесты для функциональности товаров"""
    
    @allure.title("Проверка отображения информации о товаре")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_product_information_display(self, driver):
        """Тест отображения информации о товаре"""
        with allure.step("Перейти на главную страницу"):
            main_page = MainPage(driver)
            assert main_page.is_logo_visible()
        
        with allure.step("Получить список товаров"):
            product_names = main_page.get_featured_product_names()
            assert len(product_names) > 0, "Нет товаров на главной странице"
            
        with allure.step("Открыть первый товар"):
            main_page.click_featured_product(product_names[0])
            
        with allure.step("Проверить информацию о товаре"):
            product_page = ProductPage(driver)
            assert product_page.get_product_name() == product_names[0]
            assert product_page.get_product_price() != ""
            assert product_page.get_product_images_count() > 0
            assert product_page.is_product_available()
    
    @allure.title("Добавление товара в корзину")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_add_product_to_cart(self, driver):
        """Тест добавления товара в корзину"""
        with allure.step("Перейти на главную страницу"):
            main_page = MainPage(driver)
            
        with allure.step("Открыть первый товар"):
            product_names = main_page.get_featured_product_names()
            main_page.click_featured_product(product_names[0])
            
        with allure.step("Добавить товар в корзину"):
            product_page = ProductPage(driver)
            initial_cart_count = main_page.get_cart_items_count()
            product_page.add_to_cart()
            
        with allure.step("Проверить успешность добавления"):
            assert product_page.is_add_to_cart_success()
            success_message = product_page.get_success_message()
            assert "Success" in success_message or "Успешно" in success_message
            
        with allure.step("Проверить обновление счетчика корзины"):
            main_page = MainPage(driver)
            updated_cart_count = main_page.get_cart_items_count()
            assert updated_cart_count == initial_cart_count + 1
    
    @allure.title("Добавление нескольких товаров в корзину")
    @allure.severity(allure.severity_level.NORMAL)
    def test_add_multiple_products_to_cart(self, driver):
        """Тест добавления нескольких товаров одного типа"""
        with allure.step("Перейти на главную страницу"):
            main_page = MainPage(driver)
            
        with allure.step("Открыть первый товар"):
            product_names = main_page.get_featured_product_names()
            main_page.click_featured_product(product_names[0])
            
        with allure.step("Добавить 3 товара в корзину"):
            product_page = ProductPage(driver)
            initial_cart_count = main_page.get_cart_items_count()
            product_page.add_to_cart(quantity=3)
            
        with allure.step("Проверить успешность добавления"):
            assert product_page.is_add_to_cart_success()
            
        with allure.step("Проверить обновление счетчика корзины"):
            main_page = MainPage(driver)
            updated_cart_count = main_page.get_cart_items_count()
            assert updated_cart_count == initial_cart_count + 3
    
    @allure.title("Проверка вкладок товара")
    @allure.severity(allure.severity_level.NORMAL)
    def test_product_tabs_functionality(self, driver):
        """Тест функциональности вкладок товара"""
        with allure.step("Перейти на главную страницу"):
            main_page = MainPage(driver)
            
        with allure.step("Открыть первый товар"):
            product_names = main_page.get_featured_product_names()
            main_page.click_featured_product(product_names[0])
            
        with allure.step("Проверить переключение вкладок"):
            product_page = ProductPage(driver)
            
            product_page.switch_to_description_tab()
            # Можно добавить проверку контента вкладки
            
            product_page.switch_to_specification_tab()
            # Можно добавить проверку контента вкладки
            
            product_page.switch_to_reviews_tab()
            # Можно добавить проверку контента вкладки
    
    @pytest.mark.smoke
    @allure.title("Smoke test: базовая функциональность товара")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_product_smoke(self, driver):
        """Smoke test базовой функциональности товара"""
        main_page = MainPage(driver)
        product_names = main_page.get_featured_product_names()
        main_page.click_featured_product(product_names[0])
        
        product_page = ProductPage(driver)
        
        # Проверяем базовые элементы
        assert product_page.get_product_name() != ""
        assert product_page.get_product_price() != ""
        assert product_page.is_product_available()
        
        # Проверяем добавление в корзину
        initial_count = main_page.get_cart_items_count()
        product_page.add_to_cart()
        assert product_page.is_add_to_cart_success()
        
        # Проверяем обновление счетчика
        assert main_page.get_cart_items_count() == initial_count + 1