"""Metric explanations for Lynx Information Technology Analysis."""

from __future__ import annotations
from lynx_tech.models import MetricExplanation

METRIC_EXPLANATIONS: dict[str, MetricExplanation] = {}

def _add(key, full_name, description, why_used, formula, category):
    METRIC_EXPLANATIONS[key] = MetricExplanation(key=key, full_name=full_name, description=description,
                                                  why_used=why_used, formula=formula, category=category)

# ── Valuation ──────────────────────────────────────────────────────
_add("pe_trailing", "Price-to-Earnings (TTM)", "Compares stock price to trailing 12-month earnings per share.", "Traditional anchor for mature tech. Less meaningful for growth-stage tech with negative earnings.", "P/E = Price / EPS (TTM)", "valuation")
_add("pe_forward", "Forward P/E", "Forward P/E based on next-year analyst EPS estimates.", "Useful when earnings are improving or transitioning to profitability.", "Fwd P/E = Price / Est. EPS (next FY)", "valuation")
_add("pb_ratio", "Price-to-Book", "Compares stock price to book value per share.", "Asset-light tech often trades far above book. Most useful at micro/small cap where tangible assets matter.", "P/B = Price / Book Value per Share", "valuation")
_add("ps_ratio", "Price-to-Sales", "Compares market cap to revenue.", "Dominant anchor for pre-profit tech. Benchmark: SaaS 5-15x, Hardware 1-3x, IT Services 1-2x.", "P/S = Market Cap / Revenue", "valuation")
_add("p_fcf", "Price-to-Free-Cash-Flow", "Compares market cap to free cash flow.", "The best cash-economics anchor for cash-generative software.", "P/FCF = Market Cap / FCF", "valuation")
_add("ev_ebitda", "Enterprise Value / EBITDA", "Capital-structure-neutral earnings multiple.", "Cross-company comparison for mature tech. Benchmark: 15-25x normal, <12x cheap, >30x expensive.", "EV/EBITDA = (Market Cap + Debt - Cash) / EBITDA", "valuation")
_add("ev_revenue", "Enterprise Value / Revenue", "EV divided by revenue.", "Core multiple for growth tech. SaaS median ~6-10x; hyperscaler growth premium >15x.", "EV/Revenue = EV / Revenue", "valuation")
_add("ev_gross_profit", "EV / Gross Profit", "EV divided by gross profit — a margin-adjusted variant of EV/Sales.", "Superior to EV/Sales for software: strips out cost-of-revenue differences between hosted SaaS and services.", "EV / GP = EV / (Revenue - COGS)", "valuation")
_add("ev_to_arr", "EV / ARR", "Enterprise value divided by Annual Recurring Revenue (approximated when not disclosed).", "The SaaS-native valuation metric. Growth-adjusted benchmarks: 8-15x at 30%+ ARR growth.", "EV/ARR = EV / ARR  (approx: revenue + Δdeferred rev)", "valuation")
_add("ev_per_employee", "EV per Employee", "Enterprise value divided by full-time employees.", "Productivity-adjusted scale check. Top-tier SaaS >$2M/employee; IT services $250-500k/employee.", "EV / Employees", "valuation")
_add("rule_of_40_adj_multiple", "R40-Adjusted EV/Revenue", "EV/Revenue divided by Rule-of-40 sum normalized to 40.", "Normalizes valuation by quality of growth + profitability — fair comparison across growth profiles.", "EV/Rev / (Rule40 / 40)", "valuation")
_add("peg_ratio", "PEG Ratio", "P/E adjusted by growth rate.", "Useful for mature tech with durable growth. PEG <1 suggests undervaluation vs growth.", "PEG = P/E / Annual EPS growth rate", "valuation")
_add("cash_to_market_cap", "Cash / Market Cap", "How much of market cap is backed by cash on the balance sheet.", "Critical for pre-profit tech. Apple/Alphabet historically at 10-20%; startups sometimes >50%.", "Cash / Market Cap", "valuation")

