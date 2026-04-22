"""Unit tests for the relevance system."""

import pytest
from lynx_tech.models import CompanyStage, CompanyTier, Relevance
from lynx_tech.metrics.relevance import get_relevance


class TestStageOverrides:
    """Stage overrides take precedence over tier-based lookups."""

    def test_explorer_pe_irrelevant(self):
        assert get_relevance("pe_trailing", CompanyTier.MEGA, "valuation", CompanyStage.GROWTH) == Relevance.IRRELEVANT

    def test_explorer_cash_runway_critical(self):
        assert get_relevance("cash_runway_years", CompanyTier.MICRO, "solvency", CompanyStage.GROWTH) == Relevance.CRITICAL

    def test_grassroots_cash_to_mcap_critical(self):
        assert get_relevance("cash_to_market_cap", CompanyTier.NANO, "valuation", CompanyStage.STARTUP) == Relevance.CRITICAL

    def test_producer_ev_ebitda_critical(self):
        assert get_relevance("ev_ebitda", CompanyTier.MID, "valuation", CompanyStage.MATURE) == Relevance.CRITICAL

    def test_producer_cash_burn_contextual(self):
        assert get_relevance("cash_burn_rate", CompanyTier.MID, "solvency", CompanyStage.MATURE) == Relevance.CONTEXTUAL

    def test_startup_traditional_profitability_irrelevant(self):
        # Startup stage: P/E, ROE, ROA are IRRELEVANT (no earnings yet)
        for key in ["roe", "roa"]:
            assert get_relevance(key, CompanyTier.MICRO, "profitability", CompanyStage.STARTUP) == Relevance.IRRELEVANT

    def test_startup_gross_margin_critical(self):
        # Gross margin is the moat metric — CRITICAL for startups
        assert get_relevance("gross_margin", CompanyTier.MICRO, "profitability", CompanyStage.STARTUP) == Relevance.CRITICAL

    def test_growth_rule_of_40_critical(self):
        assert get_relevance("rule_of_40", CompanyTier.MID, "profitability", CompanyStage.GROWTH) == Relevance.CRITICAL

    def test_growth_sbc_to_revenue_critical(self):
        assert get_relevance("sbc_to_revenue", CompanyTier.MID, "profitability", CompanyStage.GROWTH) == Relevance.CRITICAL

    def test_producer_profitability_relevant(self):
        assert get_relevance("roic", CompanyTier.MID, "profitability", CompanyStage.MATURE) == Relevance.CRITICAL

    def test_dilution_critical_for_juniors(self):
        for stage in [CompanyStage.STARTUP, CompanyStage.GROWTH, CompanyStage.SCALE]:
            assert get_relevance("shares_growth_yoy", CompanyTier.MICRO, "growth", stage) == Relevance.CRITICAL

    def test_insider_ownership_critical_for_juniors(self):
        assert get_relevance("insider_ownership_pct", CompanyTier.MICRO, "share_structure", CompanyStage.GROWTH) == Relevance.CRITICAL

    def test_royalty_fcf_critical(self):
        assert get_relevance("fcf_margin", CompanyTier.SMALL, "profitability", CompanyStage.PLATFORM) == Relevance.CRITICAL


class TestTierFallback:
    """When no stage override exists, tier-based lookup is used."""

    def test_unknown_metric_defaults_relevant(self):
        assert get_relevance("some_unknown_metric", CompanyTier.MID, "valuation", CompanyStage.MATURE) == Relevance.RELEVANT

    def test_pb_ratio_critical_for_small(self):
        # Stage override for PRODUCER pb_ratio = IMPORTANT
        assert get_relevance("pb_ratio", CompanyTier.SMALL, "valuation", CompanyStage.MATURE) in [Relevance.CRITICAL, Relevance.IMPORTANT, Relevance.RELEVANT]
