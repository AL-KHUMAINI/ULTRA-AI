import os
from core.logger import logger

class AuthService:
    def __init__(self):
        self.user_info = None
        self.is_authenticated = False

    def login_with_google(self, email):
        try:
            if email and "@" in email:
                self.user_info = {
                    "email": email,
                    "authenticated": True
                }
                self.is_authenticated = True
                logger.info(f"User authenticated: {email}")
                return True
            else:
                logger.warning("Invalid email provided.")
                return False
        except Exception as e:
            logger.error(f"Authentication error: {e}")
            return False

    def logout(self):
        self.user_info = None
        self.is_authenticated = False
        logger.info("User logged out.")

auth_service = AuthService()
