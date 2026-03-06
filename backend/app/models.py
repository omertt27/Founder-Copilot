"""
Founder Copilot - Pydantic Models
Request/Response schemas for the API.
"""

from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class NovaModel(str, Enum):
    """Available Amazon Nova models."""
    PRO = "pro"
    LITE = "lite"
    MICRO = "micro"


class FeatureType(str, Enum):
    """Available features/generators."""
    STARTUP_PLAN = "startup_plan"
    TECH_ARCHITECTURE = "tech_architecture"
    GITHUB_ISSUES = "github_issues"
    PITCH_DECK = "pitch_deck"
    AUTO_DETECT = "auto_detect"


# ---- Request Models ----

class StartupPlanRequest(BaseModel):
    """Request for generating a startup plan."""
    idea: str = Field(..., description="The startup idea description", min_length=10)
    model: NovaModel = Field(default=NovaModel.PRO, description="Nova model to use")


class TechArchitectureRequest(BaseModel):
    """Request for generating technical architecture."""
    product_description: str = Field(..., description="Product description", min_length=10)
    model: NovaModel = Field(default=NovaModel.PRO, description="Nova model to use")


class GitHubIssuesRequest(BaseModel):
    """Request for generating GitHub issues."""
    product_name: str = Field(..., description="Name of the product")
    product_description: str = Field(..., description="Product description", min_length=10)
    tech_stack: str = Field(
        default="To be determined",
        description="Tech stack (optional, will be suggested if not provided)"
    )
    model: NovaModel = Field(default=NovaModel.PRO, description="Nova model to use")


class PitchDeckRequest(BaseModel):
    """Request for generating a pitch deck."""
    idea: str = Field(..., description="The startup idea")
    product_description: str = Field(
        default="",
        description="Detailed product description (optional)"
    )
    model: NovaModel = Field(default=NovaModel.PRO, description="Nova model to use")


class AutoDetectRequest(BaseModel):
    """Request that auto-detects which feature to use."""
    message: str = Field(..., description="Free-form user message", min_length=5)
    model: NovaModel = Field(default=NovaModel.PRO, description="Nova model to use")
    # Context from previous generations (optional)
    context: Optional[dict] = Field(
        default=None,
        description="Context from previous generations to chain features"
    )


# ---- Response Models ----

class GenerationResponse(BaseModel):
    """Standard response for all generation endpoints."""
    feature: FeatureType
    content: str
    model_used: str
    tokens_used: Optional[int] = None


class AutoDetectResponse(BaseModel):
    """Response for auto-detect endpoint."""
    detected_feature: FeatureType
    content: str
    model_used: str


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    service: str
    version: str
    nova_models: dict
