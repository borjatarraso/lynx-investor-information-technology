"""Unit tests for metric explanations."""

import pytest
from lynx_tech.metrics.explanations import (
    get_explanation, list_metrics, get_section_explanation,
    get_conclusion_explanation, SECTION_EXPLANATIONS, CONCLUSION_METHODOLOGY,
)


class TestGetExplanation:
    def test_known_metric(self):
        e = get_explanation("cash_to_market_cap")
        assert e is not None
        assert "Cash" in e.full_name
        assert e.category == "valuation"

    def test_tech_metric_rule_of_40(self):
        e = get_explanation("rule_of_40")
        assert e is not None
        assert e.category == "profitability"

    def test_tech_metric_sbc(self):
        e = get_explanation("sbc_to_revenue")
        assert e is not None
        assert e.category == "profitability"

    def test_unknown_metric(self):
        assert get_explanation("nonexistent") is None

    def test_all_metrics_have_required_fields(self):
        for m in list_metrics():
            assert m.key != ""
            assert m.full_name != ""
            assert m.description != ""
            assert m.formula != ""
            assert m.category != ""

    def test_tech_specific_metrics_exist(self):
        keys = [m.key for m in list_metrics()]
        assert "cash_to_market_cap" in keys
        assert "quality_score" in keys
        assert "shares_growth_yoy" in keys
        assert "rule_of_40" in keys
        assert "sbc_to_revenue" in keys
        assert "ev_gross_profit" in keys

    def test_list_by_category(self):
        valuation = list_metrics("valuation")
        assert len(valuation) > 0
        assert all(m.category == "valuation" for m in valuation)


class TestSectionExplanations:
    def test_all_sections_have_title(self):
        for key, sec in SECTION_EXPLANATIONS.items():
            assert "title" in sec
            assert "description" in sec

    def test_tech_quality_section_exists(self):
        sec = get_section_explanation("tech_quality")
        assert sec is not None
        assert "Tech Quality" in sec["title"]

    def test_share_structure_section_exists(self):
        sec = get_section_explanation("share_structure")
        assert sec is not None

    def test_unknown_section(self):
        assert get_section_explanation("nonexistent") is None


class TestConclusionMethodology:
    def test_overall_exists(self):
        ce = get_conclusion_explanation("overall")
        assert ce is not None
        assert "tech quality" in ce["description"].lower()

    def test_unknown_category(self):
        assert get_conclusion_explanation("nonexistent") is None
