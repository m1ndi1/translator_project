from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.schemas.ocr import OCRResponse, OCRTranslateResponse
from app.services.ocr_service import recognize_text_from_image
from app.services.translation_service import translate_text
from app.utils.file_validation import validate_image_file
from app.utils.language import is_supported_language

router = APIRouter(tags=["ocr"])


@router.post("/ocr/image", response_model=OCRResponse)
async def ocr_image(file: UploadFile = File(...)) -> OCRResponse:
    try:
        await validate_image_file(file)
        recognized_text = await recognize_text_from_image(file)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return OCRResponse(recognized_text=recognized_text)


@router.post("/translate/image", response_model=OCRTranslateResponse)
async def translate_image(
    file: UploadFile = File(...),
    source_language: str = Form(...),
    target_language: str = Form(...),
) -> OCRTranslateResponse:
    if not is_supported_language(source_language):
        raise HTTPException(status_code=400, detail="Неподдерживаемый исходный язык")

    if not is_supported_language(target_language):
        raise HTTPException(status_code=400, detail="Неподдерживаемый целевой язык")

    if source_language == target_language:
        raise HTTPException(status_code=400, detail="Языки не должны совпадать")

    try:
        await validate_image_file(file)
        recognized_text = await recognize_text_from_image(file)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    translated = await translate_text(
        text=recognized_text,
        source_language=source_language,
        target_language=target_language,
    )

    return OCRTranslateResponse(
        recognized_text=recognized_text,
        translated_text=translated.translated_text,
        source_language=translated.source_language,
        target_language=translated.target_language,
    )