# ── Profitability ──────────────────────────────────────────────────
_add("roe", "Return on Equity", "Profit per dollar of equity.", "For mature tech, ROE >20% signals strong profitability.", "ROE = Net Income / Equity", "profitability")
_add("roic", "Return on Invested Capital", "Return on all invested capital.", "Best moat evidence — >15% ROIC compound over years is a quality hallmark (Buffett test).", "ROIC = NOPAT / Invested Capital", "profitability")
_add("gross_margin", "Gross Margin", "Revenue remaining after cost of revenue.", "THE defining moat metric in tech. SaaS target >75%, hardware 30-50%, IT services 20-35%.", "Gross Margin = (Revenue - COGS) / Revenue", "profitability")
_add("operating_margin", "Operating Margin", "Revenue remaining after all operating expenses.", "Benchmark: Mature platforms >25%, scale-up 5-15%, hyper-growth often negative.", "Operating Margin = Operating Income / Revenue", "profitability")
_add("net_margin", "Net Margin", "Bottom-line profitability.", "Traditional profitability anchor; distorted by SBC in tech.", "Net Margin = Net Income / Revenue", "profitability")
_add("fcf_margin", "FCF Margin", "Free cash flow as % of revenue.", "Better than net margin for tech. Best-in-class SaaS >30%; healthy 15-25%.", "FCF Margin = FCF / Revenue", "profitability")
_add("ebitda_margin", "EBITDA Margin", "EBITDA / revenue.", "Cyclicality-adjusted operating profit. >30% excellent for tech.", "EBITDA Margin = EBITDA / Revenue", "profitability")
_add("rule_of_40", "Rule of 40 (FCF variant)", "Revenue growth % + FCF margin %.", "The canonical SaaS quality metric. >40% passing, >60% best-in-class, <20% failing.", "Rule40 = Rev Growth % + FCF Margin %", "profitability")
_add("rule_of_40_ebitda", "Rule of 40 (EBITDA variant)", "Revenue growth % + EBITDA margin %.", "Useful for pre-FCF-positive growth tech — tracks same trade-off vs EBITDA.", "Rule40(EBITDA) = Rev Growth % + EBITDA Margin %", "profitability")
_add("magic_number", "Magic Number", "Sales efficiency: (ΔARR × 4) / S&M spend.", "A company-specific LTV/CAC proxy. >1 = invest more in sales; <0.5 = fix sales motion first.", "Magic Number = (ΔARR × 4) / S&M", "profitability")
_add("sbc_to_revenue", "SBC / Revenue", "Stock-Based Compensation as % of revenue.", "Measures non-cash dilution drag. Benchmarks: <5% low, 5-10% moderate, 10-20% high, >20% concerning.", "SBC / Revenue", "profitability")
_add("sbc_to_fcf", "SBC / FCF", "Stock-Based Compensation as % of free cash flow.", "Truer picture of shareholder dilution — if SBC > FCF, 'cash flow' is partly paper.", "SBC / FCF", "profitability")
_add("gaap_vs_adj_gap", "GAAP vs Adjusted Gap", "Spread between GAAP operating income and non-GAAP (adjusted) operating income.", "Large gap is a red flag — SBC being excluded is one reason.", "(Adj Op Inc - GAAP Op Inc) / Revenue", "profitability")

