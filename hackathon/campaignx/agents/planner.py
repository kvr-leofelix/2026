# agents/planner.py
"""
Planner Agent — powered by Google Gemini
─────────────────────────────────────────
Stage 1 of the CampaignX pipeline.

Given a raw natural-language campaign brief this agent:
  1. Calls Gemini to extract structured campaign parameters as JSON.
  2. Generates a cohort of matching Customer IDs.
  3. Returns a CampaignPlan ready for the Creator agent.
"""

from __future__ import annotations

import json
import os
import re
import random
from dataclasses import dataclass, field
from typing import Any

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyBaXhWGd9H6FI6SIBNbHzL-8Hza1lNYe2U")
_MODEL   = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
genai.configure(api_key=_API_KEY)

CTA_URL = "https://superbfsi.com/xdeposit/explore/"

# ── Data model ────────────────────────────────────────────────────────────────

@dataclass
class CampaignPlan:
    """Structured output produced by the Planner agent."""
    brief:           str
    product:         str             = "XDeposit"
    channel:         str             = "email"
    offer_headline:  str             = ""
    tone:            str             = "professional"
    schedule_iso:    str             = ""
    segment_filters: dict[str, Any]  = field(default_factory=dict)
    customer_ids:    list[str]       = field(default_factory=list)
    cta_url:         str             = CTA_URL
    reasoning:       str             = ""
    estimated_audience: int          = 0

# ── Prompt ────────────────────────────────────────────────────────────────────

_PLANNER_PROMPT = """You are a senior marketing automation planner at a fintech company.
Analyse the campaign brief below and return ONLY a valid JSON object with no markdown fences.

Brief:
{brief}

Return exactly this JSON (fill every field with real values derived from the brief):
{{
  "product": "product name (default XDeposit)",
  "channel": "email or sms or push",
  "offer_headline": "one-line compelling offer summary",
  "tone": "describe the tone e.g. professional and warm",
  "schedule_iso": "ISO-8601 datetime e.g. 2025-03-11T09:00:00-05:00",
  "segment_filters": {{
    "balance_min": 10000,
    "days_inactive": 60,
    "product": "xdeposit"
  }},
  "estimated_audience_size": 3847,
  "reasoning": "2-3 sentences explaining your segment and timing choices"
}}"""

# ── Helpers ───────────────────────────────────────────────────────────────────

def _generate_customer_ids(n: int = 20) -> list[str]:
    base = random.randint(10000, 19000)
    step = random.randint(40, 180)
    return [f"CID-{base + i * step}" for i in range(n)]

def _parse_json(text: str) -> dict:
    text = re.sub(r"```(?:json)?", "", text).strip().rstrip("`")
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return json.loads(match.group())
    raise ValueError(f"No JSON in response: {text[:200]}")

# ── Main ──────────────────────────────────────────────────────────────────────

def run_planner(brief: str) -> CampaignPlan:
    """Call Gemini to parse the brief and return a structured CampaignPlan."""
    model  = genai.GenerativeModel(_MODEL)
    prompt = _PLANNER_PROMPT.format(brief=brief)

    response = model.generate_content(
        prompt,
        generation_config=genai.GenerationConfig(temperature=0.2, max_output_tokens=600),
    )

    data     = _parse_json(response.text)
    est_size = int(data.get("estimated_audience_size", 20))
    visible  = _generate_customer_ids(min(est_size, 25))

    return CampaignPlan(
        brief              = brief,
        product            = data.get("product", "XDeposit"),
        channel            = data.get("channel", "email"),
        offer_headline     = data.get("offer_headline", ""),
        tone               = data.get("tone", "professional"),
        schedule_iso       = data.get("schedule_iso", "2025-03-11T09:00:00-05:00"),
        segment_filters    = data.get("segment_filters", {}),
        customer_ids       = visible,
        cta_url            = CTA_URL,
        reasoning          = data.get("reasoning", ""),
        estimated_audience = est_size,
    )
