from __future__ import annotations

import json
import logging
import os
import sqlite3
from collections.abc import Iterable
from pathlib import Path

logger = logging.getLogger("score_audit")

DEFAULT_DB_PATH = Path(__file__).resolve().parent.parent / "score_audit.sqlite3"


def get_db_path() -> Path:
    """Get database path from environment or use default."""
    return Path(os.getenv("SCORE_DB_PATH", DEFAULT_DB_PATH))


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(get_db_path())
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    """Initialize database schema if not exists.

    Note: SQLite in-memory databases should be used only for testing.
    Production deployments should use file-based or networked databases
    with proper access controls and backup strategies.
    """
    db_path = get_db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    try:
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
                    reason_codes TEXT NOT NULL,
                    scoring_version TEXT NOT NULL DEFAULT '1.0'
                )
                """
            )

            columns = [row["name"] for row in connection.execute("PRAGMA table_info(score_requests)")]
            if "scoring_version" not in columns:
                connection.execute(
                    "ALTER TABLE score_requests ADD COLUMN scoring_version TEXT NOT NULL DEFAULT '1.0'"
                )
        logger.info({"event": "database_initialized", "db_path": str(db_path)})
    except sqlite3.Error as e:
        logger.error({"event": "database_init_error", "error": str(e)})
        raise


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
    scoring_version: str,
) -> None:
    """Save score request to database."""
    try:
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
                    reason_codes,
                    scoring_version
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                    scoring_version,
                ),
            )
    except sqlite3.Error as e:
        logger.error({"event": "save_score_error", "request_id": request_id, "error": str(e)})
        raise


def fetch_recent_scores(limit: int = 100) -> list[sqlite3.Row]:
    """Fetch recent score requests from database."""
    try:
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
    except sqlite3.Error as e:
        logger.error({"event": "fetch_scores_error", "error": str(e)})
        return []
