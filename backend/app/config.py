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

    # Amazon Nova Model IDs
    NOVA_PRO_MODEL_ID: str = os.getenv("NOVA_PRO_MODEL_ID", "amazon.nova-pro-v1:0")
    NOVA_LITE_MODEL_ID: str = os.getenv("NOVA_LITE_MODEL_ID", "amazon.nova-lite-v1:0")
    NOVA_MICRO_MODEL_ID: str = os.getenv("NOVA_MICRO_MODEL_ID", "amazon.nova-micro-v1:0")

    # App
    APP_ENV: str = os.getenv("APP_ENV", "development")
    APP_PORT: int = int(os.getenv("APP_PORT", "8000"))
    CORS_ORIGINS: list[str] = os.getenv(
        "CORS_ORIGINS", "http://localhost:5173,http://localhost:3000"
    ).split(",")

    # Model selection mapping
    MODEL_MAP: dict[str, str] = {}

    def __init__(self):
        self.MODEL_MAP = {
            "pro": self.NOVA_PRO_MODEL_ID,
            "lite": self.NOVA_LITE_MODEL_ID,
            "micro": self.NOVA_MICRO_MODEL_ID,
        }


settings = Settings()
