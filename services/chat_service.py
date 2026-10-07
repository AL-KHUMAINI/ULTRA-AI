from database.db_manager import db_manager
from ai.gemini_client import gemini_client
from services.subscription_service import subscription_service
from localization.i18n import i18n
from core.logger import logger
from core.exceptions import UltraAIException

class ChatService:
    def __init__(self):
        self.db = db_manager
        self.ai = gemini_client
        self.sub = subscription_service

    def process_user_message(self, user_email, message_text, lang_code="ar"):
        if not message_text or not message_text.strip():
            return "Empty message."

        status = self.sub.get_user_status(user_email)
        if not status["can_send"]:
            return f"Limit reached for your plan ({status['tier']}). Please upgrade to PRO or PRO ULTRA."

        try:
            self.db.save_message(user_email, "user", message_text, lang_code)

            system_prompt = f"Respond in {i18n.SUPPORTED_LANGUAGES.get(lang_code, 'English')} language."
            if status["tier"] == "PRO_ULTRA":
                system_prompt += " Provide highly detailed, expert-level response with advanced reasoning."

            ai_response = self.ai.generate_response(message_text, system_instruction=system_prompt)
            self.db.save_message(user_email, "assistant", ai_response, lang_code)

            self.sub.consume_message(user_email)

            return ai_response
        except UltraAIException as e:
            logger.error(f"Chat service error: {e}")
            return i18n.get_text("error_network")
        except Exception as e:
            logger.error(f"Unexpected chat service error: {e}")
            return i18n.get_text("error_network")

chat_service = ChatService()
