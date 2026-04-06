# ⚡ CampaignX — AI Marketing Agent

A Streamlit-based multi-agent marketing automation system built for hackathons.

## Project Structure

```
campaignx/
├── app.py                  # Streamlit UI — main entry point
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variable template
└── agents/
    ├── __init__.py         # Package exports
    ├── planner.py          # Planner agent — parses brief, fetches cohort
    ├── creator.py          # Creator agent — generates email content
    └── executor.py         # Executor agent — calls scheduling API
```

## Quick Start

```bash
# 1. Clone / unzip the project
cd campaignx

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env and add your API keys

# 5. Run the app
streamlit run app.py
```

## Agent Pipeline

```
Brief (natural language)
        │
        ▼
  ┌───────────┐    GET /cohort/query
  │  Planner  │ ──────────────────────► InXiteOut API
  └───────────┘
        │  CampaignPlan
        ▼
  ┌───────────┐
  │  Creator  │  Generates subject + body via LLM
  └───────────┘
        │  CampaignContent
        ▼
  Human-in-the-Loop ✅ / ✕
        │  (if approved)
        ▼
  ┌───────────┐   POST /campaign/schedule
  │ Executor  │ ──────────────────────► InXiteOut API
  └───────────┘
```

## API Quota

Each InXiteOut endpoint has a **100 calls/day** limit, tracked live in the sidebar.

| Endpoint               | Path                        |
|------------------------|-----------------------------|
| Customer Cohort        | `/api/v1/cohort/query`      |
| Campaign Scheduling    | `/api/v1/campaign/schedule` |
| Performance Reports    | `/api/v1/reports/performance` |

## CTA URL

All campaigns hardcode the call-to-action URL to:
```
https://superbfsi.com/xdeposit/explore/
```

## Replacing Mock Agents with Real LLM Calls

Each agent file contains a clearly marked `TODO` block showing exactly which
LangChain components to swap in. Search for `# TODO` in any `agents/*.py` file.
