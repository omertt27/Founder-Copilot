"""
Founder Copilot - Pydantic Models
Request/Response schemas for the API.
"""

from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class NovaModel(str, Enum):
    """Available Amazon Nova models."""
    # ── Nova 2 ──
    NOVA2LITE = "nova2lite"   # default — Nova 2 Lite (Gen 2, newest)
    # ── Nova 1 ──
    NOVA_PRO  = "nova_pro"    # Nova Pro (Gen 1, high quality)
    PREMIER   = "premier"     # Nova Premier (most powerful)
    MICRO     = "micro"       # Nova Micro (fastest / intent detection)


class FeatureType(str, Enum):
    """Available features/generators."""
    STARTUP_PLAN = "startup_plan"
    TECH_ARCHITECTURE = "tech_architecture"
    GITHUB_ISSUES = "github_issues"
    PITCH_DECK = "pitch_deck"
    MARKETING_STRATEGY = "marketing_strategy"
    AUTO_DETECT = "auto_detect"


# ---- Request Models ----

class StartupPlanRequest(BaseModel):
    """Request for generating a startup plan."""
    idea: str = Field(..., description="The startup idea description", min_length=10)
    model: NovaModel = Field(default=NovaModel.NOVA2LITE, description="Nova model to use")


class TechArchitectureRequest(BaseModel):
    """Request for generating technical architecture."""
    product_description: str = Field(..., description="Product description", min_length=10)
    model: NovaModel = Field(default=NovaModel.NOVA2LITE, description="Nova model to use")


class GitHubIssuesRequest(BaseModel):
    """Request for generating GitHub issues."""
    product_name: str = Field(..., description="Name of the product")
    product_description: str = Field(..., description="Product description", min_length=10)
    tech_stack: str = Field(
        default="To be determined",
        description="Tech stack (optional, will be suggested if not provided)"
    )
    model: NovaModel = Field(default=NovaModel.NOVA2LITE, description="Nova model to use")


class PitchDeckRequest(BaseModel):
    """Request for generating a pitch deck."""
    idea: str = Field(..., description="The startup idea")
    product_description: str = Field(
        default="",
        description="Detailed product description (optional)"
    )
    model: NovaModel = Field(default=NovaModel.NOVA2LITE, description="Nova model to use")


class MarketingStrategyRequest(BaseModel):
    """Request for generating a marketing strategy."""
    startup_idea: str = Field(..., description="The startup idea description", min_length=10)
    target_audience: Optional[str] = Field(default=None, description="Target audience description")
    budget: Optional[str] = Field(default=None, description="Budget range (e.g. '$5K/month')")
    model: NovaModel = Field(default=NovaModel.NOVA2LITE, description="Nova model to use")


class AutoDetectRequest(BaseModel):
    """Request that auto-detects which feature to use."""
    message: str = Field(..., description="Free-form user message", min_length=5)
    model: NovaModel = Field(default=NovaModel.NOVA2LITE, description="Nova model to use")
    context: Optional[dict] = Field(
        default=None,
        description="Context from previous generations to chain features"
    )


class FounderPackageRequest(BaseModel):
    """Request to run the full multi-agent Founder Package pipeline."""
    idea: str = Field(..., description="The startup idea description", min_length=10)
    target_audience: Optional[str] = Field(default=None, description="Target audience (optional)")
    budget: Optional[str] = Field(default=None, description="Marketing budget (optional)")
    model: NovaModel = Field(default=NovaModel.NOVA2LITE, description="Nova model to use")


class AgentStep(BaseModel):
    """A single step in the multi-agent pipeline."""
    agent: str
    feature: FeatureType
    content: str
    tokens_used: Optional[int] = None
    generation_time: Optional[float] = None
    status: str = "success"


class FounderPackageResponse(BaseModel):
    """Response from the full multi-agent Founder Package pipeline."""
    idea: str
    steps: list[AgentStep]
    total_tokens: Optional[int] = None
    total_time: Optional[float] = None
    model_used: str
    demo_mode: bool = False


# ---- Response Models ----

class GenerationResponse(BaseModel):
    """Standard response for all generation endpoints."""
    feature: FeatureType
    content: str
    model_used: str
    tokens_used: Optional[int] = None
    generation_time: Optional[float] = Field(
        default=None,
        description="Time in seconds to generate the response"
    )
    demo_mode: bool = Field(
        default=False,
        description="Whether this response was generated in demo mode"
    )


class AutoDetectResponse(BaseModel):
    """Response for auto-detect endpoint."""
    detected_feature: FeatureType
    content: str
    model_used: str
    generation_time: Optional[float] = Field(
        default=None,
        description="Time in seconds to generate the response"
    )
    demo_mode: bool = Field(
        default=False,
        description="Whether this response was generated in demo mode"
    )


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    service: str
    version: str
    nova_models: dict
    demo_mode: bool = False
