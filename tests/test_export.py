"""Tests for export functionality."""

import pytest
import tempfile
from pathlib import Path

from lynx_tech.models import (
    AnalysisReport, CompanyProfile, CompanyTier, CompanyStage,
    ValuationMetrics, SolvencyMetrics, GrowthMetrics,
    TechQualityIndicators, ShareStructure, MarketIntelligence,
)
from lynx_tech.export import export_report, ExportFormat


@pytest.fixture
def sample_report():
    p = CompanyProfile(ticker="TEST", name="Test Software Corp",
                       sector="Technology", industry="Software - Application",
                       country="United States", market_cap=1_500_000_000)
    p.tier = CompanyTier.SMALL
    p.stage = CompanyStage.GROWTH
    r = AnalysisReport(
        profile=p,
        valuation=ValuationMetrics(pb_ratio=5.0, cash_to_market_cap=0.15, ev_revenue=6.0,
                                   ev_gross_profit=9.0),
        solvency=SolvencyMetrics(cash_runway_years=3.0, total_cash=200_000_000,
                                 current_ratio=4.0, debt_to_equity=0.1),
        growth=GrowthMetrics(shares_growth_yoy=0.03, revenue_growth_yoy=0.35,
                             rd_intensity=0.20),
        tech_quality=TechQualityIndicators(quality_score=72.0,
                                           competitive_position="Strong — High-Quality Business"),
        share_structure=ShareStructure(shares_outstanding=100_000_000,
                                       insider_ownership_pct=0.12),
    )
    return r


class TestExportFormat:
    def test_accepts_enum(self, sample_report):
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
            p = export_report(sample_report, ExportFormat.TXT, Path(f.name))
            assert p.exists()
            assert p.stat().st_size > 0

    def test_accepts_string(self, sample_report):
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
            p = export_report(sample_report, "txt", Path(f.name))
            assert p.exists()

    def test_accepts_enum_constructed_from_string(self, sample_report):
        with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as f:
            p = export_report(sample_report, ExportFormat("html"), Path(f.name))
            assert p.exists()

    def test_invalid_format_raises(self, sample_report):
        with pytest.raises(ValueError):
            export_report(sample_report, "xyz")


class TestTxtExport:
    def test_contains_company_name(self, sample_report):
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
            p = export_report(sample_report, "txt", Path(f.name))
            content = p.read_text()
            assert "Test Software Corp" in content

    def test_contains_stage(self, sample_report):
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
            content = export_report(sample_report, "txt", Path(f.name)).read_text()
            assert "Hyper-Growth" in content or "Growth" in content

    def test_no_truncation(self, sample_report):
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
            content = export_report(sample_report, "txt", Path(f.name)).read_text()
            assert len(content) > 500

    def test_contains_conclusion(self, sample_report):
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
            content = export_report(sample_report, "txt", Path(f.name)).read_text()
            assert "CONCLUSION" in content


class TestHtmlExport:
    def test_white_background(self, sample_report):
        with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as f:
            content = export_report(sample_report, "html", Path(f.name)).read_text()
            assert "#fff" in content or "#ffffff" in content

    def test_word_wrap(self, sample_report):
        with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as f:
            content = export_report(sample_report, "html", Path(f.name)).read_text()
            assert "word-wrap" in content or "overflow-wrap" in content

    def test_print_media(self, sample_report):
        with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as f:
            content = export_report(sample_report, "html", Path(f.name)).read_text()
            assert "@media print" in content

    def test_xss_prevention(self):
        r = AnalysisReport(profile=CompanyProfile(
            ticker="XSS", name='<script>alert("xss")</script>'))
        with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as f:
            content = export_report(r, "html", Path(f.name)).read_text()
            assert "<script>" not in content

    def test_contains_footer(self, sample_report):
        with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as f:
            content = export_report(sample_report, "html", Path(f.name)).read_text()
            assert "Lince Investor Suite" in content

    def test_valid_html(self, sample_report):
        with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as f:
            content = export_report(sample_report, "html", Path(f.name)).read_text()
            assert content.startswith("<!DOCTYPE html>")
            assert "</html>" in content


class TestExportWithEmptyReport:
    def test_txt_empty(self):
        r = AnalysisReport(profile=CompanyProfile(ticker="MT", name="MT"))
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
            p = export_report(r, "txt", Path(f.name))
            assert p.exists()

    def test_html_empty(self):
        r = AnalysisReport(profile=CompanyProfile(ticker="MT", name="MT"))
        with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as f:
            p = export_report(r, "html", Path(f.name))
            assert p.exists()
