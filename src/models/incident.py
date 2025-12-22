"""Модель происшествия"""

from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime, date


@dataclass
class IncidentLocation:
    """Локация происшествия"""
    latitude: float
    longitude: float
    address: str
    region: str


@dataclass
class Incident:
    """Модель происшествия"""
    id: str
    title: str
    description: str
    incident_type: str
    location: IncidentLocation
    
    # Статус
    is_active: bool = True
    severity: str = "medium"  # low, medium, high, critical
    
    # Временные данные
    incident_date: date = field(default_factory=date.today)
    reported_at: datetime = field(default_factory=datetime.now)
    resolved_at: Optional[datetime] = None
    
    # Дополнительная информация
    affected_count: int = 0
    casualties: int = 0
    damage_estimate: Optional[float] = None
    
    # Связанные данные
    related_risks: List[str] = field(default_factory=list)
    images: List[str] = field(default_factory=list)
    
    def to_dict(self) -> dict:
        """Преобразование в словарь"""
        return {
            "id": self.id,
            "title":  self.title,
            "description": self.description,
            "incident_type":  self.incident_type,
            "is_active": self. is_active,
            "severity": self.severity,
            "incident_date":  self.incident_date.isoformat(),
        }