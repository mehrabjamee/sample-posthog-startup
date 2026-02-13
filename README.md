# sample-posthog-startup

A believable early-stage startup monorepo that demonstrates realistic PostHog feature flag usage across a Python backend and a minimal React frontend.

This repository is intentionally structured so automated flag removal (for example, removing `new-billing-flow`) requires touching business logic, API routes, frontend rendering code, tests, and docs.

## Stack

- Backend: FastAPI + pytest (Python 3.11+)
- Python tooling: `uv`
- Frontend: React + Vite

## Repository layout

- `backend/` FastAPI service, feature flag wrappers, tests
- `frontend/` React app using PostHog feature flag wrapper and hook
- `docs/` feature flag inventory and lifecycle notes

## Install uv (brief)

See: https://docs.astral.sh/uv/getting-started/installation/

Typical macOS install:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Backend setup and run

Create `backend/.env.local`:

```bash
POSTHOG_API_KEY=phc_xxx
POSTHOG_HOST=https://us.i.posthog.com
```

```bash
cd backend
uv sync --extra dev
uv run uvicorn app.main:app --reload
```

Backend tests:

```bash
cd backend
uv run pytest
```

If `uv.lock` is missing, generate it with:

```bash
cd backend
uv lock
```

## Frontend setup and run

```bash
cd frontend
npm install
npm run dev
```

Frontend integration note:
- Frontend flags are read from `window.posthog.isFeatureEnabled(...)`.
- Initialize PostHog in your app shell and identify the user before rendering.

Optional frontend tests:

```bash
cd frontend
npm test
```

## How feature flags are used

- Backend uses a `PostHogClientProtocol` with a real PostHog client.
- Frontend uses a small wrapper (`isFeatureEnabled`, `useFeatureFlag`) over browser PostHog.
- Flags are used across direct branches, dependency guards, and nested conditionals.

Recommended demo flag for automated removal: `new-billing-flow`.

Removing it requires changes in:
- backend billing logic
- backend tests
- frontend billing UI
- docs/feature-flags.md
