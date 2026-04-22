"""IT-focused report synthesis engine.

Generates the weighted overall score + verdict + strengths/risks for an
Information Technology company. Weights adapt by both tier and IT lifecycle
stage. Screening checklist covers the 10 most important IT quality criteria.
"""

from __future__ import annotations

import math

from lynx_tech.models import AnalysisConclusion, AnalysisReport, CompanyStage, CompanyTier, JurisdictionTier


def _safe(val, default: float = 0.0) -> float:
    if val is None or isinstance(val, bool):
        return default
    try:
        f = float(val)
        return default if (math.isnan(f) or math.isinf(f)) else f
    except (TypeError, ValueError):
        return default


# Weights: (valuation, profitability, solvency, growth, tech_quality)
_WEIGHTS = {
    # Platforms & Mature: traditional multi-factor analysis
    (CompanyStage.PLATFORM, CompanyTier.MEGA):  (0.25, 0.25, 0.10, 0.15, 0.25),
    (CompanyStage.PLATFORM, CompanyTier.LARGE): (0.25, 0.25, 0.10, 0.15, 0.25),
    (CompanyStage.MATURE, CompanyTier.MEGA):    (0.25, 0.25, 0.10, 0.15, 0.25),
    (CompanyStage.MATURE, CompanyTier.LARGE):   (0.25, 0.25, 0.10, 0.15, 0.25),
    (CompanyStage.MATURE, CompanyTier.MID):     (0.20, 0.20, 0.15, 0.20, 0.25),

    # Scale-up: growth still matters but quality is rising
    (CompanyStage.SCALE, CompanyTier.LARGE): (0.20, 0.20, 0.15, 0.20, 0.25),
    (CompanyStage.SCALE, CompanyTier.MID):   (0.15, 0.15, 0.20, 0.25, 0.25),
    (CompanyStage.SCALE, CompanyTier.SMALL): (0.15, 0.10, 0.25, 0.25, 0.25),

    # Hyper-growth: growth + quality dominate, profitability secondary
    (CompanyStage.GROWTH, CompanyTier.LARGE): (0.15, 0.15, 0.15, 0.30, 0.25),
    (CompanyStage.GROWTH, CompanyTier.MID):   (0.15, 0.10, 0.20, 0.30, 0.25),
    (CompanyStage.GROWTH, CompanyTier.SMALL): (0.10, 0.10, 0.25, 0.30, 0.25),
    (CompanyStage.GROWTH, CompanyTier.MICRO): (0.05, 0.05, 0.30, 0.30, 0.30),

    # Startup: survival & quality dominate
    (CompanyStage.STARTUP, CompanyTier.SMALL): (0.10, 0.05, 0.35, 0.20, 0.30),
    (CompanyStage.STARTUP, CompanyTier.MICRO): (0.05, 0.05, 0.40, 0.15, 0.35),
    (CompanyStage.STARTUP, CompanyTier.NANO):  (0.05, 0.05, 0.40, 0.15, 0.35),
}
_DEFAULT_WEIGHTS = (0.15, 0.15, 0.20, 0.25, 0.25)


def generate_conclusion(report: AnalysisReport) -> AnalysisConclusion:
    c = AnalysisConclusion()
    tier, stage = report.profile.tier, report.profile.stage

    val_score = _score_valuation(report)
    prof_score = _score_profitability(report)
    solv_score = _score_solvency(report)
    grow_score = _score_growth(report)
    quality_score = _safe(report.tech_quality.quality_score) if report.tech_quality else 0

    c.category_scores = {"valuation": round(val_score, 1), "profitability": round(prof_score, 1),
                         "solvency": round(solv_score, 1), "growth": round(grow_score, 1),
                         "tech_quality": round(quality_score, 1)}

    w = _WEIGHTS.get((stage, tier), _DEFAULT_WEIGHTS)
    c.overall_score = round(val_score * w[0] + prof_score * w[1] + solv_score * w[2] + grow_score * w[3] + quality_score * w[4], 1)
    c.verdict = _verdict(c.overall_score)
    c.category_summaries = _build_summaries(report)
    c.strengths = _find_strengths(report)
    c.risks = _find_risks(report)
    c.summary = _build_narrative(report, c)
    c.tier_note = _tier_note(tier)
    c.stage_note = _stage_note(stage)
    c.screening_checklist = _tech_screening(report)
    return c


