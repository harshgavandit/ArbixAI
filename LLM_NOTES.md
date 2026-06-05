# LLM Notes

## Example Prompts Used

1. Read the Arbix AI practical exercise PDF and summarize the required deliverables.
2. Create an implementation plan aligned with the PDF, excluding Docker but including the other bonus items.
3. Implement a FastAPI scoring endpoint with Pydantic validation, audit logging, tests, and SQLite persistence.
4. Build a minimal React UI that submits to the scoring endpoint and displays score reason codes.
5. Review whether the plan remains aligned with the PDF requirements.

## Reviewed And Improved

The income band values in the PDF use en dashes for `2–5L` and `5–10L`, while code and API clients often send ASCII hyphens. I adjusted the backend validation to accept both forms and normalize internally, so the implementation remains aligned with the PDF while being easier to use from the frontend and tests.
