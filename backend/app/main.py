"""
Founder Copilot - FastAPI Application Entry Point
Amazon Nova AI Hackathon Project
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routes import router
from app.models import HealthResponse

# ============================================
# Create FastAPI App
# ============================================
app = FastAPI(
    title="Founder Copilot",
    description=(
        "🚀 AI-Powered Startup Helper Agent built with Amazon Nova AI. "
        "Generates startup plans, technical architecture, GitHub issues, "
        "and pitch decks for founders."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

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
            "pro": settings.NOVA_PRO_MODEL_ID,
            "lite": settings.NOVA_LITE_MODEL_ID,
            "micro": settings.NOVA_MICRO_MODEL_ID,
        },
    )


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health():
    """Health check endpoint."""
    return await health_check()