def _verdict(score: float) -> str:
    if score >= 75: return "Strong Buy"
    if score >= 60: return "Buy"
    if score >= 45: return "Hold"
    if score >= 30: return "Caution"
    return "Avoid"


def _score_valuation(r: AnalysisReport) -> float:
    v = r.valuation
    if v is None:
        return 50.0
    score = 50.0
    stage = r.profile.stage

    # EV / Gross Profit — the headline tech anchor
    evgp = _safe(v.ev_gross_profit, None)
    if evgp is not None:
        if evgp < 10: score += 20
        elif evgp < 18: score += 10
        elif evgp < 28: score -= 5
        else: score -= 15

    # P/FCF secondary
    pfcf = _safe(v.p_fcf, None)
    if pfcf is not None:
        if pfcf < 15: score += 15
        elif pfcf < 25: score += 8
        elif pfcf > 45: score -= 10

    # Traditional P/E for mature tech only
    if stage in (CompanyStage.MATURE, CompanyStage.PLATFORM):
        pe = _safe(v.pe_trailing, None)
        if pe is not None and pe > 0:
            if pe < 20: score += 10
            elif pe < 30: score += 3
            elif pe > 50: score -= 10

    # Rule-of-40-adjusted EV/Revenue (lower is better)
    r40a = _safe(v.rule_of_40_adj_multiple, None)
    if r40a is not None:
        if r40a < 6: score += 10
        elif r40a < 12: score += 4
        elif r40a > 20: score -= 8

    # Cash-to-market-cap bonus for startups / small caps
    ctm = _safe(v.cash_to_market_cap, None)
    if ctm is not None and stage == CompanyStage.STARTUP:
        if ctm > 0.50: score += 12
        elif ctm > 0.25: score += 6

    return max(0, min(100, score))


def _score_profitability(r: AnalysisReport) -> float:
    p = r.profitability
    stage = r.profile.stage

    # Startup / hyper-growth not penalized for lack of profit — profitability weighted lower in overall mix.
    if p is None:
        return 50.0
    score = 50.0

    # Rule of 40 is the anchor
    r40 = _safe(p.rule_of_40, None)
    if r40 is None:
        r40 = _safe(p.rule_of_40_ebitda, None)
    if r40 is not None:
        if r40 >= 60: score += 25
        elif r40 >= 40: score += 15
        elif r40 >= 20: score += 3
        else: score -= 15

    # Gross margin — moat proxy
    gm = _safe(p.gross_margin, None)
    if gm is not None:
        if gm >= 0.75: score += 15
        elif gm >= 0.55: score += 8
        elif gm >= 0.35: score += 2
        else: score -= 10

    # SBC penalty — any stage
    sbc = _safe(p.sbc_to_revenue, None)
    if sbc is not None:
        if sbc < 0.05: score += 5
        elif sbc < 0.10: score += 0
        elif sbc < 0.20: score -= 8
        else: score -= 18

    # Net margin / FCF margin for mature tech
    if stage in (CompanyStage.MATURE, CompanyStage.PLATFORM):
        nm = _safe(p.net_margin, None)
        if nm is not None:
            if nm > 0.25: score += 8
            elif nm > 0.10: score += 3
            elif nm < 0: score -= 10
        fcf = _safe(p.fcf_margin, None)
        if fcf is not None:
            if fcf > 0.25: score += 8
            elif fcf > 0.15: score += 3
            elif fcf < 0: score -= 10

    return max(0, min(100, score))


