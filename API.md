# API Documentation

## Score Endpoint

### Request

```
POST /score
Content-Type: application/json
```

### Request Body

```json
{
  "land_area_acres": 3.5,
  "crop_type": "wheat",
  "repayment_history_score": 82,
  "annual_income_band": "2–5L"
}
```

### Request Validation

- `land_area_acres`: Required, must be > 0
- `crop_type`: Required, non-empty string, max 100 characters
- `repayment_history_score`: Required, must be 0-100
- `annual_income_band`: Required, one of: `<2L`, `2–5L`, `5–10L`, `>10L`

### Response

```json
{
  "request_id": "59b8e53d-b675-4864-a641-a0b76008a403",
  "score": 73.3,
  "scoring_version": "1.0",
  "reason_codes": ["good_repayment", "moderate_landholding", "mid_income_band"],
  "timestamp": "2026-06-05T16:52:45.000000Z"
}
```

### Response Fields

- `request_id`: Unique request identifier (UUID)
- `score`: Credit score (0-100)
- `scoring_version`: API version
- `reason_codes`: Array of exactly 3 codes explaining the score
- `timestamp`: ISO 8601 timestamp

## Drift Endpoint

### Request

```
GET /drift
```

### Response

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

### Response Fields

- `record_count`: Number of recent records analyzed
- `annual_income_band`: PSI metric and drift status
- `repayment_history_score`: PSI metric and drift status

### Drift Status Values

- `stable`: PSI < 0.10
- `watch`: PSI 0.10-0.24
- `drift_detected`: PSI >= 0.25

## Health Check Endpoint

### Request

```
GET /health
```

### Response

```json
{
  "status": "healthy",
  "version": "1.0"
}
```

## Error Responses

### Validation Error (422)

```json
{
  "detail": [
    {
      "loc": ["body", "land_area_acres"],
      "msg": "Input should be greater than 0",
      "type": "greater_than"
    }
  ]
}
```

### Server Error (500)

```json
{
  "detail": "Internal server error"
}
```

## CORS Headers

The API supports CORS requests from configured origins. Add the following headers:

```
Origin: http://localhost:5173
Access-Control-Request-Method: POST
Access-Control-Request-Headers: Content-Type
```
