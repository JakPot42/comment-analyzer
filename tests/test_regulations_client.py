"""Tests for regulations_client.py — DEMO_MODE routing and structure."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest

from regulations_client import fetch_comments, fetch_docket_title
from models import RawComment
from config import DEMO_DOCKET_ID, MAX_COMMENTS


class TestFetchCommentsDemoMode:
    def test_returns_list(self):
        result = fetch_comments(DEMO_DOCKET_ID, demo_mode=True)
        assert isinstance(result, list)

    def test_returns_raw_comment_instances(self):
        result = fetch_comments(DEMO_DOCKET_ID, demo_mode=True)
        assert all(isinstance(c, RawComment) for c in result)

    def test_returns_20_demo_comments(self):
        result = fetch_comments(DEMO_DOCKET_ID, demo_mode=True)
        assert len(result) == 20

    def test_max_comments_respected(self):
        result = fetch_comments(DEMO_DOCKET_ID, max_comments=5, demo_mode=True)
        assert len(result) == 5

    def test_comment_ids_populated(self):
        result = fetch_comments(DEMO_DOCKET_ID, demo_mode=True)
        for c in result:
            assert c.comment_id, "Empty comment_id"

    def test_docket_ids_match_requested(self):
        result = fetch_comments(DEMO_DOCKET_ID, demo_mode=True)
        for c in result:
            assert c.docket_id == DEMO_DOCKET_ID

    def test_comment_texts_nonempty(self):
        result = fetch_comments(DEMO_DOCKET_ID, demo_mode=True)
        for c in result:
            assert len(c.comment_text) > 0

    def test_submitter_names_nonempty(self):
        result = fetch_comments(DEMO_DOCKET_ID, demo_mode=True)
        for c in result:
            assert c.submitter_name, "Empty submitter_name"

    def test_posted_dates_nonempty(self):
        result = fetch_comments(DEMO_DOCKET_ID, demo_mode=True)
        for c in result:
            assert c.posted_date, "Empty posted_date"

    def test_some_comments_have_organizations(self):
        result = fetch_comments(DEMO_DOCKET_ID, demo_mode=True)
        with_org = [c for c in result if c.organization is not None]
        assert len(with_org) > 0

    def test_some_comments_have_no_organization(self):
        result = fetch_comments(DEMO_DOCKET_ID, demo_mode=True)
        without_org = [c for c in result if c.organization is None]
        assert len(without_org) > 0

    def test_max_1_returns_1(self):
        result = fetch_comments(DEMO_DOCKET_ID, max_comments=1, demo_mode=True)
        assert len(result) == 1

    def test_no_duplicate_comment_ids(self):
        result = fetch_comments(DEMO_DOCKET_ID, demo_mode=True)
        ids = [c.comment_id for c in result]
        assert len(ids) == len(set(ids))

    def test_comment_texts_longer_than_20_chars(self):
        result = fetch_comments(DEMO_DOCKET_ID, demo_mode=True)
        for c in result:
            assert len(c.comment_text) > 20, f"Comment {c.comment_id} text too short"

    def test_dates_in_iso_format(self):
        result = fetch_comments(DEMO_DOCKET_ID, demo_mode=True)
        for c in result:
            # Should be YYYY-MM-DD
            assert len(c.posted_date) == 10
            assert c.posted_date[4] == "-"
            assert c.posted_date[7] == "-"

    def test_unknown_docket_still_returns_demo_data(self):
        # DEMO_MODE ignores docket_id and returns seeded data regardless
        result = fetch_comments("UNKNOWN-DOCKET", demo_mode=True)
        assert len(result) == 20


class TestFetchDocketTitle:
    def test_known_docket_returns_title(self):
        title = fetch_docket_title(DEMO_DOCKET_ID, demo_mode=True)
        assert "CMMC" in title or "Cybersecurity" in title

    def test_unknown_docket_returns_docket_id(self):
        title = fetch_docket_title("UNKNOWN-999", demo_mode=True)
        assert title == "UNKNOWN-999"

    def test_returns_string(self):
        title = fetch_docket_title(DEMO_DOCKET_ID, demo_mode=True)
        assert isinstance(title, str)
