class AppBaseException(Exception):
    """Base application exception with an HTTP status code."""

    status_code = 500

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class ValidationException(AppBaseException):
    """Raised when client input is invalid."""

    status_code = 400


class ConfigurationException(AppBaseException):
    """Raised when server configuration is incomplete or invalid."""

    status_code = 500


class OCRException(AppBaseException):
    """Raised when OCR processing fails."""

    status_code = 500


class TranslationException(AppBaseException):
    """Raised when the translation provider request fails."""

    status_code = 502
