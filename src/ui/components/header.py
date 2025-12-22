"""Компонент шапки приложения"""

import flet as ft
from src.ui. theme import MNURTheme


class Header(ft.UserControl):
    """Шапка приложения с логотипом и уведомлениями"""
    
    def __init__(
        self,
        theme: MNURTheme,
        notification_count: int = 0,
        on_notification_click=None,
    ):
        super().__init__()
        self.theme = theme
        self.notification_count = notification_count
        self.on_notification_click = on_notification_click
    
    def build(self):
        # Логотип (заменитель)
        logo = ft.Container(
            content=ft.Text(
                "🦅",
                size=40,
            ),
            width=50,
            height=50,
        )
        
        # Название министерства
        title_column = ft.Column(
            controls=[
                ft. Text(
                    "МНУР",
                    size=self.theme.font_size_xl,
                    weight=ft.FontWeight. BOLD,
                    color=self.theme.text_primary,
                ),
                ft.Text(
                    "Министерство национальной",
                    size=self.theme.font_size_sm,
                    color=self.theme. text_secondary,
                ),
                ft.Text(
                    "устойчивости и управления рисками",
                    size=self. theme.font_size_sm,
                    color=self. theme.text_secondary,
                ),
            ],
            spacing=0,
        )
        
        # Кнопка уведомлений
        notification_button = ft. Stack(
            controls=[
                ft.IconButton(
                    icon=ft.Icons.NOTIFICATIONS_OUTLINED,
                    icon_color=self. theme.primary_color,
                    icon_size=28,
                    on_click=self. on_notification_click,
                ),
                # Бейдж с количеством
                ft.Container(
                    content=ft.Text(
                        str(self.notification_count),
                        size=10,
                        color=ft.Colors.WHITE,
                        weight=ft.FontWeight.BOLD,
                    ),
                    width=18,
                    height=18,
                    border_radius=9,
                    bgcolor=self.theme. error_color,
                    alignment=ft.alignment. center,
                    right=0,
                    top=0,
                    visible=self.notification_count > 0,
                ),
            ],
            width=40,
            height=40,
        )
        
        return ft.Container(
            content=ft.Row(
                controls=[
                    logo,
                    ft.Container(width=10),
                    title_column,
                    ft.Container(expand=True),
                    notification_button,
                ],
                alignment=ft.MainAxisAlignment. START,
            ),
            padding=ft.padding.only(
                left=self.theme. padding_md,
                right=self.theme.padding_md,
                top=self.theme.padding_md,
                bottom=self.theme.padding_sm,
            ),
            bgcolor=self.theme. surface_color,
        )