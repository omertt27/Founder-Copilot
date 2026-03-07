"""
Founder Copilot - API Routes
All endpoint definitions for the startup helper agent.
"""

import json
import time
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
from app.config import settings
from app.demo_responses import get_demo_response, detect_demo_intent, stream_demo_response

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
async def generate_startup_plan(request: Request, body: StartupPlanRequest):
    """Generate a comprehensive startup plan from an idea."""
    start_time = time.time()
    try:
        if settings.DEMO_MODE:
            content, tokens_used = await get_demo_response("startup_plan")
        else:
            user_prompt = STARTUP_PLAN_PROMPT.format(user_input=body.idea)
            content, tokens_used = await _invoke_async(
                system_prompt=SYSTEM_PROMPT,
                user_prompt=user_prompt,
                model=body.model.value,
                temperature=0.3,
                max_tokens=4096,
            )

        elapsed = round(time.time() - start_time, 2)

        return GenerationResponse(
            feature=FeatureType.STARTUP_PLAN,
            content=content,
            model_used="demo" if settings.DEMO_MODE else body.model.value,
            tokens_used=tokens_used,
            generation_time=elapsed,
            demo_mode=settings.DEMO_MODE,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")


# ============================================
# FEATURE 2: Technical Architecture Generator
# ============================================
@router.post("/generate/tech-architecture", response_model=GenerationResponse)
@limiter.limit("10/minute")
async def generate_tech_architecture(request: Request, body: TechArchitectureRequest):
    """Generate technical architecture for a product."""
    start_time = time.time()
    try:
        if settings.DEMO_MODE:
            content, tokens_used = await get_demo_response("tech_architecture")
        else:
            user_prompt = TECH_ARCHITECTURE_PROMPT.format(
                product_description=body.product_description
            )
            content, tokens_used = await _invoke_async(
                system_prompt=SYSTEM_PROMPT,
                user_prompt=user_prompt,
                model=body.model.value,
                temperature=0.3,
                max_tokens=4096,
            )

        elapsed = round(time.time() - start_time, 2)

        return GenerationResponse(
            feature=FeatureType.TECH_ARCHITECTURE,
            content=content,
            model_used="demo" if settings.DEMO_MODE else body.model.value,
            tokens_used=tokens_used,
            generation_time=elapsed,
            demo_mode=settings.DEMO_MODE,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")


# ============================================
# FEATURE 3: GitHub Issues Generator
# ============================================
@router.post("/generate/github-issues", response_model=GenerationResponse)
@limiter.limit("10/minute")
async def generate_github_issues(request: Request, body: GitHubIssuesRequest):
    """Generate GitHub issues for MVP development."""
    start_time = time.time()
    try:
        if settings.DEMO_MODE:
            content, tokens_used = await get_demo_response("github_issues")
        else:
            user_prompt = GITHUB_ISSUES_PROMPT.format(
                product_name=body.product_name,
                product_description=body.product_description,
                tech_stack=body.tech_stack,
            )
            content, tokens_used = await _invoke_async(
                system_prompt=SYSTEM_PROMPT,
                user_prompt=user_prompt,
                model=body.model.value,
                temperature=0.3,
                max_tokens=4096,
            )

        elapsed = round(time.time() - start_time, 2)

        return GenerationResponse(
            feature=FeatureType.GITHUB_ISSUES,
            content=content,
            model_used="demo" if settings.DEMO_MODE else body.model.value,
            tokens_used=tokens_used,
            generation_time=elapsed,
            demo_mode=settings.DEMO_MODE,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")


# ============================================
# FEATURE 4: Pitch Deck Generator
# ============================================
@router.post("/generate/pitch-deck", response_model=GenerationResponse)
@limiter.limit("10/minute")
async def generate_pitch_deck(request: Request, body: PitchDeckRequest):
    """Generate a pitch deck outline."""
    start_time = time.time()
    try:
        if settings.DEMO_MODE:
            content, tokens_used = await get_demo_response("pitch_deck")
        else:
            user_prompt = PITCH_DECK_PROMPT.format(
                user_input=body.idea,
                product_description=body.product_description or body.idea,
            )
            content, tokens_used = await _invoke_async(
                system_prompt=SYSTEM_PROMPT,
                user_prompt=user_prompt,
                model=body.model.value,
                temperature=0.7,  # More creative for pitch decks
                max_tokens=4096,
            )

        elapsed = round(time.time() - start_time, 2)

        return GenerationResponse(
            feature=FeatureType.PITCH_DECK,
            content=content,
            model_used="demo" if settings.DEMO_MODE else body.model.value,
            tokens_used=tokens_used,
            generation_time=elapsed,
            demo_mode=settings.DEMO_MODE,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")


# ============================================
# AUTO-DETECT: Smart Agent Coordinator
# ============================================
@router.post("/generate/auto", response_model=AutoDetectResponse)
@limiter.limit("10/minute")
async def auto_generate(request: Request, body: AutoDetectRequest):
    """
    Auto-detect which feature to use based on user message,
    then generate the appropriate output.
    """
    start_time = time.time()
    try:
        if settings.DEMO_MODE:
            detected = detect_demo_intent(body.message)
            content, _ = await get_demo_response(detected)
            elapsed = round(time.time() - start_time, 2)

            feature_map = {
                "startup_plan": FeatureType.STARTUP_PLAN,
                "tech_architecture": FeatureType.TECH_ARCHITECTURE,
                "github_issues": FeatureType.GITHUB_ISSUES,
                "pitch_deck": FeatureType.PITCH_DECK,
            }

            return AutoDetectResponse(
                detected_feature=feature_map.get(detected, FeatureType.STARTUP_PLAN),
                content=content,
                model_used="demo",
                generation_time=elapsed,
                demo_mode=True,
            )

        # Step 1: Detect intent using Nova Micro (fast)
        coordinator_prompt = AGENT_COORDINATOR_PROMPT.format(
            user_input=body.message
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
            user_prompt = STARTUP_PLAN_PROMPT.format(user_input=body.message)
            temperature = 0.3
        elif detected_feature == FeatureType.TECH_ARCHITECTURE:
            desc = (
                body.context.get("product_description", body.message)
                if body.context
                else body.message
            )
            user_prompt = TECH_ARCHITECTURE_PROMPT.format(product_description=desc)
            temperature = 0.3
        elif detected_feature == FeatureType.GITHUB_ISSUES:
            ctx = body.context or {}
            user_prompt = GITHUB_ISSUES_PROMPT.format(
                product_name=ctx.get("product_name", "My Startup"),
                product_description=ctx.get("product_description", body.message),
                tech_stack=ctx.get("tech_stack", "To be determined"),
            )
            temperature = 0.3
        elif detected_feature == FeatureType.PITCH_DECK:
            ctx = body.context or {}
            user_prompt = PITCH_DECK_PROMPT.format(
                user_input=body.message,
                product_description=ctx.get("product_description", body.message),
            )
            temperature = 0.7
        else:
            user_prompt = STARTUP_PLAN_PROMPT.format(user_input=body.message)
            temperature = 0.3

        content, _ = await _invoke_async(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=user_prompt,
            model=body.model.value,
            temperature=temperature,
            max_tokens=4096,
        )

        elapsed = round(time.time() - start_time, 2)

        return AutoDetectResponse(
            detected_feature=detected_feature,
            content=content,
            model_used=body.model.value,
            generation_time=elapsed,
            demo_mode=False,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")


# ============================================
# STREAMING ENDPOINT
# ============================================
@router.post("/generate/stream/{feature}")
@limiter.limit("10/minute")
async def generate_stream(feature: FeatureType, request: Request, body: AutoDetectRequest):
    """Stream generation output for any feature."""

    if settings.DEMO_MODE:
        async def demo_stream():
            import asyncio as _asyncio
            for chunk in stream_demo_response(feature.value):
                await _asyncio.sleep(0.03)  # Simulate typing speed
                yield f"data: {json.dumps({'text': chunk})}\n\n"
            yield "data: [DONE]\n\n"

        return StreamingResponse(
            demo_stream(),
            media_type="text/event-stream",
            headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
        )

    prompt_map = {
        FeatureType.STARTUP_PLAN: (
            STARTUP_PLAN_PROMPT.format(user_input=body.message),
            0.3,
        ),
        FeatureType.TECH_ARCHITECTURE: (
            TECH_ARCHITECTURE_PROMPT.format(product_description=body.message),
            0.3,
        ),
        FeatureType.GITHUB_ISSUES: (
            GITHUB_ISSUES_PROMPT.format(
                product_name="My Startup",
                product_description=body.message,
                tech_stack="To be determined",
            ),
            0.3,
        ),
        FeatureType.PITCH_DECK: (
            PITCH_DECK_PROMPT.format(
                user_input=body.message,
                product_description=body.message,
            ),
            0.7,
        ),
    }

    user_prompt, temperature = prompt_map.get(
        feature,
        (STARTUP_PLAN_PROMPT.format(user_input=body.message), 0.3),
    )

    async def stream_generator():
        try:
            for chunk in nova_client.invoke_streaming(
                system_prompt=SYSTEM_PROMPT,
                user_prompt=user_prompt,
                model=body.model.value,
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
