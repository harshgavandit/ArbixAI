from fastapi.testclient import TestClient

from app.database import get_connection, init_db
from app.main import app

client = TestClient(app)


def setup_function() -> None:
    init_db()
    with get_connection() as connection:
        connection.execute("DELETE FROM score_requests")


def test_score_happy_path() -> None:
    response = client.post(
        "/score",
        json={
            "land_area_acres": 3.5,
            "crop_type": "wheat",
            "repayment_history_score": 82,
            "annual_income_band": "2-5L",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["request_id"]
    assert 0 <= body["score"] <= 100
    assert len(body["reason_codes"]) == 3
    assert body["timestamp"]


def test_score_validation_error() -> None:
    response = client.post(
        "/score",
        json={
            "land_area_acres": -1,
            "crop_type": "",
            "repayment_history_score": 120,
            "annual_income_band": "invalid",
        },
    )

    assert response.status_code == 422
    assert "detail" in response.json()


def test_score_request_is_persisted() -> None:
    response = client.post(
        "/score",
        json={
            "land_area_acres": 7,
            "crop_type": "rice",
            "repayment_history_score": 64,
            "annual_income_band": "5–10L",
        },
    )

    assert response.status_code == 200
    request_id = response.json()["request_id"]
    with get_connection() as connection:
        row = connection.execute(
            "SELECT request_id, annual_income_band FROM score_requests WHERE request_id = ?",
            (request_id,),
        ).fetchone()

    assert row["request_id"] == request_id
    assert row["annual_income_band"] == "5-10L"


def test_drift_endpoint_shape() -> None:
    response = client.get("/drift")

    assert response.status_code == 200
    body = response.json()
    assert "record_count" in body
    assert "annual_income_band" in body
    assert "repayment_history_score" in body
    assert "psi" in body["annual_income_band"]
    assert body["annual_income_band"]["status"] in {"stable", "watch", "drift_detected"}
