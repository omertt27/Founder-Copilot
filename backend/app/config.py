"""
Founder Copilot — Configuration
Loads environment variables and Google GenAI settings.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""

    # ── Google GenAI / Gemini ─────────────────────────────────────────────
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")

    # Text + interleaved image generation model
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-preview-image-generation")

    # Fast model for intent classification / light tasks
    GEMINI_FLASH_MODEL: str = os.getenv("GEMINI_FLASH_MODEL", "gemini-2.0-flash")

    # Imagen 3 model for high-quality standalone image generation
    IMAGEN_MODEL: str = os.getenv("IMAGEN_MODEL", "imagen-3.0-generate-002")

    # TTS model (Gemini native audio output)
    TTS_MODEL: str = os.getenv("TTS_MODEL", "gemini-2.5-flash-preview-tts")

    # Google Cloud project (for Cloud Run deployment)
    GOOGLE_CLOUD_PROJECT: str = os.getenv("GOOGLE_CLOUD_PROJECT", "")
    GOOGLE_CLOUD_REGION: str = os.getenv("GOOGLE_CLOUD_REGION", "us-central1")

    # Demo Mode — auto-enabled when no API key is set
    DEMO_MODE: bool = os.getenv("DEMO_MODE", "").lower() in ("true", "1", "yes")

    # App
    APP_ENV: str = os.getenv("APP_ENV", "development")
    APP_PORT: int = int(os.getenv("APP_PORT", "8000"))
    CORS_ORIGINS: list[str] = os.getenv(
        "CORS_ORIGINS", "http://localhost:5173,http://localhost:3000"
    ).split(",")

    # Model selection mapping (key used in API requests → Gemini model ID)
    MODEL_MAP: dict[str, str] = {}

    def __init__(self):
        self.MODEL_MAP = {
            "flash":        self.GEMINI_FLASH_MODEL,         # gemini-2.0-flash (fast)
            "flash_image":  self.GEMINI_MODEL,               # gemini-2.0-flash-preview-image-generation
            "imagen":       self.IMAGEN_MODEL,               # imagen-3.0-generate-002
            "tts":          self.TTS_MODEL,                  # gemini-2.5-flash-preview-tts
        }

        # Auto-enable demo mode when API key is missing
        if not self.GOOGLE_API_KEY:
            self.DEMO_MODE = True


settings = Settings()
