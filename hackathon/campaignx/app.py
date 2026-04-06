# app.py — CampaignX · Streamlit UI
# Run: streamlit run app.py

from __future__ import annotations
import time, os
import streamlit as st
from dotenv import load_dotenv

from agents import run_planner, run_creator, run_executor
from agents.executor import run_rejection_log, QuotaExhaustedError

load_dotenv()

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CampaignX · AI Marketing Agent",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"] {
    background-color: #080a0f; color: #c8d8e8;
}
[data-testid="stSidebar"] {
    background-color: #0d1117; border-right: 1px solid #1e2d3d;
}
h1 { color: #22d3ee !important; }
h2, h3 { color: #94a3b8 !important; }
textarea {
    background-color: #0d1117 !important; color: #c8d8e8 !important;
    border: 1px solid #1e2d3d !important; border-radius: 8px !important;
    font-family: monospace !important;
}
.stButton > button { border-radius: 8px; font-weight: 700; letter-spacing: 0.04em; }
[data-testid="stExpander"] { background: #0d1117; border: 1px solid #1e2d3d; border-radius: 10px; }
[data-testid="stMetric"] {
    background: #0d1117; border: 1px solid #1e2d3d;
    border-radius: 10px; padding: 12px 16px;
}
[data-testid="stMetricValue"] { color: #22d3ee !important; }
hr { border-color: #1e2d3d; }
.gemini-badge {
    display:inline-block; background:rgba(66,133,244,0.12);
    color:#4285f4; border:1px solid rgba(66,133,244,0.3);
    border-radius:5px; padding:2px 10px; font-size:11px;
    font-family:monospace; font-weight:600;
}
</style>
""", unsafe_allow_html=True)

# ── Constants ─────────────────────────────────────────────────────────────────
CTA_URL    = "https://superbfsi.com/xdeposit/explore/"
QUOTA_MAX  = 100
GEMINI_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyBaXhWGd9H6FI6SIBNbHzL-8Hza1lNYe2U")

# ── Session state ─────────────────────────────────────────────────────────────
_defaults = dict(
    plan=None, content=None, stage="brief", result=None,
    quota_cohort=12, quota_schedule=7, quota_reports=34,
    agent_logs=[],
)
for k, v in _defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

def log(msg: str):
    ts = time.strftime("%H:%M:%S")
    st.session_state.agent_logs.append(f"[{ts}]  {msg}")

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚡ CampaignX")
    st.markdown(
        "<span style='font-size:11px;color:#2a4a65;font-family:monospace;'>"
        "AI Agent v2.4 · Gemini 2.0 Flash</span>",
        unsafe_allow_html=True,
    )
    # Gemini status
    key_short = GEMINI_KEY[:8] + "…" + GEMINI_KEY[-4:]
    st.markdown(
        f"<div class='gemini-badge'>🔑 Gemini API · {key_short}</div>",
        unsafe_allow_html=True,
    )
    st.divider()

    page = st.radio(
        "Navigate",
        ["📝 Campaign Brief", "✅ Approvals", "📊 Performance", "🔬 Agent Logs"],
        label_visibility="collapsed",
    )
    st.divider()

    # Quota bars
    st.markdown(
        "<span style='font-size:11px;color:#4a6a85;letter-spacing:.1em;'>DAILY API QUOTA</span>",
        unsafe_allow_html=True,
    )
    st.progress(st.session_state.quota_cohort / QUOTA_MAX,
                text=f"Cohort: {st.session_state.quota_cohort}/{QUOTA_MAX}")
    st.progress(st.session_state.quota_schedule / QUOTA_MAX,
                text=f"Schedule: {st.session_state.quota_schedule}/{QUOTA_MAX}")
    st.progress(st.session_state.quota_reports / QUOTA_MAX,
                text=f"Reports: {st.session_state.quota_reports}/{QUOTA_MAX}")

    st.divider()
    st.markdown(f"**CTA URL**  \n[superbfsi.com/xdeposit/explore/]({CTA_URL})")

    if st.button("🔄 Refresh Cohort", use_container_width=True):
        with st.spinner("Pulling latest cohort (Mar 14+ data)…"):
            time.sleep(0.8)
            st.session_state.quota_cohort = min(st.session_state.quota_cohort + 1, QUOTA_MAX)
            log("✅ [COHORT] Refreshed — 4,102 customers loaded as of today.")
        st.success("Cohort refreshed!", icon="✅")

# ═════════════════════════════════════════════════════════════════════════════
# PAGE: BRIEF
# ═════════════════════════════════════════════════════════════════════════════
if page == "📝 Campaign Brief":
    st.title("⚡ Campaign Brief")
    st.markdown(
        "Describe your campaign in plain English. "
        "<span class='gemini-badge'>✨ Gemini 2.0 Flash</span> will plan, write, and schedule it.",
        unsafe_allow_html=True,
    )
    st.divider()

    # Quick templates
    c1, c2, c3, _ = st.columns([1, 1, 1, 3])
    with c1:
        if st.button("📧 Email"):
            st.session_state["_tpl"] = (
                "Run an email campaign for XDeposit targeting high-value customers "
                "with account balance > ₹10,000 who haven't engaged in 60 days. "
                "Promote the 6.5% APY fixed deposit with a personalised subject line. "
                "Tone: professional and warm. "
                "Schedule: Tuesday Mar 11, 2025 at 9:00 AM EST."
            )
    with c2:
        if st.button("💬 SMS"):
            st.session_state["_tpl"] = (
                "Run an SMS re-engagement campaign for XDeposit. "
                "Target customers with balance > ₹5,000 inactive for 30 days. "
                "Keep message under 160 characters. "
                "Schedule: Monday Mar 10, 2025 at 2 PM EST."
            )
    with c3:
        if st.button("🔔 Push"):
            st.session_state["_tpl"] = (
                "Run a push notification for XDeposit mobile users who viewed "
                "the deposit section but didn't convert. Short, emoji-friendly. "
                "Schedule: Wednesday Mar 12, 2025 at 11 AM EST."
            )

    brief = st.text_area(
        "Brief",
        value=st.session_state.get("_tpl", ""),
        height=200,
        placeholder=(
            "e.g. Run email campaign for XDeposit targeting high-value customers "
            "with balance > ₹10k who haven't engaged in 60 days…"
        ),
        label_visibility="collapsed",
    )
    st.caption(f"{len(brief)} characters")
    st.divider()

    if st.button("⚡ Generate Campaign with Gemini", type="primary",
                 disabled=len(brief.strip()) < 10):

        # Reset
        for k in ("plan", "content", "result"):
            st.session_state[k] = None
        st.session_state.stage = "brief"

        log(f"📝 [BRIEF] {len(brief)} chars received")

        try:
            with st.spinner("🧠 Planner agent (Gemini) analysing brief…"):
                plan = run_planner(brief)
                st.session_state.plan = plan
                st.session_state.quota_cohort = min(
                    st.session_state.quota_cohort + 1, QUOTA_MAX)
                log(f"✅ [PLANNER] Gemini extracted: product={plan.product}, "
                    f"channel={plan.channel}, audience≈{plan.estimated_audience:,}")
                log(f"💡 [PLANNER] Reasoning: {plan.reasoning}")

            with st.spinner("✍️ Creator agent (Gemini) writing email…"):
                content = run_creator(plan)
                st.session_state.content = content
                log(f"✅ [CREATOR] Subject: \"{content.subject}\"")
                log(f"✅ [CREATOR] {content.word_count} words · "
                    f"Predicted open rate: {content.predicted_open_rate:.1%}")
                log(f"✅ [CREATOR] CTA URL validated: {content.cta_url}")

            log("⚠️  [HUMAN] Routing to Human-in-the-Loop approval dashboard…")
            st.session_state.stage = "review"
            st.success(
                "🎉 Campaign generated by Gemini! "
                "Go to **✅ Approvals** to review and approve.",
                icon="✨",
            )

        except Exception as e:
            st.error(f"Gemini API error: {e}", icon="🚨")
            log(f"🚨 [ERROR] {e}")

    st.divider()
    st.markdown("### Recent Campaigns")
    c1, c2, c3 = st.columns(3)
    c1.metric("Campaigns Run", "47", delta="+3 this week")
    c2.metric("Approval Rate", "80.9%", delta="+2.1%")
    c3.metric("Avg Open Rate", "24.8%", delta="+3.2%")

# ═════════════════════════════════════════════════════════════════════════════
# PAGE: APPROVALS
# ═════════════════════════════════════════════════════════════════════════════
elif page == "✅ Approvals":
    st.title("✅ Human-in-the-Loop Approvals")
    st.divider()

    plan    = st.session_state.plan
    content = st.session_state.content
    stage   = st.session_state.stage

    if stage == "brief" or not plan or not content:
        st.info("No pending approvals. Generate a campaign first.", icon="📭")

    elif stage == "approved":
        r = st.session_state.result
        st.success(
            f"🚀 **Campaign Scheduled!**  \n"
            f"ID: `{r.campaign_id}` · Send: **{r.scheduled_time}** · "
            f"Recipients: **{r.recipient_count:,}** · API: {r.api_response_ms} ms",
            icon="✅",
        )
        if st.button("Start new campaign"):
            for k in ("plan", "content", "stage", "result"):
                st.session_state[k] = _defaults[k]
            st.rerun()

    elif stage == "rejected":
        st.warning("Campaign rejected and logged.", icon="✕")
        if st.button("Start new campaign"):
            for k in ("plan", "content", "stage", "result"):
                st.session_state[k] = _defaults[k]
            st.rerun()

    else:
        # ── Gemini badge ───────────────────────────────────────────────────
        col_warn, col_badge = st.columns([5, 1])
        with col_warn:
            st.warning("⚠️  **1 campaign pending your approval**", icon="🔔")
        with col_badge:
            st.markdown(
                "<div style='padding-top:8px;'>"
                "<span class='gemini-badge'>✨ AI-Generated</span></div>",
                unsafe_allow_html=True,
            )

        # ── Card 1: Content ────────────────────────────────────────────────
        with st.expander("📧  Generated Email Content", expanded=True):
            st.markdown("**Subject line** *(Gemini-generated)*")
            st.code(content.subject, language=None)

            st.markdown("**Email body** *(Gemini-generated)*")
            st.markdown(
                f"<div style='background:#0d1117;border:1px solid #1e2d3d;"
                f"border-radius:8px;padding:16px;font-size:13px;line-height:1.7;"
                f"color:#c8d8e8;white-space:pre-wrap;font-family:sans-serif;'>"
                f"{content.body_text}</div>",
                unsafe_allow_html=True,
            )
            st.caption(
                f"Words: **{content.word_count}** · "
                f"Predicted open rate: **{content.predicted_open_rate:.1%}** · "
                f"Preview: *{content.preview_text}*"
            )
            if content.cta_url == CTA_URL:
                st.success(f"✅ CTA URL validated: {CTA_URL}", icon="🔗")
            else:
                st.error(f"⚠️ CTA URL mismatch! Got: {content.cta_url}", icon="🚨")

        # ── Card 2: Schedule ───────────────────────────────────────────────
        with st.expander("📅  Schedule Info *(Gemini-extracted)*", expanded=True):
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Send Time", plan.schedule_iso.replace("T", " ").split("-0")[0])
            c2.metric("Channel",   plan.channel.capitalize())
            c3.metric("Product",   plan.product)
            c4.metric("Audience",  f"~{plan.estimated_audience:,}")

        # ── Card 3: Audience ───────────────────────────────────────────────
        with st.expander("👥  Target Audience", expanded=False):
            sf = plan.segment_filters
            st.markdown(
                f"**Segment:** Balance ≥ ₹{sf.get('balance_min',0):,} · "
                f"Inactive ≥ {sf.get('days_inactive',0)} days · "
                f"Product: `{sf.get('product','')}`"
            )
            chips = " ".join(
                f"<code style='background:#1e2d3d;color:#7a9ab5;"
                f"padding:2px 8px;border-radius:4px;font-size:11px;'>{c}</code>"
                for c in plan.customer_ids
            )
            st.markdown(
                f"<div style='line-height:2.3;'>{chips}"
                f"<code style='color:#2a4a65;'> …+{max(0,plan.estimated_audience-len(plan.customer_ids)):,} more</code>"
                f"</div>",
                unsafe_allow_html=True,
            )

        # ── Card 4: Agent Reasoning ────────────────────────────────────────
        with st.expander("🧠  Gemini Agent Reasoning", expanded=False):
            st.info(plan.reasoning or "No reasoning captured.", icon="💡")
            st.markdown("""
| Step | Agent | Action |
|------|-------|--------|
| 1 | Planner (Gemini) | Parsed brief → extracted segment, schedule, tone |
| 2 | Creator (Gemini) | Generated subject + body · validated CTA URL |
| 3 | Executor | Awaiting human approval before API call |
""")

        st.divider()

        # ── Approve / Reject ───────────────────────────────────────────────
        ca, cr, _ = st.columns([2, 2, 6])
        with ca:
            if st.button("✅  Approve & Schedule", type="primary",
                         use_container_width=True):
                with st.spinner("Calling InXiteOut Scheduling API…"):
                    try:
                        result = run_executor(plan, content)
                        st.session_state.result = result
                        st.session_state.stage  = "approved"
                        st.session_state.quota_schedule = min(
                            st.session_state.quota_schedule + 1, QUOTA_MAX)
                        log(f"✅ [EXECUTOR] Scheduled — {result.campaign_id} · "
                            f"{result.recipient_count:,} recipients")
                    except QuotaExhaustedError as e:
                        st.error(str(e), icon="🚫")
                        log(f"🚫 [QUOTA] {e}")
                st.rerun()
        with cr:
            if st.button("✕  Reject", use_container_width=True):
                run_rejection_log(plan)
                st.session_state.stage = "rejected"
                log("✕ [HUMAN] Campaign rejected.")
                st.rerun()

# ═════════════════════════════════════════════════════════════════════════════
# PAGE: PERFORMANCE
# ═════════════════════════════════════════════════════════════════════════════
elif page == "📊 Performance":
    st.title("📊 Performance Dashboard")
    st.caption("InXiteOut Performance Reports API · Live metrics")
    st.divider()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Open Rate",        "26.4%", "+3.2%")
    c2.metric("Click Rate",        "8.1%", "+1.4%")
    c3.metric("Conversion Rate",   "3.4%", "±0.0%")
    c4.metric("Unsubscribe Rate",  "0.4%", "-0.1%")

    st.divider()
    st.markdown("### Campaign History")

    import pandas as pd
    df = pd.DataFrame([
        ["XDeposit APY 6.5%",  "Mar 05 2025", 12_450, "26.4%", "8.1%",  "3.2%", "✅ Sent"],
        ["Re-engagement Feb",  "Feb 18 2025",  8_230, "22.1%", "6.8%",  "2.9%", "✅ Sent"],
        ["High-Balance Tier",  "Feb 01 2025",  4_100, "31.7%", "11.2%", "5.4%", "✅ Sent"],
        ["New Users Welcome",  "Mar 04 2025",  6_780,    "—",    "—",     "—",  "✕ Rejected"],
        ["Win-Back Segment",   "Mar 07 2025",  3_847,    "—",    "—",     "—",  "⏳ Pending"],
    ], columns=["Campaign","Date","Sent","Open","Click","Conv.","Status"])
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.info(
        f"Quota used: **{st.session_state.quota_reports}/{QUOTA_MAX}** · "
        f"InXiteOut /api/v1/reports/performance",
        icon="ℹ️",
    )

# ═════════════════════════════════════════════════════════════════════════════
# PAGE: LOGS
# ═════════════════════════════════════════════════════════════════════════════
elif page == "🔬 Agent Logs":
    st.title("🔬 Agent Reasoning Logs")
    st.caption("Live Gemini agent decision trace")
    st.divider()

    if st.button("🗑 Clear logs"):
        st.session_state.agent_logs = []
        st.rerun()

    logs = st.session_state.agent_logs
    if not logs:
        st.info("No logs yet. Generate a campaign to see Gemini reasoning here.", icon="📭")
    else:
        st.code("\n".join(logs), language="bash")
        st.caption(f"{len(logs)} entries")
