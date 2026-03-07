"""
Founder Copilot - FastAPI Application Entry Point
Amazon Nova AI Hackathon Project
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.config import settings
from app.routes import router
from app.models import HealthResponse

# ============================================
# Rate Limiter
# ============================================
limiter = Limiter(key_func=get_remote_address)

# ============================================
# Create FastAPI App
# ============================================
app = FastAPI(
    title="Founder Copilot",
    description=(
        "🚀 AI-Powered Startup Helper Agent built with Amazon Nova AI. "
        "Simulates a full founding team: generates startup plans (CEO), "
        "technical architecture (CTO), GitHub issues (Engineering Lead), "
        "pitch decks (Investor Relations), and marketing strategies (CMO). "
        "#AmazonNova"
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# ============================================
# CORS Middleware
# ============================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# Include Routes
# ============================================
app.include_router(router)


# ============================================
# Health Check
# ============================================
@app.get("/", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Root health check endpoint."""
    return HealthResponse(
        status="healthy",
        service="Founder Copilot",
        version="1.0.0",
        nova_models={
            "nova2lite":  settings.NOVA_2_LITE_MODEL_ID,
            "nova2pro":   settings.NOVA_2_PRO_MODEL_ID,
            "premier":    settings.NOVA_PREMIER_MODEL_ID,
            "micro":      settings.NOVA_MICRO_MODEL_ID,
        },
        demo_mode=settings.DEMO_MODE,
    )


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health():
    """Health check endpoint."""
    return await health_check()