def _score_solvency(r: AnalysisReport) -> float:
    s = r.solvency
    if s is None:
        return 50.0
    score = 50.0
    stage = r.profile.stage

    de = _safe(s.debt_to_equity, None)
    if de is not None:
        if stage == CompanyStage.STARTUP:
            if de < 0.1: score += 10
            elif de > 0.5: score -= 20
        else:
            if de < 0.5: score += 8
            elif de > 2: score -= 15

    cr = _safe(s.current_ratio, None)
    if cr is not None:
        if cr > 2.5: score += 10
        elif cr > 1.5: score += 5
        elif cr < 1: score -= 15

    # Cash runway (critical for startups/hyper-growth)
    burn = _safe(s.cash_burn_rate, None)
    if burn is not None and burn < 0:
        runway = _safe(s.cash_runway_years, None)
        if runway is not None:
            if runway > 3: score += 5
            elif runway < 1: score -= 25
            elif runway < 1.5: score -= 15
            elif runway < 2: score -= 5

    bpct = _safe(s.burn_as_pct_of_market_cap, None)
    if bpct is not None and bpct > 0.10:
        score -= 12

    # Goodwill-to-assets penalty (M&A-heavy impairment risk)
    gta = _safe(s.goodwill_to_assets, None)
    if gta is not None:
        if gta > 0.50: score -= 10
        elif gta > 0.35: score -= 5

    # Deferred revenue / RPO bonus — forward visibility
    drr = _safe(s.deferred_revenue_ratio, None)
    if drr is not None and drr > 0.25:
        score += 5

    return max(0, min(100, score))


def _score_growth(r: AnalysisReport) -> float:
    g = r.growth
    if g is None:
        return 50.0
    score = 50.0
    stage = r.profile.stage

    rg = _safe(g.revenue_growth_yoy, None)
    if rg is not None:
        if stage in (CompanyStage.STARTUP, CompanyStage.GROWTH):
            if rg > 0.40: score += 20
            elif rg > 0.25: score += 12
            elif rg > 0.15: score += 5
            elif rg < 0: score -= 15
        else:
            if rg > 0.20: score += 15
            elif rg > 0.05: score += 5
            elif rg < -0.05: score -= 15

    arr_g = _safe(g.arr_growth_yoy, None)
    if arr_g is not None and arr_g > 0.30:
        score += 8

    # Share dilution penalty
    dil = _safe(g.shares_growth_yoy, None)
    if dil is not None:
        if dil < 0: score += 8  # buybacks
        elif dil < 0.02: score += 4
        elif dil > 0.06: score -= 10
        elif dil > 0.10: score -= 18

    # R&D intensity — a proxy for innovation commitment
    rd = _safe(g.rd_intensity, None)
    if rd is not None:
        if rd >= 0.15 and stage in (CompanyStage.STARTUP, CompanyStage.GROWTH, CompanyStage.SCALE):
            score += 5
        elif rd < 0.03:
            score -= 5

    return max(0, min(100, score))


def _tech_screening(r: AnalysisReport) -> dict:
    """Ten-point Information Technology screening checklist."""
    checks: dict = {}
    p, s, g, ss, tq = r.profitability, r.solvency, r.growth, r.share_structure, r.tech_quality
    stage = r.profile.stage

    # 1. Rule of 40 pass (≥40%)
    r40 = _safe(p.rule_of_40, None) if p else None
    if r40 is None:
        r40 = _safe(p.rule_of_40_ebitda, None) if p else None
    checks["rule_of_40_pass"] = r40 >= 40 if r40 is not None else None

    # 2. Gross margin > 60%
    gm = _safe(p.gross_margin, None) if p else None
    checks["moat_gross_margin"] = gm > 0.60 if gm is not None else None

    # 3. SBC < 15% of revenue
    sbc = _safe(p.sbc_to_revenue, None) if p else None
    checks["sbc_contained"] = sbc < 0.15 if sbc is not None else None

    # 4. Share dilution <5%/yr
    dil = _safe(g.shares_growth_yoy, None) if g else None
    checks["low_dilution"] = dil < 0.05 if dil is not None else None

    # 5. Runway / solvency
    runway = _safe(s.cash_runway_years, None) if s else None
    if runway is not None:
        checks["cash_runway_18m"] = runway > 1.5
    elif s and _safe(s.cash_burn_rate, None) is not None and s.cash_burn_rate >= 0:
        checks["cash_runway_18m"] = True
    else:
        checks["cash_runway_18m"] = None

    # 6. R&D intensity > 10%
    rd = _safe(g.rd_intensity, None) if g else None
    checks["healthy_rd_spend"] = rd >= 0.10 if rd is not None else None

    # 7. No excessive debt
    de = _safe(s.debt_to_equity, None) if s else None
    if de is not None:
        checks["no_excessive_debt"] = de < 0.5 if stage == CompanyStage.STARTUP else de < 1.5
    else:
        checks["no_excessive_debt"] = None

    # 8. Insider ownership OR founder-led
    insider = _safe(ss.insider_ownership_pct, None) if ss else None
    checks["insider_alignment"] = insider > 0.05 if insider is not None else None

    # 9. Revenue growth positive
    rg = _safe(g.revenue_growth_yoy, None) if g else None
    checks["positive_revenue_growth"] = rg > 0 if rg is not None else None

    # 10. Tier 1/2 jurisdiction
    jt = r.profile.jurisdiction_tier
    checks["tier_1_2_jurisdiction"] = jt in (JurisdictionTier.TIER_1, JurisdictionTier.TIER_2) if jt != JurisdictionTier.UNKNOWN else None

    return checks


