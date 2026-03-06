"""
Founder Copilot - API Routes
All endpoint definitions for the startup helper agent.
"""

import json
import asyncio
from functools import partial
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.models import (
    StartupPlanRequest,
    TechArchitectureRequest,
    GitHubIssuesRequest,
    PitchDeckRequest,
    AutoDetectRequest,
    GenerationResponse,
    AutoDetectResponse,
    FeatureType,
)
from app.prompts import (
    SYSTEM_PROMPT,
    STARTUP_PLAN_PROMPT,
    TECH_ARCHITECTURE_PROMPT,
    GITHUB_ISSUES_PROMPT,
    PITCH_DECK_PROMPT,
    AGENT_COORDINATOR_PROMPT,
)
from app.nova_client import nova_client

router = APIRouter(prefix="/api", tags=["Founder Copilot"])
limiter = Limiter(key_func=get_remote_address)


async def _invoke_async(system_prompt, user_prompt, model, temperature, max_tokens):
    """Run the blocking boto3 call in a thread to avoid blocking the event loop.
    Returns (content, tokens_used) tuple."""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        None,
        partial(
            nova_client.invoke,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
        ),
    )


# ============================================
# FEATURE 1: Startup Plan Generator
# ============================================
@router.post("/generate/startup-plan", response_model=GenerationResponse)
@limiter.limit("10/minute")
async def generate_startup_plan(request: StartupPlanRequest, req: Request):
    """Generate a comprehensive startup plan from an idea."""
    try:
        user_prompt = STARTUP_PLAN_PROMPT.format(user_input=request.idea)

        content, tokens_used = await _invoke_async(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=user_prompt,
            model=request.model.value,
            temperature=0.3,
            max_tokens=4096,
        )

        return GenerationResponse(
            feature=FeatureType.STARTUP_PLAN,
            content=content,
            model_used=request.model.value,
            tokens_used=tokens_used,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")


# ============================================
# FEATURE 2: Technical Architecture Generator
# ============================================
@router.post("/generate/tech-architecture", response_model=GenerationResponse)
@limiter.limit("10/minute")
async def generate_tech_architecture(request: TechArchitectureRequest, req: Request):
    """Generate technical architecture for a product."""
    try:
        user_prompt = TECH_ARCHITECTURE_PROMPT.format(
            product_description=request.product_description
        )

        content, tokens_used = await _invoke_async(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=user_prompt,
            model=request.model.value,
            temperature=0.3,
            max_tokens=4096,
        )

        return GenerationResponse(
            feature=FeatureType.TECH_ARCHITECTURE,
            content=content,
            model_used=request.model.value,
            tokens_used=tokens_used,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")


# ============================================
# FEATURE 3: GitHub Issues Generator
# ============================================
@router.post("/generate/github-issues", response_model=GenerationResponse)
@limiter.limit("10/minute")
async def generate_github_issues(request: GitHubIssuesRequest, req: Request):
    """Generate GitHub issues for MVP development."""
    try:
        user_prompt = GITHUB_ISSUES_PROMPT.format(
            product_name=request.product_name,
            product_description=request.product_description,
            tech_stack=request.tech_stack,
        )

        content, tokens_used = await _invoke_async(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=user_prompt,
            model=request.model.value,
            temperature=0.3,
            max_tokens=4096,
        )

        return GenerationResponse(
            feature=FeatureType.GITHUB_ISSUES,
            content=content,
            model_used=request.model.value,
            tokens_used=tokens_used,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")


# ============================================
# FEATURE 4: Pitch Deck Generator
# ============================================
@router.post("/generate/pitch-deck", response_model=GenerationResponse)
@limiter.limit("10/minute")
async def generate_pitch_deck(request: PitchDeckRequest, req: Request):
    """Generate a pitch deck outline."""
    try:
        user_prompt = PITCH_DECK_PROMPT.format(
            user_input=request.idea,
            product_description=request.product_description or request.idea,
        )

        content, tokens_used = await _invoke_async(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=user_prompt,
            model=request.model.value,
            temperature=0.7,  # More creative for pitch decks
            max_tokens=4096,
        )

        return GenerationResponse(
            feature=FeatureType.PITCH_DECK,
            content=content,
            model_used=request.model.value,
            tokens_used=tokens_used,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")


# ============================================
# AUTO-DETECT: Smart Agent Coordinator
# ============================================
@router.post("/generate/auto", response_model=AutoDetectResponse)
@limiter.limit("10/minute")
async def auto_generate(request: AutoDetectRequest, req: Request):
    """
    Auto-detect which feature to use based on user message,
    then generate the appropriate output.
    """
    try:
        # Step 1: Detect intent using Nova Micro (fast)
        coordinator_prompt = AGENT_COORDINATOR_PROMPT.format(
            user_input=request.message
        )

        detected, _ = await _invoke_async(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=coordinator_prompt,
            model="micro",
            temperature=0.1,
            max_tokens=50,
        )

        detected = detected.strip().lower()

        # Map detected intent to feature
        feature_map = {
            "startup_plan": FeatureType.STARTUP_PLAN,
            "tech_architecture": FeatureType.TECH_ARCHITECTURE,
            "github_issues": FeatureType.GITHUB_ISSUES,
            "pitch_deck": FeatureType.PITCH_DECK,
        }

        detected_feature = feature_map.get(detected, FeatureType.STARTUP_PLAN)

        # Step 2: Generate content based on detected feature
        if detected_feature == FeatureType.STARTUP_PLAN:
            user_prompt = STARTUP_PLAN_PROMPT.format(user_input=request.message)
            temperature = 0.3
        elif detected_feature == FeatureType.TECH_ARCHITECTURE:
            desc = (
                request.context.get("product_description", request.message)
                if request.context
                else request.message
            )
            user_prompt = TECH_ARCHITECTURE_PROMPT.format(product_description=desc)
            temperature = 0.3
        elif detected_feature == FeatureType.GITHUB_ISSUES:
            ctx = request.context or {}
            user_prompt = GITHUB_ISSUES_PROMPT.format(
                product_name=ctx.get("product_name", "My Startup"),
                product_description=ctx.get("product_description", request.message),
                tech_stack=ctx.get("tech_stack", "To be determined"),
            )
            temperature = 0.3
        elif detected_feature == FeatureType.PITCH_DECK:
            ctx = request.context or {}
            user_prompt = PITCH_DECK_PROMPT.format(
                user_input=request.message,
                product_description=ctx.get("product_description", request.message),
            )
            temperature = 0.7
        else:
            user_prompt = STARTUP_PLAN_PROMPT.format(user_input=request.message)
            temperature = 0.3

        content, _ = await _invoke_async(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=user_prompt,
            model=request.model.value,
            temperature=temperature,
            max_tokens=4096,
        )

        return AutoDetectResponse(
            detected_feature=detected_feature,
            content=content,
            model_used=request.model.value,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")


# ============================================
# STREAMING ENDPOINT
# ============================================
@router.post("/generate/stream/{feature}")
@limiter.limit("10/minute")
async def generate_stream(feature: FeatureType, request: AutoDetectRequest, req: Request):
    """Stream generation output for any feature."""

    prompt_map = {
        FeatureType.STARTUP_PLAN: (
            STARTUP_PLAN_PROMPT.format(user_input=request.message),
            0.3,
        ),
        FeatureType.TECH_ARCHITECTURE: (
            TECH_ARCHITECTURE_PROMPT.format(product_description=request.message),
            0.3,
        ),
        FeatureType.GITHUB_ISSUES: (
            GITHUB_ISSUES_PROMPT.format(
                product_name="My Startup",
                product_description=request.message,
                tech_stack="To be determined",
            ),
            0.3,
        ),
        FeatureType.PITCH_DECK: (
            PITCH_DECK_PROMPT.format(
                user_input=request.message,
                product_description=request.message,
            ),
            0.7,
        ),
    }

    user_prompt, temperature = prompt_map.get(
        feature,
        (STARTUP_PLAN_PROMPT.format(user_input=request.message), 0.3),
    )

    async def stream_generator():
        try:
            for chunk in nova_client.invoke_streaming(
                system_prompt=SYSTEM_PROMPT,
                user_prompt=user_prompt,
                model=request.model.value,
                temperature=temperature,
                max_tokens=4096,
            ):
                yield f"data: {json.dumps({'text': chunk})}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(
        stream_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )
