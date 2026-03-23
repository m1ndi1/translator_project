from fastapi import APIRouter, File, Form, UploadFile

from app.schemas.ocr import OCRResponse, OCRTranslateResponse
from app.services.ocr_service import recognize_text_from_image
from app.services.translation_service import translate_text
from app.utils.language import validate_language_pair

router = APIRouter(tags=["ocr"])


@router.post("/ocr/image", response_model=OCRResponse)
async def ocr_image(file: UploadFile = File(...)) -> OCRResponse:
    recognized_text = await recognize_text_from_image(file)
    return OCRResponse(recognized_text=recognized_text)


@router.post("/translate/image", response_model=OCRTranslateResponse)
async def translate_image(
    file: UploadFile = File(...),
    source_language: str = Form(...),
    target_language: str = Form(...),
) -> OCRTranslateResponse:
    normalized_source_language, normalized_target_language = validate_language_pair(
        source_language,
        target_language,
    )
    recognized_text = await recognize_text_from_image(file)
    translated = await translate_text(
        text=recognized_text,
        source_language=normalized_source_language,
        target_language=normalized_target_language,
    )

    return OCRTranslateResponse(
        recognized_text=recognized_text,
        translated_text=translated.translated_text,
        source_language=translated.source_language,
        target_language=translated.target_language,
    )