def _build_summaries(r: AnalysisReport) -> dict[str, str]:
    summaries: dict[str, str] = {}
    stage = r.profile.stage
    if r.valuation:
        evgp = _safe(r.valuation.ev_gross_profit, None)
        if evgp is not None:
            summaries["valuation"] = f"EV/Gross Profit: {evgp:.1f}x"
        else:
            pe = _safe(r.valuation.pe_trailing, None)
            summaries["valuation"] = f"P/E of {pe:.1f}" if pe else "Limited valuation data"
    else:
        summaries["valuation"] = "Limited valuation data"

    if r.profitability:
        r40 = _safe(r.profitability.rule_of_40, None) or _safe(r.profitability.rule_of_40_ebitda, None)
        if r40 is not None:
            summaries["profitability"] = f"Rule-of-40 = {r40:.0f}%"
        else:
            gm = _safe(r.profitability.gross_margin, None)
            summaries["profitability"] = f"Gross margin: {gm*100:.0f}%" if gm is not None else "Limited data"
    else:
        summaries["profitability"] = "Limited data"

    if r.solvency:
        runway = _safe(r.solvency.cash_runway_years, None)
        if runway is not None:
            summaries["solvency"] = f"Cash runway: {runway:.1f} years"
        elif _safe(r.solvency.cash_burn_rate, None) is not None and r.solvency.cash_burn_rate >= 0:
            summaries["solvency"] = "Cash flow positive"
        else:
            summaries["solvency"] = "Limited solvency data"
    else:
        summaries["solvency"] = "Limited solvency data"

    if r.growth:
        rg = _safe(r.growth.revenue_growth_yoy, None)
        summaries["growth"] = f"Revenue growth: {rg*100:.1f}%/yr" if rg is not None else "Limited growth data"
    else:
        summaries["growth"] = "Limited growth data"

    summaries["tech_quality"] = (r.tech_quality.competitive_position or "N/A") if r.tech_quality else "N/A"
    return summaries


def _find_strengths(r: AnalysisReport) -> list[str]:
    strengths = []
    if r.profitability:
        r40 = _safe(r.profitability.rule_of_40, None) or _safe(r.profitability.rule_of_40_ebitda, None)
        if r40 is not None and r40 >= 50:
            strengths.append(f"Rule-of-40 of {r40:.0f}% — strong growth + profitability trade-off")
        gm = _safe(r.profitability.gross_margin, None)
        if gm is not None and gm > 0.75:
            strengths.append(f"Best-in-class gross margin ({gm*100:.0f}%) — durable moat")
    if r.solvency:
        runway = _safe(r.solvency.cash_runway_years, None)
        if runway and runway > 5:
            strengths.append(f"Fortress balance sheet ({runway:.1f} years runway)")
        if _safe(r.solvency.debt_to_equity, None) is not None and r.solvency.debt_to_equity < 0.3:
            strengths.append("Low leverage")
        drr = _safe(r.solvency.deferred_revenue_ratio, None)
        if drr and drr > 0.35:
            strengths.append(f"Strong deferred-revenue visibility ({drr*100:.0f}% of revenue)")
    if r.growth:
        rg = _safe(r.growth.revenue_growth_yoy, None)
        if rg and rg > 0.30:
            strengths.append(f"Hyper-growth revenue ({rg*100:.0f}% YoY)")
        rd = _safe(r.growth.rd_intensity, None)
        if rd and rd > 0.20:
            strengths.append(f"Heavy R&D commitment ({rd*100:.0f}% of revenue)")
    if r.share_structure:
        insider = _safe(r.share_structure.insider_ownership_pct, None)
        if insider and insider > 0.10:
            strengths.append(f"Strong insider ownership ({insider*100:.0f}%)")
    if r.profile.jurisdiction_tier == JurisdictionTier.TIER_1:
        strengths.append("Tier 1 jurisdiction (strong IP protection)")
    return strengths[:6]


def _find_risks(r: AnalysisReport) -> list[str]:
    risks = []
    if r.profitability:
        sbc = _safe(r.profitability.sbc_to_revenue, None)
        if sbc and sbc > 0.20:
            risks.append(f"Severe SBC dilution ({sbc*100:.0f}% of revenue)")
        r40 = _safe(r.profitability.rule_of_40, None) or _safe(r.profitability.rule_of_40_ebitda, None)
        if r40 is not None and r40 < 20:
            risks.append(f"Rule-of-40 only {r40:.0f}% — quality gate failed")
    if r.solvency:
        runway = _safe(r.solvency.cash_runway_years, None)
        if runway is not None and runway < 1.5:
            risks.append(f"Cash runway under 18 months ({runway:.1f} years)")
        bpct = _safe(r.solvency.burn_as_pct_of_market_cap, None)
        if bpct and bpct > 0.10:
            risks.append(f"Burn is {bpct*100:.0f}% of market cap/yr")
        gta = _safe(r.solvency.goodwill_to_assets, None)
        if gta and gta > 0.40:
            risks.append(f"Goodwill is {gta*100:.0f}% of assets — impairment risk")
    if r.growth:
        dil = _safe(r.growth.shares_growth_yoy, None)
        if dil is not None and dil > 0.08:
            risks.append(f"Heavy share dilution ({dil*100:.1f}%/yr)")
    if r.share_structure and r.share_structure.sbc_overhang_risk:
        if "Severe" in r.share_structure.sbc_overhang_risk:
            risks.append("Severe stock-based-compensation overhang")
    if r.profile.jurisdiction_tier == JurisdictionTier.TIER_3:
        risks.append("Tier 3 jurisdiction — elevated regulatory/geopolitical risk")
    if r.profile.stage == CompanyStage.STARTUP:
        risks.append("Early-stage tech — product-market-fit risk dominates")
    return risks[:6]


def _build_narrative(r: AnalysisReport, c: AnalysisConclusion) -> str:
    parts = [f"{r.profile.name} ({r.profile.tier.value}, {r.profile.stage.value}) scores {c.overall_score:.0f}/100 — '{c.verdict}'."]
    if c.strengths:
        parts.append(f"Strengths: {c.strengths[0].lower()}" + (f" and {c.strengths[1].lower()}" if len(c.strengths) > 1 else "") + ".")
    if c.risks:
        parts.append(f"Risks: {c.risks[0].lower()}" + (f" and {c.risks[1].lower()}" if len(c.risks) > 1 else "") + ".")
    return " ".join(parts)


def _tier_note(tier: CompanyTier) -> str:
    return {
        CompanyTier.MEGA: "Mega-cap: DCF and durable-quality factors dominate. Multi-year ROIC compounding is the signal.",
        CompanyTier.LARGE: "Large-cap: balanced growth + profitability. Rule-of-40 and EV/GP primary.",
        CompanyTier.MID: "Mid-cap: watch operating margin trajectory and NRR carefully.",
        CompanyTier.SMALL: "Small-cap tech: execution & financing risk elevated. Runway and dilution critical.",
        CompanyTier.MICRO: "Micro-cap: survival metrics dominate. Cash runway, SBC, dilution are must-checks.",
        CompanyTier.NANO: "Nano-cap: highly speculative. Most metrics unreliable — asset / cash backing only.",
    }.get(tier, "")


def _stage_note(stage: CompanyStage) -> str:
    return {
        CompanyStage.PLATFORM: "Dominant Platform: durable moats + cash generation compound for decades. DCF & ROIC primary.",
        CompanyStage.MATURE: "Mature / Cash-Generative: predictable FCF, buybacks, possibly dividends. EV/EBITDA and P/FCF primary.",
        CompanyStage.SCALE: "Scale-Up: growth still strong, profitability on the horizon. Watch operating-margin trajectory.",
        CompanyStage.GROWTH: "Hyper-Growth: land-and-expand motion. Rule-of-40 and NRR are the quality gates.",
        CompanyStage.STARTUP: "Startup: product-market-fit risk dominates. Cash runway, SBC/dilution, and moat-seed are key.",
    }.get(stage, "")
