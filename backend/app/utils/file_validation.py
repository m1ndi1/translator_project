from fastapi import UploadFile

from app.config import settings


ALLOWED_IMAGE_TYPES = {
    "image/png",
    "image/jpeg",
}


def validate_image_file_type(file: UploadFile) -> None:
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise ValueError("Допустимы только изображения PNG и JPEG")


async def validate_image_file_size(file: UploadFile) -> None:
    max_size_bytes = settings.max_image_size_mb * 1024 * 1024

    contents = await file.read()
    size = len(contents)

    if size > max_size_bytes:
        raise ValueError(f"Размер изображения превышает {settings.max_image_size_mb} МБ")

    await file.seek(0)


async def validate_image_file(file: UploadFile) -> None:
    validate_image_file_type(file)
    await validate_image_file_size(file)