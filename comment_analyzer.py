"""
Claude Haiku comment classifier.

Live mode: batches comments and sends them to Claude for classification.
DEMO_MODE: returns pre-classified DEMO_ANALYSES directly.

Each comment is classified into:
  theme, stakeholder_type, stance, key_argument
"""
from __future__ import annotations

import json

from claude_client import call_claude

from config import (
    BATCH_SIZE,
    DEMO_MODE,
    MODEL,
    STANCES,
    STAKEHOLDER_TYPES,
    THEMES,
)
from models import CommentAnalysis, RawComment


def analyze_comments(
    comments: list[RawComment],
    *,
    demo_mode: bool = DEMO_MODE,
) -> list[CommentAnalysis]:
    """
    Classify all comments. Returns one CommentAnalysis per RawComment.
    In DEMO_MODE returns DEMO_ANALYSES keyed by comment_id, supplemented
    with full text from matching RawComments.
    """
    if demo_mode:
        from seed_data import DEMO_ANALYSES, DEMO_COMMENTS
        raw_by_id = {c["comment_id"]: c for c in DEMO_COMMENTS}
        return [
            _build_analysis(a, raw_by_id.get(a["comment_id"], {}))
            for a in DEMO_ANALYSES
        ]

    raw_by_id = {c.comment_id: c for c in comments}
    results: list[CommentAnalysis] = []
    for batch in _batches(comments, BATCH_SIZE):
        results.extend(_analyze_batch(batch, raw_by_id))
    return results


def _analyze_batch(
    batch: list[RawComment],
    raw_by_id: dict[str, RawComment],
) -> list[CommentAnalysis]:
    prompt = _build_batch_prompt(batch)
    raw_json = call_claude(prompt, model=MODEL, max_tokens=2000, on_error="raise")
    try:
        # Strip markdown code fences if present
        if raw_json.startswith("```"):
            raw_json = raw_json.split("```")[1]
            if raw_json.startswith("json"):
                raw_json = raw_json[4:]
        parsed: list[dict] = json.loads(raw_json)
    except Exception as exc:
        raise RuntimeError(f"Claude classification error: {exc}") from exc

    analyses: list[CommentAnalysis] = []
    for item in parsed:
        cid = item.get("comment_id", "")
        raw = raw_by_id.get(cid)
        if raw is None:
            continue
        analyses.append(_build_analysis(item, {
            "comment_id": raw.comment_id,
            "submitter_name": raw.submitter_name,
            "organization": raw.organization,
            "comment_text": raw.comment_text,
        }))
    return analyses


def _build_analysis(classified: dict, raw: dict) -> CommentAnalysis:
    text = raw.get("comment_text", "")
    return CommentAnalysis(
        comment_id=classified.get("comment_id", raw.get("comment_id", "")),
        submitter_name=raw.get("submitter_name", "Anonymous"),
        organization=raw.get("organization"),
        excerpt=text[:200].strip(),
        theme=_validate(classified.get("theme", "OTHER"), THEMES, "OTHER"),
        stakeholder_type=_validate(classified.get("stakeholder_type", "CITIZEN"), STAKEHOLDER_TYPES, "CITIZEN"),
        stance=_validate(classified.get("stance", "NEUTRAL"), STANCES, "NEUTRAL"),
        key_argument=classified.get("key_argument", ""),
    )


def _validate(value: str, valid_set: dict, fallback: str) -> str:
    return value if value in valid_set else fallback


def _batches(items: list, size: int):
    for i in range(0, len(items), size):
        yield items[i:i + size]


def _build_batch_prompt(batch: list[RawComment]) -> str:
    theme_list = ", ".join(THEMES.keys())
    stakeholder_list = ", ".join(STAKEHOLDER_TYPES.keys())
    stance_list = ", ".join(STANCES.keys())

    items = [
        {
            "comment_id": c.comment_id,
            "submitter_name": c.submitter_name,
            "organization": c.organization or "(none)",
            "text": c.comment_text[:600],
        }
        for c in batch
    ]

    return (
        f"Analyze the following {len(batch)} public comments on a proposed federal rule.\n"
        "For each comment return a JSON object with these fields:\n"
        '  "comment_id": the id from the input (copy exactly)\n'
        f'  "stakeholder_type": one of {stakeholder_list}\n'
        "    INDUSTRY = company, trade group, or defense contractor\n"
        "    ADVOCACY = NGO, public interest group, or think tank\n"
        "    ACADEMIC = university or research institution\n"
        "    GOVERNMENT = federal, state, or local agency\n"
        "    CITIZEN = private individual\n"
        f'  "stance": one of {stance_list}\n'
        "    SUPPORT = endorses rule as proposed\n"
        "    OPPOSE = opposes the rule\n"
        "    MODIFY = supports rule but requests specific changes\n"
        "    NEUTRAL = informational, no clear position\n"
        f'  "theme": one of {theme_list}\n'
        "    IMPLEMENTATION_TIMELINE = phase-in schedule concerns\n"
        "    COST_AND_BURDEN = compliance costs, assessment fees\n"
        "    ASSESSMENT_METHODOLOGY = C3PAO process, criteria, consistency\n"
        "    SCOPE_APPLICABILITY = who is covered, boundary definitions\n"
        "    TECHNICAL_REQUIREMENTS = specific control or practice requirements\n"
        "    SMB_IMPACT = small business burden\n"
        "    INTERNATIONAL_SUPPLY_CHAIN = foreign subsidiaries, allied partners\n"
        "    ALTERNATIVE_APPROACHES = different frameworks or approaches proposed\n"
        "    OTHER = does not fit the above\n"
        '  "key_argument": one sentence under 25 words capturing the main point\n\n'
        "Return ONLY a JSON array. No explanation, no markdown.\n\n"
        f"Comments:\n{json.dumps(items, indent=2)}"
    )
