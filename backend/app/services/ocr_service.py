from pathlib import Path

import pytesseract
from PIL import Image, ImageOps, UnidentifiedImageError
from fastapi import UploadFile

from app.config import settings
from app.exceptions import OCRException, ValidationException
from app.services.image_service import save_bytes_to_temp
from app.utils.file_validation import validate_image_file


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
    except UnidentifiedImageError as exc:
        raise ValidationException("Файл не является корректным изображением") from exc
    except pytesseract.TesseractNotFoundError as exc:
        raise OCRException("Tesseract не найден в окружении приложения") from exc
    except Exception as exc:
        raise OCRException(f"Ошибка OCR: {exc}") from exc

    recognized_text = text.strip()
    if not recognized_text:
        raise OCRException("На изображении не удалось распознать текст")

    return recognized_text


async def recognize_text_from_image(file: UploadFile) -> str:
    contents = await validate_image_file(file)
    temp_file_path = save_bytes_to_temp(file.filename, contents)

    try:
        return extract_text_from_path(temp_file_path)
    finally:
        temp_file_path.unlink(missing_ok=True)
