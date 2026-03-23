from pydantic import BaseModel, ConfigDict, Field


class TranslateTextRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    text: str = Field(..., min_length=1, description="Текст для перевода")
    source_language: str = Field(..., description="Исходный язык")
    target_language: str = Field(..., description="Целевой язык")


class TranslateTextResponse(BaseModel):
    translated_text: str
    source_language: str
    target_language: str
