import os
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class JenkinsConfig:
    """Конфигурация параметров Jenkins job"""
    
    # Параметры по умолчанию
    DEFAULT_SELENOID_URL: str = "http://localhost:4444/wd/hub"
    DEFAULT_APP_URL: str = "http://opencart:8080"
    DEFAULT_BROWSER: str = "chrome"
    DEFAULT_BROWSER_VERSION: str = "latest"
    DEFAULT_THREADS: int = 2
    DEFAULT_TEST_TIMEOUT: int = 30
    
    # Настройки отчетности
    ALLURE_RESULTS_DIR: str = "reports/allure-results"
    ALLURE_REPORT_DIR: str = "reports/allure-report"
    SCREENSHOTS_DIR: str = "reports/screenshots"
    LOGS_DIR: str = "reports/logs"
    
    # Настройки тестов
    TEST_PATH: str = "src/tests"
    TEST_PATTERN: str = "test_*.py"
    
    def get_environment_variables(self) -> Dict[str, str]:
        """Получить переменные окружения для тестов"""
        return {
            'SELENOID_URL': os.getenv('SELENOID_URL', self.DEFAULT_SELENOID_URL),
            'APP_URL': os.getenv('APP_URL', self.DEFAULT_APP_URL),
            'BROWSER': os.getenv('BROWSER', self.DEFAULT_BROWSER),
            'BROWSER_VERSION': os.getenv('BROWSER_VERSION', self.DEFAULT_BROWSER_VERSION),
            'THREADS': str(os.getenv('THREADS', self.DEFAULT_THREADS)),
            'TEST_TIMEOUT': str(self.DEFAULT_TEST_TIMEOUT)
        }
    
    def get_pytest_args(self) -> list:
        """Сформировать аргументы для pytest"""
        env_vars = self.get_environment_variables()
        
        return [
            f"--numprocesses={env_vars['THREADS']}",
            f"--alluredir={self.ALLURE_RESULTS_DIR}",
            "--tb=short",
            "-v",
            "--strict-markers",
            f"--timeout={self.DEFAULT_TEST_TIMEOUT}",
            f"{self.TEST_PATH}/{self.TEST_PATTERN}"
        ]
    
    def validate_config(self) -> bool:
        """Валидация конфигурации"""
        required_dirs = [self.ALLURE_RESULTS_DIR, self.SCREENSHOTS_DIR, self.LOGS_DIR]
        
        for directory in required_dirs:
            os.makedirs(directory, exist_ok=True)
            
        return all([
            self.DEFAULT_THREADS > 0,
            self.DEFAULT_TEST_TIMEOUT > 0,
            self.DEFAULT_BROWSER in ['chrome', 'firefox']
        ])


# Создание экземпляра конфигурации
jenkins_config = JenkinsConfig()