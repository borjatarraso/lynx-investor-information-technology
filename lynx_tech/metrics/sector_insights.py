"""Information-Technology-focused sector and industry insights."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class SectorInsight:
    sector: str; overview: str; critical_metrics: list[str] = field(default_factory=list)
    key_risks: list[str] = field(default_factory=list); what_to_watch: list[str] = field(default_factory=list)
    typical_valuation: str = ""

@dataclass
class IndustryInsight:
    industry: str; sector: str; overview: str; critical_metrics: list[str] = field(default_factory=list)
    key_risks: list[str] = field(default_factory=list); what_to_watch: list[str] = field(default_factory=list)
    typical_valuation: str = ""

_SECTORS: dict[str, SectorInsight] = {}
_INDUSTRIES: dict[str, IndustryInsight] = {}

def _add_sector(sector, overview, cm, kr, wtw, tv):
    _SECTORS[sector.lower()] = SectorInsight(sector=sector, overview=overview, critical_metrics=cm, key_risks=kr, what_to_watch=wtw, typical_valuation=tv)

def _add_industry(industry, sector, overview, cm, kr, wtw, tv):
    _INDUSTRIES[industry.lower()] = IndustryInsight(industry=industry, sector=sector, overview=overview, critical_metrics=cm, key_risks=kr, what_to_watch=wtw, typical_valuation=tv)


_add_sector("Technology",
    "Information Technology is the highest-return-dispersion sector in public markets. Dominated by software (asset-light, high-margin, recurring revenue), semiconductors (cyclical, capex-heavy, winner-take-all), and hyperscale cloud (capital-intensive but durable moats). Valuation is driven by the trade-off between growth and cash-flow generation — the Rule of 40 is the canonical quality gate. Stock-based compensation (SBC) is a structural feature and creates real shareholder dilution even when GAAP results look non-cash.",
    ["Rule of 40 (growth + FCF margin)", "Gross margin (moat proxy)", "Net Revenue Retention (NRR)", "SBC / Revenue", "R&D intensity & efficiency", "FCF margin", "EV/Gross-Profit"],
    ["Rate-driven multiple compression for high-growth (duration sensitivity)", "SBC dilution eroding per-share compounding", "AI platform shifts obsoleting incumbents", "Regulatory scrutiny (antitrust, AI governance, privacy)", "Talent-cost escalation in an engineer-led cost base", "Export controls on advanced semiconductors"],
    ["NRR / GRR trends per cohort", "AI capex growth from hyperscalers", "Operating margin trajectory as growth decelerates", "Insider selling under 10b5-1 vs open-market buying", "Share buybacks offsetting SBC"],
    "EV/Gross-Profit and EV/ARR dominate for software. EV/EBITDA 15-25x for mature platforms; hyperscalers trade at premium. P/E only meaningful for profitable, cash-generative names.")

_add_sector("Communication Services",
    "Tech-adjacent sector covering internet platforms (Meta, Alphabet, Netflix). Shares many IT characteristics: platform economics, ad-driven or subscription business models.",
    ["DAU/MAU engagement", "ARPU", "Operating margin", "FCF margin"],
    ["Ad cycle sensitivity", "Platform regulation", "Content cost inflation"],
    ["User engagement trends", "Ad market health", "Subscriber growth vs churn"],
    "Similar to tech — EV/EBITDA 12-20x; FCF yield for mature platforms.")

# ── SaaS / Application Software ───────────────────────────────────
_add_industry("Software - Application", "Technology",
    "Application SaaS companies (CRM, ERP, workflow, vertical SaaS). The archetype of modern tech investing. Valued on EV/ARR, Rule-of-40, NRR, and gross margin. Subscription revenue creates high visibility. Winners exhibit 120%+ NRR and 75%+ gross margin.",
    ["ARR Growth (>30% hyper-growth)", "Gross Margin (target >75%)", "Rule of 40 (>40% passing)", "NRR (>120% expansion)", "Magic Number (>0.75)", "EV/ARR multiple"],
    ["Churn acceleration as TAM saturates", "Feature commoditization by platforms (Microsoft, Salesforce bundling)", "S&M efficiency collapse", "SBC dilution (often 10-20% of revenue)", "Horizontal vs vertical competitive dynamics"],
    ["NRR / GRR trajectory", "Billings vs reported revenue", "Free cash flow inflection timing", "Sales cycle length & deal sizes", "Enterprise vs SMB mix"],
    "EV/ARR: 8-15x at 30%+ growth; 4-8x at 15-25% growth; <3x if decelerating. Rule-of-40 gate applies above all else.")

_add_industry("Software - Infrastructure", "Technology",
    "Database, observability, DevOps, identity, middleware. Mission-critical infrastructure — higher switching costs than application SaaS. Tends to monetize via consumption (usage-based), which creates expansion potential but also exposure to customer cost-optimization.",
    ["ARR Growth", "Gross Margin (target >75%)", "NRR (consumption-based >120%)", "Operating margin trajectory", "RPO / Deferred Revenue coverage"],
    ["Customer optimization reducing consumption", "Open-source competition (Elastic, MongoDB models)", "Cloud-provider native services (AWS, Azure) competing directly", "Outage / security incidents destroying trust"],
    ["Consumption trends by cohort", "Enterprise logo growth", "Cloud partnership economics", "Net new ARR additions"],
    "EV/ARR 10-18x at high growth + high NRR; premium for mission-critical workloads; discount for open-source model risk.")

_add_industry("Information Technology Services", "Technology",
    "Consulting, systems integration, managed services, outsourcing (Accenture, Infosys, Cognizant). Lower margins and lower multiples than product software but more stable cyclical patterns. Revenue tied to enterprise IT spending.",
    ["Revenue Growth (6-15% typical)", "Operating Margin (12-20%)", "Utilization rate", "Bookings / Book-to-Bill", "Employee Productivity (rev/FTE $150-250k)"],
    ["Wage inflation (Indian offshoring arbitrage eroding)", "Slowdowns in enterprise IT budgets", "GenAI compressing billable-hours model", "Client concentration risk"],
    ["Bookings growth, large-deal momentum", "Discretionary vs run-the-business project mix", "Gen-AI adoption impact on services demand"],
    "EV/EBITDA 10-16x; P/E 15-22x; dividend payers at the mature end. Much lower than product software.")

# ── Cloud / Hyperscalers ──────────────────────────────────────────
_add_industry("Internet Content & Information", "Technology",
    "Search, social media, digital advertising, streaming. Platform economics with massive fixed-cost leverage. Valuation similar to SaaS but ad-cycle-sensitive rather than recurring-revenue anchored.",
    ["DAU/MAU and engagement", "ARPU", "Ad-revenue growth", "Operating margin", "Capex intensity"],
    ["Ad cycle reversals (fast multi-quarter downturns)", "Regulatory / antitrust actions", "Platform-shift risk (TikTok vs Meta)", "iOS privacy changes compressing attribution"],
    ["Ad pricing & impression growth", "AI capex intensity of hyperscaler investments", "Ad-share shifts between platforms"],
    "EV/EBITDA 10-18x; P/E 15-25x; FCF yield anchor for mature names.")

# ── Semiconductors ─────────────────────────────────────────────────
_add_industry("Semiconductors", "Technology",
    "Chipmakers (Nvidia, AMD, Broadcom, Intel, TSMC). Intensely cyclical — 3-5 year demand/capacity cycles. Winner-take-most dynamics (Nvidia in AI, TSMC in foundry, ASML in lithography). Capex-heavy: 15-25% of revenue. Export controls and geopolitics are now first-order drivers.",
    ["Revenue Growth", "Gross Margin (target >50%)", "Operating Margin (best-in-class >35%)", "Capex intensity", "Inventory days"],
    ["Cycle-downturn inventory correction (30-50% revenue drops)", "Geopolitical risk (Taiwan / China)", "Export controls on advanced nodes", "AI-capex normalization (after 2025 ramp)"],
    ["Design-win momentum", "Inventory normalization at end customers", "Semi-equipment order trends (leading indicator)", "Fab capacity additions"],
    "EV/EBITDA highly cycle-dependent. Mid-cycle: 12-18x. Trough: 8-10x. Peak AI capex beneficiaries may trade >30x on forward estimates.")

_add_industry("Semiconductor Equipment & Materials", "Technology",
    "ASML, Applied Materials, Lam Research, KLA, EDA vendors (Synopsys, Cadence). Shovel-sellers to chipmakers. Often less volatile than pure chipmakers. Monopoly positions in EUV lithography and EDA drive high margins.",
    ["Revenue Growth", "Gross Margin", "Bookings / Book-to-Bill", "Backlog duration", "R&D intensity"],
    ["Concentrated customer base (top-5 foundries = 80% of revenue)", "Geopolitical restrictions limiting addressable market", "Capex cycle mismatch", "Technology shifts (EUV, gate-all-around, 3D-NAND)"],
    ["Equipment order trends", "ASML system shipments", "Customer capex guidance"],
    "EV/EBITDA 18-28x for premium names (ASML, Cadence, Synopsys). P/E 25-40x.")

# ── Cybersecurity ─────────────────────────────────────────────────
_add_industry("Software - Security", "Technology",
    "Cybersecurity software (CrowdStrike, Palo Alto, Fortinet, Zscaler). A must-have spend category — even in budget cuts, security holds up. Consolidation trend favors platform vendors over point-solutions.",
    ["ARR Growth (>25%)", "Gross Margin (>70%)", "NRR (>115%)", "Platform vs point-solution positioning", "Rule of 40"],
    ["Major breach / outage destroying trust (CrowdStrike July 2024)", "Platform consolidation compressing point-solution players", "AI-driven commoditization of endpoint security"],
    ["Breach incident recovery trajectory", "Platform consolidation wins", "Government / critical-infrastructure mandates"],
    "EV/ARR 10-15x at 25%+ growth + 115%+ NRR; premium for category leadership; discount for sub-scale specialists.")

# ── Fintech Software ──────────────────────────────────────────────
_add_industry("Software - Financial", "Technology",
    "Payment processors (Stripe-adjacent public names), trading platforms, core banking software (Temenos, Fiserv). Infrastructure-heavy fintech. Revenue tied to payment volumes + take rates.",
    ["Payment volume growth", "Take rate", "Operating margin", "Gross margin"],
    ["Take-rate compression from competition", "Banking-as-a-service regulatory scrutiny", "Recession-driven consumer spending softness"],
    ["Payment volume normalization post-2021 surge", "Fed funds rate impact on float income", "Interchange reform"],
    "EV/EBITDA 12-20x; EV/Revenue 5-10x for high-growth payments.")

# ── Hardware ──────────────────────────────────────────────────────
_add_industry("Computer Hardware", "Technology",
    "PCs, servers, storage, networking (Dell, HPE, NetApp, Arista, Cisco). Lower margins (20-45% gross) and lower multiples than software. Revenue tied to enterprise refresh cycles and hyperscaler capex.",
    ["Revenue Growth", "Gross Margin (20-45%)", "Operating margin", "Inventory days", "Capex intensity"],
    ["Commoditization pressure", "Hyperscaler in-housing (custom silicon + ODM)", "Component cost volatility", "Currency (large non-US exposure)"],
    ["Hyperscaler capex growth", "Enterprise refresh cycle timing", "Gross margin trends"],
    "EV/EBITDA 8-14x; P/E 15-22x; dividend payers common.")

_add_industry("Consumer Electronics", "Technology",
    "Apple-like consumer-facing hardware + services. Apple is a category unto itself given its scale. Most others (Sony, Garmin) trade as hardware cyclicals.",
    ["Revenue Growth", "Services Mix (higher = higher multiple)", "Gross Margin", "Operating margin"],
    ["Consumer spending cycles", "Device refresh slowdown", "China market exposure"],
    ["Services revenue growth", "Installed base monetization"],
    "Apple: 25-35x P/E (premium for services compounding). Others: 10-15x P/E as hardware cyclicals.")


def get_sector_insight(sector: str | None) -> SectorInsight | None:
    return _SECTORS.get(sector.lower()) if sector else None

def get_industry_insight(industry: str | None) -> IndustryInsight | None:
    return _INDUSTRIES.get(industry.lower()) if industry else None

def list_sectors() -> list[str]:
    return sorted(s.sector for s in _SECTORS.values())

def list_industries() -> list[str]:
    return sorted(i.industry for i in _INDUSTRIES.values())
