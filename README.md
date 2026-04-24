# 🏢 Talent Groups — Business Pulse Agent

> **[Live Demo →](https://your-username-pulse-agent.streamlit.app)**

An AI agent that synthesizes **Bullhorn ATS** and **Microsoft Dynamics 365 Business Central** data into a single, concise executive briefing for the CIO — surfacing billing gaps, AR anomalies, recruiter performance drops, and aged job orders across both systems.

---

## What It Does

Every morning, the CIO clicks one button and receives:

- **Operational snapshot** — active placements, fill rates, submission pipeline
- **Financial snapshot** — revenue attainment, DSO, AR aging buckets
- **Anomaly detection** — billing gaps (placements with no invoice), overdue AR, stalled job orders
- **Recruiter performance** — week-over-week drops flagged automatically
- **Upcoming risks** — placement end dates with no redeployment plan

---

## Stack

| Layer | Technology |
|-------|-----------|
| AI Engine | Claude API (Anthropic — `claude-opus-4-5`) |
| UI | Streamlit |
| Data | Bullhorn REST API + BC OData v2.0 (mock for demo) |
| Language | Python 3.11+ |

---

## Run Locally

```bash
# 1. Clone
git clone https://github.com/your-username/pulse-agent.git
cd pulse-agent

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set your API key
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# 4. Run
streamlit run app.py
```

---

## Deploy to Streamlit Cloud

1. Push this repo to GitHub (make sure `.env` is in `.gitignore`)
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**
3. Select your repo, branch `main`, file `app.py`
4. Under **Advanced settings → Secrets**, add:
   ```toml
   ANTHROPIC_API_KEY = "sk-ant-..."
   ```
5. Click **Deploy** — live in ~2 minutes

---

## Project Structure

```
pulse-agent/
├── mock_data/
│   ├── bullhorn/           # Placements, job orders, submissions, clients
│   └── business_central/  # Invoices, customers, payments (AR aging)
├── agent/
│   ├── fetcher.py          # Loads + cross-references both data sources
│   └── synthesizer.py      # Claude API call + prompt engineering
├── app.py                  # Streamlit UI
└── requirements.txt
```

---

*Built by Bhanu Prakash Simhadri · Demonstrates AI agent development, data synthesis, and API integration across Bullhorn ATS and Microsoft Dynamics 365 Business Central.*
