from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class SelenoidConfig:
    """Конфигурация для Selenoid capabilities"""
    
    # Базовые capabilities
    ENABLE_VNC: bool = True
    ENABLE_VIDEO: bool = False
    ENABLE_LOG: bool = True
    SCREEN_RESOLUTION: str = "1920x1080x24"
    SESSION_TIMEOUT: str = "5m"
    
    # Браузерные специфичные настройки
    CHROME_OPTIONS = {
        "args": [
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-gpu",
            "--ignore-certificate-errors",
            "--disable-extensions"
        ],
        "prefs": {
            "download.default_directory": "/tmp/downloads",
            "profile.default_content_settings.popups": 0
        }
    }
    
    FIREFOX_OPTIONS = {
        "args": [
            "--no-sandbox",
            "--disable-dev-shm-usage"
        ],
        "prefs": {
            "browser.download.folderList": 2,
            "browser.download.dir": "/tmp/downloads"
        }
    }
    
    def get_capabilities(self, browser: str, browser_version: str = "latest") -> Dict[str, Any]:
        """Получить capabilities для браузера"""
        base_caps = {
            "browserName": browser,
            "browserVersion": browser_version,
            "selenoid:options": {
                "enableVNC": self.ENABLE_VNC,
                "enableVideo": self.ENABLE_VIDEO,
                "enableLog": self.ENABLE_LOG,
                "screenResolution": self.SCREEN_RESOLUTION,
                "sessionTimeout": self.SESSION_TIMEOUT
            },
            "acceptInsecureCerts": True
        }
        
        # Добавляем специфичные опции для браузеров
        if browser == "chrome":
            base_caps["goog:chromeOptions"] = self.CHROME_OPTIONS
        elif browser == "firefox":
            base_caps["moz:firefoxOptions"] = self.FIREFOX_OPTIONS
            
        return base_caps
    
    def get_selenoid_url(self, base_url: str) -> str:
        """Сформировать URL для Selenoid"""
        return f"{base_url}/wd/hub"


# Создание экземпляра конфигурации
selenoid_config = SelenoidConfig()