# Arbix AI Practical Exercise

This repository contains a small full-stack scoring application built for the Arbix AI Round 1 practical exercise.

The project follows the PDF requirements closely:

- Python backend API
- React frontend UI
- clear validation and error handling
- basic explainability through reason codes
- structured audit logging
- backend tests
- LLM/tool disclosure

Docker/docker-compose is not included. The rest of the required scope and the selected non-Docker bonus items are implemented.

## Project Structure

```text
backend/
  app/
    main.py        FastAPI routes and request handling
    models.py      Pydantic request/response validation models
    scoring.py     Rule-based scoring and reason-code logic
    database.py    SQLite persistence helpers
    drift.py       Toy PSI-style drift calculation
  tests/
    test_score_api.py
  requirements.txt
  pyproject.toml

frontend/
  src/
    main.jsx       React form and API integration
    styles.css     Minimal UI styling
  package.json
  package-lock.json
  eslint.config.js

README.md
LLM_NOTES.md
```

## Features Implemented

### Required Features

- `POST /score` backend endpoint
- Four required input fields:
  - `land_area_acres`
  - `crop_type`
  - `repayment_history_score`
  - `annual_income_band`
- Input validation using Pydantic
- Useful `422` responses for invalid input
- Score returned from `0` to `100`
- Exactly three reason codes returned for every successful scoring response
- UUID request id
- ISO 8601 timestamp
- Structured audit logging for every successful scoring request
- Minimal React frontend form
- Frontend loading, validation-error, backend-error, and result states
- Backend tests for success, validation, persistence, and drift response shape
- `README.md` and `LLM_NOTES.md`

### Bonus Features Included

- Lightweight SQLite persistence
- Simple toy PSI-style drift endpoint: `GET /drift`
- Lightweight linting/formatting setup:
  - backend: Ruff
  - frontend: ESLint and Prettier

### Bonus Feature Skipped

- Docker/docker-compose was intentionally not included.

## Backend Setup

From the repository root:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The backend runs at:

```text
http://127.0.0.1:8000
```

The SQLite database file is created automatically at runtime as:

```text
backend/score_audit.sqlite3
```

This database file is ignored by Git because it is local runtime data.

## Frontend Setup

In a second terminal, from the repository root:

```powershell
cd frontend
npm install
npm run dev
```

The frontend runs at:

```text
http://127.0.0.1:5173
```

## API Usage

### Score Endpoint

```text
POST /score
```

Example request:

```json
{
  "land_area_acres": 3.5,
  "crop_type": "wheat",
  "repayment_history_score": 82,
  "annual_income_band": "2–5L"
}
```

Valid `annual_income_band` values:

- `<2L`
- `2–5L`
- `5–10L`
- `>10L`

The backend also accepts ASCII equivalents `2-5L` and `5-10L`, then normalizes them internally.

Example response:

```json
{
  "request_id": "59b8e53d-b675-4864-a641-a0b76008a403",
  "score": 73.3,
  "reason_codes": [
    "good_repayment",
    "moderate_landholding",
    "mid_income_band"
  ],
  "timestamp": "2026-06-05T16:52:45.000000Z"
}
```

### Drift Endpoint

```text
GET /drift
```

This endpoint reads recent persisted score records and compares their distribution against a small fixed baseline using a toy PSI-style calculation.

Example response:

```json
{
  "record_count": 5,
  "annual_income_band": {
    "psi": 0.1532,
    "status": "watch"
  },
  "repayment_history_score": {
    "psi": 0.0841,
    "status": "stable"
  }
}
```

Possible drift statuses:

- `stable`
- `watch`
- `drift_detected`

## Scoring Logic

The scoring logic is simple and rule-based, as allowed by the PDF.

The score uses:

- repayment history as the strongest factor
- land area as a secondary factor
- income band as a secondary factor

The final score is clamped between `0` and `100`.

Reason codes explain the main scoring factors. For example:

- `good_repayment`
- `average_repayment`
- `weak_repayment`
- `small_landholding`
- `moderate_landholding`
- `large_landholding`
- `low_income_band`
- `mid_income_band`
- `high_income_band`

Every successful response always returns exactly three reason codes:

1. one repayment reason
2. one landholding reason
3. one income-band reason

## Validation Behavior

Invalid requests return FastAPI/Pydantic `422` validation responses.

Examples of invalid input:

- missing required field
- negative or zero `land_area_acres`
- empty `crop_type`
- `repayment_history_score` below `0` or above `100`
- unsupported `annual_income_band`
- wrong data type

## Audit Logging And Persistence

For every successful scoring request, the backend:

- logs a structured audit event to the console
- stores the scoring record in SQLite

Stored fields include:

- request id
- timestamp
- land area
- crop type
- repayment history score
- normalized income band
- score
- reason codes

No authentication, personal documents, or unnecessary sensitive data are stored.

## Tests And Checks

Backend:

```powershell
cd backend
.\.venv\Scripts\activate
pytest
ruff check .
ruff format --check .
```

Frontend:

```powershell
cd frontend
npm run lint
npm run format
npm run build
```

## Design Choices And Tradeoffs

- FastAPI was chosen because it gives clean request validation and simple API development.
- Pydantic models keep input and output schemas explicit.
- The scoring model is intentionally rule-based because the exercise evaluates engineering judgement, not ML complexity.
- SQLite is used for lightweight persistence because it is simple and local.
- The drift endpoint is intentionally small and demonstrative, not production monitoring.
- The frontend is minimal so the main focus stays on correctness, validation, integration, logging, and tests.
- Docker was skipped to keep the submission focused on the requested implementation and because Docker was explicitly excluded for this version.



## Completed

- Backend scoring endpoint
- Backend validation and error handling
- Rule-based scoring
- Exactly three reason codes
- Structured audit logging
- SQLite persistence
- Drift-check endpoint
- React frontend
- Loading/error/result handling in the UI
- Backend tests
- Linting/formatting setup
- README documentation
- LLM usage notes

## Skipped

- Docker/docker-compose, intentionally excluded because i dont have it installed locally.
- Authentication, because it is outside the PDF scope.
- Production deployment setup, because it is outside the PDF scope.
- Trained ML model, because the PDF states that simple rule-based scoring is acceptable.

## LLM / Tool Usage Disclosure

I used Codex as an implementation assistant to:

- understand the PDF requirements
- create an implementation plan
- generate and refine backend/frontend code
- run tests and checks
- review alignment with the final codebase

I personally reviewed the generated output, checked PDF alignment, removed extra generated files, removed an unnecessary `/health` endpoint, and verified that the remaining codebase is focused on the required scope plus the selected non-Docker bonus items.

## What I Would Improve With 2 More Hours

- Add more edge-case tests for scoring boundaries.
- Add frontend component tests.
- Add a small read-only audit-record view for persisted scores.
- Make drift baselines configurable through a small config file.
- Add clearer API examples in generated OpenAPI docs.
