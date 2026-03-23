from typing import Any

import httpx

from app.config import settings
from app.core.logger import logger
from app.exceptions import ConfigurationException, TranslationException, ValidationException
from app.schemas.translation import TranslateTextResponse


def ensure_yandex_settings() -> None:
    if not settings.yandex_folder_id:
        raise ConfigurationException("Не задан YANDEX_FOLDER_ID в .env")

    if not settings.yandex_api_key:
        raise ConfigurationException("Не задан YANDEX_API_KEY в .env")


def build_translation_payload(
    text: str,
    source_language: str,
    target_language: str,
) -> dict[str, Any]:
    return {
        "sourceLanguageCode": source_language,
        "targetLanguageCode": target_language,
        "folderId": settings.yandex_folder_id,
        "texts": [text],
    }


def extract_translated_text(response_data: dict[str, Any]) -> str:
    translations = response_data.get("translations")
    if not isinstance(translations, list) or not translations:
        raise TranslationException("Сервис перевода не вернул перевод")

    first_translation = translations[0]
    if not isinstance(first_translation, dict):
        raise TranslationException("Сервис перевода вернул некорректный ответ")

    translated_text = str(first_translation.get("text", "")).strip()
    if not translated_text:
        raise TranslationException("Сервис перевода вернул пустой перевод")

    return translated_text


async def translate_text(
    text: str,
    source_language: str,
    target_language: str,
) -> TranslateTextResponse:
    ensure_yandex_settings()

    normalized_text = text.strip()
    if not normalized_text:
        raise ValidationException("Пустой текст нельзя перевести")

    payload = build_translation_payload(
        text=normalized_text,
        source_language=source_language,
        target_language=target_language,
    )
    headers = {
        "Authorization": f"Api-Key {settings.yandex_api_key}",
        "Content-Type": "application/json",
    }

    try:
        async with httpx.AsyncClient(timeout=settings.translation_timeout_seconds) as client:
            response = await client.post(
                settings.yandex_translate_url,
                headers=headers,
                json=payload,
            )
    except httpx.RequestError as exc:
        logger.error("Translation request failed: %s", exc)
        raise TranslationException(f"Ошибка сети при обращении к сервису перевода: {exc}") from exc

    if response.status_code == 401:
        raise ConfigurationException("Ошибка авторизации в сервисе перевода: проверь API key")

    if response.status_code == 403:
        raise ConfigurationException("Доступ к сервису перевода запрещен: проверь права ключа")

    if response.status_code != 200:
        logger.error(
            "Translation service returned unexpected status %s: %s",
            response.status_code,
            response.text,
        )
        raise TranslationException(
            f"Сервис перевода вернул ошибку {response.status_code}: {response.text}"
        )

    try:
        response_data = response.json()
    except ValueError as exc:
        raise TranslationException("Сервис перевода вернул некорректный JSON") from exc

    translated_text = extract_translated_text(response_data)

    return TranslateTextResponse(
        translated_text=translated_text,
        source_language=source_language,
        target_language=target_language,
    )
