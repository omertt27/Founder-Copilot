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

    # ── Amazon Nova 2 Lite (cross-region inference profile required) ────────
    NOVA_2_LITE_MODEL_ID: str = os.getenv("NOVA_2_LITE_MODEL_ID", "us.amazon.nova-2-lite-v1:0")

    # ── Amazon Nova Pro Gen 1 (cross-region inference profile) ───────────────
    NOVA_PRO_MODEL_ID: str = os.getenv("NOVA_PRO_MODEL_ID", "us.amazon.nova-pro-v1:0")

    # ── Amazon Nova Premier + Micro Gen 1 (cross-region inference profiles) ──
    NOVA_PREMIER_MODEL_ID: str = os.getenv("NOVA_PREMIER_MODEL_ID", "us.amazon.nova-premier-v1:0")
    NOVA_MICRO_MODEL_ID: str   = os.getenv("NOVA_MICRO_MODEL_ID",   "us.amazon.nova-micro-v1:0")

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
            # ── Nova 2 Lite (newest, default) ──
            "nova2lite":  self.NOVA_2_LITE_MODEL_ID,   # us.amazon.nova-2-lite-v1:0
            # ── Nova Pro Gen 1 (high quality) ──
            "nova2pro":   self.NOVA_PRO_MODEL_ID,      # us.amazon.nova-pro-v1:0
            # ── Nova Premier Gen 1 (most powerful) ──
            "premier":    self.NOVA_PREMIER_MODEL_ID,  # us.amazon.nova-premier-v1:0
            # ── Nova Micro Gen 1 (intent detection, fastest) ──
            "micro":      self.NOVA_MICRO_MODEL_ID,    # us.amazon.nova-micro-v1:0
        }

        # Auto-enable demo mode when credentials are missing
        if not self.AWS_ACCESS_KEY_ID or not self.AWS_SECRET_ACCESS_KEY:
            self.DEMO_MODE = True


settings = Settings()
