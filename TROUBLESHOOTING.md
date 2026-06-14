# Troubleshooting Guide

## Common Issues and Solutions

### Backend Won't Start

**Error**: `Address already in use`

**Solution**: Port 8000 is already in use.
```bash
# Find process using port 8000
lsof -i :8000
# Kill the process
kill -9 <PID>
# Or use different port
uvicorn app.main:app --port 8001
```

### Database Connection Error

**Error**: `Cannot open database file`

**Solution**: Database path is invalid or not writable.
```bash
# Check directory exists
ls -la $(dirname $SCORE_DB_PATH)
# Ensure directory is writable
chmod 755 $(dirname $SCORE_DB_PATH)
```

### CORS Errors

**Error**: `Cross-Origin Request Blocked`

**Solution**: Frontend origin not in CORS_ORIGINS.
```bash
# Check current CORS configuration
echo $CORS_ORIGINS
# Update to include frontend origin
export CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

### API Not Responding

**Solution**: Check health endpoint.
```bash
curl -v http://127.0.0.1:8000/health
```

### Validation Errors

**Error**: `422 Unprocessable Entity`

**Solution**: Check request body against API docs.
```bash
# Verify JSON is valid
curl -X POST http://127.0.0.1:8000/score \
  -H "Content-Type: application/json" \
  -d '{"land_area_acres": 3.5, "crop_type": "wheat", "repayment_history_score": 82, "annual_income_band": "2-5L"}'
```

## Debugging

### Enable Debug Logging

```bash
export LOG_LEVEL=DEBUG
uvicorn app.main:app --reload
```

### Check Database Contents

```bash
sqlite3 score_audit.sqlite3
sqlite> SELECT * FROM score_requests;
sqlite> .headers on
sqlite> .mode column
```

### Frontend Issues

- Check browser console for errors (F12)
- Check network tab for API requests
- Verify API_BASE_URL is correct
- Clear browser cache if needed

## Performance Issues

### Slow API Responses

1. Check database size: `ls -lh score_audit.sqlite3`
2. Create indexes if needed
3. Monitor CPU/Memory usage

### Frontend Lag

1. Check for large form delays
2. Profile in browser DevTools
3. Optimize bundle size: `npm run build`

## Getting Help

1. Check logs: `export LOG_LEVEL=DEBUG`
2. Review API.md for endpoint requirements
3. Run tests: `pytest`
4. Check git history for recent changes
