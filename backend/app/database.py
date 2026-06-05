from __future__ import annotations

import json
import os
import sqlite3
from collections.abc import Iterable
from pathlib import Path

DEFAULT_DB_PATH = Path(__file__).resolve().parent.parent / "score_audit.sqlite3"


def get_db_path() -> Path:
    return Path(os.getenv("SCORE_DB_PATH", DEFAULT_DB_PATH))


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(get_db_path())
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    db_path = get_db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS score_requests (
                request_id TEXT PRIMARY KEY,
                timestamp TEXT NOT NULL,
                land_area_acres REAL NOT NULL,
                crop_type TEXT NOT NULL,
                repayment_history_score REAL NOT NULL,
                annual_income_band TEXT NOT NULL,
                score REAL NOT NULL,
                reason_codes TEXT NOT NULL
            )
            """
        )


def save_score_request(
    *,
    request_id: str,
    timestamp: str,
    land_area_acres: float,
    crop_type: str,
    repayment_history_score: float,
    annual_income_band: str,
    score: float,
    reason_codes: list[str],
) -> None:
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO score_requests (
                request_id,
                timestamp,
                land_area_acres,
                crop_type,
                repayment_history_score,
                annual_income_band,
                score,
                reason_codes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                request_id,
                timestamp,
                land_area_acres,
                crop_type,
                repayment_history_score,
                annual_income_band,
                score,
                json.dumps(reason_codes),
            ),
        )


def fetch_recent_scores(limit: int = 100) -> list[sqlite3.Row]:
    with get_connection() as connection:
        rows: Iterable[sqlite3.Row] = connection.execute(
            """
            SELECT annual_income_band, repayment_history_score
            FROM score_requests
            ORDER BY timestamp DESC
            LIMIT ?
            """,
            (limit,),
        )
        return list(rows)
