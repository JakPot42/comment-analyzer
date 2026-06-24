"""Rulemaking Comment Analyzer CLI."""
from __future__ import annotations

import os
import sys

import click

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import DEMO_MODE, DEMO_DOCKET_ID, STAKEHOLDER_TYPES, STANCES, THEMES
from regulations_client import fetch_comments, fetch_docket_title
from comment_analyzer import analyze_comments
from cluster_engine import build_summary, filter_analyses
from memo_generator import generate_memo
from dashboard import (
    console,
    print_banner,
    print_comments,
    print_memo,
    print_summary,
    print_themes,
    print_json_export,
)

_THEME_CHOICES = sorted(THEMES.keys()) + ["ALL"]
_STAK_CHOICES = sorted(STAKEHOLDER_TYPES.keys()) + ["ALL"]
_STANCE_CHOICES = sorted(STANCES.keys()) + ["ALL"]


@click.group()
def cli() -> None:
    """
    Rulemaking Comment Analyzer: ingests Regulations.gov public comments,
    clusters by theme and stakeholder type, generates structured decision memos.

    \b
    Data source: Regulations.gov API (free API key required for live mode)
    Algorithm  : Claude Haiku classification + deterministic clustering
    Demo docket: DoD-2023-OS-0063 (CMMC 2.0 Proposed Rule)

    \b
    Commands:
      analyze   -- fetch, classify, and summarize a docket
      themes    -- show theme breakdown for a docket
      comments  -- browse comments with optional filters
      memo      -- generate a structured decision memorandum
      export    -- export analysis as JSON
      demo      -- run all demos against seeded data (no API keys needed)

    Set DEMO_MODE=False + provide API keys for live mode.
    """


def _run_docket(docket_id: str, demo_mode: bool) -> tuple:
    """Shared: fetch → analyze → build_summary. Returns (summary, analyses)."""
    comments = fetch_comments(docket_id, demo_mode=demo_mode)
    if not comments:
        console.print(f"[red]No comments found for docket {docket_id}.[/red]")
        raise SystemExit(1)
    analyses = analyze_comments(comments, demo_mode=demo_mode)
    summary = build_summary(docket_id, analyses)
    return summary, analyses


@cli.command()
@click.argument("docket_id", default=DEMO_DOCKET_ID)
def analyze(docket_id: str) -> None:
    """
    Fetch and classify all comments for DOCKET_ID, then show the summary.

    \b
    Example:
      analyze DoD-2023-OS-0063
    """
    print_banner()
    console.print(f"[dim]Fetching comments for {docket_id}...[/dim]")
    summary, _ = _run_docket(docket_id, DEMO_MODE)
    print_summary(summary)
    if DEMO_MODE:
        console.print("[dim]DEMO_MODE=True -- set DEMO_MODE=False for live Regulations.gov data.[/dim]")


@cli.command()
@click.argument("docket_id", default=DEMO_DOCKET_ID)
def themes(docket_id: str) -> None:
    """Show per-theme comment breakdown for DOCKET_ID."""
    print_banner()
    summary, _ = _run_docket(docket_id, DEMO_MODE)
    print_summary(summary)
    print_themes(summary)
    if DEMO_MODE:
        console.print("[dim]DEMO_MODE=True -- set DEMO_MODE=False for live Regulations.gov data.[/dim]")


