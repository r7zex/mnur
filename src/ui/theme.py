"""Тема приложения МНУР"""

from dataclasses import dataclass


@dataclass
class MNURTheme:
    """Тема приложения"""
    
    # Основные цвета
    primary_color: str = "#1565C0"  # Синий
    primary_light:  str = "#42A5F5"
    primary_dark: str = "#0D47A1"
    
    # Цвета акцентов
    accent_color: str = "#FF5722"
    accent_light: str = "#FF8A65"
    
    # Цвета состояний
    success_color: str = "#4CAF50"
    warning_color:  str = "#FFC107"
    error_color: str = "#D32F2F"
    danger_color: str = "#C62828"
    
    # Нейтральные цвета
    background_color:  str = "#F5F7FA"
    surface_color: str = "#FFFFFF"
    card_color: str = "#FFFFFF"
    
    # Текстовые цвета
    text_primary: str = "#212121"
    text_secondary: str = "#757575"
    text_hint: str = "#9E9E9E"
    text_on_primary: str = "#FFFFFF"
    
    # Границы и тени
    border_color: str = "#E0E0E0"
    shadow_color: str = "#00000020"
    
    # Размеры
    border_radius: int = 16
    border_radius_small: int = 8
    border_radius_large: int = 24
    
    # Отступы
    padding_xs: int = 4
    padding_sm: int = 8
    padding_md: int = 16
    padding_lg: int = 24
    padding_xl: int = 32
    
    # Размеры шрифтов
    font_size_xs: int = 10
    font_size_sm: int = 12
    font_size_md:  int = 14
    font_size_lg: int = 16
    font_size_xl: int = 20
    font_size_xxl: int = 24
    font_size_title: int = 28
    
    # Цвета карточек меню
    emergency_card_color: str = "#D32F2F"
    instructions_card_color:  str = "#E3F2FD"
    risks_card_color:  str = "#E3F2FD"
    weather_card_color:  str = "#E3F2FD"