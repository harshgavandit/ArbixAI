from fastapi.testclient import TestClient # pyright: ignore[reportMissingImports]

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
    assert body["scoring_version"] == "1.0"
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
            "SELECT request_id, annual_income_band, scoring_version FROM score_requests WHERE request_id = ?",
            (request_id,),
        ).fetchone()

    assert row["request_id"] == request_id
    assert row["annual_income_band"] == "5-10L"
    assert row["scoring_version"] == "1.0"


def test_drift_endpoint_shape() -> None:
    response = client.get("/drift")

    assert response.status_code == 200
    body = response.json()
    assert "record_count" in body
    assert "annual_income_band" in body
    assert "repayment_history_score" in body
    assert "psi" in body["annual_income_band"]
    assert body["annual_income_band"]["status"] in {"stable", "watch", "drift_detected"}


def test_health_endpoint() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "healthy"
    assert body["version"] == "1.0"


def test_score_with_boundary_values() -> None:
    response = client.post(
        "/score",
        json={
            "land_area_acres": 0.01,
            "crop_type": "corn",
            "repayment_history_score": 0,
            "annual_income_band": "<2L",
        },
    )
    assert response.status_code == 200
    assert 0 <= response.json()["score"] <= 100


def test_score_with_maximum_values() -> None:
    response = client.post(
        "/score",
        json={
            "land_area_acres": 100,
            "crop_type": "soybean",
            "repayment_history_score": 100,
            "annual_income_band": ">10L",
        },
    )
    assert response.status_code == 200
    assert 0 <= response.json()["score"] <= 100


def test_crop_type_sanitization() -> None:
    response = client.post(
        "/score",
        json={
            "land_area_acres": 2.5,
            "crop_type": "  wheat  ",
            "repayment_history_score": 75,
            "annual_income_band": "2-5L",
        },
    )
    assert response.status_code == 200


def test_crop_type_too_long() -> None:
    response = client.post(
        "/score",
        json={
            "land_area_acres": 2.5,
            "crop_type": "x" * 101,
            "repayment_history_score": 75,
            "annual_income_band": "2-5L",
        },
    )
    assert response.status_code == 422


def test_income_band_normalization() -> None:
    response = client.post(
        "/score",
        json={
            "land_area_acres": 2.5,
            "crop_type": "wheat",
            "repayment_history_score": 75,
            "annual_income_band": "2-5L",
        },
    )
    assert response.status_code == 200
    request_id = response.json()["request_id"]
    with get_connection() as connection:
        row = connection.execute(
            "SELECT annual_income_band FROM score_requests WHERE request_id = ?",
            (request_id,),
        ).fetchone()
    assert row["annual_income_band"] == "2-5L"
