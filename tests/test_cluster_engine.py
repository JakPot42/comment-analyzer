"""Tests for cluster_engine.py — deterministic aggregation, filtering, edge cases."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest

from models import CommentAnalysis, DocketSummary, ThemeCluster
from cluster_engine import build_summary, filter_analyses
from config import DEMO_DOCKET_ID, THEMES, STAKEHOLDER_TYPES, STANCES


def _make_analysis(
    comment_id="c1",
    theme="COST_AND_BURDEN",
    stakeholder_type="INDUSTRY",
    stance="OPPOSE",
    key_argument="Too expensive.",
) -> CommentAnalysis:
    return CommentAnalysis(
        comment_id=comment_id,
        submitter_name="Test Submitter",
        organization="Test Org",
        excerpt="Test excerpt",
        theme=theme,
        stakeholder_type=stakeholder_type,
        stance=stance,
        key_argument=key_argument,
    )


# ---------------------------------------------------------------------------
# build_summary
# ---------------------------------------------------------------------------

class TestBuildSummary:
    def test_returns_docket_summary(self):
        analyses = [_make_analysis()]
        result = build_summary(DEMO_DOCKET_ID, analyses)
        assert isinstance(result, DocketSummary)

    def test_docket_id_stored(self):
        analyses = [_make_analysis()]
        result = build_summary(DEMO_DOCKET_ID, analyses)
        assert result.docket_id == DEMO_DOCKET_ID

    def test_total_analyzed_correct(self):
        analyses = [_make_analysis(f"c{i}") for i in range(5)]
        result = build_summary(DEMO_DOCKET_ID, analyses)
        assert result.total_analyzed == 5

    def test_stance_totals_correct(self):
        analyses = [
            _make_analysis("c1", stance="SUPPORT"),
            _make_analysis("c2", stance="SUPPORT"),
            _make_analysis("c3", stance="OPPOSE"),
        ]
        result = build_summary(DEMO_DOCKET_ID, analyses)
        assert result.stance_totals["SUPPORT"] == 2
        assert result.stance_totals["OPPOSE"] == 1

    def test_stakeholder_totals_correct(self):
        analyses = [
            _make_analysis("c1", stakeholder_type="INDUSTRY"),
            _make_analysis("c2", stakeholder_type="CITIZEN"),
            _make_analysis("c3", stakeholder_type="CITIZEN"),
        ]
        result = build_summary(DEMO_DOCKET_ID, analyses)
        assert result.stakeholder_totals["INDUSTRY"] == 1
        assert result.stakeholder_totals["CITIZEN"] == 2

    def test_theme_clusters_created(self):
        analyses = [
            _make_analysis("c1", theme="COST_AND_BURDEN"),
            _make_analysis("c2", theme="COST_AND_BURDEN"),
            _make_analysis("c3", theme="ASSESSMENT_METHODOLOGY"),
        ]
        result = build_summary(DEMO_DOCKET_ID, analyses)
        themes = {c.theme for c in result.theme_clusters}
        assert "COST_AND_BURDEN" in themes
        assert "ASSESSMENT_METHODOLOGY" in themes

    def test_clusters_sorted_by_total_desc(self):
        analyses = [
            _make_analysis("c1", theme="COST_AND_BURDEN"),
            _make_analysis("c2", theme="ASSESSMENT_METHODOLOGY"),
            _make_analysis("c3", theme="ASSESSMENT_METHODOLOGY"),
            _make_analysis("c4", theme="ASSESSMENT_METHODOLOGY"),
        ]
        result = build_summary(DEMO_DOCKET_ID, analyses)
        assert result.theme_clusters[0].theme == "ASSESSMENT_METHODOLOGY"
        assert result.theme_clusters[0].total == 3

    def test_cluster_stance_counts_correct(self):
        analyses = [
            _make_analysis("c1", theme="COST_AND_BURDEN", stance="OPPOSE"),
            _make_analysis("c2", theme="COST_AND_BURDEN", stance="SUPPORT"),
            _make_analysis("c3", theme="COST_AND_BURDEN", stance="OPPOSE"),
        ]
        result = build_summary(DEMO_DOCKET_ID, analyses)
        cluster = result.theme_clusters[0]
        assert cluster.stance_counts["OPPOSE"] == 2
        assert cluster.stance_counts["SUPPORT"] == 1

    def test_cluster_top_arguments_populated(self):
        analyses = [
            _make_analysis("c1", key_argument="Arg one."),
            _make_analysis("c2", key_argument="Arg two."),
        ]
        result = build_summary(DEMO_DOCKET_ID, analyses)
        cluster = result.theme_clusters[0]
        assert len(cluster.top_arguments) >= 1
        assert "Arg" in cluster.top_arguments[0]

    def test_cluster_top_arguments_capped_at_three(self):
        analyses = [_make_analysis(f"c{i}", key_argument=f"Arg {i}.") for i in range(10)]
        result = build_summary(DEMO_DOCKET_ID, analyses)
        cluster = result.theme_clusters[0]
        assert len(cluster.top_arguments) <= 3

    def test_empty_analyses(self):
        result = build_summary(DEMO_DOCKET_ID, [])
        assert result.total_analyzed == 0
        assert result.theme_clusters == []

    def test_analyses_stored(self):
        analyses = [_make_analysis()]
        result = build_summary(DEMO_DOCKET_ID, analyses)
        assert result.analyses == analyses

    def test_title_populated_from_docket_meta(self):
        analyses = [_make_analysis()]
        result = build_summary(DEMO_DOCKET_ID, analyses)
        assert "CMMC" in result.title or "Cybersecurity" in result.title

    def test_unknown_docket_uses_fallback(self):
        result = build_summary("UNKNOWN-DOCKET", [_make_analysis()])
        assert result.title == "UNKNOWN-DOCKET" or result.agency == "Unknown Agency"

    def test_theme_label_populated(self):
        analyses = [_make_analysis(theme="COST_AND_BURDEN")]
        result = build_summary(DEMO_DOCKET_ID, analyses)
        cluster = result.theme_clusters[0]
        assert cluster.theme_label == "Cost and Burden"

    def test_multiple_themes_each_get_cluster(self):
        themes_used = ["COST_AND_BURDEN", "ASSESSMENT_METHODOLOGY", "SMB_IMPACT"]
        analyses = [_make_analysis(f"c{i}", theme=t) for i, t in enumerate(themes_used)]
        result = build_summary(DEMO_DOCKET_ID, analyses)
        result_themes = {c.theme for c in result.theme_clusters}
        assert set(themes_used) == result_themes

    def test_stakeholder_counts_in_cluster(self):
        analyses = [
            _make_analysis("c1", theme="COST_AND_BURDEN", stakeholder_type="INDUSTRY"),
            _make_analysis("c2", theme="COST_AND_BURDEN", stakeholder_type="CITIZEN"),
            _make_analysis("c3", theme="COST_AND_BURDEN", stakeholder_type="INDUSTRY"),
        ]
        result = build_summary(DEMO_DOCKET_ID, analyses)
        cluster = result.theme_clusters[0]
        assert cluster.stakeholder_counts["INDUSTRY"] == 2
        assert cluster.stakeholder_counts["CITIZEN"] == 1


# ---------------------------------------------------------------------------
# filter_analyses
# ---------------------------------------------------------------------------

class TestFilterAnalyses:
    def _sample(self):
        return [
            _make_analysis("c1", theme="COST_AND_BURDEN",         stakeholder_type="INDUSTRY", stance="OPPOSE"),
            _make_analysis("c2", theme="ASSESSMENT_METHODOLOGY",  stakeholder_type="ACADEMIC", stance="MODIFY"),
            _make_analysis("c3", theme="COST_AND_BURDEN",         stakeholder_type="CITIZEN",  stance="OPPOSE"),
            _make_analysis("c4", theme="TECHNICAL_REQUIREMENTS",  stakeholder_type="INDUSTRY", stance="SUPPORT"),
            _make_analysis("c5", theme="ASSESSMENT_METHODOLOGY",  stakeholder_type="INDUSTRY", stance="MODIFY"),
        ]

    def test_no_filter_returns_all(self):
        data = self._sample()
        result = filter_analyses(data)
        assert len(result) == 5

    def test_filter_by_theme(self):
        data = self._sample()
        result = filter_analyses(data, theme="COST_AND_BURDEN")
        assert len(result) == 2
        assert all(a.theme == "COST_AND_BURDEN" for a in result)

    def test_filter_by_stakeholder(self):
        data = self._sample()
        result = filter_analyses(data, stakeholder_type="INDUSTRY")
        assert len(result) == 3
        assert all(a.stakeholder_type == "INDUSTRY" for a in result)

    def test_filter_by_stance(self):
        data = self._sample()
        result = filter_analyses(data, stance="OPPOSE")
        assert len(result) == 2
        assert all(a.stance == "OPPOSE" for a in result)

    def test_combined_theme_and_stance(self):
        data = self._sample()
        result = filter_analyses(data, theme="COST_AND_BURDEN", stance="OPPOSE")
        assert len(result) == 2

    def test_combined_stakeholder_and_theme(self):
        data = self._sample()
        result = filter_analyses(data, theme="ASSESSMENT_METHODOLOGY", stakeholder_type="INDUSTRY")
        assert len(result) == 1
        assert result[0].comment_id == "c5"

    def test_no_match_returns_empty(self):
        data = self._sample()
        result = filter_analyses(data, theme="INTERNATIONAL_SUPPLY_CHAIN")
        assert result == []

    def test_filter_case_insensitive_theme(self):
        data = self._sample()
        result = filter_analyses(data, theme="cost_and_burden")
        assert len(result) == 2

    def test_filter_case_insensitive_stakeholder(self):
        data = self._sample()
        result = filter_analyses(data, stakeholder_type="academic")
        assert len(result) == 1

    def test_empty_input(self):
        result = filter_analyses([], theme="COST_AND_BURDEN")
        assert result == []


# ---------------------------------------------------------------------------
# Integration: demo data through cluster_engine
# ---------------------------------------------------------------------------

class TestDemoDataClusters:
    def _load_demo(self):
        from seed_data import DEMO_ANALYSES, DEMO_COMMENTS
        from comment_analyzer import analyze_comments
        return analyze_comments([], demo_mode=True)

    def test_demo_produces_20_analyses(self):
        analyses = self._load_demo()
        assert len(analyses) == 20

    def test_demo_summary_total_correct(self):
        analyses = self._load_demo()
        summary = build_summary(DEMO_DOCKET_ID, analyses)
        assert summary.total_analyzed == 20

    def test_demo_has_correct_stance_distribution(self):
        analyses = self._load_demo()
        summary = build_summary(DEMO_DOCKET_ID, analyses)
        # 10 MODIFY, 6 SUPPORT, 3 OPPOSE, 1 NEUTRAL
        assert summary.stance_totals.get("MODIFY", 0) == 10
        assert summary.stance_totals.get("SUPPORT", 0) == 6
        assert summary.stance_totals.get("OPPOSE", 0) == 3
        assert summary.stance_totals.get("NEUTRAL", 0) == 1

    def test_demo_has_correct_stakeholder_distribution(self):
        analyses = self._load_demo()
        summary = build_summary(DEMO_DOCKET_ID, analyses)
        # 9 INDUSTRY, 4 CITIZEN, 3 ACADEMIC, 2 ADVOCACY, 2 GOVERNMENT
        assert summary.stakeholder_totals.get("INDUSTRY", 0) == 9
        assert summary.stakeholder_totals.get("CITIZEN", 0) == 4
        assert summary.stakeholder_totals.get("ACADEMIC", 0) == 3
        assert summary.stakeholder_totals.get("ADVOCACY", 0) == 2
        assert summary.stakeholder_totals.get("GOVERNMENT", 0) == 2

    def test_demo_top_theme_is_assessment_methodology(self):
        analyses = self._load_demo()
        summary = build_summary(DEMO_DOCKET_ID, analyses)
        assert summary.theme_clusters[0].theme == "ASSESSMENT_METHODOLOGY"
        assert summary.theme_clusters[0].total == 5

    def test_demo_filter_oppose_returns_3(self):
        analyses = self._load_demo()
        oppose = filter_analyses(analyses, stance="OPPOSE")
        assert len(oppose) == 3

    def test_demo_filter_industry_returns_9(self):
        analyses = self._load_demo()
        industry = filter_analyses(analyses, stakeholder_type="INDUSTRY")
        assert len(industry) == 9
