from __future__ import annotations

from math import isfinite
from typing import TypeAlias

from app.models import ScoreRequest

ReasonCode: TypeAlias = str
INCOME_POINTS = {
    "<2L": 4,
    "2-5L": 10,
    "5-10L": 16,
    ">10L": 22,
}


def clamp_score(value: float) -> float:
    """Clamp score between 0-100 and round to 2 decimal places."""
    return round(max(0, min(100, value)), 2)


def calculate_score(payload: ScoreRequest) -> tuple[float, list[ReasonCode]]:
    """Calculate credit score based on repayment history, land area, and income band.

    Returns tuple of (score: float, reason_codes: list[str])."""
    repayment_component = payload.repayment_history_score * 0.65

    if payload.land_area_acres < 1:
        land_component = 4
        land_reason = "small_landholding"
    elif payload.land_area_acres <= 5:
        land_component = 10
        land_reason = "moderate_landholding"
    else:
        land_component = 14
        land_reason = "large_landholding"

    income_component = INCOME_POINTS[payload.annual_income_band]
    score = clamp_score(repayment_component + land_component + income_component)

    if payload.repayment_history_score >= 75:
        repayment_reason = "good_repayment"
    elif payload.repayment_history_score >= 50:
        repayment_reason = "average_repayment"
    else:
        repayment_reason = "weak_repayment"

    if payload.annual_income_band == "<2L":
        income_reason = "low_income_band"
    elif payload.annual_income_band in {"2-5L", "5-10L"}:
        income_reason = "mid_income_band"
    else:
        income_reason = "high_income_band"

    reason_codes = [repayment_reason, land_reason, income_reason]
    return score, reason_codes


def bucket_repayment_score(score: float) -> str:
    """Bucket repayment score into ranges for drift analysis."""
    if not isfinite(score):
        return "invalid"
    if score < 50:
        return "0-49"
    if score < 75:
        return "50-74"
    return "75-100"
