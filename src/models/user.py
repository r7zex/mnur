"""Модель пользователя"""

from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime


@dataclass
class UserLocation:
    """Локация пользователя"""
    latitude:  float
    longitude:  float
    address: Optional[str] = None
    region: Optional[str] = None


@dataclass
class User:
    """Модель пользователя"""
    id: str
    phone: Optional[str] = None
    email: Optional[str] = None
    full_name: Optional[str] = None
    
    # Локации
    home_location: Optional[UserLocation] = None
    current_location: Optional[UserLocation] = None
    saved_routes: List[dict] = field(default_factory=list)
    
    # Настройки уведомлений
    notifications_enabled:  bool = True
    risk_types_subscribed: List[str] = field(default_factory=list)
    
    # Семья
    family_members: List[dict] = field(default_factory=list)
    
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> dict:
        """Преобразование в словарь"""
        return {
            "id": self. id,
            "phone": self.phone,
            "email": self.email,
            "full_name": self.full_name,
            "notifications_enabled": self. notifications_enabled,
        }