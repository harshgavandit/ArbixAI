# Arbix AI Practical Exercise

Small full-stack scoring application for the Arbix AI Round 1 practical exercise.

## What Is Included

- Python FastAPI backend with `POST /score`
- React frontend with a form for the four required scoring inputs
- Pydantic validation and useful `422` responses
- Structured audit logging for successful scoring requests
- SQLite persistence for scoring audit records
- Simple toy PSI-style `GET /drift` endpoint
- Backend tests
- Lightweight linting/formatting setup

Docker is intentionally skipped because it was excluded for this submission.

## Run Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API runs at `http://127.0.0.1:8000`.

## Run Frontend

```powershell
cd frontend
npm install
npm run dev
```

The UI runs at `http://127.0.0.1:5173`.

## Tests And Checks

```powershell
cd backend
pytest
ruff check .
ruff format --check .
```

```powershell
cd frontend
npm run lint
npm run format
npm run build
```

## API Notes

`POST /score` accepts:

- `land_area_acres`: positive number
- `crop_type`: non-empty string
- `repayment_history_score`: number from `0` to `100`
- `annual_income_band`: `<2L`, `2–5L`, `5–10L`, or `>10L`

The backend also accepts ASCII `2-5L` and `5-10L`, then normalizes internally.

The response includes a unique request id, score, exactly three reason codes, and an ISO 8601 timestamp.

## Design Choices And Tradeoffs

- FastAPI was chosen for concise request validation and simple API structure.
- Scoring is intentionally rule-based because the exercise does not require ML training.
- Repayment history is weighted most heavily, with land size and income band as smaller adjustments.
- SQLite persistence stores successful scoring requests only, keeping the implementation lightweight.
- The drift endpoint uses a toy PSI-style comparison against fixed baseline distributions. It is useful for demonstrating the idea, not for production monitoring.
- The frontend is deliberately minimal and focused on the required workflow.

## Time-Box Details

- Start time (IST): 2026-06-05 22:01
- End time (IST): 2026-06-05 22:18
- Approximate total time spent: 18 minutes

## Completed

- Backend scoring endpoint
- Validation and error handling
- Structured audit logging
- SQLite persistence
- Drift-check endpoint
- React frontend
- Loading and error handling in UI
- Backend tests
- Linting/formatting setup

## Skipped

- Docker/docker-compose, because it was explicitly excluded.
- Authentication and production deployment concerns, because they are outside the exercise scope.
- A trained ML model, because the PDF asks for simple rule-based scoring.

## LLM / Tool Usage Disclosure

I used Codex as an implementation assistant to read the PDF, plan the project, generate initial code, and run verification commands. I reviewed the generated structure, kept the scope aligned with the PDF, and corrected enum handling so both PDF-style income bands and ASCII equivalents are accepted safely.

## With 2 More Hours

- Add more scoring edge-case tests.
- Add frontend component tests.
- Make drift baselines configurable.
- Add a small admin view for persisted score audit records.
