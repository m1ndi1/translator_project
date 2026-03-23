from fastapi import APIRouter

from app.schemas.translation import TranslateTextRequest, TranslateTextResponse
from app.services.translation_service import translate_text
from app.utils.language import validate_language_pair

router = APIRouter(tags=["translate"])


@router.post("/translate/text", response_model=TranslateTextResponse)
async def translate_text_endpoint(payload: TranslateTextRequest) -> TranslateTextResponse:
    source_language, target_language = validate_language_pair(
        payload.source_language,
        payload.target_language,
    )
    return await translate_text(
        text=payload.text,
        source_language=source_language,
        target_language=target_language,
    )
