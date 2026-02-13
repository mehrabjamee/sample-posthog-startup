# Backend

FastAPI service for the sample startup app.

## Run

```bash
uv sync --extra dev
POSTHOG_API_KEY=phc_xxx uv run uvicorn app.main:app --reload
```

Optional host override:

```bash
POSTHOG_HOST=https://us.i.posthog.com
```

## Test

```bash
uv run pytest
```
