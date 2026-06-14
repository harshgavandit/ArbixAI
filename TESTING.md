# Testing Guide

## Backend Tests

### Run All Tests

```bash
cd backend
.venv/Scripts/activate  # Windows: .\.venv\Scripts\activate
pytest
```

### Run Specific Test

```bash
pytest tests/test_score_api.py::test_score_happy_path -v
```

### Test Coverage

```bash
pytest --cov=app tests/
```

## Test Categories

### 1. Happy Path Tests
- `test_score_happy_path`: Basic scoring functionality
- `test_score_with_boundary_values`: Edge case handling

### 2. Validation Tests
- `test_score_validation_error`: Invalid input rejection
- `test_crop_type_sanitization`: Input sanitization
- `test_crop_type_too_long`: Length validation

### 3. Persistence Tests
- `test_score_request_is_persisted`: Database storage
- `test_income_band_normalization`: Data normalization

### 4. API Tests
- `test_health_endpoint`: Health check
- `test_security_headers_present`: Security validation
- `test_drift_endpoint_shape`: Drift response format

## Linting and Formatting

### Backend

```bash
cd backend
ruff check app/ tests/
ruff format app/ tests/
```

### Frontend

```bash
cd frontend
npm run lint
npm run format
npm run build
```

## Integration Testing

Test the full flow:

1. Start backend: `cd backend && uvicorn app.main:app --reload`
2. Start frontend: `cd frontend && npm run dev`
3. Use browser to test form submission
4. Check database: `sqlite3 backend/score_audit.sqlite3 "SELECT * FROM score_requests;"`

## Environment Setup for Testing

```bash
# Backend
export LOG_LEVEL=DEBUG  # Enable debug logging
export SCORE_DB_PATH=./test.sqlite3  # Use separate test DB

# Run tests
pytest
```

## CI/CD Checklist

- [ ] All tests passing
- [ ] No linting errors
- [ ] No type checking errors
- [ ] Build succeeds
- [ ] API responds on /health
- [ ] Database initializes
