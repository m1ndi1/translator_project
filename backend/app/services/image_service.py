from pathlib import Path
from uuid import uuid4

from app.config import settings


BASE_DIR = Path(__file__).resolve().parents[2]


def ensure_temp_dir() -> Path:
    temp_path = BASE_DIR / settings.temp_dir
    temp_path.mkdir(parents=True, exist_ok=True)
    return temp_path


def build_temp_file_path(filename: str | None) -> Path:
    temp_dir = ensure_temp_dir()
    suffix = Path(filename or "").suffix.lower() or ".tmp"
    return temp_dir / f"{uuid4()}{suffix}"


def save_bytes_to_temp(filename: str | None, contents: bytes) -> Path:
    temp_file_path = build_temp_file_path(filename)
    temp_file_path.write_bytes(contents)
    return temp_file_path