@cli.command()
@click.argument("docket_id", default=DEMO_DOCKET_ID)
@click.option(
    "--theme", "-t",
    type=click.Choice(_THEME_CHOICES, case_sensitive=False),
    default="ALL",
    help="Filter by theme.",
)
@click.option(
    "--stakeholder", "-s",
    type=click.Choice(_STAK_CHOICES, case_sensitive=False),
    default="ALL",
    help="Filter by stakeholder type.",
)
@click.option(
    "--stance",
    type=click.Choice(_STANCE_CHOICES, case_sensitive=False),
    default="ALL",
    help="Filter by stance.",
)
@click.option("--limit", default=20, show_default=True, help="Max comments to show.")
def comments(
    docket_id: str,
    theme: str,
    stakeholder: str,
    stance: str,
    limit: int,
) -> None:
    """
    Browse comments for DOCKET_ID with optional filters.

    \b
    Examples:
      comments DoD-2023-OS-0063 --theme COST_AND_BURDEN
      comments DoD-2023-OS-0063 --stakeholder INDUSTRY --stance OPPOSE
      comments DoD-2023-OS-0063 --theme ASSESSMENT_METHODOLOGY --limit 10
    """
    print_banner()
    _, analyses = _run_docket(docket_id, DEMO_MODE)

    t = None if theme.upper() == "ALL" else theme.upper()
    s = None if stakeholder.upper() == "ALL" else stakeholder.upper()
    st = None if stance.upper() == "ALL" else stance.upper()

    filtered = filter_analyses(analyses, theme=t, stakeholder_type=s, stance=st)
    if not filtered:
        console.print("[yellow]No comments match the selected filters.[/yellow]")
        return
    console.print(
        f"  [dim]{len(filtered)} comment{'s' if len(filtered) != 1 else ''}"
        + (f" matching filters" if any([t, s, st]) else "")
        + "[/dim]\n"
    )
    print_comments(filtered, max_show=limit)
    if DEMO_MODE:
        console.print("[dim]DEMO_MODE=True -- set DEMO_MODE=False for live data.[/dim]")


@cli.command()
@click.argument("docket_id", default=DEMO_DOCKET_ID)
def memo(docket_id: str) -> None:
    """
    Generate a structured government decision memorandum for DOCKET_ID.

    \b
    Example:
      memo DoD-2023-OS-0063
    """
    print_banner()
    console.print(f"[dim]Analyzing {docket_id} and generating decision memo...[/dim]")
    summary, _ = _run_docket(docket_id, DEMO_MODE)
    text = generate_memo(summary, demo_mode=DEMO_MODE)
    print_memo(text, docket_id)
    if DEMO_MODE:
        console.print("[dim]DEMO_MODE=True -- set DEMO_MODE=False for live data + Claude memo.[/dim]")


@cli.command()
@click.argument("docket_id", default=DEMO_DOCKET_ID)
def export(docket_id: str) -> None:
    """Export comment analysis as JSON."""
    summary, _ = _run_docket(docket_id, DEMO_MODE)
    print_json_export(summary)


@cli.command()
def demo() -> None:
    """
    Run all Rulemaking Comment Analyzer demos against seeded CMMC 2.0 data.
    No API keys required.
    """
    print_banner()
    docket_id = DEMO_DOCKET_ID

    console.rule(f"[bold]Demo 1: Comment Volume Summary — {docket_id}[/bold]")
    summary, analyses = _run_docket(docket_id, demo_mode=True)
    print_summary(summary)

    console.rule("[bold]Demo 2: Theme Breakdown[/bold]")
    print_themes(summary)

    console.rule("[bold]Demo 3: Browse All Comments[/bold]")
    print_comments(analyses)

    console.rule("[bold]Demo 4: Filter — OPPOSE Comments[/bold]")
    oppose = filter_analyses(analyses, stance="OPPOSE")
    print_comments(oppose)

    console.rule("[bold]Demo 5: Filter — ASSESSMENT_METHODOLOGY Theme[/bold]")
    assessment = filter_analyses(analyses, theme="ASSESSMENT_METHODOLOGY")
    print_comments(assessment)

    console.rule("[bold]Demo 6: Filter — INDUSTRY Stakeholder[/bold]")
    industry = filter_analyses(analyses, stakeholder_type="INDUSTRY")
    print_comments(industry)

    console.rule("[bold]Demo 7: Decision Memorandum[/bold]")
    memo_text = generate_memo(summary, demo_mode=True)
    print_memo(memo_text, docket_id)

    console.print(
        "[dim]All demo output uses seeded CMMC 2.0 data. "
        "Set DEMO_MODE=False + provide API keys for live Regulations.gov data.[/dim]"
    )


if __name__ == "__main__":
    cli()
