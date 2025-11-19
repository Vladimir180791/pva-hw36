import pytest
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="Browser to run tests")
    parser.addoption("--browser-version", action="store", default="latest", help="Browser version")


@pytest.fixture(scope="function")
def driver(request):
    browser = os.getenv('BROWSER', 'chrome')
    browser_version = os.getenv('BROWSER_VERSION', 'latest')
    app_url = os.getenv('APP_URL', 'http://opencart:8080')
    selenoid_url = os.getenv('SELENOID_URL', 'http://localhost:4444/wd/hub')
    
    if browser == 'chrome':
        options = ChromeOptions()
    elif browser == 'firefox':
        options = FirefoxOptions()
    else:
        raise ValueError(f"Unsupported browser: {browser}")
    
    # Настройки для Selenoid
    capabilities = {
        "browserName": browser,
        "browserVersion": browser_version,
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": False
        }
    }
    
    options.set_capability("selenoid:options", capabilities["selenoid:options"])
    
    driver = webdriver.Remote(
        command_executor=selenoid_url,
        options=options
    )
    
    driver.maximize_window()
    driver.get(app_url)
    
    yield driver
    
    driver.quit()


@pytest.fixture(scope="session")
def base_url():
    return os.getenv('APP_URL', 'http://opencart:8080')