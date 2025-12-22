"""Сервис укрытий"""

from typing import List, Optional
from src.models.shelter import Shelter, ShelterLocation, ShelterCapacity
from src. services.location_service import LocationService


class ShelterService:
    """Сервис для работы с укрытиями"""
    
    def __init__(self):
        self. location_service = LocationService()
        self._shelters = self._load_mock_shelters()
    
    def _load_mock_shelters(self) -> List[Shelter]: 
        """Загрузка моковых данных об укрытиях"""
        return [
            Shelter(
                id="shelter_1",
                name="Школа №564, корпус №5",
                shelter_type="shelter",
                location=ShelterLocation(
                    latitude=55.758,
                    longitude=37.620,
                    address="ул. Примерная, д. 10",
                ),
                capacity=ShelterCapacity(total=200, current=45),
                has_medical=True,
                has_food=True,
                phone="+7 (495) 123-45-67",
            ),
            Shelter(
                id="shelter_2",
                name="Бункер ГО №12",
                shelter_type="bunker",
                location=ShelterLocation(
                    latitude=55.755,
                    longitude=37.618,
                    address="ул. Безопасная, д.  5",
                    floor=-2,
                ),
                capacity=ShelterCapacity(total=500, current=0),
                has_medical=True,
                has_food=True,
                has_communication=True,
                phone="+7 (495) 987-65-43",
            ),
            Shelter(
                id="shelter_3",
                name="Пункт эвакуации #3",
                shelter_type="evacuation_point",
                location=ShelterLocation(
                    latitude=55.760,
                    longitude=37.625,
                    address="пр. Мира, д. 25",
                ),
                capacity=ShelterCapacity(total=150, current=20),
                is_accessible=True,
                has_medical=False,
                has_food=False,
                phone="+7 (495) 111-22-33",
            ),
        ]
    
    def get_all_shelters(self) -> List[Shelter]:
        """Получение всех укрытий"""
        return self._shelters
    
    def get_active_shelters(self) -> List[Shelter]:
        """Получение активных укрытий"""
        return [s for s in self._shelters if s.is_active]
    
    def get_shelter_by_id(self, shelter_id:  str) -> Optional[Shelter]:
        """Получение укрытия по ID"""
        for shelter in self._shelters:
            if shelter.id == shelter_id:
                return shelter
        return None
    
    def get_shelters_by_type(self, shelter_type: str) -> List[Shelter]: 
        """Получение укрытий по типу"""
        return [s for s in self._shelters if s.shelter_type == shelter_type]
    
    def get_nearest_shelters(
        self, lat: float, lon: float, limit: int = 5
    ) -> List[tuple]:
        """Получение ближайших укрытий с расстоянием"""
        shelters_with_distance = []
        
        for shelter in self. get_active_shelters():
            distance = self.location_service.calculate_distance(
                lat, lon,
                shelter.location.latitude,
                shelter.location.longitude
            )
            shelters_with_distance.append((shelter, distance))
        
        shelters_with_distance.sort(key=lambda x: x[1])
        return shelters_with_distance[:limit]
    
    def get_shelters_with_capacity(self, min_capacity: int = 1) -> List[Shelter]: 
        """Получение укрытий с доступной вместимостью"""
        return [
            s for s in self. get_active_shelters()
            if s.capacity.available >= min_capacity
        ]