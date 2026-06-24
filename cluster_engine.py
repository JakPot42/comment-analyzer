"""
Deterministic clustering engine — aggregates CommentAnalysis objects into
ThemeCluster and DocketSummary. No Claude involvement.
"""
from __future__ import annotations

from collections import Counter, defaultdict

from config import DOCKET_META, DEMO_DOCKET_ID, STAKEHOLDER_TYPES, STANCES, THEMES
from models import CommentAnalysis, DocketSummary, ThemeCluster


def build_summary(
    docket_id: str,
    analyses: list[CommentAnalysis],
) -> DocketSummary:
    """Build a full DocketSummary from classified analyses."""
    meta = DOCKET_META.get(docket_id, {
        "title": docket_id,
        "agency": "Unknown Agency",
        "fr_citation": "",
        "comment_period": "",
        "rule_type": "Rule",
    })

    stance_totals = Counter(a.stance for a in analyses)
    stakeholder_totals = Counter(a.stakeholder_type for a in analyses)

    # Group analyses by theme
    by_theme: dict[str, list[CommentAnalysis]] = defaultdict(list)
    for a in analyses:
        by_theme[a.theme].append(a)

    clusters: list[ThemeCluster] = []
    for theme, members in by_theme.items():
        stance_counts = Counter(a.stance for a in members)
        stakeholder_counts = Counter(a.stakeholder_type for a in members)
        # Top 3 representative arguments (prefer non-NEUTRAL, then by order)
        ordered = sorted(members, key=lambda a: (a.stance == "NEUTRAL", ""))
        top_args = [a.key_argument for a in ordered[:3] if a.key_argument]
        clusters.append(ThemeCluster(
            theme=theme,
            theme_label=THEMES.get(theme, theme),
            total=len(members),
            stance_counts=dict(stance_counts),
            stakeholder_counts=dict(stakeholder_counts),
            top_arguments=top_args,
        ))

    # Sort clusters by total desc
    clusters.sort(key=lambda c: c.total, reverse=True)

    return DocketSummary(
        docket_id=docket_id,
        title=meta["title"],
        agency=meta["agency"],
        fr_citation=meta.get("fr_citation", ""),
        comment_period=meta.get("comment_period", ""),
        total_analyzed=len(analyses),
        stance_totals=dict(stance_totals),
        stakeholder_totals=dict(stakeholder_totals),
        theme_clusters=clusters,
        analyses=analyses,
    )


def filter_analyses(
    analyses: list[CommentAnalysis],
    theme: str | None = None,
    stakeholder_type: str | None = None,
    stance: str | None = None,
) -> list[CommentAnalysis]:
    """Return analyses matching optional filters."""
    result = analyses
    if theme:
        result = [a for a in result if a.theme == theme.upper()]
    if stakeholder_type:
        result = [a for a in result if a.stakeholder_type == stakeholder_type.upper()]
    if stance:
        result = [a for a in result if a.stance == stance.upper()]
    return result
