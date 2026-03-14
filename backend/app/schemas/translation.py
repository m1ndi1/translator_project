from pydantic import BaseModel, Field


class TranslateTextRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Текст для перевода")
    source_language: str = Field(..., description="Исходный язык")
    target_language: str = Field(..., description="Целевой язык")


class TranslateTextResponse(BaseModel):
    translated_text: str
    source_language: str
    target_language: str