from database.db_manager import db_manager
from ai.gemini_client import gemini_client
from localization.i18n import i18n
from core.logger import logger
from core.exceptions import UltraAIException

class ChatService:
    def __init__(self):
        self.db = db_manager
        self.ai = gemini_client

    def process_user_message(self, message_text, lang_code="ar"):
        if not message_text or not message_text.strip():
            return None

        try:
            self.db.save_message("user", message_text, lang_code)
            system_prompt = f"Respond in {i18n.SUPPORTED_LANGUAGES.get(lang_code, 'English')} language."
            ai_response = self.ai.generate_response(message_text, system_instruction=system_prompt)
            self.db.save_message("assistant", ai_response, lang_code)
            return ai_response
        except UltraAIException as e:
            logger.error(f"Chat service error: {e}")
            return i18n.get_text("error_network")
        except Exception as e:
            logger.error(f"Unexpected chat service error: {e}")
            return i18n.get_text("error_network")

    def get_chat_history(self, limit=50):
        return self.db.fetch_chat_history(limit=limit)

    def clear_history(self):
        self.db.clear_chat_history()

chat_service = ChatService()
