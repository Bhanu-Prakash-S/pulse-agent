"""
synthesizer.py
--------------
Sends the unified context dict to Claude and returns
a concise, markdown-formatted executive briefing.
"""

import os
import json
import anthropic
from dotenv import load_dotenv

load_dotenv()


def _build_prompt(ctx: dict) -> str:
    # Format flagged invoices
    invoice_lines = "\n".join(
        f"  - {inv['invoiceId']} | {inv['customerName']} | ${inv['amount']:,} | "
        f"{inv['daysOverdue']} days overdue | Action: {inv['action']}"
        for inv in ctx["flaggedInvoices"]
    )

    # Format billing gaps
    gap_lines = "\n".join(
        f"  - Placement {g['placementId']} ({g['candidateName']} @ {g['clientName']}) "
        f"— estimated unbilled: ${g['estimatedUnbilled']:,}"
        for g in ctx["billingGaps"]
    )

    # Format flagged recruiters
    recruiter_lines = "\n".join(
        f"  - {r['recruiter']}: {r['week2Placements']} placements this week "
        f"(was {r['week1Placements']} last week) — {r['flag']}. {r['note']}"
        for r in ctx["flaggedRecruiters"]
    )

    # Format aged job orders
    aged_critical_lines = "\n".join(
        f"  - {j['id']} | {j['clientName']} | {j['role']} | "
        f"{j['daysOpen']} days open | {j['submissions']} submissions"
        for j in ctx["agedCriticalOrders"]
    )
    stalled_lines = "\n".join(
        f"  - {j['id']} | {j['clientName']} | {j['role']} | "
        f"{j['daysOpen']} days open | 0 submissions"
        for j in ctx["stalledOrders"]
    )

    # Format upcoming placement ends
    end_lines = "\n".join(
        f"  - {u['candidateName']} @ {u['clientName']} — ends {u['endDate']} "
        f"({u['daysRemaining']} days) | {u['redeploymentStatus']}"
        for u in ctx["upcomingEnds"]
    )

    prompt = f"""You are an AI executive briefing assistant for Talent Groups, a staffing firm.
Your job is to synthesize operational and financial data into a sharp, concise morning briefing for the CIO.

TODAY'S DATE: Thursday, April 24, 2026

RULES:
- Lead with what needs the CIO's attention TODAY (critical first)
- Use bullet points — no paragraphs
- Flag severity: 🔴 critical action needed | ⚠️ watch closely | ✅ on track
- Be specific with numbers — never vague
- Max ~400 words. Every line must earn its place.
- Format in clean markdown with section headers using bold text
- End with a "Bottom Line" — one sentence on what the CIO's focus should be today

---

BULLHORN ATS DATA:

Active Placements on Billing: {ctx['activePlacements']} contracts
Billable Hours This Week: {ctx['weeklyBillableHours']:,} hrs
Avg Bill Rate: ${ctx['avgBillRate']}/hr | Avg Margin: {ctx['avgMarginPct']}%
Projected Weekly Revenue: ${ctx['projectedWeeklyRevenue']:,}

Submissions This Week (Apr 17–24):
  - Submissions: {ctx['week2']['submissions']} (was {ctx['week1']['submissions']} last week, {round((ctx['week2']['submissions']-ctx['week1']['submissions'])/ctx['week1']['submissions']*100,1)}% WoW)
  - Interviews: {ctx['week2']['interviews']} (was {ctx['week1']['interviews']})
  - Offers: {ctx['week2']['offers']} (was {ctx['week1']['offers']})
  - Placements: {ctx['week2']['placements']} (was {ctx['week1']['placements']})
  - Fill Rate: {ctx['week2']['fillRate']}% (was {ctx['week1']['fillRate']}% last week)
  - Avg Time-to-Fill: {ctx['week2']['timeToFill']} days (was {ctx['week1']['timeToFill']} days)
  - Overall trend: {ctx['wowTrend']}

Open Job Orders: {ctx['totalOpenJobOrders']} total

Aged Critical Orders (100+ days, escalate):
{aged_critical_lines if aged_critical_lines else '  None'}

Stalled Orders (open 7+ days, 0 submissions):
{stalled_lines if stalled_lines else '  None'}

Flagged Recruiters:
{recruiter_lines if recruiter_lines else '  None'}

Dallas Team Fill Rate: {ctx['dallasTeamFillRateWk1']}% last week → {ctx['dallasTeamFillRateWk2']}% this week ({ctx['dallasWoWChange']}% WoW)

Upcoming Placement Ends (next 14 days):
{end_lines if end_lines else '  None'}

---

BUSINESS CENTRAL DATA:

April Revenue: ${ctx['monthlyRevenue']:,} vs ${ctx['monthlyTarget']:,} target ({ctx['monthlyAttainmentPct']}% attainment)
Weekly Run Rate: ${ctx['weeklyRunRate']:,} vs ${ctx['weeklyRunRateTarget']:,} target
Gross Margin: {ctx['grossMarginPct']}% (target: {ctx['grossMarginTarget']}%)
DSO: {ctx['dsoDays']} days (target: <{ctx['dsoTarget']} days)

AR Aging:
  - Total Outstanding: ${ctx['totalAR']:,}
  - 61–90 days overdue: ${ctx['ar_61_90']:,}
  - 90+ days overdue: ${ctx['ar_90plus']:,}

Flagged Invoices (require action):
{invoice_lines if invoice_lines else '  None'}

Billing Gap (Bullhorn placements with NO invoice in Business Central):
{gap_lines if gap_lines else '  None'}
  Total estimated unbilled: ${ctx['totalUnbilledEstimate']:,}

---

Now generate the executive briefing. Be sharp, decisive, and specific. The CIO reads this before their first meeting.
"""
    return prompt


def generate_briefing(context: dict) -> str:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not set. Add it to your .env file.")

    client = anthropic.Anthropic(api_key=api_key)
    prompt = _build_prompt(context)

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text
