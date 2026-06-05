from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, field_validator

IncomeBand = Literal["<2L", "2-5L", "5-10L", ">10L"]


class ScoreRequest(BaseModel):
    land_area_acres: float = Field(gt=0)
    crop_type: str = Field(min_length=1)
    repayment_history_score: float = Field(ge=0, le=100)
    annual_income_band: IncomeBand

    @field_validator("crop_type")
    @classmethod
    def crop_type_must_not_be_blank(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("crop_type must be a non-empty string")
        return stripped

    @field_validator("annual_income_band", mode="before")
    @classmethod
    def normalize_income_band(cls, value: str) -> str:
        if not isinstance(value, str):
            return value
        return value.strip().replace("–", "-")


class ScoreResponse(BaseModel):
    request_id: str
    score: float
    reason_codes: list[str] = Field(min_length=3, max_length=3)
    timestamp: datetime


class DriftMetric(BaseModel):
    psi: float
    status: Literal["stable", "watch", "drift_detected"]


class DriftResponse(BaseModel):
    record_count: int
    annual_income_band: DriftMetric
    repayment_history_score: DriftMetric
