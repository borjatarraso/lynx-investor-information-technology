"""Data models for Lynx Information Technology — IT-focused fundamental analysis."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


# ---------------------------------------------------------------------------
# Company tier classification (market cap based)
# ---------------------------------------------------------------------------

class CompanyTier(str, Enum):
    MEGA = "Mega Cap"
    LARGE = "Large Cap"
    MID = "Mid Cap"
    SMALL = "Small Cap"
    MICRO = "Micro Cap"
    NANO = "Nano Cap"


def classify_tier(market_cap: Optional[float]) -> CompanyTier:
    if market_cap is None or market_cap <= 0:
        return CompanyTier.NANO
    if market_cap >= 200_000_000_000:
        return CompanyTier.MEGA
    if market_cap >= 10_000_000_000:
        return CompanyTier.LARGE
    if market_cap >= 2_000_000_000:
        return CompanyTier.MID
    if market_cap >= 300_000_000:
        return CompanyTier.SMALL
    if market_cap >= 50_000_000:
        return CompanyTier.MICRO
    return CompanyTier.NANO


# ---------------------------------------------------------------------------
# IT company lifecycle stage classification
# ---------------------------------------------------------------------------

class CompanyStage(str, Enum):
    STARTUP = "Startup / Early-Stage"
    GROWTH = "Hyper-Growth"
    SCALE = "Scale-Up"
    MATURE = "Mature / Cash-Generative"
    PLATFORM = "Dominant Platform"


# ---------------------------------------------------------------------------
# IT sub-sector classification (replaces Commodity)
# ---------------------------------------------------------------------------

class TechCategory(str, Enum):
    SAAS = "SaaS / Application Software"
    INFRA_SOFTWARE = "Infrastructure Software"
    CLOUD = "Cloud / Hyperscaler"
    CYBERSECURITY = "Cybersecurity"
    SEMICONDUCTOR = "Semiconductors"
    SEMI_EQUIPMENT = "Semi Equipment / EDA"
    IT_SERVICES = "IT Services & Consulting"
    HARDWARE = "Hardware / Devices"
    INTERNET = "Internet / Digital Platforms"
    FINTECH = "Fintech Software"
    DATA_AI = "Data / AI / Analytics"
    OTHER = "Other Technology"


# ---------------------------------------------------------------------------
# Regulatory / jurisdiction tiering (IT lens: IP protection, data privacy, export controls)
# ---------------------------------------------------------------------------

class JurisdictionTier(str, Enum):
    TIER_1 = "Tier 1 — Strong IP & Stable Regulation"
    TIER_2 = "Tier 2 — Moderate Regulatory Risk"
    TIER_3 = "Tier 3 — High Regulatory / Geopolitical Risk"
    UNKNOWN = "Unknown"


class Relevance(str, Enum):
    CRITICAL = "critical"
    IMPORTANT = "important"
    RELEVANT = "relevant"
    CONTEXTUAL = "contextual"
    IRRELEVANT = "irrelevant"


class Severity(str, Enum):
    CRITICAL = "CRITICAL"
    WARNING = "WARNING"
    WATCH = "WATCH"
    OK = "OK"
    STRONG = "STRONG"
    NA = "N/A"


# ---------------------------------------------------------------------------
# Presentation helpers for Severity and Relevance (colors + wrappers)
# ---------------------------------------------------------------------------

SEVERITY_STYLE = {
    Severity.CRITICAL: {"wrap": ("***", "***"), "color": "bold red",  "label": "CRITICAL"},
    Severity.WARNING:  {"wrap": ("*", "*"),     "color": "#ff8800",   "label": "WARNING"},
    Severity.WATCH:    {"wrap": ("[", "]"),     "color": "yellow",    "label": "WATCH"},
    Severity.OK:       {"wrap": ("[", "]"),     "color": "green",     "label": "OK"},
    Severity.STRONG:   {"wrap": ("[", "]"),     "color": "grey70",    "label": "STRONG"},
    Severity.NA:       {"wrap": ("[", "]"),     "color": "grey50",    "label": "N/A"},
}


def format_severity(sev: "Severity") -> str:
    """Return a Rich-markup formatted severity tag.

    CRITICAL -> [bold red]***CRITICAL***[/]
    WARNING  -> [#ff8800]*WARNING*[/]
    WATCH    -> [yellow][WATCH][/]
    OK       -> [green][OK][/]
    STRONG   -> [grey70][STRONG][/]
    """
    style = SEVERITY_STYLE.get(sev, SEVERITY_STYLE[Severity.NA])
    pre, post = style["wrap"]
    label = style["label"]
    if sev == Severity.CRITICAL:
        label = label.upper()
    return f"[{style['color']}]{pre}{label}{post}[/]"


def severity_plain(sev: "Severity") -> str:
    """Plain-text severity token (no markup)."""
    style = SEVERITY_STYLE.get(sev, SEVERITY_STYLE[Severity.NA])
    pre, post = style["wrap"]
    label = style["label"]
    if sev == Severity.CRITICAL:
        label = label.upper()
    return f"{pre}{label}{post}"


IMPACT_STYLE = {
    Relevance.CRITICAL:   {"color": "blink bold red",  "label": "Critical"},
    Relevance.IMPORTANT:  {"color": "#ff8800",         "label": "Important"},
    Relevance.RELEVANT:   {"color": "yellow",          "label": "Relevant"},
    Relevance.CONTEXTUAL: {"color": "green",           "label": "Informational"},
    Relevance.IRRELEVANT: {"color": "grey70",          "label": "Irrelevant"},
}


def format_impact(rel: "Relevance") -> str:
    """Return Rich-markup formatted impact label for tables."""
    style = IMPACT_STYLE.get(rel, IMPACT_STYLE[Relevance.RELEVANT])
    return f"[{style['color']}]{style['label']}[/]"


def impact_plain(rel: "Relevance") -> str:
    style = IMPACT_STYLE.get(rel, IMPACT_STYLE[Relevance.RELEVANT])
    return style["label"]


# ---------------------------------------------------------------------------
# Core data models
# ---------------------------------------------------------------------------

@dataclass
class CompanyProfile:
    ticker: str
    name: str
    isin: Optional[str] = None
    sector: Optional[str] = None
    industry: Optional[str] = None
    country: Optional[str] = None
    exchange: Optional[str] = None
    currency: Optional[str] = None
    market_cap: Optional[float] = None
    description: Optional[str] = None
    website: Optional[str] = None
    employees: Optional[int] = None
    tier: CompanyTier = CompanyTier.NANO
    stage: CompanyStage = CompanyStage.STARTUP
    tech_category: TechCategory = TechCategory.OTHER
    jurisdiction_tier: JurisdictionTier = JurisdictionTier.UNKNOWN
    jurisdiction_country: Optional[str] = None


@dataclass
class ValuationMetrics:
    pe_trailing: Optional[float] = None
    pe_forward: Optional[float] = None
    pb_ratio: Optional[float] = None
    ps_ratio: Optional[float] = None
    p_fcf: Optional[float] = None
    ev_ebitda: Optional[float] = None
    ev_revenue: Optional[float] = None
    ev_gross_profit: Optional[float] = None
    peg_ratio: Optional[float] = None
    dividend_yield: Optional[float] = None
    earnings_yield: Optional[float] = None
    enterprise_value: Optional[float] = None
    market_cap: Optional[float] = None
    price_to_tangible_book: Optional[float] = None
    price_to_ncav: Optional[float] = None
    cash_to_market_cap: Optional[float] = None
    # IT-specific valuation
    ev_to_arr: Optional[float] = None
    ev_per_employee: Optional[float] = None
    rule_of_40_adj_multiple: Optional[float] = None


@dataclass
class ProfitabilityMetrics:
    roe: Optional[float] = None
    roa: Optional[float] = None
    roic: Optional[float] = None
    gross_margin: Optional[float] = None
    operating_margin: Optional[float] = None
    net_margin: Optional[float] = None
    fcf_margin: Optional[float] = None
    ebitda_margin: Optional[float] = None
    # IT-specific profitability
    rule_of_40: Optional[float] = None
    rule_of_40_ebitda: Optional[float] = None
    magic_number: Optional[float] = None
    gaap_vs_adj_gap: Optional[float] = None
    sbc_to_revenue: Optional[float] = None
    sbc_to_fcf: Optional[float] = None


@dataclass
class SolvencyMetrics:
    debt_to_equity: Optional[float] = None
    debt_to_ebitda: Optional[float] = None
    current_ratio: Optional[float] = None
    quick_ratio: Optional[float] = None
    interest_coverage: Optional[float] = None
    altman_z_score: Optional[float] = None
    net_debt: Optional[float] = None
    total_debt: Optional[float] = None
    total_cash: Optional[float] = None
    cash_burn_rate: Optional[float] = None
    cash_runway_years: Optional[float] = None
    working_capital: Optional[float] = None
    cash_per_share: Optional[float] = None
    tangible_book_value: Optional[float] = None
    ncav: Optional[float] = None
    ncav_per_share: Optional[float] = None
    quarterly_burn_rate: Optional[float] = None
    burn_as_pct_of_market_cap: Optional[float] = None
    # IT-specific solvency
    cash_coverage_months: Optional[float] = None
    capex_to_revenue: Optional[float] = None
    rpo_coverage: Optional[float] = None
    goodwill_to_assets: Optional[float] = None
    deferred_revenue_ratio: Optional[float] = None


@dataclass
class GrowthMetrics:
    revenue_growth_yoy: Optional[float] = None
    revenue_cagr_3y: Optional[float] = None
    revenue_cagr_5y: Optional[float] = None
    earnings_growth_yoy: Optional[float] = None
    earnings_cagr_3y: Optional[float] = None
    earnings_cagr_5y: Optional[float] = None
    fcf_growth_yoy: Optional[float] = None
    book_value_growth_yoy: Optional[float] = None
    dividend_growth_5y: Optional[float] = None
    shares_growth_yoy: Optional[float] = None
    shares_growth_3y_cagr: Optional[float] = None
    fully_diluted_shares: Optional[float] = None
    dilution_ratio: Optional[float] = None
    # IT-specific growth
    arr_growth_yoy: Optional[float] = None
    net_revenue_retention: Optional[float] = None
    gross_revenue_retention: Optional[float] = None
    rd_intensity: Optional[float] = None
    rd_growth_yoy: Optional[float] = None
    sales_marketing_intensity: Optional[float] = None
    employee_growth_yoy: Optional[float] = None
    revenue_per_employee: Optional[float] = None
    operating_leverage: Optional[float] = None


@dataclass
class EfficiencyMetrics:
    asset_turnover: Optional[float] = None
    inventory_turnover: Optional[float] = None
    receivables_turnover: Optional[float] = None
    days_sales_outstanding: Optional[float] = None
    days_inventory: Optional[float] = None
    cash_conversion_cycle: Optional[float] = None
    # IT-specific efficiency
    rule_of_x_score: Optional[float] = None
    cac_payback_months: Optional[float] = None
    fcf_conversion: Optional[float] = None


@dataclass
class TechQualityIndicators:
    """Quality scoring specific to IT companies."""
    quality_score: Optional[float] = None
    management_quality: Optional[str] = None
    insider_ownership_pct: Optional[float] = None
    founder_led: Optional[str] = None
    moat_assessment: Optional[str] = None
    moat_type: Optional[str] = None
    competitive_position: Optional[str] = None
    rd_efficiency_assessment: Optional[str] = None
    unit_economics: Optional[str] = None
    platform_position: Optional[str] = None
    financial_position: Optional[str] = None
    dilution_risk: Optional[str] = None
    rule_of_40_assessment: Optional[str] = None
    sbc_risk_assessment: Optional[str] = None
    catalyst_density: Optional[str] = None
    near_term_catalysts: list[str] = field(default_factory=list)
    revenue_predictability: Optional[str] = None
    roic_history: list[Optional[float]] = field(default_factory=list)
    gross_margin_history: list[Optional[float]] = field(default_factory=list)


@dataclass
class IntrinsicValue:
    dcf_value: Optional[float] = None
    graham_number: Optional[float] = None
    lynch_fair_value: Optional[float] = None
    ncav_value: Optional[float] = None
    asset_based_value: Optional[float] = None
    ev_sales_implied_price: Optional[float] = None
    reverse_dcf_growth: Optional[float] = None
    current_price: Optional[float] = None
    margin_of_safety_dcf: Optional[float] = None
    margin_of_safety_graham: Optional[float] = None
    margin_of_safety_ncav: Optional[float] = None
    margin_of_safety_asset: Optional[float] = None
    margin_of_safety_ev_sales: Optional[float] = None
    primary_method: Optional[str] = None
    secondary_method: Optional[str] = None


@dataclass
class ShareStructure:
    shares_outstanding: Optional[float] = None
    fully_diluted_shares: Optional[float] = None
    warrants_outstanding: Optional[float] = None
    options_outstanding: Optional[float] = None
    rsu_outstanding: Optional[float] = None
    insider_ownership_pct: Optional[float] = None
    institutional_ownership_pct: Optional[float] = None
    float_shares: Optional[float] = None
    dual_class_structure: Optional[bool] = None
    share_structure_assessment: Optional[str] = None
    sbc_overhang_risk: Optional[str] = None


@dataclass
class InsiderTransaction:
    insider: str = ""
    position: str = ""
    transaction_type: str = ""
    shares: Optional[float] = None
    value: Optional[float] = None
    date: str = ""


@dataclass
class MarketIntelligence:
    """Market sentiment, insider activity, institutional holdings, and technicals."""
    insider_transactions: list[InsiderTransaction] = field(default_factory=list)
    net_insider_shares_3m: Optional[float] = None
    insider_buy_signal: Optional[str] = None

    top_holders: list[str] = field(default_factory=list)
    institutions_count: Optional[int] = None
    institutions_pct: Optional[float] = None

    analyst_count: Optional[int] = None
    recommendation: Optional[str] = None
    target_high: Optional[float] = None
    target_low: Optional[float] = None
    target_mean: Optional[float] = None
    target_upside_pct: Optional[float] = None

    shares_short: Optional[float] = None
    short_pct_of_float: Optional[float] = None
    short_ratio_days: Optional[float] = None
    short_squeeze_risk: Optional[str] = None

    price_current: Optional[float] = None
    price_52w_high: Optional[float] = None
    price_52w_low: Optional[float] = None
    pct_from_52w_high: Optional[float] = None
    pct_from_52w_low: Optional[float] = None
    price_52w_range_position: Optional[float] = None
    sma_50: Optional[float] = None
    sma_200: Optional[float] = None
    above_sma_50: Optional[bool] = None
    above_sma_200: Optional[bool] = None
    golden_cross: Optional[bool] = None
    beta: Optional[float] = None
    avg_volume: Optional[float] = None
    volume_10d_avg: Optional[float] = None
    volume_trend: Optional[str] = None

    projected_dilution_annual_pct: Optional[float] = None
    projected_shares_in_2y: Optional[float] = None
    financing_warning: Optional[str] = None

    # Tech benchmark context (QQQ / IGV / SMH replaces commodity context)
    benchmark_name: Optional[str] = None
    benchmark_ticker: Optional[str] = None
    benchmark_price: Optional[float] = None
    benchmark_52w_high: Optional[float] = None
    benchmark_52w_low: Optional[float] = None
    benchmark_52w_position: Optional[float] = None
    benchmark_ytd_change: Optional[float] = None

    sector_etf_name: Optional[str] = None
    sector_etf_ticker: Optional[str] = None
    sector_etf_price: Optional[float] = None
    sector_etf_3m_perf: Optional[float] = None
    peer_etf_name: Optional[str] = None
    peer_etf_ticker: Optional[str] = None
    peer_etf_price: Optional[float] = None
    peer_etf_3m_perf: Optional[float] = None

    risk_warnings: list[str] = field(default_factory=list)
    disclaimers: list[str] = field(default_factory=list)


@dataclass
class FinancialStatement:
    period: str
    revenue: Optional[float] = None
    cost_of_revenue: Optional[float] = None
    gross_profit: Optional[float] = None
    operating_income: Optional[float] = None
    net_income: Optional[float] = None
    ebitda: Optional[float] = None
    interest_expense: Optional[float] = None
    total_assets: Optional[float] = None
    total_liabilities: Optional[float] = None
    total_equity: Optional[float] = None
    total_debt: Optional[float] = None
    total_cash: Optional[float] = None
    current_assets: Optional[float] = None
    current_liabilities: Optional[float] = None
    operating_cash_flow: Optional[float] = None
    capital_expenditure: Optional[float] = None
    free_cash_flow: Optional[float] = None
    dividends_paid: Optional[float] = None
    shares_outstanding: Optional[float] = None
    eps: Optional[float] = None
    book_value_per_share: Optional[float] = None
    # IT-specific financial line items
    research_development: Optional[float] = None
    selling_general_admin: Optional[float] = None
    stock_based_compensation: Optional[float] = None
    deferred_revenue: Optional[float] = None
    goodwill: Optional[float] = None
    intangibles: Optional[float] = None


@dataclass
class AnalysisConclusion:
    overall_score: float = 0.0
    verdict: str = ""
    summary: str = ""
    category_scores: dict = field(default_factory=dict)
    category_summaries: dict = field(default_factory=dict)
    strengths: list = field(default_factory=list)
    risks: list = field(default_factory=list)
    tier_note: str = ""
    stage_note: str = ""
    screening_checklist: dict = field(default_factory=dict)


@dataclass
class MetricExplanation:
    key: str
    full_name: str
    description: str
    why_used: str
    formula: str
    category: str


@dataclass
class Filing:
    form_type: str
    filing_date: str
    period: str
    url: str
    description: Optional[str] = None
    local_path: Optional[str] = None


@dataclass
class NewsArticle:
    title: str
    url: str
    published: Optional[str] = None
    source: Optional[str] = None
    summary: Optional[str] = None
    local_path: Optional[str] = None


@dataclass
class AnalysisReport:
    profile: CompanyProfile
    valuation: Optional[ValuationMetrics] = None
    profitability: Optional[ProfitabilityMetrics] = None
    solvency: Optional[SolvencyMetrics] = None
    growth: Optional[GrowthMetrics] = None
    efficiency: Optional[EfficiencyMetrics] = None
    tech_quality: Optional[TechQualityIndicators] = None
    intrinsic_value: Optional[IntrinsicValue] = None
    share_structure: Optional[ShareStructure] = None
    market_intelligence: Optional[MarketIntelligence] = None
    financials: list[FinancialStatement] = field(default_factory=list)
    filings: list[Filing] = field(default_factory=list)
    news: list[NewsArticle] = field(default_factory=list)
    fetched_at: str = field(default_factory=lambda: datetime.now().isoformat())


# ---------------------------------------------------------------------------
# Stage classification helpers (IT lifecycle)
# ---------------------------------------------------------------------------

_STAGE_KEYWORDS = {
    CompanyStage.PLATFORM: [
        "hyperscale", "platform", "dominant", "operating system", "marketplace leader",
        "ecosystem", "global platform", "market-leading cloud",
    ],
    CompanyStage.MATURE: [
        "mature", "free cash flow positive", "buyback", "dividend", "cash-generative",
        "established", "legacy software", "profitable",
    ],
    CompanyStage.SCALE: [
        "scaling", "expanding internationally", "scale-up", "profitability pathway",
        "go-to-market",
    ],
    CompanyStage.GROWTH: [
        "hyper-growth", "hypergrowth", "rapid growth", "annual recurring revenue",
        "ARR", "subscription growth", "land and expand",
    ],
    CompanyStage.STARTUP: [
        "startup", "early stage", "seed", "pre-revenue", "emerging", "venture-backed",
        "newly public",
    ],
}


_CATEGORY_KEYWORDS = {
    TechCategory.SAAS: [
        "saas", "software as a service", "subscription software", "cloud software",
        "application software", "workflow software", "business software",
    ],
    TechCategory.INFRA_SOFTWARE: [
        "infrastructure software", "database", "middleware", "devops", "container",
        "kubernetes", "observability", "monitoring", "identity management",
    ],
    TechCategory.CLOUD: [
        "hyperscaler", "public cloud", "cloud infrastructure", "iaas", "paas",
        "data center", "hosting",
    ],
    TechCategory.CYBERSECURITY: [
        "cybersecurity", "cyber security", "security software", "endpoint security",
        "firewall", "zero trust", "siem", "xdr", "threat intelligence", "pentest",
    ],
    TechCategory.SEMICONDUCTOR: [
        "semiconductor", "chip design", "chipmaker", "foundry", "fabless",
        "integrated circuit", "gpu", "cpu", "asic", "wafer",
    ],
    TechCategory.SEMI_EQUIPMENT: [
        "semiconductor equipment", "lithography", "euv", "etch", "deposition",
        "eda", "electronic design automation", "chip design software",
    ],
    TechCategory.IT_SERVICES: [
        "it services", "consulting", "systems integrator", "managed services",
        "outsourcing", "professional services",
    ],
    TechCategory.HARDWARE: [
        "computer hardware", "networking equipment", "consumer electronics",
        "servers", "storage devices", "pc maker",
    ],
    TechCategory.INTERNET: [
        "internet content", "digital advertising", "search engine", "social media",
        "e-commerce", "online marketplace", "streaming",
    ],
    TechCategory.FINTECH: [
        "fintech", "payments software", "trading platform", "neobank",
        "payment processor",
    ],
    TechCategory.DATA_AI: [
        "artificial intelligence", "machine learning", "ai platform", "llm",
        "generative ai", "data analytics", "big data",
    ],
}


_TIER_1_JURISDICTIONS = {
    "united states", "usa", "canada", "united kingdom", "uk", "ireland",
    "germany", "france", "netherlands", "sweden", "denmark", "finland",
    "norway", "switzerland", "luxembourg", "belgium", "austria",
    "australia", "new zealand", "japan", "south korea", "singapore",
    "israel", "taiwan",
}

_TIER_2_JURISDICTIONS = {
    "spain", "portugal", "italy", "poland", "czech republic", "estonia",
    "latvia", "lithuania", "hungary", "greece", "cyprus",
    "hong kong", "india", "brazil", "mexico", "south africa", "chile",
    "uruguay", "turkey",
}


def classify_stage(description: Optional[str], revenue: Optional[float],
                   info: Optional[dict] = None) -> CompanyStage:
    if description is None:
        description = ""
    desc_lower = description.lower()

    rev = revenue or 0
    info = info or {}
    profit_margin = info.get("profitMargins")
    growth = info.get("revenueGrowth")

    if rev < 10_000_000 and (growth is None or growth < 0.10):
        return CompanyStage.STARTUP

    for stage in [CompanyStage.PLATFORM, CompanyStage.MATURE, CompanyStage.SCALE,
                  CompanyStage.GROWTH, CompanyStage.STARTUP]:
        for kw in _STAGE_KEYWORDS[stage]:
            if kw.lower() in desc_lower:
                return stage

    mcap = info.get("marketCap") or 0
    if mcap >= 200_000_000_000:
        return CompanyStage.PLATFORM
    if profit_margin is not None and profit_margin > 0.20 and mcap >= 10_000_000_000:
        return CompanyStage.MATURE
    if growth is not None and growth > 0.30:
        return CompanyStage.GROWTH
    if rev >= 500_000_000:
        return CompanyStage.SCALE
    return CompanyStage.GROWTH


def classify_category(description: Optional[str],
                      industry: Optional[str] = None) -> TechCategory:
    import re
    text = ((description or "") + " " + (industry or "")).lower()
    scores: dict[TechCategory, int] = {}
    for cat, keywords in _CATEGORY_KEYWORDS.items():
        count = 0
        for kw in keywords:
            kw_lower = kw.lower()
            if len(kw_lower) <= 3:
                if re.search(r'\b' + re.escape(kw_lower) + r'\b', text):
                    count += 1
            else:
                if kw_lower in text:
                    count += 1
        if count > 0:
            scores[cat] = count
    if scores:
        return max(scores, key=scores.get)
    return TechCategory.OTHER


def classify_jurisdiction(country: Optional[str],
                          description: Optional[str] = None) -> JurisdictionTier:
    if not country:
        return JurisdictionTier.UNKNOWN
    c_lower = country.lower().strip()
    desc_lower = (description or "").lower()
    for j in _TIER_1_JURISDICTIONS:
        if j in c_lower or j in desc_lower:
            return JurisdictionTier.TIER_1
    for j in _TIER_2_JURISDICTIONS:
        if j in c_lower or j in desc_lower:
            return JurisdictionTier.TIER_2
    return JurisdictionTier.TIER_3


# Backwards-compat aliases — kept for callers that still import the old names.
classify_commodity = classify_category  # pragma: no cover
Commodity = TechCategory  # pragma: no cover
