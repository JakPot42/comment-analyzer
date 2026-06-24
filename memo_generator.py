"""
Claude Haiku decision memo generator.

Live mode: generates a structured government decision memorandum from the
DocketSummary. DEMO_MODE: returns pre-baked DEMO_MEMO.
"""
from __future__ import annotations

from datetime import date

import anthropic

from config import ANTHROPIC_API_KEY, DEMO_MODE, MODEL, THEMES
from models import DocketSummary


def generate_memo(
    summary: DocketSummary,
    *,
    demo_mode: bool = DEMO_MODE,
) -> str:
    """Generate a decision memorandum from the docket analysis summary."""
    if demo_mode:
        from seed_data import DEMO_MEMO
        return DEMO_MEMO

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    try:
        msg = client.messages.create(
            model=MODEL,
            max_tokens=1500,
            messages=[{"role": "user", "content": _build_memo_prompt(summary)}],
        )
        return msg.content[0].text.strip()
    except Exception as exc:
        raise RuntimeError(f"Claude memo generation error: {exc}") from exc


def _build_memo_prompt(summary: DocketSummary) -> str:
    today = date.today().isoformat()

    # Build theme summary lines
    theme_lines = "\n".join(
        f"  {c.theme_label}: {c.total} comments — "
        f"stances: {c.stance_counts} — "
        f"stakeholders: {c.stakeholder_counts}"
        for c in summary.theme_clusters
    )

    # Top arguments from all themes
    all_args = []
    for c in summary.theme_clusters[:4]:  # top 4 themes
        for arg in c.top_arguments[:2]:
            all_args.append(f"  [{c.theme}] {arg}")
    args_block = "\n".join(all_args)

    return (
        "Write a formal government decision memorandum analyzing public comments on a "
        "proposed federal rule. Use exactly this 5-section structure:\n\n"
        "DECISION MEMORANDUM\n"
        "TO: [Agency Head]\n"
        "FROM: Office of Regulatory Analysis\n"
        f"RE: Public Comment Analysis — {summary.title}\n"
        f"    Docket {summary.docket_id}"
        + (f"  |  {summary.fr_citation}" if summary.fr_citation else "")
        + "\n"
        f"DATE: {today}\n\n"
        "I. EXECUTIVE SUMMARY (2-3 sentences)\n"
        "II. COMMENT VOLUME AND DISTRIBUTION (reference actual numbers)\n"
        "III. KEY THEMES BY STAKEHOLDER TYPE\n"
        "IV. AREAS OF CONSENSUS AND CONTENTION\n"
        "V. RECOMMENDED AGENCY CONSIDERATIONS (3-5 numbered items)\n\n"
        "Use formal government prose. Be specific — reference actual numbers and "
        "commenter names/organizations where available. Do not hedge.\n\n"
        f"DOCKET: {summary.docket_id}\n"
        f"TITLE: {summary.title}\n"
        f"AGENCY: {summary.agency}\n"
        f"TOTAL COMMENTS ANALYZED: {summary.total_analyzed}\n\n"
        f"STANCE BREAKDOWN: {summary.stance_totals}\n"
        f"STAKEHOLDER BREAKDOWN: {summary.stakeholder_totals}\n\n"
        f"THEME BREAKDOWN:\n{theme_lines}\n\n"
        f"REPRESENTATIVE ARGUMENTS:\n{args_block}\n"
    )
