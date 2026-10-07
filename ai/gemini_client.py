import google.generativeai as genai
from core.config import GEMINI_API_KEY, DEFAULT_MODEL_NAME
from core.logger import logger
from core.exceptions import AIProviderError

class GeminiClient:
    def __init__(self, api_key=GEMINI_API_KEY, model_name=DEFAULT_MODEL_NAME):
        self.api_key = api_key
        self.model_name = model_name
        self.model = None
        self._configure_client()

    def _configure_client(self):
        if self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel(self.model_name)
                logger.info(f"Gemini AI client configured with model: {self.model_name}")
            except Exception as e:
                logger.error(f"Failed to configure Gemini API: {e}")
                raise AIProviderError(f"Gemini initialization error: {e}")
        else:
            logger.warning("No GEMINI_API_KEY provided. Gemini client is running in unauthenticated mode.")

    def set_api_key(self, new_api_key):
        self.api_key = new_api_key
        self._configure_client()

    def generate_response(self, prompt, system_instruction=None):
        if not self.model:
            raise AIProviderError("Gemini API key is not configured.")

        try:
            if system_instruction:
                model = genai.GenerativeModel(
                    model_name=self.model_name,
                    system_instruction=system_instruction
                )
                response = model.generate_content(prompt)
            else:
                response = self.model.generate_content(prompt)

            if response and hasattr(response, 'text'):
                return response.text
            else:
                raise AIProviderError("Empty response received from Gemini API.")
        except Exception as e:
            logger.error(f"Error during Gemini text generation: {e}")
            raise AIProviderError(f"Gemini API generation error: {e}")

gemini_client = GeminiClient()
