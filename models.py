"""Data models for the Rulemaking Comment Analyzer."""
from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class RawComment:
    comment_id: str
    docket_id: str
    submitter_name: str
    organization: str | None
    comment_text: str
    posted_date: str


@dataclass
class CommentAnalysis:
    comment_id: str
    submitter_name: str
    organization: str | None
    excerpt: str              # first 200 chars of comment text
    theme: str                # key from THEMES
    stakeholder_type: str     # key from STAKEHOLDER_TYPES
    stance: str               # key from STANCES
    key_argument: str         # one-sentence summary


@dataclass
class ThemeCluster:
    theme: str
    theme_label: str
    total: int
    stance_counts: dict[str, int]
    stakeholder_counts: dict[str, int]
    top_arguments: list[str]  # up to 3 representative key_arguments


@dataclass
class DocketSummary:
    docket_id: str
    title: str
    agency: str
    fr_citation: str
    comment_period: str
    total_analyzed: int
    stance_totals: dict[str, int]
    stakeholder_totals: dict[str, int]
    theme_clusters: list[ThemeCluster]  # sorted by total desc
    analyses: list[CommentAnalysis]
