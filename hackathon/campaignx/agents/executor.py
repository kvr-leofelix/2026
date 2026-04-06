# agents/executor.py
"""
Executor Agent
──────────────
Stage 3 — runs only after human approval.

Calls the InXiteOut Campaign Scheduling API with the approved plan + content.
Enforces the 100-calls/day quota per endpoint.
"""

from __future__ import annotations

import time
import random
import string
from dataclasses import dataclass

from .planner import CampaignPlan
from .creator import CampaignContent

# ── Exceptions ────────────────────────────────────────────────────────────────

class QuotaExhaustedError(RuntimeError):
    """Raised when the daily API call limit for an endpoint is reached."""

# ── Data model ────────────────────────────────────────────────────────────────

@dataclass
class ExecutionResult:
    """Returned after successfully scheduling a campaign."""
    campaign_id:     str
    status:          str   # "scheduled" | "failed" | "rejected"
    scheduled_time:  str
    recipient_count: int
    api_response_ms: int  = 0
    message:         str  = ""

# ── Quota tracker ─────────────────────────────────────────────────────────────

_DAILY_QUOTA: dict[str, int] = {"cohort": 12, "schedule": 7, "reports": 34}
_QUOTA_LIMIT = 100

def _check_and_increment(endpoint: str) -> None:
    used = _DAILY_QUOTA.get(endpoint, 0)
    if used >= _QUOTA_LIMIT:
        raise QuotaExhaustedError(
            f"Daily quota exhausted for '{endpoint}' ({used}/{_QUOTA_LIMIT})."
        )
    _DAILY_QUOTA[endpoint] = used + 1

# ── Main ──────────────────────────────────────────────────────────────────────

def run_executor(plan: CampaignPlan, content: CampaignContent) -> ExecutionResult:
    """
    Schedule the approved campaign via the InXiteOut Scheduling API.

    POST /api/v1/campaign/schedule
    Payload includes: campaign metadata, customer IDs, content, CTA URL.
    """
    _check_and_increment("schedule")

    t0 = time.monotonic()
    time.sleep(0.35)   # simulated API round-trip
    elapsed_ms = int((time.monotonic() - t0) * 1000)

    campaign_id = "CX-2025-" + "".join(random.choices(string.digits, k=3))
    count       = plan.estimated_audience or len(plan.customer_ids)

    # ── TODO: replace stub with real HTTP call ────────────────────────────
    # import requests, os
    # payload = {
    #     "campaign_id":   campaign_id,
    #     "cohort_ids":    plan.customer_ids,
    #     "schedule_time": plan.schedule_iso,
    #     "channel":       plan.channel,
    #     "cta_url":       content.cta_url,
    #     "subject":       content.subject,
    #     "body":          content.body_text,
    #     "approved_by":   "marketing_lead",
    # }
    # resp = requests.post(
    #     os.getenv("INXITEOUT_BASE_URL") + "/api/v1/campaign/schedule",
    #     json=payload,
    #     headers={"Authorization": f"Bearer {os.getenv('INXITEOUT_API_KEY')}"},
    #     timeout=10,
    # )
    # resp.raise_for_status()
    # ─────────────────────────────────────────────────────────────────────

    return ExecutionResult(
        campaign_id     = campaign_id,
        status          = "scheduled",
        scheduled_time  = plan.schedule_iso or "2025-03-11T09:00:00-05:00",
        recipient_count = count,
        api_response_ms = elapsed_ms,
        message         = f"Campaign {campaign_id} queued for {count:,} recipients.",
    )


def run_rejection_log(plan: CampaignPlan, reason: str = "Human rejected") -> None:
    """Log a rejected campaign to the audit trail."""
    print(f"[AUDIT] Rejected — Brief: '{plan.brief[:60]}…' | Reason: {reason}")
