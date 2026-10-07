import os
import google.generativeai as genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
genai.configure(api_key=GEMINI_API_KEY)

class GeminiClient:
    def __init__(self):
        # إلغاء كافة القيود عدا المحتوى الإباحي والمخل بالآداب
        self.safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"  # حظر صارم للمحتوى الإباحي فقط
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE"
            }
        ]

    def generate_response(self, prompt, system_instruction=""):
        try:
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                system_instruction=system_instruction,
                safety_settings=self.safety_settings
            )
            
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"خطأ أثناء معالجة الطلب: {str(e)}"

gemini_client = GeminiClient()
