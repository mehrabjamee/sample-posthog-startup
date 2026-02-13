# Backend

FastAPI service for the sample startup app.

## Run

Create `backend/.env.local`:

```bash
POSTHOG_API_KEY=phc_xxx
POSTHOG_HOST=https://us.i.posthog.com
```

```bash
uv sync --extra dev
uv run uvicorn app.main:app --reload
```

## Test

```bash
uv run pytest
```
