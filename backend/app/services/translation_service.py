import httpx

from app.config import settings
from app.schemas.translation import TranslateTextResponse


def ensure_yandex_settings() -> None:
    if not settings.yandex_folder_id:
        raise RuntimeError("Не задан YANDEX_FOLDER_ID в .env")

    if not settings.yandex_api_key:
        raise RuntimeError("Не задан YANDEX_API_KEY в .env")


async def translate_text(
    text: str,
    source_language: str,
    target_language: str,
) -> TranslateTextResponse:
    ensure_yandex_settings()

    if not text or not text.strip():
        raise ValueError("Пустой текст нельзя перевести")

    payload = {
        "sourceLanguageCode": source_language,
        "targetLanguageCode": target_language,
        "folderId": settings.yandex_folder_id,
        "texts": [text],
    }

    headers = {
        "Authorization": f"Api-Key {settings.yandex_api_key}",
        "Content-Type": "application/json",
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                settings.yandex_translate_url,
                headers=headers,
                json=payload,
            )
    except httpx.RequestError as exc:
        raise RuntimeError(f"Ошибка сети при обращении к сервису перевода: {exc}") from exc

    if response.status_code == 401:
        raise RuntimeError("Ошибка авторизации в сервисе перевода: проверь API key")

    if response.status_code == 403:
        raise RuntimeError("Доступ к сервису перевода запрещен: проверь права ключа")

    if response.status_code != 200:
        raise RuntimeError(
            f"Сервис перевода вернул ошибку {response.status_code}: {response.text}"
        )

    try:
        response_data = response.json()
    except ValueError as exc:
        raise RuntimeError("Сервис перевода вернул некорректный JSON") from exc

    translations = response_data.get("translations")
    if not translations:
        raise RuntimeError("Сервис перевода не вернул перевод")

    translated_text = translations[0].get("text", "").strip()
    if not translated_text:
        raise RuntimeError("Сервис перевода вернул пустой перевод")

    return TranslateTextResponse(
        translated_text=translated_text,
        source_language=source_language,
        target_language=target_language,
    )