"""Unit tests for the metrics calculator."""

import pytest
from lynx_tech.models import (
    CompanyStage, CompanyTier, FinancialStatement,
    GrowthMetrics, ProfitabilityMetrics, ShareStructure, SolvencyMetrics,
)
from lynx_tech.metrics.calculator import (
    calc_valuation, calc_profitability, calc_solvency, calc_growth,
    calc_efficiency, calc_share_structure, calc_tech_quality,
    calc_intrinsic_value,
)


@pytest.fixture
def sample_info():
    return {
        "currentPrice": 5.0, "marketCap": 500_000_000,
        "sharesOutstanding": 100_000_000, "totalCash": 200_000_000,
        "totalDebt": 10_000_000, "priceToBook": 2.0,
        "trailingPE": 15.0, "enterpriseValue": 310_000_000,
        "enterpriseToEbitda": 8.0, "returnOnEquity": 0.12,
        "grossMargins": 0.45, "profitMargins": 0.10,
        "currentRatio": 3.0, "debtToEquity": 20.0,
        "heldPercentInsiders": 0.15,
        "heldPercentInstitutions": 0.40,
        "floatShares": 85_000_000,
    }


@pytest.fixture
def sample_statements():
    return [
        FinancialStatement(period="2025", revenue=50_000_000, net_income=5_000_000,
                           total_assets=300_000_000, total_equity=200_000_000,
                           total_cash=200_000_000, total_liabilities=100_000_000,
                           current_assets=250_000_000, current_liabilities=50_000_000,
                           operating_cash_flow=-20_000_000, free_cash_flow=-25_000_000,
                           shares_outstanding=100_000_000, eps=0.05,
                           book_value_per_share=2.0, operating_income=8_000_000),
        FinancialStatement(period="2024", revenue=40_000_000, net_income=3_000_000,
                           total_assets=280_000_000, total_equity=190_000_000,
                           total_cash=180_000_000, operating_cash_flow=-15_000_000,
                           shares_outstanding=95_000_000),
    ]


class TestCalcValuation:
    def test_basic_valuation(self, sample_info, sample_statements):
        v = calc_valuation(sample_info, sample_statements, CompanyTier.MICRO, CompanyStage.GROWTH)
        assert v.pe_trailing == 15.0
        assert v.pb_ratio == 2.0
        assert v.market_cap == 500_000_000

    def test_cash_to_market_cap(self, sample_info, sample_statements):
        v = calc_valuation(sample_info, sample_statements, CompanyTier.MICRO, CompanyStage.GROWTH)
        assert v.cash_to_market_cap == pytest.approx(0.4, abs=0.01)

    def test_empty_info(self):
        v = calc_valuation({}, [], CompanyTier.NANO, CompanyStage.STARTUP)
        assert v.pe_trailing is None
        assert v.cash_to_market_cap is None


class TestCalcSolvency:
    def test_cash_burn_detected(self, sample_info, sample_statements):
        s = calc_solvency(sample_info, sample_statements, CompanyTier.MICRO, CompanyStage.GROWTH)
        assert s.cash_burn_rate is not None
        assert s.cash_burn_rate < 0

    def test_cash_runway_calculated(self, sample_info, sample_statements):
        s = calc_solvency(sample_info, sample_statements, CompanyTier.MICRO, CompanyStage.GROWTH)
        assert s.cash_runway_years is not None
        assert s.cash_runway_years > 0

    def test_ncav_calculated(self, sample_info, sample_statements):
        s = calc_solvency(sample_info, sample_statements, CompanyTier.MICRO, CompanyStage.GROWTH)
        assert s.ncav is not None
        # NCAV = current_assets - total_liabilities = 250M - 100M = 150M
        assert s.ncav == 150_000_000

    def test_burn_pct_of_market_cap(self, sample_info, sample_statements):
        s = calc_solvency(sample_info, sample_statements, CompanyTier.MICRO, CompanyStage.GROWTH)
        assert s.burn_as_pct_of_market_cap is not None
        assert s.burn_as_pct_of_market_cap > 0


