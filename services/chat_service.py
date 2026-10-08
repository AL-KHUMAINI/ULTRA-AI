import os

try:
    import google.generativeai as genai
except ImportError:
    genai = None

class ChatService:
    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY", "")
        
        if genai and self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-1.5-flash')
            except Exception as e:
                self.model = None
                self.init_error = str(e)
        else:
            self.model = None
            self.init_error = "API Key not configured in environment"

    def process_user_message(self, user_email, message, lang='en'):
        if not self.model:
            return f"ULT Error: AI Model not initialized. ({getattr(self, 'init_error', 'Check key')})"
        
        try:
            response = self.model.generate_content(message)
            return response.text
        except Exception as e:
            return f"ULT Error: {str(e)}"

chat_service = ChatService()
