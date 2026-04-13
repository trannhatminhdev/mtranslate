"""
Application configuration loaded from environment variables.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings from environment."""

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False
    CORS_ORIGINS: list[str] = ["http://localhost:1420", "http://localhost:3000"]

    # API Keys
    OPENAI_API_KEY: str = ""
    DEEPGRAM_API_KEY: str = ""

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Database
    DATABASE_URL: str = "postgresql://mtrans:mtrans@localhost:5432/mtrans"

    # STT
    STT_PROVIDER: str = "openai"  # openai | whisper_local | deepgram

    # Translation
    TRANSLATION_PROVIDER: str = "openai"
    TRANSLATION_MODEL: str = "gpt-4o"

    # TTS
    TTS_PROVIDER: str = "openai"  # openai | edge_tts
    TTS_VOICE: str = "alloy"

    # JWT
    JWT_SECRET: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 1440

    model_config = {"env_file": "../.env", "env_file_encoding": "utf-8", "extra": "ignore"}


settings = Settings()
