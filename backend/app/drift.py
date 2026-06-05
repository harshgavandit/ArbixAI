from __future__ import annotations

import math
from collections import Counter

from app.database import fetch_recent_scores
from app.models import DriftMetric, DriftResponse
from app.scoring import bucket_repayment_score

BASELINE_INCOME_BAND = {
    "<2L": 0.25,
    "2-5L": 0.35,
    "5-10L": 0.25,
    ">10L": 0.15,
}

BASELINE_REPAYMENT = {
    "0-49": 0.20,
    "50-74": 0.35,
    "75-100": 0.45,
}


def psi_status(value: float) -> str:
    if value >= 0.25:
        return "drift_detected"
    if value >= 0.10:
        return "watch"
    return "stable"


def calculate_psi(actual_counts: Counter[str], baseline: dict[str, float]) -> float:
    total = sum(actual_counts.values())
    if total == 0:
        return 0.0

    psi = 0.0
    epsilon = 0.0001
    for bucket, expected_ratio in baseline.items():
        actual_ratio = actual_counts.get(bucket, 0) / total
        actual = max(actual_ratio, epsilon)
        expected = max(expected_ratio, epsilon)
        psi += (actual - expected) * math.log(actual / expected)
    return round(psi, 4)


def drift_metric(actual_counts: Counter[str], baseline: dict[str, float]) -> DriftMetric:
    psi = calculate_psi(actual_counts, baseline)
    return DriftMetric(psi=psi, status=psi_status(psi))


def get_drift(limit: int = 100) -> DriftResponse:
    rows = fetch_recent_scores(limit=limit)
    income_counts: Counter[str] = Counter(row["annual_income_band"] for row in rows)
    repayment_counts: Counter[str] = Counter(
        bucket_repayment_score(row["repayment_history_score"]) for row in rows
    )

    return DriftResponse(
        record_count=len(rows),
        annual_income_band=drift_metric(income_counts, BASELINE_INCOME_BAND),
        repayment_history_score=drift_metric(repayment_counts, BASELINE_REPAYMENT),
    )
