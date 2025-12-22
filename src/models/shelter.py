"""Модель укрытия"""

from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime


@dataclass
class ShelterLocation:
    """Локация укрытия"""
    latitude: float
    longitude: float
    address: str
    floor: Optional[int] = None


@dataclass
class ShelterCapacity:
    """Вместимость укрытия"""
    total:  int
    current: int = 0
    
    @property
    def available(self) -> int:
        return self.total - self.current
    
    @property
    def occupancy_percent(self) -> float:
        if self.total == 0:
            return 0
        return (self.current / self.total) * 100


@dataclass
class Shelter:
    """Модель укрытия"""
    id: str
    name: str
    shelter_type: str  # bunker, shelter, evacuation_point, temporary_housing, medical
    location: ShelterLocation
    capacity: ShelterCapacity
    
    # Характеристики
    is_accessible: bool = True  # Доступно для маломобильных
    has_medical: bool = False
    has_food: bool = False
    has_water: bool = True
    has_power: bool = True
    has_communication: bool = True
    
    # Контактная информация
    phone: Optional[str] = None
    responsible_person: Optional[str] = None
    
    # Рабочие часы (None = круглосуточно)
    working_hours:  Optional[str] = None
    
    # Статус
    is_active: bool = True
    last_verified:  datetime = field(default_factory=datetime.now)
    
    # Дополнительно
    notes: Optional[str] = None
    images: List[str] = field(default_factory=list)
    
    def get_type_icon(self) -> str:
        """Получение иконки типа укрытия"""
        icons = {
            "bunker":  "🏛️",
            "shelter": "🏠",
            "evacuation_point":  "🚩",
            "temporary_housing": "🏕️",
            "medical": "🏥",
        }
        return icons. get(self.shelter_type, "📍")
    
    def to_dict(self) -> dict:
        """Преобразование в словарь"""
        return {
            "id": self.id,
            "name": self. name,
            "type": self.shelter_type,
            "address": self.location. address,
            "capacity_available": self.capacity. available,
            "is_active": self.is_active,
        }