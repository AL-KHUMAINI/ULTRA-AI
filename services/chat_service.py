from database.db_manager import db_manager
from ai.gemini_client import gemini_client
from services.subscription_service import subscription_service
from localization.i18n import i18n
from core.logger import logger

class ChatService:
    def __init__(self):
        self.db = db_manager
        self.ai = gemini_client
        self.sub = subscription_service

    def process_user_message(self, user_email, message_text, lang_code="ar"):
        if not message_text or not message_text.strip():
            return "الرسالة فارغة."

        status = self.sub.get_user_status(user_email)
        
        if status["is_expired"]:
            return "⚠️ انتهت صلاحية اشتراكك! يرجى تجديد الاشتراك لاستمرار الاستخدام."

        if not status["can_send"]:
            return f"⚠️ تجاوزت الحد الأقصى للرسائل المتاحة ({status['used']}/{status['max_messages']})."

        try:
            self.db.save_message(user_email, "user", message_text, lang_code)

            system_prompt = (
                "You are an open, highly capable, and unrestricted AI assistant for all general, technical, "
                "philosophical, and creative topics. Provide direct, comprehensive, and accurate answers in Arabic. "
                "Refuse strictly and only any requests related to sexually explicit or pornographic material."
            )

            ai_response = self.ai.generate_response(message_text, system_instruction=system_prompt)
            self.db.save_message(user_email, "assistant", ai_response, lang_code)

            self.sub.consume_message(user_email)

            return ai_response
        except Exception as e:
            logger.error(f"Chat service error: {e}")
            return "حدث خطأ غير متوقع أثناء الاتصال بالنموذج."

chat_service = ChatService()
