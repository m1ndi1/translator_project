from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.config import settings


BASE_DIR = Path(__file__).resolve().parents[2]


def ensure_temp_dir() -> Path:
    temp_path = BASE_DIR / settings.temp_dir
    temp_path.mkdir(parents=True, exist_ok=True)
    return temp_path


async def save_upload_file_to_temp(file: UploadFile) -> Path:
    temp_dir = ensure_temp_dir()

    suffix = Path(file.filename).suffix.lower() or ".tmp"
    temp_file_path = temp_dir / f"{uuid4()}{suffix}"

    contents = await file.read()
    temp_file_path.write_bytes(contents)
    await file.seek(0)

    return temp_file_path