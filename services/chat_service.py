import os

try:
    import google.generativeai as genai
except ImportError:
    genai = None

class ChatService:
    def __init__(self):
        # ضع مفتاح Gemini API الحقيقي هنا مباشرة
        self.api_key = "YOUR_ACTUAL_API_KEY"
        if genai and self.api_key and self.api_key != "YOUR_ACTUAL_API_KEY":
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-1.5-flash')
            except Exception:
                self.model = None
        else:
            self.model = None

    def process_user_message(self, user_email, message, lang='en'):
        if not self.model:
            return "ULT Error: API Key is not configured. Please add your Gemini API Key in chat_service.py."
        
        try:
            response = self.model.generate_content(message)
            return response.text
        except Exception as e:
            return f"ULT Error: {str(e)}"

chat_service = ChatService()
