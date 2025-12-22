"""Сервис управления рисками"""

from typing import List, Optional, Dict
from datetime import datetime
from src.models.risk import Risk, RiskLevel, RiskType, RiskZone
from src.services.database_service import DatabaseService


class RiskService:
    """Сервис для работы с рисками"""
    
    def __init__(self, db_service:  Optional[DatabaseService] = None):
        self.db_service = db_service or DatabaseService()
        self._cache:  Dict[str, Risk] = {}
    
    async def get_active_risks(
        self, lat:  Optional[float] = None, lon: Optional[float] = None
    ) -> List[Risk]:
        """Получение активных рисков"""
        # Возвращаем моковые данные для демонстрации
        return self._get_mock_risks()
    
    async def get_risk_by_id(self, risk_id: str) -> Optional[Risk]: 
        """Получение риска по ID"""
        if risk_id in self._cache:
            return self._cache[risk_id]
        return None
    
    async def get_risks_for_location(
        self, lat: float, lon: float, radius_km: float = 50
    ) -> List[Risk]:
        """Получение рисков для локации"""
        all_risks = await self.get_active_risks()
        # В реальном приложении здесь была бы фильтрация по расстоянию
        return all_risks
    
    async def get_risk_statistics(self) -> Dict:
        """Получение статистики по рискам"""
        risks = await self.get_active_risks()
        
        stats = {
            "total":  len(risks),
            "by_level": {
                "low":  0,
                "medium": 0,
                "high": 0,
                "critical": 0,
            },
            "by_type":  {},
        }
        
        for risk in risks: 
            stats["by_level"][risk.level. value] += 1
            risk_type = risk. type.value
            stats["by_type"][risk_type] = stats["by_type"]. get(risk_type, 0) + 1
        
        return stats
    
    def _get_mock_risks(self) -> List[Risk]:
        """Моковые данные о рисках"""
        return [
            Risk(
                id="risk_1",
                type=RiskType. FLOOD,
                level=RiskLevel.MEDIUM,
                title="Паводковая ситуация",
                description="Возможен подъём уровня воды в реках региона",
                zone=RiskZone(
                    latitude=55.7558,
                    longitude=37.6173,
                    radius_km=25,
                ),
                instructions=[
                    "Подготовьте тревожный рюкзак",
                    "Переместите ценные вещи на верхние этажи",
                    "Следите за сообщениями МЧС",
                ],
                source="Росгидромет",
            ),
            Risk(
                id="risk_2",
                type=RiskType.HEAT,
                level=RiskLevel.LOW,
                title="Аномальная жара",
                description="Ожидается повышение температуры до +35°C",
                zone=RiskZone(
                    latitude=55.7558,
                    longitude=37.6173,
                    radius_km=100,
                ),
                instructions=[
                    "Избегайте длительного пребывания на солнце",
                    "Пейте больше воды",
                    "Носите головной убор",
                ],
                source="Росгидромет",
            ),
        ]
    
    def get_risk_type_name(self, risk_type: RiskType) -> str:
        """Получение названия типа риска"""
        names = {
            RiskType.FLOOD: "Паводок",
            RiskType.FIRE: "Пожар",
            RiskType.EARTHQUAKE: "Землетрясение",
            RiskType.STORM: "Шторм",
            RiskType. HEAT: "Аномальная жара",
            RiskType. COLD: "Аномальный холод",
            RiskType. TECHNOGENIC: "Техногенная авария",
            RiskType. EPIDEMIC: "Эпидемия",
            RiskType. RADIATION: "Радиационная угроза",
            RiskType. CHEMICAL: "Химическая угроза",
        }
        return names.get(risk_type, "Неизвестно")
    
    def get_risk_icon(self, risk_type: RiskType) -> str:
        """Получение иконки типа риска"""
        icons = {
            RiskType. FLOOD: "🌊",
            RiskType.FIRE: "🔥",
            RiskType.EARTHQUAKE:  "🌋",
            RiskType.STORM: "🌪️",
            RiskType. HEAT: "☀️",
            RiskType. COLD: "❄️",
            RiskType.TECHNOGENIC: "⚠️",
            RiskType.EPIDEMIC: "🦠",
            RiskType.RADIATION: "☢️",
            RiskType. CHEMICAL: "☣️",
        }
        return icons. get(risk_type, "⚠️")