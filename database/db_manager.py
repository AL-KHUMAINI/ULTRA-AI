import sqlite3
from pathlib import Path
from core.config import DATABASE_PATH
from core.logger import logger
from core.exceptions import DatabaseError

class DatabaseManager:
    def __init__(self, db_path=DATABASE_PATH):
        self.db_path = db_path
        self._init_db()

    def get_connection(self):
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            return conn
        except sqlite3.Error as e:
            logger.error(f"Failed to connect to database: {e}")
            raise DatabaseError(f"Database connection error: {e}")

    def _init_db(self):
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS chat_history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        sender TEXT NOT NULL,
                        message TEXT NOT NULL,
                        language_code TEXT DEFAULT 'en',
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS app_settings (
                        key TEXT PRIMARY KEY,
                        value TEXT NOT NULL
                    )
                """)
                conn.commit()
                logger.info("Database initialized successfully.")
        except sqlite3.Error as e:
            logger.error(f"Failed to initialize database: {e}")
            raise DatabaseError(f"Database initialization error: {e}")

    def save_message(self, sender, message, language_code="en"):
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO chat_history (sender, message, language_code) VALUES (?, ?, ?)",
                    (sender, message, language_code)
                )
                conn.commit()
                return cursor.lastrowid
        except sqlite3.Error as e:
            logger.error(f"Failed to save message: {e}")
            raise DatabaseError(f"Failed to save message: {e}")

    def fetch_chat_history(self, limit=50):
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT sender, message, language_code, timestamp FROM chat_history ORDER BY id DESC LIMIT ?",
                    (limit,)
                )
                rows = cursor.fetchall()
                return [dict(row) for row in reversed(rows)]
        except sqlite3.Error as e:
            logger.error(f"Failed to fetch chat history: {e}")
            raise DatabaseError(f"Failed to fetch chat history: {e}")

    def clear_chat_history(self):
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM chat_history")
                conn.commit()
                logger.info("Chat history cleared.")
        except sqlite3.Error as e:
            logger.error(f"Failed to clear chat history: {e}")
            raise DatabaseError(f"Failed to clear chat history: {e}")

db_manager = DatabaseManager()
