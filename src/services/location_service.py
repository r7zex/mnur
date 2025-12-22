"""Сервис геолокации"""

from dataclasses import dataclass
from typing import Optional, List, Tuple
import math


@dataclass
class Location:
    """Локация"""
    latitude: float
    longitude: float
    accuracy: Optional[float] = None
    address: Optional[str] = None
    city: Optional[str] = None
    region: Optional[str] = None


class LocationService: 
    """Сервис для работы с геолокацией"""
    
    def __init__(self):
        self._current_location: Optional[Location] = None
        self._default_location = Location(
            latitude=55.7558,
            longitude=37.6173,
            city="Москва",
            region="Московская область",
        )
    
    def get_current_location(self) -> Location:
        """Получение текущей локации"""
        if self._current_location:
            return self._current_location
        return self._default_location
    
    def set_current_location(self, lat: float, lon: float):
        """Установка текущей локации"""
        self._current_location = Location(
            latitude=lat,
            longitude=lon,
        )
    
    @staticmethod
    def calculate_distance(
        lat1: float, lon1: float, lat2: float, lon2: float
    ) -> float:
        """Расчёт расстояния между двумя точками (км)"""
        R = 6371  # Радиус Земли в км
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)
        
        a = (
            math.sin(delta_lat / 2) ** 2 +
            math. cos(lat1_rad) * math.cos(lat2_rad) *
            math.sin(delta_lon / 2) ** 2
        )
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        return R * c
    
    @staticmethod
    def get_bearing(
        lat1: float, lon1: float, lat2: float, lon2: float
    ) -> float:
        """Расчёт направления между двумя точками (градусы)"""
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lon = math.radians(lon2 - lon1)
        
        x = math.sin(delta_lon) * math.cos(lat2_rad)
        y = (
            math.cos(lat1_rad) * math.sin(lat2_rad) -
            math.sin(lat1_rad) * math.cos(lat2_rad) * math.cos(delta_lon)
        )
        
        bearing = math. atan2(x, y)
        bearing = math.degrees(bearing)
        bearing = (bearing + 360) % 360
        
        return bearing
    
    @staticmethod
    def get_direction_name(bearing: float) -> str:
        """Получение названия направления"""
        directions = [
            "север", "северо-восток", "восток", "юго-восток",
            "юг", "юго-запад", "запад", "северо-запад"
        ]
        index = round(bearing / 45) % 8
        return directions[index]
    
    def find_nearest_point(
        self, points: List[Tuple[float, float]], from_lat: float, from_lon: float
    ) -> Optional[Tuple[int, float]]:
        """Поиск ближайшей точки"""
        if not points:
            return None
        
        min_distance = float('inf')
        min_index = 0
        
        for i, (lat, lon) in enumerate(points):
            distance = self.calculate_distance(from_lat, from_lon, lat, lon)
            if distance < min_distance: 
                min_distance = distance
                min_index = i
        
        return min_index, min_distance