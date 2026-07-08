"""
Regulations.gov API v4 client.

Live mode: fetches public comments via api.regulations.gov.
DEMO_MODE: returns seeded data from seed_data.py -- no HTTP calls.

API reference: https://open.fda.gov/apis/... (actually regulations.gov/developer)
Endpoint: GET /v4/comments?filter[docketId]={docket_id}&page[size]=250
Auth: X-Api-Key header
Rate limit: 1,000 requests/hour with free API key.
"""
from __future__ import annotations

import time

import requests

from config import (
    DEMO_MODE,
    DOCKET_META,
    MAX_COMMENTS,
    REGULATIONS_API_KEY,
    REGS_BASE,
    REGS_RATE_LIMIT,
    REGS_TIMEOUT,
)
from models import RawComment

USER_AGENT = "RulemakingCommentAnalyzer/1.0 (portfolio; contact jak.potvin@gmail.com)"


def fetch_comments(
    docket_id: str,
    max_comments: int = MAX_COMMENTS,
    *,
    demo_mode: bool = DEMO_MODE,
) -> list[RawComment]:
    """
    Return up to max_comments raw comments for the given docket_id.
    In DEMO_MODE, returns seeded comments regardless of docket_id.
    """
    if demo_mode:
        from seed_data import DEMO_COMMENTS
        return [_dict_to_raw(d) for d in DEMO_COMMENTS[:max_comments]]
    return _fetch_live(docket_id, max_comments)


def fetch_docket_title(docket_id: str, *, demo_mode: bool = DEMO_MODE) -> str:
    """Return the docket title. Falls back to docket_id if not in DOCKET_META."""
    if docket_id in DOCKET_META:
        return DOCKET_META[docket_id]["title"]
    if demo_mode:
        return docket_id
    return _fetch_live_title(docket_id)


def _dict_to_raw(d: dict) -> RawComment:
    return RawComment(
        comment_id=d["comment_id"],
        docket_id=d["docket_id"],
        submitter_name=d.get("submitter_name", "Anonymous"),
        organization=d.get("organization"),
        comment_text=d.get("comment_text", ""),
        posted_date=d.get("posted_date", ""),
    )


def _fetch_live(docket_id: str, max_comments: int) -> list[RawComment]:
    session = requests.Session()
    session.headers.update({
        "X-Api-Key": REGULATIONS_API_KEY,
        "User-Agent": USER_AGENT,
    })

    comments: list[RawComment] = []
    page = 1
    per_page = min(250, max_comments)

    while len(comments) < max_comments:
        params = {
            "filter[docketId]": docket_id,
            "page[size]": per_page,
            "page[number]": page,
            "sort": "postedDate,DESC",
        }
        try:
            resp = session.get(
                f"{REGS_BASE}/comments",
                params=params,
                timeout=REGS_TIMEOUT,
            )
            resp.raise_for_status()
            data = resp.json()
        except Exception as exc:
            raise RuntimeError(f"Regulations.gov API error: {exc}") from exc

        items = data.get("data", [])
        if not items:
            break

        for item in items:
            attrs = item.get("attributes", {})
            text = (attrs.get("comment") or attrs.get("commentText") or "").strip()
            if not text:
                continue
            comments.append(RawComment(
                comment_id=item.get("id", ""),
                docket_id=docket_id,
                submitter_name=attrs.get("submitterName", "Anonymous"),
                organization=attrs.get("organization") or None,
                comment_text=text,
                posted_date=attrs.get("postedDate", ""),
            ))
            if len(comments) >= max_comments:
                break

        total = data.get("meta", {}).get("totalElements", 0)
        if len(comments) >= total or len(items) < per_page:
            break
        page += 1
        time.sleep(REGS_RATE_LIMIT)

    return comments


def _fetch_live_title(docket_id: str) -> str:
    session = requests.Session()
    session.headers.update({
        "X-Api-Key": REGULATIONS_API_KEY,
        "User-Agent": USER_AGENT,
    })
    try:
        resp = session.get(
            f"{REGS_BASE}/dockets/{docket_id}",
            timeout=REGS_TIMEOUT,
        )
        resp.raise_for_status()
        attrs = resp.json().get("data", {}).get("attributes", {})
        return attrs.get("title", docket_id)
    except Exception:
        return docket_id
