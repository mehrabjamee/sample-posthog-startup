from __future__ import annotations

from dataclasses import dataclass

from app.feature_gate import with_flag
from app.flags import NEW_BILLING_FLOW
from app.posthog_client import PostHogClientProtocol


@dataclass
class InvoiceRequest:
    distinct_id: str
    seats: int
    usage_units: int
    is_enterprise: bool = False
    annual_commit: bool = False


def calculate_invoice_total(
    invoice: InvoiceRequest, posthog_client: PostHogClientProtocol
) -> dict[str, int | str]:
    # TODO: remove after full rollout of new-billing-flow.
    def legacy_path() -> dict[str, int | str]:
        base = invoice.seats * 1200
        overage = max(invoice.usage_units - 1000, 0) * 2
        total = base + overage
        return {"flow": "legacy", "subtotal": total, "discount": 0, "total": total}

    def new_path() -> dict[str, int | str]:
        base = invoice.seats * 1000
        usage_fee = max(invoice.usage_units - 1200, 0)
        total = base + usage_fee
        discount = 0

        # Nested conditional to mirror realistic business rollout complexity.
        if invoice.is_enterprise:
            if invoice.annual_commit:
                discount = int(total * 0.2)
            else:
                discount = int(total * 0.1)

        total_after_discount = max(total - discount, 0)
        return {
            "flow": "new",
            "subtotal": total,
            "discount": discount,
            "total": total_after_discount,
        }

    return with_flag(
        posthog_client=posthog_client,
        flag_key=NEW_BILLING_FLOW,
        distinct_id=invoice.distinct_id,
        on_fn=new_path,
        off_fn=legacy_path,
    )
