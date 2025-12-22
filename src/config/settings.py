"""Настройки приложения"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Settings:
    """Класс настроек приложения"""
    
    # API настройки
    weather_api_url: str = "https://api.openweathermap.org/data/2.5"
    weather_api_key:  Optional[str] = None
    
    # База данных
    db_path: str = "data/mnur.db"
    
    # Уведомления
    notification_check_interval: int = 300  # секунды
    
    # Геолокация
    default_latitude: float = 55.7558  # Москва
    default_longitude: float = 37.6173
    
    # Кэширование
    cache_ttl: int = 3600  # секунды
    
    @classmethod
    def load(cls) -> "Settings":
        """Загрузка настроек"""
        return cls()