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
                    CREATE TABLE IF NOT EXISTS users (
                        email TEXT PRIMARY KEY,
                        tier TEXT DEFAULT 'FREE',
                        messages_used INTEGER DEFAULT 0,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS chat_history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_email TEXT,
                        sender TEXT NOT NULL,
                        message TEXT NOT NULL,
                        language_code TEXT DEFAULT 'en',
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS redeem_codes (
                        code TEXT PRIMARY KEY,
                        tier TEXT NOT NULL,
                        is_used INTEGER DEFAULT 0
                    )
                """)
                # Insert default preset promo codes
                cursor.execute("INSERT OR IGNORE INTO redeem_codes (code, tier) VALUES ('PRO-2026', 'PRO')")
                cursor.execute("INSERT OR IGNORE INTO redeem_codes (code, tier) VALUES ('ULTRA-VIP', 'PRO_ULTRA')")
                cursor.execute("INSERT OR IGNORE INTO redeem_codes (code, tier) VALUES ('ULTRA-MAX', 'PRO_ULTRA')")

                conn.commit()
                logger.info("Database initialized successfully.")
        except sqlite3.Error as e:
            logger.error(f"Failed to initialize database: {e}")
            raise DatabaseError(f"Database initialization error: {e}")

    def get_or_create_user(self, email):
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
                user = cursor.fetchone()
                if not user:
                    cursor.execute("INSERT INTO users (email, tier, messages_used) VALUES (?, 'FREE', 0)", (email,))
                    conn.commit()
                    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
                    user = cursor.fetchone()
                return dict(user)
        except sqlite3.Error as e:
            logger.error(f"Failed to get or create user: {e}")
            raise DatabaseError(f"User DB error: {e}")

    def update_user_tier(self, email, tier):
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET tier = ? WHERE email = ?", (tier, email))
                conn.commit()
                logger.info(f"Updated user {email} tier to {tier}")
        except sqlite3.Error as e:
            logger.error(f"Failed to update user tier: {e}")
            raise DatabaseError(f"Tier update error: {e}")

    def redeem_code_for_user(self, email, code):
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM redeem_codes WHERE code = ?", (code,))
                item = cursor.fetchone()
                if item:
                    tier = item["tier"]
                    cursor.execute("UPDATE users SET tier = ? WHERE email = ?", (tier, email))
                    conn.commit()
                    return True, tier
                return False, "Invalid Code"
        except sqlite3.Error as e:
            logger.error(f"Failed to redeem code: {e}")
            return False, "Database Error"

    def increment_user_message(self, email):
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET messages_used = messages_used + 1 WHERE email = ?", (email,))
                conn.commit()
        except sqlite3.Error as e:
            logger.error(f"Failed to increment message count: {e}")

    def save_message(self, user_email, sender, message, language_code="en"):
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO chat_history (user_email, sender, message, language_code) VALUES (?, ?, ?, ?)",
                    (user_email, sender, message, language_code)
                )
                conn.commit()
        except sqlite3.Error as e:
            logger.error(f"Failed to save message: {e}")

db_manager = DatabaseManager()
