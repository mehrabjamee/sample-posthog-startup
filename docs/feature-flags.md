# Feature Flags

This document tracks feature flags used in `sample-posthog-startup`.

## `new-billing-flow`

- Owner: `payments@startup.dev`
- Intended lifecycle: temporary rollout flag, remove after stable launch
- Created: 2025-08-18
- Purpose: move billing quotes from legacy seat + overage model to new pricing and discount engine
- Usage:
  - Backend billing logic branch
  - Frontend conditional render (`NewBilling` vs `LegacyBilling`)
- Cleanup note: remove after full rollout and delete legacy branch + related tests

## `onboarding-v2`

- Owner: `growth@startup.dev`
- Intended lifecycle: experiment
- Created: 2025-09-01
- Purpose: compare guided onboarding v2 to existing onboarding flow
- Usage:
  - Frontend hook-based gate (`useFeatureFlag("onboarding-v2")`)

## `debug-admin-panel`

- Owner: `platform@startup.dev`
- Intended lifecycle: kill-switch
- Created: 2025-10-14
- Purpose: gate access to internal admin diagnostics route
- Usage:
  - Backend FastAPI dependency guard for `GET /admin/debug`

## `exp-search-ranking`

- Owner: `search@startup.dev`
- Intended lifecycle: experiment
- Created: 2025-11-05
- Purpose: evaluate alternate ranking algorithm prioritizing title relevance
- Usage:
  - Backend utility (`rank_results`) and `/search` API
  - Frontend local search ranking simulation
