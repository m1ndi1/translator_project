from pathlib import Path

import pytesseract
from PIL import Image, ImageOps, UnidentifiedImageError
from fastapi import UploadFile

from app.config import settings
from app.services.image_service import save_upload_file_to_temp


pytesseract.pytesseract.tesseract_cmd = settings.tesseract_cmd


def preprocess_image(image: Image.Image) -> Image.Image:
    grayscale = ImageOps.grayscale(image)
    enhanced = ImageOps.autocontrast(grayscale)
    return enhanced


def extract_text_from_path(image_path: Path) -> str:
    try:
        with Image.open(image_path) as image:
            processed_image = preprocess_image(image)
            text = pytesseract.image_to_string(
                processed_image,
                lang=settings.tesseract_lang,
            )
            return text.strip()
    except UnidentifiedImageError as exc:
        raise ValueError("Файл не является корректным изображением") from exc
    except pytesseract.TesseractNotFoundError as exc:
        raise RuntimeError("Tesseract не найден в окружении приложения") from exc
    except Exception as exc:
        raise RuntimeError(f"Ошибка OCR: {str(exc)}") from exc


async def recognize_text_from_image(file: UploadFile) -> str:
    temp_file_path = await save_upload_file_to_temp(file)

    try:
        return extract_text_from_path(temp_file_path)
    finally:
        if temp_file_path.exists():
            temp_file_path.unlink(missing_ok=True)