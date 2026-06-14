from __future__ import annotations

import logging
import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from datetime import UTC, datetime
from uuid import uuid4

from fastapi import FastAPI  # type: ignore
from fastapi.middleware.cors import CORSMiddleware   # type: ignore

from app.database import init_db, save_score_request
from app.drift import get_drift
from app.models import DriftResponse, ScoreRequest, ScoreResponse
from app.scoring import calculate_score

SCORING_VERSION = os.getenv("SCORING_VERSION", "1.0")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",")

logging.basicConfig(level=getattr(logging, LOG_LEVEL), format="%(message)s")
logger = logging.getLogger("score_audit")


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    init_db()
    yield


app = FastAPI(title="Arbix AI Scoring API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/score", response_model=ScoreResponse)
def score(payload: ScoreRequest) -> ScoreResponse:
    request_id = str(uuid4())
    timestamp = datetime.now(UTC)
    score_value, reason_codes = calculate_score(payload)

    response = ScoreResponse(
        request_id=request_id,
        score=score_value,
        scoring_version=SCORING_VERSION,
        reason_codes=reason_codes,
        timestamp=timestamp,
    )

    save_score_request(
        request_id=request_id,
        timestamp=timestamp.isoformat(),
        land_area_acres=payload.land_area_acres,
        crop_type=payload.crop_type,
        repayment_history_score=payload.repayment_history_score,
        annual_income_band=payload.annual_income_band,
        score=score_value,
        reason_codes=reason_codes,
        scoring_version=SCORING_VERSION,
    )

    logger.info(
        {
            "event": "score_request",
            "request_id": request_id,
            "timestamp": timestamp.isoformat(),
            "land_area_acres": payload.land_area_acres,
            "crop_type": payload.crop_type,
            "repayment_history_score": payload.repayment_history_score,
            "annual_income_band": payload.annual_income_band,
            "score": score_value,
            "scoring_version": SCORING_VERSION,
            "reason_codes": reason_codes,
        }
    )

    return response


@app.get("/drift", response_model=DriftResponse)
def drift() -> DriftResponse:
    return get_drift()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy", "version": SCORING_VERSION}
