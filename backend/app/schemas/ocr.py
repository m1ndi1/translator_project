from pydantic import BaseModel


class OCRResponse(BaseModel):
    recognized_text: str


class OCRTranslateResponse(BaseModel):
    recognized_text: str
    translated_text: str
    source_language: str
    target_language: str