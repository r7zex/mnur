"""Сервис уведомлений"""

from dataclasses import dataclass
from typing import List, Optional, Callable
from datetime import datetime
from enum import Enum
import uuid


class NotificationType(Enum):
    """Типы уведомлений"""
    INFO = "info"
    WARNING = "warning"
    ALERT = "alert"
    EMERGENCY = "emergency"


@dataclass
class Notification:
    """Уведомление"""
    id: str
    title: str
    message: str
    type: NotificationType
    is_read: bool = False
    created_at: datetime = None
    
    # Действия
    action_url: Optional[str] = None
    action_label: Optional[str] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
    
    def get_type_color(self) -> str:
        """Цвет типа уведомления"""
        colors = {
            NotificationType.INFO: "#2196F3",
            NotificationType. WARNING: "#FFC107",
            NotificationType. ALERT: "#FF9800",
            NotificationType.EMERGENCY: "#F44336",
        }
        return colors.get(self.type, "#9E9E9E")
    
    def get_type_icon(self) -> str:
        """Иконка типа уведомления"""
        icons = {
            NotificationType.INFO:  "ℹ️",
            NotificationType.WARNING: "⚠️",
            NotificationType. ALERT: "🔔",
            NotificationType.EMERGENCY:  "🚨",
        }
        return icons.get(self.type, "📌")


class NotificationService:
    """Сервис управления уведомлениями"""
    
    def __init__(self):
        self._notifications: List[Notification] = []
        self._callbacks: List[Callable] = []
        self._load_mock_notifications()
    
    def _load_mock_notifications(self):
        """Загрузка моковых уведомлений"""
        self._notifications = [
            Notification(
                id="notif_1",
                title="Предупреждение о погоде",
                message="Завтра ожидается сильный ветер.  Будьте осторожны! ",
                type=NotificationType.WARNING,
                is_read=False,
            ),
        ]
    
    def get_all_notifications(self) -> List[Notification]:
        """Получение всех уведомлений"""
        return sorted(
            self._notifications,
            key=lambda n: n.created_at,
            reverse=True
        )
    
    def get_unread_notifications(self) -> List[Notification]:
        """Получение непрочитанных уведомлений"""
        return [n for n in self._notifications if not n.is_read]
    
    def get_unread_count(self) -> int:
        """Количество непрочитанных уведомлений"""
        return len(self.get_unread_notifications())
    
    def mark_as_read(self, notification_id: str) -> bool:
        """Пометить уведомление как прочитанное"""
        for notification in self._notifications:
            if notification. id == notification_id:
                notification. is_read = True
                self._notify_callbacks()
                return True
        return False
    
    def mark_all_as_read(self):
        """Пометить все уведомления как прочитанные"""
        for notification in self._notifications:
            notification.is_read = True
        self._notify_callbacks()
    
    def add_notification(
        self,
        title: str,
        message: str,
        notification_type: NotificationType = NotificationType.INFO,
        action_url: Optional[str] = None,
        action_label:  Optional[str] = None,
    ) -> Notification: 
        """Добавление нового уведомления"""
        notification = Notification(
            id=f"notif_{uuid.uuid4().hex[: 8]}",
            title=title,
            message=message,
            type=notification_type,
            action_url=action_url,
            action_label=action_label,
        )
        self._notifications.append(notification)
        self._notify_callbacks()
        return notification
    
    def delete_notification(self, notification_id: str) -> bool:
        """Удаление уведомления"""
        for i, notification in enumerate(self._notifications):
            if notification.id == notification_id: 
                del self._notifications[i]
                self._notify_callbacks()
                return True
        return False
    
    def subscribe(self, callback:  Callable):
        """Подписка на изменения"""
        self._callbacks.append(callback)
    
    def unsubscribe(self, callback:  Callable):
        """Отписка от изменений"""
        if callback in self._callbacks:
            self._callbacks.remove(callback)
    
    def _notify_callbacks(self):
        """Уведомление подписчиков"""
        for callback in self._callbacks:
            try:
                callback()
            except Exception: 
                pass