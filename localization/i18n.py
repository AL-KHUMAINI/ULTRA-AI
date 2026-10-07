from core.exceptions import LocalizationError

class LocalizationManager:
    SUPPORTED_LANGUAGES = {
        "ar": "العربية",
        "fa": "فارسی",
        "ru": "Русский",
        "zh": "中文",
        "en": "English"
    }

    TRANSLATIONS = {
        "app_title": {
            "ar": "ألترا ذكاء اصطناعي",
            "fa": "اولترا هوش مصنوعی",
            "ru": "Ультра ИИ",
            "zh": "超级人工智能",
            "en": "ULTRA AI"
        },
        "send_button": {
            "ar": "إرسال",
            "fa": "ارسال",
            "ru": "Отправить",
            "zh": "发送",
            "en": "Send"
        },
        "input_placeholder": {
            "ar": "اكتب رسالتك هنا...",
            "fa": "پیام خود را اینجا بنویسید...",
            "ru": "Введите ваше сообщение здесь...",
            "zh": "在此处输入您的消息...",
            "en": "Type your message here..."
        },
        "clear_chat": {
            "ar": "مسح المحادثة",
            "fa": "پاک کردن گپ",
            "ru": "Очистить чат",
            "zh": "清除聊天",
            "en": "Clear Chat"
        },
        "settings": {
            "ar": "الإعدادات",
            "fa": "تنظیمات",
            "ru": "Настройки",
            "zh": "设置",
            "en": "Settings"
        },
        "error_network": {
            "ar": "خطأ في الاتصال بالشبكة",
            "fa": "خطا در اتصال به شبکه",
            "ru": "Ошибка подключения к сети",
            "zh": "网络连接错误",
            "en": "Network connection error"
        }
    }

    def __init__(self, current_lang="ar"):
        if current_lang not in self.SUPPORTED_LANGUAGES:
            current_lang = "ar"
        self.current_lang = current_lang

    def set_language(self, lang_code):
        if lang_code in self.SUPPORTED_LANGUAGES:
            self.current_lang = lang_code
            return True
        raise LocalizationError(f"Unsupported language code: {lang_code}")

    def get_text(self, key):
        if key in self.TRANSLATIONS:
            return self.TRANSLATIONS[key].get(self.current_lang, self.TRANSLATIONS[key].get("en", key))
        return key

i18n = LocalizationManager()
