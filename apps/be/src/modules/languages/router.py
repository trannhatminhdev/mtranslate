"""Supported languages endpoint."""

from fastapi import APIRouter

router = APIRouter()

SUPPORTED_LANGUAGES = [
    {"code": "vi", "name": "Tiếng Việt", "name_en": "Vietnamese"},
    {"code": "en", "name": "English", "name_en": "English"},
    {"code": "zh", "name": "中文", "name_en": "Chinese"},
    {"code": "ja", "name": "日本語", "name_en": "Japanese"},
    {"code": "ko", "name": "한국어", "name_en": "Korean"},
    {"code": "fr", "name": "Français", "name_en": "French"},
    {"code": "de", "name": "Deutsch", "name_en": "German"},
    {"code": "es", "name": "Español", "name_en": "Spanish"},
    {"code": "th", "name": "ไทย", "name_en": "Thai"},
    {"code": "id", "name": "Bahasa Indonesia", "name_en": "Indonesian"},
]


@router.get("/languages")
async def list_languages():
    """List all supported languages for translation."""
    return {"languages": SUPPORTED_LANGUAGES}