# ── Solvency ───────────────────────────────────────────────────────
_add("debt_to_equity", "Debt / Equity", "Debt financing vs equity financing.", "Tech is typically low-leverage. >1.0x in tech is unusual and may indicate aggressive buybacks.", "D/E = Total Debt / Equity", "solvency")
_add("current_ratio", "Current Ratio", "Short-term asset coverage.", ">2 healthy for tech; <1 critical.", "Current Ratio = Current Assets / Current Liabilities", "solvency")
_add("interest_coverage", "Interest Coverage", "Ability to pay interest from operating income.", ">6 comfortable, <2 dangerous. Low for early-stage tech with debt.", "Operating Income / Interest Expense", "solvency")
_add("altman_z_score", "Altman Z-Score", "Bankruptcy probability predictor.", "Z >2.99: Safe. 1.81-2.99: Grey. <1.81: Distress. Less meaningful for early-stage tech.", "Z = 1.2(WC/TA) + 1.4(RE/TA) + 3.3(EBIT/TA) + 0.6(MV/TL) + 1.0(Sales/TA)", "solvency")
_add("cash_burn_rate", "Cash Burn Rate", "Annual rate of cash consumption.", "Critical for pre-FCF tech. Determines runway to profitability.", "Operating Cash Flow (negative)", "solvency")
_add("cash_runway_years", "Cash Runway", "Years of operation at current burn rate.", "<1yr = imminent financing. >3yr = comfortable. Startups target 18-24 months.", "Total Cash / Annual Burn", "solvency")
_add("burn_as_pct_of_market_cap", "Burn % of Market Cap", "How fast the company burns shareholder value.", "<5%/yr is healthy. >10%/yr is a serious dilution setup.", "|Burn| / Market Cap", "solvency")
_add("capex_to_revenue", "Capex / Revenue", "Capital intensity.", "Asset-light SaaS <5%; hyperscalers 15-25%; semi >20%; pure software <2%.", "Capex / Revenue", "solvency")
_add("rpo_coverage", "RPO / Revenue Coverage", "Remaining Performance Obligations vs annual revenue.", "Forward-visibility proxy. >100% means more than a year of backlog.", "Deferred Revenue / Revenue", "solvency")
_add("deferred_revenue_ratio", "Deferred Revenue Ratio", "Deferred revenue vs annual revenue.", "Subscription billing strength. Higher = stronger subscription revenue visibility.", "Deferred Revenue / Revenue", "solvency")
_add("goodwill_to_assets", "Goodwill / Total Assets", "Goodwill from acquisitions as share of assets.", ">40% is impairment-risk territory — acquisition-driven growth is fragile if deals don't work.", "Goodwill / Total Assets", "solvency")

# ── Growth ─────────────────────────────────────────────────────────
_add("revenue_growth_yoy", "Revenue Growth (YoY)", "Annual revenue change.", "THE primary growth metric. Durable >20% in mature tech is rare & valuable.", "(Rev - Rev_Prior) / |Rev_Prior|", "growth")
_add("revenue_cagr_3y", "Revenue CAGR (3Y)", "3-year compound revenue growth.", "Smooths COVID/cycle noise. >30% = hyper-growth, 15-30% = healthy, <5% = mature.", "CAGR = (End / Start)^(1/3) - 1", "growth")
_add("earnings_growth_yoy", "Earnings Growth (YoY)", "Annual net income change.", "Drives mature tech valuation. Distorted by SBC changes.", "(NI - NI_Prior) / |NI_Prior|", "growth")
_add("shares_growth_yoy", "Share Dilution (YoY)", "Annual change in shares outstanding.", "Tech dilutes via RSUs and acquisitions. <3%/yr acceptable; >6%/yr concerning.", "(Shares - Shares_Prior) / Shares_Prior", "growth")
_add("arr_growth_yoy", "ARR Growth (YoY)", "Annual Recurring Revenue growth.", "The true growth signal for subscription businesses. Approximated here as revenue + deferred-revenue growth.", "(ARR - ARR_Prior) / ARR_Prior", "growth")
_add("net_revenue_retention", "Net Revenue Retention", "% of cohort revenue retained after expansion & churn.", "The GOAT metric. >120% = expansion economy; <100% = churning. Best-in-class SaaS: 130%+.", "NRR = (Starting ARR + Expansion - Contraction - Churn) / Starting ARR", "growth")
_add("gross_revenue_retention", "Gross Revenue Retention", "% of cohort revenue retained before expansion.", "Pure retention signal. >90% = sticky product; <80% = product-market-fit risk.", "GRR = (Starting ARR - Contraction - Churn) / Starting ARR", "growth")
_add("rd_intensity", "R&D Intensity", "R&D as % of revenue.", "Innovation commitment. SaaS 15-30%, semi 15-20%, mega-cap platforms 10-15%.", "R&D / Revenue", "growth")
_add("rd_growth_yoy", "R&D Growth (YoY)", "Year-over-year R&D spending change.", "Early warning for innovation slowdown.", "(R&D - R&D_Prior) / R&D_Prior", "growth")
_add("sales_marketing_intensity", "S&M Intensity", "Sales & marketing as % of revenue.", "Growth-mode SaaS runs 30-60%; mature software 15-25%.", "S&M / Revenue", "growth")
_add("employee_growth_yoy", "Employee Growth (YoY)", "Headcount change.", "Growth leader but watch productivity — employees should lead revenue, not lag.", "(Emp - Emp_Prior) / Emp_Prior", "growth")
_add("revenue_per_employee", "Revenue per Employee", "Productivity metric.", "Top-tier software: $500k-$2M/employee. Hardware: $300-500k. Services: $150-250k.", "Revenue / Employees", "growth")

