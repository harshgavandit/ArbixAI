# Configuration Guide

## Backend Configuration

All backend configuration is managed through environment variables.

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `SCORING_VERSION` | `1.0` | API version |
| `LOG_LEVEL` | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL) |
| `CORS_ORIGINS` | `http://localhost:5173,http://127.0.0.1:5173` | Comma-separated CORS origins |
| `SCORE_DB_PATH` | `./score_audit.sqlite3` | Path to SQLite database file |

### Setup Instructions

1. Copy `.env.example` to `.env`:
```bash
cp backend/.env.example backend/.env
```

2. Edit `.env` with your values:
```env
SCORING_VERSION=1.0
LOG_LEVEL=INFO
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
SCORE_DB_PATH=./score_audit.sqlite3
```

3. Load environment before running:
```bash
export $(cat .env | xargs)
```

## Frontend Configuration

Frontend configuration uses Vite environment variables.

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `VITE_API_BASE_URL` | `http://127.0.0.1:8000` | Backend API base URL |

### Setup Instructions

1. Copy `.env.example` to `.env.local`:
```bash
cp frontend/.env.example frontend/.env.local
```

2. Edit `.env.local`:
```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

## Security Considerations

1. **Database Path**: For production, use absolute path or network storage
2. **CORS Origins**: Restrict to known, trusted domains only
3. **Log Level**: Use `WARNING` or higher in production
4. **API Keys**: If adding authentication, store securely in `.env`

## Production Configuration

For production deployment:

```env
SCORING_VERSION=1.0
LOG_LEVEL=WARNING
CORS_ORIGINS=https://yourdomain.com
SCORE_DB_PATH=/data/score_audit.sqlite3
```

For frontend:
```env
VITE_API_BASE_URL=https://api.yourdomain.com
```

## Configuration Validation

The application validates all configuration on startup:
- Verifies database path is accessible
- Checks CORS origins are properly formatted
- Validates log level is recognized
