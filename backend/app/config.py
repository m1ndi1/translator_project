from typing import Any

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "TheBest Translator API"
    app_version: str = "0.1.0"
    debug: bool = False
    api_prefix: str = "/api"

    tesseract_cmd: str = "tesseract"
    tesseract_lang: str = "rus+eng"
    max_image_size_mb: int = Field(default=10, ge=1)
    temp_dir: str = "temp"

    yandex_folder_id: str = ""
    yandex_api_key: str = ""
    yandex_translate_url: str = "https://translate.api.cloud.yandex.net/translate/v2/translate"
    translation_timeout_seconds: float = Field(default=30.0, gt=0)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @field_validator("debug", mode="before")
    @classmethod
    def parse_debug_value(cls, value: Any) -> bool:
        if isinstance(value, bool):
            return value

        normalized_value = str(value).strip().lower()
        if normalized_value in {"1", "true", "yes", "on", "debug", "development", "dev"}:
            return True
        if normalized_value in {"0", "false", "no", "off", "release", "production", "prod"}:
            return False

        raise ValueError("DEBUG must be a boolean-like value")


settings = Settings()