# ── Tech Quality ───────────────────────────────────────────────────
_add("quality_score", "Tech Quality Score", "Composite IT-quality score (0-100).", "Weighted: Moat (20), Rule-of-40 (20), Financial Position (15), Dilution/SBC (15), R&D Efficiency (10), Unit Econ (10), Revenue Predictability (10). >75 elite, <30 weak.", "Weighted sum of 7 IT-specific axes", "tech_quality")
_add("moat_assessment", "Moat Assessment", "Qualitative moat classification tied to gross margin + category.", "Network effects, switching costs, IP, scale, brand — the 5 Buffett moats.", "Derived from GM %, category, NRR", "tech_quality")
_add("rule_of_40_assessment", "Rule-of-40 Verdict", "Assessment of Rule-of-40 score.", "Pass/fail grade used by public-market SaaS investors (Bessemer/Meritech benchmarks).", "Rule40 band", "tech_quality")
_add("unit_economics", "Unit Economics", "Summary of magic number, CAC payback, NRR.", "Evaluates whether growth is economically sustainable, not just fueled by burn.", "Magic#, CAC payback, NRR", "tech_quality")
_add("sbc_risk_assessment", "SBC Risk", "Stock-based compensation risk framing.", "Tech dilution risk category: Contained / Moderate / High / Severe.", "SBC / Revenue band", "tech_quality")
_add("platform_position", "Platform Position", "Scale/network/ecosystem position.", "A Meta/Alphabet/AWS-scale platform compounds for decades; a commoditized vendor doesn't.", "Tier + category analysis", "tech_quality")
_add("founder_led", "Founder-Led Signal", "Founder or strong insider control.", "Founder-led tech historically outperforms. Look for 10%+ insider ownership.", "Insider ownership % band", "tech_quality")

# ── Share Structure ────────────────────────────────────────────────
_add("shares_outstanding", "Shares Outstanding", "Basic shares currently issued.", "Baseline for per-share metrics.", "—", "share_structure")
_add("fully_diluted_shares", "Fully Diluted Shares", "Shares + RSUs + options + warrants.", "True dilution floor — use this for per-share calculations.", "Basic + RSUs + Options + Warrants", "share_structure")
_add("insider_ownership_pct", "Insider Ownership %", "% of shares held by insiders/founders.", ">10% is meaningful alignment; >20% is founder-level skin in the game.", "Insider Shares / Total Shares", "share_structure")
_add("dual_class_structure", "Dual-Class Structure", "Whether insiders hold super-voting shares.", "Common in tech (Meta, Alphabet). Locks in founder control — governance trade-off.", "Voting class structure", "share_structure")
_add("sbc_overhang_risk", "SBC Overhang Risk", "Forward dilution pressure from future equity comp grants.", "Large overhangs depress EPS growth even when revenue compounds.", "Cumulative SBC run-rate vs float", "share_structure")

# ── Efficiency ─────────────────────────────────────────────────────
_add("rule_of_x_score", "Rule of X (Altimeter)", "Revenue growth × (1 + FCF margin).", "Altimeter's multiplicative refinement of Rule-of-40 — emphasizes compounding of growth × profitability.", "Growth × (1 + FCF margin)", "efficiency")
_add("cac_payback_months", "CAC Payback (months)", "Months to recover customer acquisition cost via gross profit.", "Best-in-class SaaS <18 months; healthy <24 months; >36 months = fix the motion.", "S&M / (Quarterly GP Delta × 3)", "efficiency")
_add("fcf_conversion", "FCF Conversion", "FCF divided by net income.", ">1 = high-quality earnings; <0.8 = earnings may overstate cash.", "FCF / Net Income", "efficiency")

