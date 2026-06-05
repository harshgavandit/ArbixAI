# LLM Notes

This project used Codex as an implementation assistant. LLM usage was limited to planning, code generation, review, and verification support. The final code was reviewed and adjusted to stay aligned with the PDF requirements.

## Tools Used

- Codex
- PowerShell commands for local verification
- Python/FastAPI tooling
- React/Vite tooling

## Example Prompts Used

1. Summarize the Arbix AI practical exercise PDF and identify the required backend, frontend, testing, documentation, and bonus deliverables.
2. Create a plan that follows the PDF exactly, excluding Docker but including linting/formatting, SQLite persistence, and a simple drift-check endpoint.
3. Implement a FastAPI `POST /score` endpoint with Pydantic validation, rule-based scoring, reason codes, audit logging, and tests.
4. Build a minimal React frontend with the four required fields, loading state, validation-error handling, and score/result display.
5. Review the codebase and remove any unnecessary files or endpoints so the final submission is easy to explain and aligned with the PDF.

## What Was Personally Checked

- Confirmed that `POST /score` accepts exactly the required scoring fields.
- Confirmed that validation covers missing fields, invalid types, non-positive land area, empty crop type, invalid repayment score, and invalid income band.
- Confirmed that successful responses include request id, score, exactly three reason codes, and timestamp.
- Confirmed that SQLite persistence stores successful scoring requests.
- Confirmed that `GET /drift` is the only extra endpoint and is included because it is a listed bonus item.
- Confirmed that Docker/docker-compose is not included.
- Removed generated local artifacts such as `.venv`, `node_modules`, build output, caches, and local SQLite data.
- Removed an unnecessary `/health` endpoint to keep the API surface aligned with the PDF.

## Example Improvement After Reviewing Tool Output

The PDF uses en dash values for income bands: `2–5L` and `5–10L`. Code and API clients commonly send ASCII hyphen values like `2-5L` and `5-10L`.

To make the API both PDF-aligned and practical, the backend accepts both forms and normalizes them internally. This keeps the UI labels aligned with the PDF while avoiding user/API friction during testing.

## Final Scope Decision

Implemented:

- required backend
- required frontend
- validation
- audit logging
- tests
- README
- LLM notes
- SQLite persistence bonus
- drift-check bonus
- linting/formatting bonus

Skipped:

- Docker/docker-compose
- authentication
- production deployment setup
- trained ML model
