"""
Founder Copilot - Configuration
Loads environment variables and app settings.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""

    # AWS
    AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    AWS_REGION: str = os.getenv("AWS_REGION", "us-east-1")

    # ── Amazon Nova 2 Models (Gen 2 — Hackathon focus) ──────────────────────
    NOVA_2_PRO_MODEL_ID: str  = os.getenv("NOVA_2_PRO_MODEL_ID",  "amazon.nova-pro-v2:0")
    NOVA_2_LITE_MODEL_ID: str = os.getenv("NOVA_2_LITE_MODEL_ID", "amazon.nova-lite-v2:0")

    # ── Amazon Nova 1 Models (Gen 1 — kept for Premier + Micro) ─────────────
    NOVA_PREMIER_MODEL_ID: str = os.getenv("NOVA_PREMIER_MODEL_ID", "amazon.nova-premier-v1:0")
    NOVA_MICRO_MODEL_ID: str   = os.getenv("NOVA_MICRO_MODEL_ID",   "amazon.nova-micro-v1:0")

    # Demo Mode — auto-enabled when no AWS credentials are set
    DEMO_MODE: bool = os.getenv("DEMO_MODE", "").lower() in ("true", "1", "yes")

    # App
    APP_ENV: str = os.getenv("APP_ENV", "development")
    APP_PORT: int = int(os.getenv("APP_PORT", "8000"))
    CORS_ORIGINS: list[str] = os.getenv(
        "CORS_ORIGINS", "http://localhost:5173,http://localhost:3000"
    ).split(",")

    # Model selection mapping  (key used in API requests → Bedrock model ID)
    MODEL_MAP: dict[str, str] = {}

    def __init__(self):
        self.MODEL_MAP = {
            # ── Nova 2 (new gen — primary choices) ──
            "nova2lite":  self.NOVA_2_LITE_MODEL_ID,   # default
            "nova2pro":   self.NOVA_2_PRO_MODEL_ID,    # high quality
            # ── Nova 1 (kept for Premier power + Micro speed) ──
            "premier":    self.NOVA_PREMIER_MODEL_ID,  # most powerful
            "micro":      self.NOVA_MICRO_MODEL_ID,    # intent detection
        }

        # Auto-enable demo mode when credentials are missing
        if not self.AWS_ACCESS_KEY_ID or not self.AWS_SECRET_ACCESS_KEY:
            self.DEMO_MODE = True


settings = Settings()
