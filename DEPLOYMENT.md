# Deployment Guide

## Prerequisites

- Python 3.9+
- Node.js 16+
- pip/npm package managers

## Backend Deployment

### Development

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Environment Variables

```bash
export SCORING_VERSION=1.0
export LOG_LEVEL=INFO
export CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
export SCORE_DB_PATH=./score_audit.sqlite3
```

### Health Check

```bash
curl http://127.0.0.1:8000/health
```

## Frontend Deployment

### Development

```bash
cd frontend
npm install
npm run dev
```

### Build

```bash
npm run build
npm run preview
```

## Database

SQLite database is created automatically at runtime. For production, consider:
- Backing up `score_audit.sqlite3` regularly
- Storing database path externally via `SCORE_DB_PATH` environment variable
- Implementing a proper database backup strategy

## API Endpoints

- `POST /score` - Calculate score for applicant
- `GET /drift` - Get drift metrics
- `GET /health` - Health check
- `OPTIONS /*` - CORS preflight

See README.md for full API documentation.
