# Logging Configuration Guide

## Backend Logging

The backend uses Python's standard logging library with structured JSON logging for audit events.

### Configuration

```python
# Set via environment variable
export LOG_LEVEL=INFO  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
```

### Log Levels

- **DEBUG**: Detailed diagnostic information
- **INFO**: General informational messages (default)
- **WARNING**: Warning messages for suspicious activity
- **ERROR**: Error messages for failures
- **CRITICAL**: Critical failures

### Log Output

All logs are output as JSON for easy parsing and aggregation:

```json
{
  "event": "score_request",
  "request_id": "59b8e53d-b675-4864-a641-a0b76008a403",
  "timestamp": "2026-06-05T16:52:45.000000Z",
  "land_area_acres": 3.5,
  "crop_type": "wheat",
  "score": 73.3,
  "event_type": "success"
}
```

### Log Events

- `score_request`: Successful score calculation
- `database_initialized`: Database schema initialized
- `database_init_error`: Database initialization failure
- `save_score_error`: Error saving score to database
- `fetch_scores_error`: Error fetching scores from database

## Monitoring

### Health Check

```bash
curl http://127.0.0.1:8000/health
```

Returns:
```json
{
  "status": "healthy",
  "version": "1.0"
}
```

### Drift Monitoring

```bash
curl http://127.0.0.1:8000/drift
```

Monitor for `drift_detected` status changes.

## Log Aggregation

For production, integrate with:
- ELK Stack (Elasticsearch, Logstash, Kibana)
- CloudWatch (AWS)
- Datadog
- New Relic
- Splunk

All logs are emitted as structured JSON for easy integration.
