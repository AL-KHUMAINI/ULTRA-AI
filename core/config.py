import os
from pathlib import Path
from dotenv import load_dotenv

# تحميل متغيرات البيئة من ملف .env إن وجد
load_dotenv()

# المسارات الأساسية للمشروع
BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "ultra_ai.db"
LOG_FILE_PATH = BASE_DIR / "ultra_ai.log"

# إعدادات الذكاء الاصطناعي
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
DEFAULT_MODEL_NAME = "gemini-1.5-flash"

# إعدادات التطبيق العامة
APP_NAME = "ULTRA AI"
APP_VERSION = "1.0.0"
DEFAULT_LANGUAGE = "ar"
MAX_CHAT_HISTORY = 200

# التأكد من وجود مجلد الأصول
ASSETS_DIR = BASE_DIR / "assets"
