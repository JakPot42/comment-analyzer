"""Rich terminal dashboard -- ASCII-safe for Windows cp1252 console."""
from __future__ import annotations

import json

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from config import STANCE_COLORS, STANCES, STAKEHOLDER_TYPES, THEMES
from models import CommentAnalysis, DocketSummary

console = Console()

_BANNER = (
    "[bold cyan]Rulemaking Comment Analyzer[/bold cyan]  [dim]v1.0[/dim]\n"
    "[dim]Ingests Regulations.gov public comments, clusters by theme and stakeholder "
    "type, generates structured decision memos.[/dim]"
)


def _pct(n: int, total: int) -> str:
    if total == 0:
        return " 0%"
    return f"{n/total*100:3.0f}%"


def _bar(n: int, max_n: int, width: int = 15) -> str:
    if max_n == 0:
        return "." * width
    filled = max(0, min(width, int(n / max_n * width)))
    return "#" * filled + "." * (width - filled)


def print_banner() -> None:
    console.print(_BANNER)
    console.print()


def print_summary(summary: DocketSummary) -> None:
    """Print volume and stance/stakeholder breakdown tables."""
    console.rule(f"[bold]{summary.docket_id} -- Comment Analysis[/bold]")
    console.print(f"  [bold]{summary.title}[/bold]")
    console.print(f"  {summary.agency}  |  {summary.fr_citation}  |  {summary.comment_period}")
    console.print(f"  [bold]Total analyzed: {summary.total_analyzed}[/bold]")
    console.print()

    # Stance table
    t = Table(box=box.SIMPLE, show_header=True, header_style="bold", title="Stance Distribution")
    t.add_column("Stance", width=10)
    t.add_column("Count", justify="right", width=7)
    t.add_column("Pct", justify="right", width=5)
    t.add_column("Bar", width=18)
    max_stance = max(summary.stance_totals.values(), default=1)
    for stance in ["MODIFY", "SUPPORT", "OPPOSE", "NEUTRAL"]:
        n = summary.stance_totals.get(stance, 0)
        color = STANCE_COLORS.get(stance, "white")
        t.add_row(
            f"[{color}]{stance}[/{color}]",
            str(n),
            _pct(n, summary.total_analyzed),
            f"[{color}]{_bar(n, max_stance)}[/{color}]",
        )
    console.print(t)

    # Stakeholder table
    t2 = Table(box=box.SIMPLE, show_header=True, header_style="bold", title="Stakeholder Distribution")
    t2.add_column("Stakeholder", width=12)
    t2.add_column("Count", justify="right", width=7)
    t2.add_column("Pct", justify="right", width=5)
    max_stak = max(summary.stakeholder_totals.values(), default=1)
    for stype in STAKEHOLDER_TYPES:
        n = summary.stakeholder_totals.get(stype, 0)
        t2.add_row(stype, str(n), _pct(n, summary.total_analyzed))
    console.print(t2)
    console.print()


def print_themes(summary: DocketSummary) -> None:
    """Print per-theme breakdown with stance and stakeholder mini-tables."""
    console.rule("[bold]Theme Breakdown[/bold]")
    console.print()

    for cluster in summary.theme_clusters:
        color = _dominant_stance_color(cluster.stance_counts)
        console.print(
            f"  [{color}][bold]{cluster.theme_label}[/bold][/{color}]  "
            f"[dim]{cluster.total} comment{'s' if cluster.total != 1 else ''}[/dim]"
        )
        # Stance mini-bar
        parts = []
        for stance, n in sorted(cluster.stance_counts.items(), key=lambda x: -x[1]):
            sc = STANCE_COLORS.get(stance, "white")
            parts.append(f"[{sc}]{stance} {n}[/{sc}]")
        console.print("    Stances:     " + "  ".join(parts))
        # Stakeholder mini-line
        stak_parts = [f"{k}:{v}" for k, v in sorted(cluster.stakeholder_counts.items(), key=lambda x: -x[1])]
        console.print("    Stakeholders: " + "  ".join(stak_parts))
        # Top arguments
        for i, arg in enumerate(cluster.top_arguments[:2], 1):
            console.print(f"    [{i}] [italic]{arg}[/italic]")
        console.print()


def print_comments(
    analyses: list[CommentAnalysis],
    max_show: int = 20,
) -> None:
    """Print a browsable comment list."""
    total = len(analyses)
    show = analyses[:max_show]

    t = Table(box=box.SIMPLE, show_header=True, header_style="bold")
    # overflow="fold": on a narrow console this wide table WRAPS cells instead
    # of truncating with a Unicode ellipsis (U+2026), which would crash a strict
    # OEM console (cp850/cp437). Keeps output pure ASCII at any console width.
    t.add_column("#", width=4, justify="right", overflow="fold")
    t.add_column("Submitter", width=22, overflow="fold")
    t.add_column("Org", width=24, overflow="fold")
    t.add_column("Stance", width=8, overflow="fold")
    t.add_column("Theme", width=22, overflow="fold")
    t.add_column("Key Argument", width=40, overflow="fold")

    for i, a in enumerate(show, 1):
        color = STANCE_COLORS.get(a.stance, "white")
        org = (a.organization or "--")[:24]
        arg = a.key_argument[:40] if a.key_argument else "--"
        t.add_row(
            str(i),
            a.submitter_name[:22],
            org,
            f"[{color}]{a.stance}[/{color}]",
            THEMES.get(a.theme, a.theme),
            arg,
        )

    console.print(t)
    if total > max_show:
        console.print(f"  [dim]Showing {max_show} of {total} comments.[/dim]")
    console.print()


def print_memo(memo_text: str, docket_id: str) -> None:
    console.print(Panel(
        memo_text,
        title=f"[bold]Decision Memorandum -- {docket_id}[/bold]",
        border_style="cyan",
        padding=(1, 2),
    ))
    console.print()


def print_json_export(summary: DocketSummary) -> None:
    data = {
        "docket_id": summary.docket_id,
        "title": summary.title,
        "total_analyzed": summary.total_analyzed,
        "stance_totals": summary.stance_totals,
        "stakeholder_totals": summary.stakeholder_totals,
        "themes": [
            {
                "theme": c.theme,
                "label": c.theme_label,
                "total": c.total,
                "stance_counts": c.stance_counts,
                "stakeholder_counts": c.stakeholder_counts,
                "top_arguments": c.top_arguments,
            }
            for c in summary.theme_clusters
        ],
        "comments": [
            {
                "comment_id": a.comment_id,
                "submitter_name": a.submitter_name,
                "organization": a.organization,
                "theme": a.theme,
                "stakeholder_type": a.stakeholder_type,
                "stance": a.stance,
                "key_argument": a.key_argument,
            }
            for a in summary.analyses
        ],
    }
    console.print(json.dumps(data, indent=2))


def _dominant_stance_color(stance_counts: dict[str, int]) -> str:
    if not stance_counts:
        return "white"
    dominant = max(stance_counts, key=stance_counts.get)
    return STANCE_COLORS.get(dominant, "white")
