SUPPORTED_LANGUAGES = {"ru", "en"}


def is_supported_language(lang: str) -> bool:
    return lang in SUPPORTED_LANGUAGES