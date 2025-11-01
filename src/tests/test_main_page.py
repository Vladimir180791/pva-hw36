import pytest
from src.pages.main_page import MainPage


class TestMainPage:
    def test_main_page_loads(self, driver, base_url):
        """Test that main page loads successfully"""
        main_page = MainPage(driver)
        assert main_page.is_logo_visible()
        assert "Your Store" in driver.title

    def test_navigation_menu(self, driver):
        """Test main navigation menu"""
        main_page = MainPage(driver)
        assert main_page.is_navigation_visible()
        
        # Test menu items
        menu_items = main_page.get_menu_items()
        assert len(menu_items) > 0
        assert "Desktops" in menu_items or "Components" in menu_items

    def test_search_functionality(self, driver):
        """Test search functionality"""
        main_page = MainPage(driver)
        main_page.search_for_product("iphone")
        
        # Verify search results
        assert "Search - iphone" in driver.title
        assert main_page.is_search_results_visible()