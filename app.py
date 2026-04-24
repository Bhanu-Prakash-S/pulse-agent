"""
app.py
------
Talent Groups — Business Pulse Agent
Streamlit UI: Talent Groups branded, button-click briefing generation.
"""

import streamlit as st
from datetime import date
from agent.fetcher import build_context
from agent.synthesizer import generate_briefing

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Talent Groups | Business Pulse",
    page_icon="📋",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Header bar */
    .tg-header {
        background: linear-gradient(90deg, #003366 0%, #0055a5 100%);
        padding: 1.5rem 2rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
    }
    .tg-header h1 {
        color: white;
        font-size: 1.6rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: 0.5px;
    }
    .tg-header p {
        color: #a8c8f0;
        font-size: 0.85rem;
        margin: 0.3rem 0 0 0;
    }
    /* Briefing output */
    .briefing-box {
        background: #f8fafc;
        border-left: 4px solid #0055a5;
        padding: 1.5rem 2rem;
        border-radius: 0 8px 8px 0;
        font-size: 0.95rem;
        line-height: 1.7;
    }
    /* Metric cards */
    .metric-row {
        display: flex;
        gap: 1rem;
        margin-bottom: 1rem;
    }
    /* Footer */
    .tg-footer {
        color: #94a3b8;
        font-size: 0.75rem;
        text-align: center;
        margin-top: 2rem;
        border-top: 1px solid #e2e8f0;
        padding-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────────────
today = date.today().strftime("%A, %B %d, %Y")

st.markdown(f"""
<div class="tg-header">
    <h1>🏢 Talent Groups &nbsp;|&nbsp; Business Pulse Agent</h1>
    <p>Executive Briefing &nbsp;·&nbsp; {today} &nbsp;·&nbsp; Powered by Claude AI (Anthropic)</p>
</div>
""", unsafe_allow_html=True)

# ── Quick stats bar (always visible) ──────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
col1.metric("Active Placements", "147", "+3 vs last wk")
col2.metric("Fill Rate (Wk)", "38%", "-4pts WoW", delta_color="inverse")
col3.metric("Apr Revenue", "$3.47M", "99% of target")
col4.metric("DSO", "52 days", "+7 vs target", delta_color="inverse")

st.divider()

# ── Generate button ────────────────────────────────────────────────────────────
st.markdown("#### Ready to brief your day?")
st.caption("Pulls live data from Bullhorn ATS and Microsoft Dynamics 365 Business Central, "
           "analyzes for anomalies, and generates your executive summary.")

if st.button("▶  Generate Today's Briefing", type="primary", use_container_width=True):
    with st.spinner("🔄  Pulling data from Bullhorn & Business Central..."):
        try:
            context  = build_context()
        except Exception as e:
            st.error(f"❌ Failed to load data: {e}")
            st.stop()

    with st.spinner("🧠  Analyzing with Claude AI..."):
        try:
            briefing = generate_briefing(context)
        except ValueError as e:
            st.error(f"❌ API Key Error: {e}")
            st.stop()
        except Exception as e:
            st.error(f"❌ Claude API error: {e}")
            st.stop()

    st.success("✅ Briefing ready")
    st.divider()

    # Render briefing
    st.markdown(briefing)

    st.divider()

    # Data sources callout
    with st.expander("📂 Data Sources"):
        st.markdown("""
**Bullhorn ATS/CRM**
- Active placements, job orders, submission pipeline
- Recruiter performance, candidate tracking

**Microsoft Dynamics 365 Business Central**
- Invoice status, AR aging, payment collections
- Revenue recognition, gross margin, DSO

> *This demo uses realistic mock data modelled on the Bullhorn REST API and Business Central OData v2.0 API schemas.*
        """)

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="tg-footer">
    Built by <strong>Bhanu Prakash Simhadri</strong> &nbsp;·&nbsp;
    Stack: Python · Claude API (Anthropic) · Streamlit &nbsp;·&nbsp;
    <a href="https://github.com/Bhanu-Prakash-S" target="_blank">GitHub</a>
</div>
""", unsafe_allow_html=True)
