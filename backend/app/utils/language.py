from app.exceptions import ValidationException


SUPPORTED_LANGUAGES = frozenset({"ru", "en"})


def normalize_language(lang: str) -> str:
    return (lang or "").strip().lower()


def is_supported_language(lang: str) -> bool:
    return normalize_language(lang) in SUPPORTED_LANGUAGES


def validate_language(lang: str, role: str) -> str:
    normalized_lang = normalize_language(lang)
    if normalized_lang not in SUPPORTED_LANGUAGES:
        raise ValidationException(f"Неподдерживаемый {role} язык")
    return normalized_lang


def validate_language_pair(source_language: str, target_language: str) -> tuple[str, str]:
    source = validate_language(source_language, "исходный")
    target = validate_language(target_language, "целевой")

    if source == target:
        raise ValidationException("Языки не должны совпадать")

    return source, target