SECTION_EXPLANATIONS = {
    "profile": {"title": "Company Profile", "description": "Company identification, market cap tier, IT lifecycle stage, tech sub-category (SaaS/Cloud/Cybersecurity/Semi/etc.), and jurisdiction risk."},
    "valuation": {"title": "Valuation Metrics", "description": "Traditional + tech-specific valuation ratios. EV/Gross-Profit and EV/ARR are emphasized for software; P/FCF and EV/EBITDA for mature platforms; Cash-to-Market-Cap for startups."},
    "profitability": {"title": "Profitability Metrics", "description": "Margin analysis plus IT-specific: Rule-of-40, Magic Number (sales efficiency), SBC/Revenue, SBC/FCF. Rule-of-40 is the canonical SaaS quality gate."},
    "solvency": {"title": "Solvency & Survival", "description": "Balance sheet strength, cash runway, burn rate, deferred revenue (forward visibility), goodwill-to-assets (M&A impairment risk), and capex intensity (asset vs asset-light classification)."},
    "growth": {"title": "Growth & Retention", "description": "Revenue + ARR growth, R&D intensity & growth, employee & productivity trends, S&M efficiency. NRR and GRR slots reserved for company-disclosed metrics."},
    "share_structure": {"title": "Share Structure", "description": "Basic/fully-diluted shares, insider & institutional ownership, dual-class flag, SBC overhang risk — tech-specific dilution concerns."},
    "tech_quality": {"title": "Tech Quality Assessment", "description": "IT-specialized scoring. Evaluates moat quality, Rule-of-40, unit economics, financial position, R&D efficiency, dilution/SBC risk, and revenue predictability."},
    "intrinsic_value": {"title": "Intrinsic Value Estimates", "description": "Multiple methods adapted by stage. Mature/Platform: DCF. Scale/Growth: EV/Gross-Profit peer multiples. Startup: Cash + option value. Reverse DCF shows the growth rate embedded in the price."},
    "conclusion": {"title": "Assessment Conclusion", "description": "Weighted scoring across 5 categories with weights adapted by tier AND IT lifecycle stage. Includes a 10-point tech screening checklist evaluating the key IT quality criteria."},
}

CONCLUSION_METHODOLOGY = {
    "overall": {"title": "Conclusion Methodology", "description": "Score is a weighted average of 5 categories (valuation, profitability, solvency, growth, tech quality). Weights vary by company tier AND IT lifecycle stage. Startups weight solvency at 35-40% and tech quality at 30%. Mature platforms use balanced weights. Verdicts: Strong Buy (>=75), Buy (>=60), Hold (>=45), Caution (>=30), Avoid (<30)."},
    "valuation": {"title": "Valuation Score", "description": "Starts at 50. Adjusted by EV/Gross-Profit, P/FCF, Rule-of-40-adjusted EV/Revenue, cash-to-market-cap (bonus for startups), and P/E where applicable."},
    "profitability": {"title": "Profitability Score", "description": "Starts at 50. Rule-of-40, gross margin vs category benchmark, FCF margin, SBC penalty. Early-stage startups are not penalized for lack of profit."},
    "solvency": {"title": "Solvency Score", "description": "Starts at 50. Debt/equity, current ratio, cash runway, burn rate, goodwill-to-assets. Startups are penalized heavily for any debt. Cash runway <1 year = -25 points."},
    "tech_quality": {"title": "Tech Quality Score", "description": "Composite of moat/gross-margin (20pts), Rule-of-40 (20pts), financial position (15pts), dilution/SBC risk (15pts), R&D efficiency (10pts), unit economics (10pts), revenue predictability (10pts)."},
}

def get_explanation(key): return METRIC_EXPLANATIONS.get(key)
def get_section_explanation(section): return SECTION_EXPLANATIONS.get(section)
def get_conclusion_explanation(category=None): return CONCLUSION_METHODOLOGY.get(category or "overall")
def list_metrics(category=None):
    metrics = list(METRIC_EXPLANATIONS.values())
    return [m for m in metrics if m.category == category] if category else metrics
