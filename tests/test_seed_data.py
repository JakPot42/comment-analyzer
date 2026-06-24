"""Tests for seed_data.py — structure, coverage, plausibility."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest

from seed_data import DEMO_COMMENTS, DEMO_ANALYSES, DEMO_MEMO
from config import THEMES, STAKEHOLDER_TYPES, STANCES, DEMO_DOCKET_ID


# ---------------------------------------------------------------------------
# DEMO_COMMENTS
# ---------------------------------------------------------------------------

class TestDemoComments:
    def test_twenty_comments(self):
        assert len(DEMO_COMMENTS) == 20

    def test_all_have_required_fields(self):
        required = {"comment_id", "docket_id", "submitter_name", "comment_text", "posted_date"}
        for comment in DEMO_COMMENTS:
            for field in required:
                assert field in comment, f"Missing field {field}"

    def test_docket_id_matches_demo_docket(self):
        for comment in DEMO_COMMENTS:
            assert comment["docket_id"] == DEMO_DOCKET_ID

    def test_no_duplicate_comment_ids(self):
        ids = [c["comment_id"] for c in DEMO_COMMENTS]
        assert len(ids) == len(set(ids))

    def test_comment_texts_are_nonempty(self):
        for c in DEMO_COMMENTS:
            assert len(c["comment_text"]) > 20

    def test_submitter_names_nonempty(self):
        for c in DEMO_COMMENTS:
            assert c["submitter_name"]

    def test_some_have_organizations(self):
        with_org = [c for c in DEMO_COMMENTS if c.get("organization")]
        assert len(with_org) > 5

    def test_some_have_no_organization(self):
        without = [c for c in DEMO_COMMENTS if not c.get("organization")]
        assert len(without) >= 3

    def test_posted_dates_are_valid(self):
        for c in DEMO_COMMENTS:
            d = c["posted_date"]
            assert len(d) == 10
            assert d[4] == "-"
            assert d[7] == "-"
            year, month, day = int(d[:4]), int(d[5:7]), int(d[8:10])
            assert 2020 <= year <= 2030
            assert 1 <= month <= 12
            assert 1 <= day <= 31

    def test_comment_ids_start_with_docket_id(self):
        for c in DEMO_COMMENTS:
            assert c["comment_id"].startswith(DEMO_DOCKET_ID)

    def test_all_comments_are_dicts(self):
        for c in DEMO_COMMENTS:
            assert isinstance(c, dict)


# ---------------------------------------------------------------------------
# DEMO_ANALYSES
# ---------------------------------------------------------------------------

class TestDemoAnalyses:
    def test_twenty_analyses(self):
        assert len(DEMO_ANALYSES) == 20

    def test_all_comment_ids_match_demo_comments(self):
        comment_ids = {c["comment_id"] for c in DEMO_COMMENTS}
        for a in DEMO_ANALYSES:
            assert a["comment_id"] in comment_ids

    def test_no_duplicate_comment_ids(self):
        ids = [a["comment_id"] for a in DEMO_ANALYSES]
        assert len(ids) == len(set(ids))

    def test_all_themes_valid(self):
        for a in DEMO_ANALYSES:
            assert a["theme"] in THEMES, f"Invalid theme: {a['theme']} in {a['comment_id']}"

    def test_all_stakeholder_types_valid(self):
        for a in DEMO_ANALYSES:
            assert a["stakeholder_type"] in STAKEHOLDER_TYPES

    def test_all_stances_valid(self):
        for a in DEMO_ANALYSES:
            assert a["stance"] in STANCES

    def test_all_have_key_arguments(self):
        for a in DEMO_ANALYSES:
            assert a.get("key_argument"), f"Empty key_argument in {a['comment_id']}"

    def test_correct_stance_counts(self):
        from collections import Counter
        counts = Counter(a["stance"] for a in DEMO_ANALYSES)
        assert counts["MODIFY"] == 10
        assert counts["SUPPORT"] == 6
        assert counts["OPPOSE"] == 3
        assert counts["NEUTRAL"] == 1

    def test_correct_stakeholder_counts(self):
        from collections import Counter
        counts = Counter(a["stakeholder_type"] for a in DEMO_ANALYSES)
        assert counts["INDUSTRY"] == 9
        assert counts["CITIZEN"] == 4
        assert counts["ACADEMIC"] == 3
        assert counts["ADVOCACY"] == 2
        assert counts["GOVERNMENT"] == 2

    def test_correct_theme_counts(self):
        from collections import Counter
        counts = Counter(a["theme"] for a in DEMO_ANALYSES)
        assert counts["ASSESSMENT_METHODOLOGY"] == 5
        assert counts["SCOPE_APPLICABILITY"] == 4
        assert counts["TECHNICAL_REQUIREMENTS"] == 3
        assert counts["COST_AND_BURDEN"] == 3
        assert counts["IMPLEMENTATION_TIMELINE"] == 2

    def test_all_stakeholder_types_represented(self):
        types_present = {a["stakeholder_type"] for a in DEMO_ANALYSES}
        assert types_present == set(STAKEHOLDER_TYPES.keys())

    def test_industry_oppose_comments_present(self):
        industry_oppose = [a for a in DEMO_ANALYSES if a["stakeholder_type"] == "INDUSTRY" and a["stance"] == "OPPOSE"]
        assert len(industry_oppose) >= 1


# ---------------------------------------------------------------------------
# DEMO_MEMO
# ---------------------------------------------------------------------------

class TestDemoMemo:
    def test_is_string(self):
        assert isinstance(DEMO_MEMO, str)

    def test_nonempty(self):
        assert len(DEMO_MEMO) > 500

    def test_contains_decision_memorandum_header(self):
        assert "DECISION MEMORANDUM" in DEMO_MEMO

    def test_contains_docket_id(self):
        assert DEMO_DOCKET_ID in DEMO_MEMO

    def test_contains_five_sections(self):
        for section in ["I.", "II.", "III.", "IV.", "V."]:
            assert section in DEMO_MEMO

    def test_contains_executive_summary_section(self):
        assert "EXECUTIVE SUMMARY" in DEMO_MEMO

    def test_contains_recommendations_section(self):
        assert "RECOMMENDED" in DEMO_MEMO or "RECOMMENDATION" in DEMO_MEMO

    def test_contains_total_comment_count(self):
        assert "20" in DEMO_MEMO

    def test_contains_cmmc_reference(self):
        assert "CMMC" in DEMO_MEMO

    def test_contains_consensus_section(self):
        assert "CONSENSUS" in DEMO_MEMO

    def test_references_stakeholder_types(self):
        text_upper = DEMO_MEMO.upper()
        assert "INDUSTRY" in text_upper
        assert "ACADEMIC" in text_upper or "ACADEMIC" in DEMO_MEMO

    def test_contains_numbered_recommendations(self):
        # Should have at least 3 numbered recommendations
        for n in ["1.", "2.", "3."]:
            assert n in DEMO_MEMO

    def test_contains_agency_name(self):
        assert "Defense" in DEMO_MEMO or "DoD" in DEMO_MEMO

    def test_memo_has_to_from_re_date_header(self):
        assert "TO:" in DEMO_MEMO
        assert "FROM:" in DEMO_MEMO
        assert "RE:" in DEMO_MEMO
        assert "DATE:" in DEMO_MEMO
