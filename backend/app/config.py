from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "TheBest Translator API"
    app_version: str = "0.1.0"
    debug: bool = True
    api_prefix: str = "/api"

    tesseract_cmd: str = "tesseract"
    tesseract_lang: str = "rus+eng"
    max_image_size_mb: int = 10
    temp_dir: str = "temp"

    yandex_folder_id: str = ""
    yandex_api_key: str = ""
    yandex_translate_url: str = "https://translate.api.cloud.yandex.net/translate/v2/translate"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()