"""
FastAPI application for ReverseBottom.

POST /analyze          → run a mode on input text
GET  /modes            → list available modes
GET  /health           → health check
"""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from .config import Mode, get_settings
from .router import Router

# ── app setup ─────────────────────────────────────────────────────────────────

api_app = FastAPI(
    title="ReverseBottom",
    description="An anti-assistant for stress-testing ideas, inverting assumptions, and exposing cognitive biases.",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

api_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── models ────────────────────────────────────────────────────────────────────


class AnalyzeRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=10,
        max_length=8000,
        description="The idea, argument, or decision to analyze.",
        examples=["We should build an AI-powered social network for pets."],
    )
    mode: Mode = Field(
        default=Mode.DESTROY,
        description="Operating mode: destroy, reverse, or shadow.",
    )


class AnalyzeResponse(BaseModel):
    mode: str
    input: str
    output: str


class ModeInfo(BaseModel):
    name: str
    description: str


class ModesResponse(BaseModel):
    modes: list[ModeInfo]


class HealthResponse(BaseModel):
    status: str
    provider: str
    model: str


# ── error handling ────────────────────────────────────────────────────────────


@api_app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)},
    )


@api_app.exception_handler(Exception)
async def generic_error_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal error: {type(exc).__name__}: {exc}"},
    )


# ── routes ────────────────────────────────────────────────────────────────────

_MODE_DESCRIPTIONS = {
    Mode.DESTROY: "Find every flaw, contradiction, and risk in the idea.",
    Mode.REVERSE: "Invert core assumptions and rebuild the logic from the opposite frame.",
    Mode.SHADOW: "Surface hidden motives, cognitive biases, and blind spots in the framing.",
}


@api_app.get("/health", response_model=HealthResponse, tags=["meta"])
async def health() -> HealthResponse:
    settings = get_settings()
    return HealthResponse(
        status="ok",
        provider=settings.provider.value,
        model=settings.model,
    )


@api_app.get("/modes", response_model=ModesResponse, tags=["meta"])
async def list_modes() -> ModesResponse:
    return ModesResponse(
        modes=[
            ModeInfo(name=mode.value, description=_MODE_DESCRIPTIONS[mode])
            for mode in Mode
        ]
    )


@api_app.post("/analyze", response_model=AnalyzeResponse, tags=["analysis"])
async def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    """
    Analyze text using the specified mode.

    - **destroy**: Finds every flaw, risk, and contradiction.
    - **reverse**: Inverts core assumptions and constructs the mirror world.
    - **shadow**: Exposes hidden motives, cognitive biases, and blind spots.
    """
    router = Router()

    try:
        result = router.run(request.text, request.mode)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    return AnalyzeResponse(
        mode=result.mode.value,
        input=result.input_text,
        output=result.output,
    )
