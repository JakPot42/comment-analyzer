"""Tests for comment_analyzer.py — DEMO_MODE routing, validation, batch prompt."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest

from comment_analyzer import (
    analyze_comments,
    _build_batch_prompt,
    _validate,
    _batches,
    _build_analysis,
)
from models import CommentAnalysis, RawComment
from config import THEMES, STAKEHOLDER_TYPES, STANCES


def _make_raw(comment_id="c1", text="Test comment.", org=None) -> RawComment:
    return RawComment(
        comment_id=comment_id,
        docket_id="TEST-DOCKET",
        submitter_name="Test User",
        organization=org,
        comment_text=text,
        posted_date="2024-01-01",
    )


# ---------------------------------------------------------------------------
# analyze_comments — DEMO_MODE
# ---------------------------------------------------------------------------

class TestAnalyzeCommentsDemoMode:
    def test_returns_list_of_comment_analysis(self):
        result = analyze_comments([], demo_mode=True)
        assert isinstance(result, list)
        assert all(isinstance(a, CommentAnalysis) for a in result)

    def test_returns_20_demo_analyses(self):
        result = analyze_comments([], demo_mode=True)
        assert len(result) == 20

    def test_all_themes_valid(self):
        result = analyze_comments([], demo_mode=True)
        for a in result:
            assert a.theme in THEMES, f"Invalid theme: {a.theme}"

    def test_all_stakeholder_types_valid(self):
        result = analyze_comments([], demo_mode=True)
        for a in result:
            assert a.stakeholder_type in STAKEHOLDER_TYPES, f"Invalid type: {a.stakeholder_type}"

    def test_all_stances_valid(self):
        result = analyze_comments([], demo_mode=True)
        for a in result:
            assert a.stance in STANCES, f"Invalid stance: {a.stance}"

    def test_all_analyses_have_comment_ids(self):
        result = analyze_comments([], demo_mode=True)
        for a in result:
            assert a.comment_id, "Empty comment_id"

    def test_all_analyses_have_key_arguments(self):
        result = analyze_comments([], demo_mode=True)
        for a in result:
            assert a.key_argument, f"Empty key_argument for {a.comment_id}"

    def test_all_analyses_have_excerpts(self):
        result = analyze_comments([], demo_mode=True)
        for a in result:
            assert len(a.excerpt) > 0, f"Empty excerpt for {a.comment_id}"

    def test_excerpts_at_most_200_chars(self):
        result = analyze_comments([], demo_mode=True)
        for a in result:
            assert len(a.excerpt) <= 200

    def test_industry_count(self):
        result = analyze_comments([], demo_mode=True)
        industry = [a for a in result if a.stakeholder_type == "INDUSTRY"]
        assert len(industry) == 9

    def test_modify_stance_count(self):
        result = analyze_comments([], demo_mode=True)
        modify = [a for a in result if a.stance == "MODIFY"]
        assert len(modify) == 10

    def test_oppose_stance_count(self):
        result = analyze_comments([], demo_mode=True)
        oppose = [a for a in result if a.stance == "OPPOSE"]
        assert len(oppose) == 3

    def test_assessment_theme_count(self):
        result = analyze_comments([], demo_mode=True)
        assessment = [a for a in result if a.theme == "ASSESSMENT_METHODOLOGY"]
        assert len(assessment) == 5

    def test_no_duplicate_comment_ids(self):
        result = analyze_comments([], demo_mode=True)
        ids = [a.comment_id for a in result]
        assert len(ids) == len(set(ids))

    def test_submitter_names_populated(self):
        result = analyze_comments([], demo_mode=True)
        for a in result:
            assert a.submitter_name, "Empty submitter_name"


# ---------------------------------------------------------------------------
# _validate
# ---------------------------------------------------------------------------

class TestValidate:
    def test_valid_value_passes_through(self):
        assert _validate("SUPPORT", STANCES, "NEUTRAL") == "SUPPORT"

    def test_invalid_value_returns_fallback(self):
        assert _validate("GARBAGE", STANCES, "NEUTRAL") == "NEUTRAL"

    def test_empty_string_returns_fallback(self):
        assert _validate("", THEMES, "OTHER") == "OTHER"

    def test_valid_theme(self):
        assert _validate("COST_AND_BURDEN", THEMES, "OTHER") == "COST_AND_BURDEN"

    def test_invalid_theme(self):
        assert _validate("INVALID_THEME", THEMES, "OTHER") == "OTHER"

    def test_valid_stakeholder(self):
        assert _validate("INDUSTRY", STAKEHOLDER_TYPES, "CITIZEN") == "INDUSTRY"

    def test_case_sensitive(self):
        # lowercase should fail (keys are uppercase)
        assert _validate("industry", STAKEHOLDER_TYPES, "CITIZEN") == "CITIZEN"


# ---------------------------------------------------------------------------
# _batches
# ---------------------------------------------------------------------------

class TestBatches:
    def test_single_batch_when_smaller_than_size(self):
        items = list(range(5))
        batches = list(_batches(items, 10))
        assert len(batches) == 1
        assert batches[0] == items

    def test_exact_fit(self):
        items = list(range(10))
        batches = list(_batches(items, 10))
        assert len(batches) == 1

    def test_multiple_batches(self):
        items = list(range(25))
        batches = list(_batches(items, 10))
        assert len(batches) == 3
        assert len(batches[0]) == 10
        assert len(batches[1]) == 10
        assert len(batches[2]) == 5

    def test_empty_input(self):
        batches = list(_batches([], 10))
        assert batches == []

    def test_batch_size_1(self):
        items = [1, 2, 3]
        batches = list(_batches(items, 1))
        assert len(batches) == 3

    def test_all_items_preserved(self):
        items = list(range(17))
        batches = list(_batches(items, 5))
        flat = [x for b in batches for x in b]
        assert flat == items


# ---------------------------------------------------------------------------
# _build_batch_prompt
# ---------------------------------------------------------------------------

class TestBuildBatchPrompt:
    def test_returns_string(self):
        raw = [_make_raw()]
        prompt = _build_batch_prompt(raw)
        assert isinstance(prompt, str)

    def test_contains_comment_id(self):
        raw = [_make_raw("test-id-123")]
        prompt = _build_batch_prompt(raw)
        assert "test-id-123" in prompt

    def test_contains_all_theme_keys(self):
        raw = [_make_raw()]
        prompt = _build_batch_prompt(raw)
        for theme in THEMES:
            assert theme in prompt

    def test_contains_all_stakeholder_keys(self):
        raw = [_make_raw()]
        prompt = _build_batch_prompt(raw)
        for stype in STAKEHOLDER_TYPES:
            assert stype in prompt

    def test_contains_all_stance_keys(self):
        raw = [_make_raw()]
        prompt = _build_batch_prompt(raw)
        for stance in STANCES:
            assert stance in prompt

    def test_requests_json_array(self):
        raw = [_make_raw()]
        prompt = _build_batch_prompt(raw)
        assert "JSON" in prompt or "json" in prompt.lower()

    def test_text_truncated_to_600_chars(self):
        long_text = "X" * 1000
        raw = [_make_raw(text=long_text)]
        prompt = _build_batch_prompt(raw)
        # The text should appear truncated in the prompt
        assert "X" * 600 in prompt
        assert "X" * 601 not in prompt

    def test_multiple_comments_in_prompt(self):
        raws = [_make_raw(f"c{i}") for i in range(3)]
        prompt = _build_batch_prompt(raws)
        for i in range(3):
            assert f"c{i}" in prompt


# ---------------------------------------------------------------------------
# _build_analysis
# ---------------------------------------------------------------------------

class TestBuildAnalysis:
    def test_builds_comment_analysis(self):
        classified = {
            "comment_id": "c1",
            "theme": "COST_AND_BURDEN",
            "stakeholder_type": "INDUSTRY",
            "stance": "OPPOSE",
            "key_argument": "Too expensive.",
        }
        raw = {
            "comment_id": "c1",
            "submitter_name": "Test",
            "organization": "TestOrg",
            "comment_text": "The proposed rule is too expensive for small businesses.",
        }
        result = _build_analysis(classified, raw)
        assert isinstance(result, CommentAnalysis)
        assert result.theme == "COST_AND_BURDEN"
        assert result.stance == "OPPOSE"
        assert result.stakeholder_type == "INDUSTRY"
        assert result.key_argument == "Too expensive."

    def test_excerpt_truncated(self):
        classified = {"comment_id": "c1", "theme": "OTHER", "stakeholder_type": "CITIZEN", "stance": "NEUTRAL", "key_argument": "X"}
        raw = {"comment_id": "c1", "submitter_name": "T", "organization": None, "comment_text": "A" * 300}
        result = _build_analysis(classified, raw)
        assert len(result.excerpt) <= 200

    def test_invalid_theme_falls_back_to_other(self):
        classified = {"comment_id": "c1", "theme": "INVALID", "stakeholder_type": "CITIZEN", "stance": "NEUTRAL", "key_argument": "x"}
        raw = {"comment_id": "c1", "submitter_name": "T", "organization": None, "comment_text": "text"}
        result = _build_analysis(classified, raw)
        assert result.theme == "OTHER"

    def test_invalid_stance_falls_back(self):
        classified = {"comment_id": "c1", "theme": "OTHER", "stakeholder_type": "CITIZEN", "stance": "MAYBESORTA", "key_argument": "x"}
        raw = {"comment_id": "c1", "submitter_name": "T", "organization": None, "comment_text": "text"}
        result = _build_analysis(classified, raw)
        assert result.stance == "NEUTRAL"

    def test_none_organization_preserved(self):
        classified = {"comment_id": "c1", "theme": "OTHER", "stakeholder_type": "CITIZEN", "stance": "NEUTRAL", "key_argument": "x"}
        raw = {"comment_id": "c1", "submitter_name": "T", "organization": None, "comment_text": "text"}
        result = _build_analysis(classified, raw)
        assert result.organization is None
