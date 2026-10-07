from database.db_manager import db_manager
from core.logger import logger

class SubscriptionService:
    TIER_LIMITS = {
        "FREE": 5,
        "PRO": 50,
        "PRO_ULTRA": 999999
    }

    def __init__(self):
        self.db = db_manager

    def get_user_status(self, email):
        user = self.db.get_or_create_user(email)
        tier = user["tier"]
        used = user["messages_used"]
        limit = self.TIER_LIMITS.get(tier, 5)
        remaining = max(0, limit - used) if limit < 999999 else "Unlimited"

        return {
            "email": email,
            "tier": tier,
            "used": used,
            "limit": limit,
            "remaining": remaining,
            "can_send": used < limit or tier == "PRO_ULTRA"
        }

    def consume_message(self, email):
        status = self.get_user_status(email)
        if status["can_send"]:
            self.db.increment_user_message(email)
            return True
        return False

    def redeem_code(self, email, code):
        return self.db.redeem_code_for_user(email, code.strip())

subscription_service = SubscriptionService()
