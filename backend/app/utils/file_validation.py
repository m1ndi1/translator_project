from fastapi import UploadFile

from app.config import settings
from app.exceptions import ValidationException


ALLOWED_IMAGE_TYPES = frozenset(
    {
        "image/png",
        "image/jpeg",
    }
)


def validate_image_file_type(file: UploadFile) -> None:
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise ValidationException("Допустимы только изображения PNG и JPEG")


async def read_upload_file(file: UploadFile) -> bytes:
    contents = await file.read()
    await file.seek(0)
    return contents


def validate_image_size(contents: bytes, max_size_mb: int | None = None) -> None:
    size_limit_mb = max_size_mb or settings.max_image_size_mb
    max_size_bytes = size_limit_mb * 1024 * 1024
    if len(contents) > max_size_bytes:
        raise ValidationException(f"Размер изображения превышает {size_limit_mb} МБ")


async def validate_image_file(file: UploadFile) -> bytes:
    validate_image_file_type(file)
    contents = await read_upload_file(file)
    validate_image_size(contents)
    return contents
