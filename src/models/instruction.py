"""Модель инструкции"""

from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime


@dataclass
class InstructionStep:
    """Шаг инструкции"""
    order:  int
    title:  str
    description:  str
    image:  Optional[str] = None
    is_critical: bool = False


@dataclass
class Instruction:
    """Модель инструкции"""
    id: str
    title: str
    category: str  # preparation, emergency, evacuation, first_aid
    risk_type: Optional[str] = None
    
    # Содержимое
    summary: str = ""
    steps: List[InstructionStep] = field(default_factory=list)
    
    # Чеклист
    checklist: List[dict] = field(default_factory=list)
    
    # Метаданные
    difficulty: str = "easy"  # easy, medium, hard
    estimated_time: Optional[int] = None  # в минутах
    priority: int = 0
    
    # Версионирование
    version:  str = "1.0"
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    # Статистика
    views_count: int = 0
    completed_count: int = 0
    
    def get_category_name(self) -> str:
        """Получение названия категории"""
        categories = {
            "preparation": "Подготовка",
            "emergency":  "Экстренная ситуация",
            "evacuation":  "Эвакуация",
            "first_aid":  "Первая помощь",
        }
        return categories.get(self. category, "Общее")
    
    def to_dict(self) -> dict:
        """Преобразование в словарь"""
        return {
            "id":  self.id,
            "title": self.title,
            "category": self. category,
            "risk_type": self.risk_type,
            "summary":  self.summary,
            "steps_count": len(self.steps),
        }