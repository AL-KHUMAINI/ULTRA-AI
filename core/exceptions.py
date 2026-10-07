class UltraAIException(Exception):
    """Base exception class for ULTRA AI application."""
    pass

class ConfigurationError(UltraAIException):
    """Raised when configuration parameters are invalid or missing."""
    pass

class DatabaseError(UltraAIException):
    """Raised when database CRUD operations fail."""
    pass

class AIProviderError(UltraAIException):
    """Raised when Gemini API communication fails."""
    pass

class LocalizationError(UltraAIException):
    """Raised when a requested language or string key is missing."""
    pass
