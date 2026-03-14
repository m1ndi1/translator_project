class AppBaseException(Exception):
    """Базовое исключение приложения."""


class ValidationException(AppBaseException):
    """Ошибка валидации входных данных."""


class OCRException(AppBaseException):
    """Ошибка OCR."""


class TranslationException(AppBaseException):
    """Ошибка перевода."""