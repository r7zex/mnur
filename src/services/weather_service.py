"""Сервис погоды"""

from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime
import httpx


@dataclass
class WeatherData:
    """Данные о погоде"""
    temperature: float
    feels_like: float
    humidity: int
    pressure: int
    wind_speed: float
    wind_direction: str
    description: str
    icon: str
    
    # Предупреждения
    alerts: List[str] = None
    
    def __post_init__(self):
        if self.alerts is None:
            self. alerts = []


@dataclass
class WeatherForecast:
    """Прогноз погоды"""
    date: datetime
    temp_min: float
    temp_max: float
    description: str
    icon: str
    precipitation_probability: float = 0


class WeatherService: 
    """Сервис для получения данных о погоде"""
    
    def __init__(self, api_key:  Optional[str] = None):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap. org/data/2.5"
    
    async def get_current_weather(
        self, lat:  float, lon: float
    ) -> Optional[WeatherData]: 
        """Получение текущей погоды"""
        if not self.api_key:
            return self._get_mock_weather()
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/weather",
                    params={
                        "lat": lat,
                        "lon": lon,
                        "appid": self. api_key,
                        "units":  "metric",
                        "lang": "ru",
                    }
                )
                response.raise_for_status()
                data = response.json()
                
                return WeatherData(
                    temperature=data["main"]["temp"],
                    feels_like=data["main"]["feels_like"],
                    humidity=data["main"]["humidity"],
                    pressure=data["main"]["pressure"],
                    wind_speed=data["wind"]["speed"],
                    wind_direction=self._get_wind_direction(data["wind"]. get("deg", 0)),
                    description=data["weather"][0]["description"],
                    icon=data["weather"][0]["icon"],
                )
        except Exception: 
            return self._get_mock_weather()
    
    async def get_forecast(
        self, lat: float, lon:  float, days: int = 5
    ) -> List[WeatherForecast]:
        """Получение прогноза погоды"""
        if not self.api_key:
            return self._get_mock_forecast(days)
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/forecast",
                    params={
                        "lat": lat,
                        "lon": lon,
                        "appid": self.api_key,
                        "units": "metric",
                        "lang": "ru",
                    }
                )
                response.raise_for_status()
                data = response.json()
                
                forecasts = []
                for item in data["list"][:days * 8: 8]: 
                    forecasts. append(WeatherForecast(
                        date=datetime.fromtimestamp(item["dt"]),
                        temp_min=item["main"]["temp_min"],
                        temp_max=item["main"]["temp_max"],
                        description=item["weather"][0]["description"],
                        icon=item["weather"][0]["icon"],
                        precipitation_probability=item.get("pop", 0) * 100,
                    ))
                return forecasts
        except Exception:
            return self._get_mock_forecast(days)
    
    async def get_weather_alerts(self, lat: float, lon: float) -> List[str]: 
        """Получение погодных предупреждений"""
        # В реальном приложении здесь был бы запрос к API
        return []
    
    def _get_wind_direction(self, degrees: int) -> str:
        """Преобразование градусов в направление ветра"""
        directions = ["С", "СВ", "В", "ЮВ", "Ю", "ЮЗ", "З", "СЗ"]
        index = round(degrees / 45) % 8
        return directions[index]
    
    def _get_mock_weather(self) -> WeatherData:
        """Моковые данные о погоде"""
        return WeatherData(
            temperature=-5,
            feels_like=-10,
            humidity=75,
            pressure=1013,
            wind_speed=5. 2,
            wind_direction="СВ",
            description="облачно с прояснениями",
            icon="03d",
            alerts=[],
        )
    
    def _get_mock_forecast(self, days: int) -> List[WeatherForecast]: 
        """Моковый прогноз погоды"""
        from datetime import timedelta
        
        forecasts = []
        base_date = datetime. now()
        
        for i in range(days):
            forecasts.append(WeatherForecast(
                date=base_date + timedelta(days=i),
                temp_min=-8 + i,
                temp_max=-2 + i,
                description="переменная облачность",
                icon="03d",
                precipitation_probability=20 + i * 5,
            ))
        
        return forecasts