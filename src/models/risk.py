"""Модель риска"""

from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class RiskLevel(Enum):
    """Уровни риска"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RiskType(Enum):
    """Типы рисков"""
    FLOOD = "flood"
    FIRE = "fire"
    EARTHQUAKE = "earthquake"
    STORM = "storm"
    HEAT = "heat"
    COLD = "cold"
    TECHNOGENIC = "technogenic"
    EPIDEMIC = "epidemic"
    RADIATION = "radiation"
    CHEMICAL = "chemical"


@dataclass
class RiskZone:
    """Зона риска"""
    latitude: float
    longitude: float
    radius_km: float
    polygon: Optional[List[tuple]] = None


@dataclass
class Risk:
    """Модель риска"""
    id: str
    type: RiskType
    level: RiskLevel
    title: str
    description: str
    zone: RiskZone
    
    # Временные рамки
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    
    # Инструкции
    instructions: List[str] = field(default_factory=list)
    evacuation_required: bool = False
    
    # Метаданные
    source: str = "МЧС"
    created_at: datetime = field(default_factory=datetime.now)
    updated_at:  datetime = field(default_factory=datetime. now)
    
    @property
    def is_active(self) -> bool:
        """Проверка активности риска"""
        now = datetime.now()
        if self.start_time and now < self.start_time:
            return False
        if self. end_time and now > self.end_time:
            return False
        return True
    
    def get_level_color(self) -> str:
        """Получение цвета уровня риска"""
        colors = {
            RiskLevel.LOW:  "#4CAF50",
            RiskLevel.MEDIUM:  "#FFC107",
            RiskLevel.HIGH: "#FF9800",
            RiskLevel. CRITICAL: "#F44336",
        }
        return colors. get(self.level, "#9E9E9E")