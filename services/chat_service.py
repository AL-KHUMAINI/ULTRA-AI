import os

try:
    import google.generativeai as genai
except ImportError:
    genai = None

class ChatService:
    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")
        if genai and self.api_key and self.api_key != "YOUR_GEMINI_API_KEY_HERE":
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-1.5-flash')
            except Exception:
                self.model = None
        else:
            self.model = None

    def process_user_message(self, user_email, message, lang='en'):
        if not self.model:
            return f"UL ULTRA: I received your message -> '{message}'. (Please configure your API Key to get live responses)."
        
        try:
            response = self.model.generate_content(message)
            return response.text
        except Exception as e:
            return f"UL ULTRA Error: {str(e)}"

chat_service = ChatService()
