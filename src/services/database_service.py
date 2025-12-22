"""Сервис базы данных"""

import json
import os
from typing import Optional, List, Dict, Any
from datetime import datetime, date
import aiosqlite


class DatabaseService: 
    """Сервис для работы с базой данных"""
    
    def __init__(self, db_path: str = "data/mnur.db"):
        self.db_path = db_path
        self._ensure_data_dir()
    
    def _ensure_data_dir(self):
        """Создание директории для данных"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
    
    async def init_db(self):
        """Инициализация базы данных"""
        async with aiosqlite.connect(self. db_path) as db:
            # Таблица пользователей
            await db.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id TEXT PRIMARY KEY,
                    phone TEXT,
                    email TEXT,
                    full_name TEXT,
                    notifications_enabled INTEGER DEFAULT 1,
                    home_lat REAL,
                    home_lon REAL,
                    created_at TEXT,
                    updated_at TEXT
                )
            """)
            
            # Таблица рисков
            await db.execute("""
                CREATE TABLE IF NOT EXISTS risks (
                    id TEXT PRIMARY KEY,
                    type TEXT,
                    level TEXT,
                    title TEXT,
                    description TEXT,
                    lat REAL,
                    lon REAL,
                    radius_km REAL,
                    start_time TEXT,
                    end_time TEXT,
                    source TEXT,
                    created_at TEXT
                )
            """)
            
            # Таблица происшествий
            await db.execute("""
                CREATE TABLE IF NOT EXISTS incidents (
                    id TEXT PRIMARY KEY,
                    title TEXT,
                    description TEXT,
                    incident_type TEXT,
                    lat REAL,
                    lon REAL,
                    address TEXT,
                    is_active INTEGER,
                    severity TEXT,
                    incident_date TEXT,
                    created_at TEXT
                )
            """)
            
            # Таблица укрытий
            await db.execute("""
                CREATE TABLE IF NOT EXISTS shelters (
                    id TEXT PRIMARY KEY,
                    name TEXT,
                    shelter_type TEXT,
                    lat REAL,
                    lon REAL,
                    address TEXT,
                    capacity_total INTEGER,
                    capacity_current INTEGER,
                    is_active INTEGER,
                    phone TEXT,
                    created_at TEXT
                )
            """)
            
            # Таблица уведомлений
            await db.execute("""
                CREATE TABLE IF NOT EXISTS notifications (
                    id TEXT PRIMARY KEY,
                    user_id TEXT,
                    title TEXT,
                    message TEXT,
                    type TEXT,
                    is_read INTEGER DEFAULT 0,
                    created_at TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            """)
            
            await db.commit()
    
    async def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Получение пользователя"""
        async with aiosqlite.connect(self. db_path) as db:
            db. row_factory = aiosqlite.Row
            cursor = await db.execute(
                "SELECT * FROM users WHERE id = ? ", (user_id,)
            )
            row = await cursor.fetchone()
            return dict(row) if row else None
    
    async def save_user(self, user_data: Dict[str, Any]) -> bool:
        """Сохранение пользователя"""
        async with aiosqlite. connect(self.db_path) as db:
            await db.execute("""
                INSERT OR REPLACE INTO users 
                (id, phone, email, full_name, notifications_enabled, 
                 home_lat, home_lon, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                user_data. get("id"),
                user_data. get("phone"),
                user_data. get("email"),
                user_data. get("full_name"),
                user_data.get("notifications_enabled", 1),
                user_data.get("home_lat"),
                user_data.get("home_lon"),
                user_data.get("created_at", datetime.now().isoformat()),
                datetime.now().isoformat(),
            ))
            await db.commit()
            return True
    
    async def get_active_risks(self, lat: float = None, lon: float = None) -> List[Dict]: 
        """Получение активных рисков"""
        async with aiosqlite.connect(self. db_path) as db:
            db.row_factory = aiosqlite. Row
            cursor = await db.execute("""
                SELECT * FROM risks 
                WHERE (end_time IS NULL OR end_time > ?)
                ORDER BY created_at DESC
            """, (datetime. now().isoformat(),))
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]
    
    async def get_incidents_by_date(self, target_date: date) -> List[Dict]: 
        """Получение происшествий по дате"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute("""
                SELECT * FROM incidents 
                WHERE incident_date = ?
                ORDER BY created_at DESC
            """, (target_date.isoformat(),))
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]
    
    async def get_nearby_shelters(
        self, lat: float, lon:  float, radius_km: float = 10
    ) -> List[Dict]:
        """Получение ближайших укрытий"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            # Упрощённый запрос без расчёта расстояния
            cursor = await db. execute("""
                SELECT * FROM shelters 
                WHERE is_active = 1
                ORDER BY name
            """)
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]
    
    async def get_unread_notifications(self, user_id: str) -> List[Dict]:
        """Получение непрочитанных уведомлений"""
        async with aiosqlite. connect(self.db_path) as db:
            db. row_factory = aiosqlite.Row
            cursor = await db.execute("""
                SELECT * FROM notifications 
                WHERE user_id = ?  AND is_read = 0
                ORDER BY created_at DESC
            """, (user_id,))
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]
    
    def get_mock_incidents_for_month(self, year: int, month:  int) -> Dict[int, List]: 
        """Получение моковых данных о происшествиях за месяц"""
        # Моковые данные для демонстрации
        incidents = {
            14: [{"type": "flood", "severity": "medium"}],
            20: [{"type":  "fire", "severity": "high"}],
            21: [{"type":  "storm", "severity": "low"}],
            27: [{"type":  "technogenic", "severity":  "medium"}],
            28: [{"type": "heat", "severity": "low"}],
        }
        return incidents