class TestCalcGrowth:
    def test_revenue_growth(self, sample_statements):
        g = calc_growth(sample_statements, CompanyTier.MICRO, CompanyStage.GROWTH)
        assert g.revenue_growth_yoy is not None
        assert g.revenue_growth_yoy == pytest.approx(0.25, abs=0.01)

    def test_share_dilution(self, sample_statements):
        g = calc_growth(sample_statements, CompanyTier.MICRO, CompanyStage.GROWTH)
        assert g.shares_growth_yoy is not None
        assert g.shares_growth_yoy > 0  # 100M vs 95M = dilution

    def test_empty_statements(self):
        g = calc_growth([], CompanyTier.NANO, CompanyStage.STARTUP)
        assert g.revenue_growth_yoy is None

    def test_single_statement(self):
        g = calc_growth([FinancialStatement(period="2025")], CompanyTier.NANO, CompanyStage.STARTUP)
        assert g.revenue_growth_yoy is None


class TestCalcShareStructure:
    def test_share_assessment(self, sample_info, sample_statements):
        g = GrowthMetrics()
        ss = calc_share_structure(sample_info, sample_statements, g, CompanyTier.MICRO, CompanyStage.GROWTH)
        assert ss.shares_outstanding == 100_000_000
        assert ss.insider_ownership_pct == 0.15
        assert ss.share_structure_assessment is not None
        # With 100M shares, IT-tier threshold classifies as "Standard"
        assert "Standard" in ss.share_structure_assessment or "Tight" in ss.share_structure_assessment

    def test_hyper_diluted_structure(self):
        info = {"sharesOutstanding": 12_000_000_000, "impliedSharesOutstanding": 12_500_000_000}
        ss = calc_share_structure(info, [], GrowthMetrics(), CompanyTier.MEGA, CompanyStage.MATURE)
        assert "Hyper-Diluted" in ss.share_structure_assessment or "Mega Float" in ss.share_structure_assessment


class TestCalcTechQuality:
    def test_quality_score_range(self, sample_info, sample_statements):
        g = GrowthMetrics(shares_growth_yoy=0.02, rd_intensity=0.15, revenue_growth_yoy=0.25)
        s = SolvencyMetrics(cash_runway_years=5.0, cash_burn_rate=-10_000_000, ncav=100_000_000,
                            tangible_book_value=200_000_000)
        ss = ShareStructure(insider_ownership_pct=0.15, share_structure_assessment="Standard (100-500M shares)")
        p = ProfitabilityMetrics(gross_margin=0.75, rule_of_40=55.0, magic_number=1.1)
        m = calc_tech_quality(p, g, s, ss, sample_statements, sample_info,
                              CompanyTier.MID, CompanyStage.GROWTH)
        assert 0 <= m.quality_score <= 100
        assert m.competitive_position is not None
        assert m.moat_assessment is not None
        assert m.rule_of_40_assessment is not None

    def test_empty_inputs(self):
        m = calc_tech_quality(ProfitabilityMetrics(), GrowthMetrics(), SolvencyMetrics(),
                              ShareStructure(), [], {}, CompanyTier.NANO, CompanyStage.STARTUP)
        assert m.quality_score is not None


class TestCalcIntrinsicValue:
    def test_method_selection_mature(self, sample_info, sample_statements):
        iv = calc_intrinsic_value(sample_info, sample_statements, GrowthMetrics(),
                                  SolvencyMetrics(), CompanyTier.MID, CompanyStage.MATURE)
        assert "DCF" in (iv.primary_method or "") or "FCF" in (iv.primary_method or "")

    def test_method_selection_growth(self, sample_info, sample_statements):
        iv = calc_intrinsic_value(sample_info, sample_statements, GrowthMetrics(),
                                  SolvencyMetrics(), CompanyTier.MICRO, CompanyStage.GROWTH)
        assert "EV" in (iv.primary_method or "")

    def test_method_selection_startup(self, sample_info, sample_statements):
        iv = calc_intrinsic_value(sample_info, sample_statements, GrowthMetrics(),
                                  SolvencyMetrics(), CompanyTier.NANO, CompanyStage.STARTUP)
        assert "Cash" in (iv.primary_method or "")
