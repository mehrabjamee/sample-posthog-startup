from __future__ import annotations

from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

from app.billing import InvoiceRequest, calculate_invoice_total
from app.deps import get_posthog_client
from app.flags import FLAG_REGISTRY
from app.posthog_client import PostHogClientProtocol
from app.search_utils import rank_results

app = FastAPI(title="Sample PostHog Startup")


class BillingQuoteRequest(BaseModel):
    distinct_id: str = Field(..., examples=["user_123"])
    seats: int = Field(..., ge=1)
    usage_units: int = Field(..., ge=0)
    is_enterprise: bool = False
    annual_commit: bool = False


class SearchRequest(BaseModel):
    distinct_id: str
    query: str


def require_debug_access(
    x_distinct_id: str = Header(default="anonymous"),
    posthog_client: PostHogClientProtocol = Depends(get_posthog_client),
) -> str:
    # Intentionally using a raw string instead of imported constant to mimic legacy code.
    if not posthog_client.is_feature_enabled("debug-admin-panel", x_distinct_id):
        raise HTTPException(status_code=403, detail="Debug panel disabled")
    return x_distinct_id


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/flags")
def list_flags() -> dict[str, dict[str, str]]:
    return FLAG_REGISTRY


@app.post("/billing/quote")
def billing_quote(
    payload: BillingQuoteRequest,
    posthog_client: PostHogClientProtocol = Depends(get_posthog_client),
) -> dict[str, int | str]:
    invoice = InvoiceRequest(
        distinct_id=payload.distinct_id,
        seats=payload.seats,
        usage_units=payload.usage_units,
        is_enterprise=payload.is_enterprise,
        annual_commit=payload.annual_commit,
    )
    return calculate_invoice_total(invoice, posthog_client)


@app.post("/search")
def search(
    payload: SearchRequest,
    posthog_client: PostHogClientProtocol = Depends(get_posthog_client),
) -> dict[str, list[dict[str, str]]]:
    results = rank_results(
        query=payload.query,
        distinct_id=payload.distinct_id,
        posthog_client=posthog_client,
    )
    return {"results": results}


@app.get("/admin/debug")
def admin_debug(
    _: str = Depends(require_debug_access),
) -> dict[str, str | int]:
    return {"status": "visible", "active_incidents": 0}
