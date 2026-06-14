from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, field_validator  # type: ignore[import]

IncomeBand = Literal["<2L", "2-5L", "5-10L", ">10L"]


class ScoreRequest(BaseModel):
    land_area_acres: float = Field(gt=0, description="Land area in acres, must be greater than 0")
    crop_type: str = Field(min_length=1, description="Type of crop being cultivated")
    repayment_history_score: float = Field(ge=0, le=100, description="Credit score from 0 to 100")
    annual_income_band: IncomeBand = Field(description="Annual income range classification")

    @field_validator("crop_type")
    @classmethod
    def crop_type_must_not_be_blank(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("crop_type must be a non-empty string")
        if len(stripped) > 100:
            raise ValueError("crop_type must not exceed 100 characters")
        return stripped

    @field_validator("annual_income_band", mode="before")
    @classmethod
    def normalize_income_band(cls, value: str) -> str:
        if not isinstance(value, str):
            return value
        normalized = value.strip().replace("–", "-")
        valid_bands = {"<2L", "2-5L", "5-10L", ">10L"}
        if normalized not in valid_bands:
            raise ValueError(f"Invalid income band. Must be one of: {', '.join(valid_bands)}")
        return normalized


class ScoreResponse(BaseModel):
    request_id: str
    score: float
    scoring_version: str = Field(min_length=1)
    reason_codes: list[str] = Field(min_length=3, max_length=3)
    timestamp: datetime


class DriftMetric(BaseModel):
    psi: float
    status: Literal["stable", "watch", "drift_detected"]


class DriftResponse(BaseModel):
    record_count: int
    annual_income_band: DriftMetric
    repayment_history_score: DriftMetric
