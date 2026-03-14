from fastapi import APIRouter, HTTPException

from app.schemas.translation import TranslateTextRequest, TranslateTextResponse
from app.services.translation_service import translate_text
from app.utils.language import is_supported_language

router = APIRouter(tags=["translate"])


@router.post("/translate/text", response_model=TranslateTextResponse)
async def translate_text_endpoint(payload: TranslateTextRequest) -> TranslateTextResponse:
    if not is_supported_language(payload.source_language):
        raise HTTPException(status_code=400, detail="Неподдерживаемый исходный язык")

    if not is_supported_language(payload.target_language):
        raise HTTPException(status_code=400, detail="Неподдерживаемый целевой язык")

    if payload.source_language == payload.target_language:
        raise HTTPException(status_code=400, detail="Языки не должны совпадать")

    try:
        return await translate_text(
            text=payload.text,
            source_language=payload.source_language,
            target_language=payload.target_language,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc