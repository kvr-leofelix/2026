# agents/creator.py
"""
Creator Agent — powered by Google Gemini
─────────────────────────────────────────
Stage 2 of the CampaignX pipeline.

Given a CampaignPlan this agent:
  1. Calls Gemini to generate the email subject line and body.
  2. Hard-validates the CTA URL before returning.
  3. Returns a CampaignContent for human-in-the-loop review.
"""

from __future__ import annotations

import os
import re
import json
from dataclasses import dataclass

import google.generativeai as genai
from dotenv import load_dotenv

from .planner import CampaignPlan

load_dotenv()

_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyBaXhWGd9H6FI6SIBNbHzL-8Hza1lNYe2U")
_MODEL   = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
genai.configure(api_key=_API_KEY)

CTA_URL = "https://superbfsi.com/xdeposit/explore/"

# ── Data model ────────────────────────────────────────────────────────────────

@dataclass
class CampaignContent:
    """Email content produced by the Creator agent."""
    subject:              str
    body_text:            str
    body_html:            str
    cta_url:              str
    preview_text:         str
    word_count:           int   = 0
    predicted_open_rate:  float = 0.0

# ── Prompts ───────────────────────────────────────────────────────────────────

_CREATOR_PROMPT = """You are an expert email copywriter for a fintech company called SuperbFSI.
Write a marketing email for the following campaign plan. Return ONLY valid JSON with no markdown.

Campaign details:
- Product: {product}
- Offer: {offer_headline}
- Tone: {tone}
- Channel: {channel}
- Target: customers inactive {days_inactive}+ days with balance >= {balance_min}
- CTA URL (use EXACTLY this): {cta_url}

Return this exact JSON:
{{
  "subject": "compelling subject line with relevant emoji",
  "preview_text": "inbox preview snippet under 90 chars",
  "body_text": "full plain-text email body (150-200 words). Use [First Name] as placeholder. Include the CTA URL exactly as {cta_url}",
  "predicted_open_rate": 0.27
}}"""

# ── Helpers ───────────────────────────────────────────────────────────────────

def _parse_json(text: str) -> dict:
    text = re.sub(r"```(?:json)?", "", text).strip().rstrip("`")
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return json.loads(match.group())
    raise ValueError(f"No JSON in creator response: {text[:200]}")

def _build_html(subject: str, body_text: str, cta_url: str) -> str:
    """Convert plain-text body to a simple but clean HTML email."""
    paragraphs = "".join(
        f"<p style='margin:0 0 14px;line-height:1.7;'>{line}</p>"
        for line in body_text.split("\n")
        if line.strip() and cta_url not in line
    )
    return f"""<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="font-family:Arial,sans-serif;color:#333;max-width:600px;margin:0 auto;padding:24px;">
  <div style="background:#0891b2;padding:20px 24px;border-radius:8px 8px 0 0;">
    <h1 style="color:#fff;font-size:20px;margin:0;">{subject}</h1>
  </div>
  <div style="border:1px solid #e5e7eb;border-top:none;padding:24px;border-radius:0 0 8px 8px;">
    {paragraphs}
    <div style="text-align:center;margin:28px 0 16px;">
      <a href="{cta_url}"
         style="background:#0891b2;color:#fff;padding:14px 32px;text-decoration:none;
                border-radius:6px;font-weight:bold;font-size:15px;display:inline-block;">
        Explore XDeposit Now →
      </a>
    </div>
    <p style="font-size:11px;color:#9ca3af;text-align:center;margin-top:24px;">
      SuperbFSI · <a href="{cta_url}" style="color:#9ca3af;">{cta_url}</a><br>
      T&amp;Cs apply. You are receiving this as a registered SuperbFSI customer.
    </p>
  </div>
</body>
</html>"""

# ── Main ──────────────────────────────────────────────────────────────────────

def run_creator(plan: CampaignPlan) -> CampaignContent:
    """Call Gemini to generate personalised email content from a CampaignPlan."""
    model  = genai.GenerativeModel(_MODEL)
    prompt = _CREATOR_PROMPT.format(
        product        = plan.product,
        offer_headline = plan.offer_headline,
        tone           = plan.tone,
        channel        = plan.channel,
        days_inactive  = plan.segment_filters.get("days_inactive", 60),
        balance_min    = plan.segment_filters.get("balance_min", 10000),
        cta_url        = CTA_URL,
    )

    response = model.generate_content(
        prompt,
        generation_config=genai.GenerationConfig(temperature=0.7, max_output_tokens=900),
    )

    data        = _parse_json(response.text)
    subject     = data.get("subject", "Your exclusive offer is waiting 🎯")
    body_text   = data.get("body_text", "")
    preview     = data.get("preview_text", "")
    open_rate   = float(data.get("predicted_open_rate", 0.25))

    # Hard-validate CTA URL — replace any hallucinated URL with the real one
    body_text = re.sub(r"https?://\S+xdeposit\S*", CTA_URL, body_text)

    return CampaignContent(
        subject             = subject,
        body_text           = body_text,
        body_html           = _build_html(subject, body_text, CTA_URL),
        cta_url             = CTA_URL,
        preview_text        = preview,
        word_count          = len(body_text.split()),
        predicted_open_rate = open_rate,
    )
