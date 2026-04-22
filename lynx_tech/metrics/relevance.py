"""Metric relevance by company tier AND IT lifecycle stage.

Defines which metrics are CRITICAL, IMPORTANT, RELEVANT, CONTEXTUAL (informational)
or IRRELEVANT for each combination of company size tier and IT development stage.

For Information Technology analysis:
  CRITICAL    — Must-check metric. Highlighted; feeds Critical Impact column (blinking red).
  IMPORTANT   — Primary metric for this stage (Impact column → Important, orange).
  RELEVANT    — Useful context (Impact column → Relevant, yellow).
  CONTEXTUAL  — Shown dimmed, informational only (Impact column → Informational, green).
  IRRELEVANT  — Not meaningful; hidden or struck-through (Impact column → Irrelevant, silver).

Stage axis (IT-specific):
  STARTUP    - Startup / Early-Stage
  GROWTH     - Hyper-Growth
  SCALE      - Scale-Up
  MATURE     - Mature / Cash-Generative
  PLATFORM   - Dominant Platform

Example: For a GROWTH-stage SaaS company, Rule-of-40 and NRR are CRITICAL,
P/E is IRRELEVANT, and EV/Gross-Profit is IMPORTANT.
"""

from __future__ import annotations

from lynx_tech.models import CompanyStage, CompanyTier, Relevance

C = Relevance.CRITICAL
P = Relevance.IMPORTANT
R = Relevance.RELEVANT
X = Relevance.CONTEXTUAL
I = Relevance.IRRELEVANT


def get_relevance(
    metric_key: str,
    tier: CompanyTier,
    category: str = "valuation",
    stage: CompanyStage = CompanyStage.GROWTH,
) -> Relevance:
    """Look up relevance for a metric given tier and stage.

    Stage overrides take precedence — the lifecycle stage is the primary axis
    for IT analysis just as mining stage was for Basic Materials.
    """
    stage_override = _STAGE_OVERRIDES.get(metric_key, {}).get(stage)
    if stage_override is not None:
        return stage_override

    table = {
        "valuation": VALUATION_RELEVANCE,
        "profitability": PROFITABILITY_RELEVANCE,
        "solvency": SOLVENCY_RELEVANCE,
        "growth": GROWTH_RELEVANCE,
        "tech_quality": TECH_QUALITY_RELEVANCE,
        "share_structure": SHARE_STRUCTURE_RELEVANCE,
        "efficiency": EFFICIENCY_RELEVANCE,
    }.get(category, {})
    entry = table.get(metric_key, {})
    return entry.get(tier, Relevance.RELEVANT)


# ======================================================================
# Stage-based overrides (take precedence over tier-based lookups)
# ======================================================================

_STAGE_OVERRIDES: dict[str, dict[CompanyStage, Relevance]] = {
    # ── VALUATION ──────────────────────────────────────────────────
    "pe_trailing":           {CompanyStage.STARTUP: I, CompanyStage.GROWTH: I, CompanyStage.SCALE: X, CompanyStage.MATURE: C, CompanyStage.PLATFORM: C},
    "pe_forward":            {CompanyStage.STARTUP: I, CompanyStage.GROWTH: X, CompanyStage.SCALE: P, CompanyStage.MATURE: C, CompanyStage.PLATFORM: C},
    "pb_ratio":              {CompanyStage.STARTUP: X, CompanyStage.GROWTH: X, CompanyStage.SCALE: R, CompanyStage.MATURE: R, CompanyStage.PLATFORM: R},
    "ps_ratio":              {CompanyStage.STARTUP: P, CompanyStage.GROWTH: P, CompanyStage.SCALE: P, CompanyStage.MATURE: R, CompanyStage.PLATFORM: R},
    "p_fcf":                 {CompanyStage.STARTUP: I, CompanyStage.GROWTH: R, CompanyStage.SCALE: C, CompanyStage.MATURE: C, CompanyStage.PLATFORM: C},
    "ev_ebitda":             {CompanyStage.STARTUP: I, CompanyStage.GROWTH: X, CompanyStage.SCALE: P, CompanyStage.MATURE: C, CompanyStage.PLATFORM: C},
    "ev_revenue":            {CompanyStage.STARTUP: P, CompanyStage.GROWTH: C, CompanyStage.SCALE: P, CompanyStage.MATURE: R, CompanyStage.PLATFORM: R},
    "ev_gross_profit":       {CompanyStage.STARTUP: P, CompanyStage.GROWTH: C, CompanyStage.SCALE: C, CompanyStage.MATURE: P, CompanyStage.PLATFORM: P},
    "ev_to_arr":             {CompanyStage.STARTUP: C, CompanyStage.GROWTH: C, CompanyStage.SCALE: P, CompanyStage.MATURE: R, CompanyStage.PLATFORM: R},
    "rule_of_40_adj_multiple":{CompanyStage.STARTUP: R, CompanyStage.GROWTH: C, CompanyStage.SCALE: C, CompanyStage.MATURE: P, CompanyStage.PLATFORM: P},
    "ev_per_employee":       {CompanyStage.STARTUP: R, CompanyStage.GROWTH: P, CompanyStage.SCALE: P, CompanyStage.MATURE: R, CompanyStage.PLATFORM: R},
    "peg_ratio":             {CompanyStage.STARTUP: I, CompanyStage.GROWTH: X, CompanyStage.SCALE: P, CompanyStage.MATURE: P, CompanyStage.PLATFORM: R},
    "dividend_yield":        {CompanyStage.STARTUP: I, CompanyStage.GROWTH: I, CompanyStage.SCALE: I, CompanyStage.MATURE: R, CompanyStage.PLATFORM: R},
    "earnings_yield":        {CompanyStage.STARTUP: I, CompanyStage.GROWTH: I, CompanyStage.SCALE: R, CompanyStage.MATURE: P, CompanyStage.PLATFORM: P},
    "cash_to_market_cap":    {CompanyStage.STARTUP: C, CompanyStage.GROWTH: P, CompanyStage.SCALE: R, CompanyStage.MATURE: X, CompanyStage.PLATFORM: X},
    "price_to_tangible_book":{CompanyStage.STARTUP: R, CompanyStage.GROWTH: X, CompanyStage.SCALE: X, CompanyStage.MATURE: X, CompanyStage.PLATFORM: I},
    "price_to_ncav":         {CompanyStage.STARTUP: P, CompanyStage.GROWTH: X, CompanyStage.SCALE: I, CompanyStage.MATURE: I, CompanyStage.PLATFORM: I},
    # ── PROFITABILITY ───────────────────────────────────────────────
    "roe":                   {CompanyStage.STARTUP: I, CompanyStage.GROWTH: I, CompanyStage.SCALE: R, CompanyStage.MATURE: C, CompanyStage.PLATFORM: C},
    "roa":                   {CompanyStage.STARTUP: I, CompanyStage.GROWTH: I, CompanyStage.SCALE: R, CompanyStage.MATURE: P, CompanyStage.PLATFORM: P},
    "roic":                  {CompanyStage.STARTUP: I, CompanyStage.GROWTH: X, CompanyStage.SCALE: P, CompanyStage.MATURE: C, CompanyStage.PLATFORM: C},
    "gross_margin":          {CompanyStage.STARTUP: C, CompanyStage.GROWTH: C, CompanyStage.SCALE: C, CompanyStage.MATURE: C, CompanyStage.PLATFORM: C},
    "operating_margin":      {CompanyStage.STARTUP: X, CompanyStage.GROWTH: P, CompanyStage.SCALE: C, CompanyStage.MATURE: C, CompanyStage.PLATFORM: C},
    "net_margin":            {CompanyStage.STARTUP: X, CompanyStage.GROWTH: R, CompanyStage.SCALE: P, CompanyStage.MATURE: C, CompanyStage.PLATFORM: C},
    "fcf_margin":            {CompanyStage.STARTUP: R, CompanyStage.GROWTH: C, CompanyStage.SCALE: C, CompanyStage.MATURE: C, CompanyStage.PLATFORM: C},
    "ebitda_margin":         {CompanyStage.STARTUP: R, CompanyStage.GROWTH: P, CompanyStage.SCALE: P, CompanyStage.MATURE: P, CompanyStage.PLATFORM: P},
    "rule_of_40":            {CompanyStage.STARTUP: P, CompanyStage.GROWTH: C, CompanyStage.SCALE: C, CompanyStage.MATURE: P, CompanyStage.PLATFORM: P},
    "rule_of_40_ebitda":     {CompanyStage.STARTUP: P, CompanyStage.GROWTH: P, CompanyStage.SCALE: P, CompanyStage.MATURE: P, CompanyStage.PLATFORM: P},
    "magic_number":          {CompanyStage.STARTUP: C, CompanyStage.GROWTH: C, CompanyStage.SCALE: C, CompanyStage.MATURE: R, CompanyStage.PLATFORM: X},
    "sbc_to_revenue":        {CompanyStage.STARTUP: C, CompanyStage.GROWTH: C, CompanyStage.SCALE: C, CompanyStage.MATURE: P, CompanyStage.PLATFORM: P},
    "sbc_to_fcf":            {CompanyStage.STARTUP: R, CompanyStage.GROWTH: P, CompanyStage.SCALE: C, CompanyStage.MATURE: C, CompanyStage.PLATFORM: C},
    "gaap_vs_adj_gap":       {CompanyStage.STARTUP: X, CompanyStage.GROWTH: P, CompanyStage.SCALE: P, CompanyStage.MATURE: R, CompanyStage.PLATFORM: R},
    # ── SOLVENCY ────────────────────────────────────────────────────
    "cash_burn_rate":        {CompanyStage.STARTUP: C, CompanyStage.GROWTH: C, CompanyStage.SCALE: P, CompanyStage.MATURE: X, CompanyStage.PLATFORM: I},
    "cash_runway_years":     {CompanyStage.STARTUP: C, CompanyStage.GROWTH: C, CompanyStage.SCALE: P, CompanyStage.MATURE: X, CompanyStage.PLATFORM: I},
    "burn_as_pct_of_market_cap":{CompanyStage.STARTUP: C, CompanyStage.GROWTH: P, CompanyStage.SCALE: R, CompanyStage.MATURE: I, CompanyStage.PLATFORM: I},
    "working_capital":       {CompanyStage.STARTUP: C, CompanyStage.GROWTH: P, CompanyStage.SCALE: P, CompanyStage.MATURE: R, CompanyStage.PLATFORM: R},
    "cash_per_share":        {CompanyStage.STARTUP: P, CompanyStage.GROWTH: P, CompanyStage.SCALE: R, CompanyStage.MATURE: X, CompanyStage.PLATFORM: X},
    "ncav_per_share":        {CompanyStage.STARTUP: P, CompanyStage.GROWTH: X, CompanyStage.SCALE: I, CompanyStage.MATURE: I, CompanyStage.PLATFORM: I},
    "current_ratio":         {CompanyStage.STARTUP: C, CompanyStage.GROWTH: P, CompanyStage.SCALE: P, CompanyStage.MATURE: R, CompanyStage.PLATFORM: R},
    "quick_ratio":           {CompanyStage.STARTUP: P, CompanyStage.GROWTH: P, CompanyStage.SCALE: P, CompanyStage.MATURE: R, CompanyStage.PLATFORM: R},
    "debt_to_equity":        {CompanyStage.STARTUP: C, CompanyStage.GROWTH: P, CompanyStage.SCALE: P, CompanyStage.MATURE: P, CompanyStage.PLATFORM: P},
    "debt_to_ebitda":        {CompanyStage.STARTUP: I, CompanyStage.GROWTH: P, CompanyStage.SCALE: P, CompanyStage.MATURE: C, CompanyStage.PLATFORM: C},
    "interest_coverage":     {CompanyStage.STARTUP: I, CompanyStage.GROWTH: R, CompanyStage.SCALE: P, CompanyStage.MATURE: P, CompanyStage.PLATFORM: R},
    "altman_z_score":        {CompanyStage.STARTUP: X, CompanyStage.GROWTH: P, CompanyStage.SCALE: P, CompanyStage.MATURE: P, CompanyStage.PLATFORM: X},
    "total_cash":            {CompanyStage.STARTUP: C, CompanyStage.GROWTH: P, CompanyStage.SCALE: R, CompanyStage.MATURE: X, CompanyStage.PLATFORM: X},
    "total_debt":            {CompanyStage.STARTUP: P, CompanyStage.GROWTH: P, CompanyStage.SCALE: P, CompanyStage.MATURE: P, CompanyStage.PLATFORM: P},
    "net_debt":              {CompanyStage.STARTUP: P, CompanyStage.GROWTH: P, CompanyStage.SCALE: P, CompanyStage.MATURE: P, CompanyStage.PLATFORM: P},
    "rpo_coverage":          {CompanyStage.STARTUP: R, CompanyStage.GROWTH: C, CompanyStage.SCALE: C, CompanyStage.MATURE: P, CompanyStage.PLATFORM: P},
    "deferred_revenue_ratio":{CompanyStage.STARTUP: P, CompanyStage.GROWTH: C, CompanyStage.SCALE: C, CompanyStage.MATURE: P, CompanyStage.PLATFORM: P},
    "goodwill_to_assets":    {CompanyStage.STARTUP: R, CompanyStage.GROWTH: P, CompanyStage.SCALE: P, CompanyStage.MATURE: P, CompanyStage.PLATFORM: P},
    "capex_to_revenue":      {CompanyStage.STARTUP: R, CompanyStage.GROWTH: P, CompanyStage.SCALE: P, CompanyStage.MATURE: P, CompanyStage.PLATFORM: P},
    # ── GROWTH ─────────────────────────────────────────────────────
    "revenue_growth_yoy":    {CompanyStage.STARTUP: C, CompanyStage.GROWTH: C, CompanyStage.SCALE: C, CompanyStage.MATURE: P, CompanyStage.PLATFORM: P},
    "revenue_cagr_3y":       {CompanyStage.STARTUP: R, CompanyStage.GROWTH: C, CompanyStage.SCALE: C, CompanyStage.MATURE: P, CompanyStage.PLATFORM: P},
    "revenue_cagr_5y":       {CompanyStage.STARTUP: X, CompanyStage.GROWTH: P, CompanyStage.SCALE: P, CompanyStage.MATURE: R, CompanyStage.PLATFORM: R},
    "earnings_growth_yoy":   {CompanyStage.STARTUP: I, CompanyStage.GROWTH: X, CompanyStage.SCALE: P, CompanyStage.MATURE: C, CompanyStage.PLATFORM: C},
    "earnings_cagr_3y":      {CompanyStage.STARTUP: I, CompanyStage.GROWTH: R, CompanyStage.SCALE: P, CompanyStage.MATURE: P, CompanyStage.PLATFORM: P},
    "earnings_cagr_5y":      {CompanyStage.STARTUP: I, CompanyStage.GROWTH: X, CompanyStage.SCALE: R, CompanyStage.MATURE: P, CompanyStage.PLATFORM: P},
    "fcf_growth_yoy":        {CompanyStage.STARTUP: R, CompanyStage.GROWTH: P, CompanyStage.SCALE: C, CompanyStage.MATURE: C, CompanyStage.PLATFORM: C},
    "book_value_growth_yoy": {CompanyStage.STARTUP: X, CompanyStage.GROWTH: X, CompanyStage.SCALE: R, CompanyStage.MATURE: P, CompanyStage.PLATFORM: P},
    "shares_growth_yoy":     {CompanyStage.STARTUP: C, CompanyStage.GROWTH: C, CompanyStage.SCALE: C, CompanyStage.MATURE: P, CompanyStage.PLATFORM: P},
    "shares_growth_3y_cagr": {CompanyStage.STARTUP: C, CompanyStage.GROWTH: C, CompanyStage.SCALE: C, CompanyStage.MATURE: P, CompanyStage.PLATFORM: R},
    "arr_growth_yoy":        {CompanyStage.STARTUP: C, CompanyStage.GROWTH: C, CompanyStage.SCALE: C, CompanyStage.MATURE: P, CompanyStage.PLATFORM: R},
    "net_revenue_retention": {CompanyStage.STARTUP: P, CompanyStage.GROWTH: C, CompanyStage.SCALE: C, CompanyStage.MATURE: P, CompanyStage.PLATFORM: P},
    "gross_revenue_retention":{CompanyStage.STARTUP: P, CompanyStage.GROWTH: C, CompanyStage.SCALE: C, CompanyStage.MATURE: P, CompanyStage.PLATFORM: P},
    "rd_intensity":          {CompanyStage.STARTUP: P, CompanyStage.GROWTH: C, CompanyStage.SCALE: C, CompanyStage.MATURE: P, CompanyStage.PLATFORM: P},
    "rd_growth_yoy":         {CompanyStage.STARTUP: R, CompanyStage.GROWTH: P, CompanyStage.SCALE: P, CompanyStage.MATURE: R, CompanyStage.PLATFORM: R},
    "sales_marketing_intensity":{CompanyStage.STARTUP: P, CompanyStage.GROWTH: C, CompanyStage.SCALE: C, CompanyStage.MATURE: R, CompanyStage.PLATFORM: X},
    "employee_growth_yoy":   {CompanyStage.STARTUP: P, CompanyStage.GROWTH: P, CompanyStage.SCALE: P, CompanyStage.MATURE: R, CompanyStage.PLATFORM: R},
    "revenue_per_employee":  {CompanyStage.STARTUP: R, CompanyStage.GROWTH: P, CompanyStage.SCALE: P, CompanyStage.MATURE: C, CompanyStage.PLATFORM: C},
    # ── TECH QUALITY ───────────────────────────────────────────────
    "quality_score":         {CompanyStage.STARTUP: C, CompanyStage.GROWTH: C, CompanyStage.SCALE: C, CompanyStage.MATURE: P, CompanyStage.PLATFORM: P},
    "moat_assessment":       {CompanyStage.STARTUP: P, CompanyStage.GROWTH: C, CompanyStage.SCALE: C, CompanyStage.MATURE: C, CompanyStage.PLATFORM: C},
    "rule_of_40_assessment": {CompanyStage.STARTUP: R, CompanyStage.GROWTH: C, CompanyStage.SCALE: C, CompanyStage.MATURE: P, CompanyStage.PLATFORM: P},
    "rd_efficiency_assessment":{CompanyStage.STARTUP: P, CompanyStage.GROWTH: C, CompanyStage.SCALE: C, CompanyStage.MATURE: P, CompanyStage.PLATFORM: P},
    "unit_economics":        {CompanyStage.STARTUP: C, CompanyStage.GROWTH: C, CompanyStage.SCALE: C, CompanyStage.MATURE: R, CompanyStage.PLATFORM: R},
    "financial_position":    {CompanyStage.STARTUP: C, CompanyStage.GROWTH: C, CompanyStage.SCALE: P, CompanyStage.MATURE: P, CompanyStage.PLATFORM: R},
    "dilution_risk":         {CompanyStage.STARTUP: C, CompanyStage.GROWTH: C, CompanyStage.SCALE: C, CompanyStage.MATURE: P, CompanyStage.PLATFORM: P},
    "sbc_risk_assessment":   {CompanyStage.STARTUP: P, CompanyStage.GROWTH: C, CompanyStage.SCALE: C, CompanyStage.MATURE: C, CompanyStage.PLATFORM: C},
    "platform_position":     {CompanyStage.STARTUP: R, CompanyStage.GROWTH: P, CompanyStage.SCALE: P, CompanyStage.MATURE: C, CompanyStage.PLATFORM: C},
    "founder_led":           {CompanyStage.STARTUP: C, CompanyStage.GROWTH: C, CompanyStage.SCALE: P, CompanyStage.MATURE: R, CompanyStage.PLATFORM: R},
    "revenue_predictability":{CompanyStage.STARTUP: R, CompanyStage.GROWTH: C, CompanyStage.SCALE: C, CompanyStage.MATURE: C, CompanyStage.PLATFORM: P},
    # ── SHARE STRUCTURE ────────────────────────────────────────────
    "shares_outstanding":    {CompanyStage.STARTUP: C, CompanyStage.GROWTH: P, CompanyStage.SCALE: P, CompanyStage.MATURE: R, CompanyStage.PLATFORM: R},
    "fully_diluted_shares":  {CompanyStage.STARTUP: C, CompanyStage.GROWTH: C, CompanyStage.SCALE: C, CompanyStage.MATURE: P, CompanyStage.PLATFORM: P},
    "insider_ownership_pct": {CompanyStage.STARTUP: C, CompanyStage.GROWTH: C, CompanyStage.SCALE: P, CompanyStage.MATURE: R, CompanyStage.PLATFORM: R},
    "institutional_ownership_pct":{CompanyStage.STARTUP: R, CompanyStage.GROWTH: P, CompanyStage.SCALE: P, CompanyStage.MATURE: P, CompanyStage.PLATFORM: R},
    "dual_class_structure":  {CompanyStage.STARTUP: R, CompanyStage.GROWTH: P, CompanyStage.SCALE: P, CompanyStage.MATURE: P, CompanyStage.PLATFORM: P},
    "sbc_overhang_risk":     {CompanyStage.STARTUP: P, CompanyStage.GROWTH: C, CompanyStage.SCALE: C, CompanyStage.MATURE: C, CompanyStage.PLATFORM: C},
    "share_structure_assessment":{CompanyStage.STARTUP: C, CompanyStage.GROWTH: P, CompanyStage.SCALE: P, CompanyStage.MATURE: R, CompanyStage.PLATFORM: R},
    # ── EFFICIENCY ─────────────────────────────────────────────────
    "rule_of_x_score":       {CompanyStage.STARTUP: R, CompanyStage.GROWTH: C, CompanyStage.SCALE: C, CompanyStage.MATURE: P, CompanyStage.PLATFORM: P},
    "cac_payback_months":    {CompanyStage.STARTUP: C, CompanyStage.GROWTH: C, CompanyStage.SCALE: C, CompanyStage.MATURE: R, CompanyStage.PLATFORM: X},
    "fcf_conversion":        {CompanyStage.STARTUP: X, CompanyStage.GROWTH: P, CompanyStage.SCALE: C, CompanyStage.MATURE: C, CompanyStage.PLATFORM: C},
}


# ======================================================================
# Tier-based relevance tables (fallback when no stage override exists)
# ======================================================================

VALUATION_RELEVANCE: dict[str, dict[CompanyTier, Relevance]] = {
    "pe_trailing":           {CompanyTier.MEGA: C, CompanyTier.LARGE: C, CompanyTier.MID: C, CompanyTier.SMALL: P, CompanyTier.MICRO: X, CompanyTier.NANO: I},
    "pb_ratio":              {CompanyTier.MEGA: R, CompanyTier.LARGE: R, CompanyTier.MID: R, CompanyTier.SMALL: R, CompanyTier.MICRO: X, CompanyTier.NANO: X},
    "ps_ratio":              {CompanyTier.MEGA: P, CompanyTier.LARGE: P, CompanyTier.MID: C, CompanyTier.SMALL: C, CompanyTier.MICRO: P, CompanyTier.NANO: R},
    "p_fcf":                 {CompanyTier.MEGA: C, CompanyTier.LARGE: C, CompanyTier.MID: C, CompanyTier.SMALL: P, CompanyTier.MICRO: R, CompanyTier.NANO: X},
    "ev_ebitda":             {CompanyTier.MEGA: C, CompanyTier.LARGE: C, CompanyTier.MID: C, CompanyTier.SMALL: P, CompanyTier.MICRO: R, CompanyTier.NANO: X},
    "ev_gross_profit":       {CompanyTier.MEGA: P, CompanyTier.LARGE: P, CompanyTier.MID: C, CompanyTier.SMALL: C, CompanyTier.MICRO: C, CompanyTier.NANO: P},
    "cash_to_market_cap":    {CompanyTier.MEGA: I, CompanyTier.LARGE: X, CompanyTier.MID: R, CompanyTier.SMALL: P, CompanyTier.MICRO: C, CompanyTier.NANO: C},
    "price_to_tangible_book":{CompanyTier.MEGA: X, CompanyTier.LARGE: X, CompanyTier.MID: R, CompanyTier.SMALL: P, CompanyTier.MICRO: P, CompanyTier.NANO: P},
    "ev_to_arr":             {CompanyTier.MEGA: P, CompanyTier.LARGE: P, CompanyTier.MID: C, CompanyTier.SMALL: C, CompanyTier.MICRO: C, CompanyTier.NANO: P},
}

PROFITABILITY_RELEVANCE: dict[str, dict[CompanyTier, Relevance]] = {
    "roe":              {CompanyTier.MEGA: C, CompanyTier.LARGE: C, CompanyTier.MID: C, CompanyTier.SMALL: P, CompanyTier.MICRO: X, CompanyTier.NANO: I},
    "roic":             {CompanyTier.MEGA: C, CompanyTier.LARGE: C, CompanyTier.MID: C, CompanyTier.SMALL: P, CompanyTier.MICRO: R, CompanyTier.NANO: X},
    "gross_margin":     {CompanyTier.MEGA: C, CompanyTier.LARGE: C, CompanyTier.MID: C, CompanyTier.SMALL: C, CompanyTier.MICRO: C, CompanyTier.NANO: C},
    "fcf_margin":       {CompanyTier.MEGA: C, CompanyTier.LARGE: C, CompanyTier.MID: P, CompanyTier.SMALL: P, CompanyTier.MICRO: R, CompanyTier.NANO: X},
    "rule_of_40":       {CompanyTier.MEGA: P, CompanyTier.LARGE: P, CompanyTier.MID: C, CompanyTier.SMALL: C, CompanyTier.MICRO: C, CompanyTier.NANO: P},
    "sbc_to_revenue":   {CompanyTier.MEGA: P, CompanyTier.LARGE: P, CompanyTier.MID: C, CompanyTier.SMALL: C, CompanyTier.MICRO: C, CompanyTier.NANO: C},
}

SOLVENCY_RELEVANCE: dict[str, dict[CompanyTier, Relevance]] = {
    "debt_to_equity":    {CompanyTier.MEGA: C, CompanyTier.LARGE: C, CompanyTier.MID: C, CompanyTier.SMALL: C, CompanyTier.MICRO: C, CompanyTier.NANO: C},
    "current_ratio":     {CompanyTier.MEGA: P, CompanyTier.LARGE: P, CompanyTier.MID: P, CompanyTier.SMALL: C, CompanyTier.MICRO: C, CompanyTier.NANO: C},
    "cash_burn_rate":    {CompanyTier.MEGA: I, CompanyTier.LARGE: I, CompanyTier.MID: X, CompanyTier.SMALL: P, CompanyTier.MICRO: C, CompanyTier.NANO: C},
    "cash_runway_years": {CompanyTier.MEGA: I, CompanyTier.LARGE: I, CompanyTier.MID: X, CompanyTier.SMALL: P, CompanyTier.MICRO: C, CompanyTier.NANO: C},
    "goodwill_to_assets":{CompanyTier.MEGA: P, CompanyTier.LARGE: P, CompanyTier.MID: P, CompanyTier.SMALL: R, CompanyTier.MICRO: R, CompanyTier.NANO: X},
}

GROWTH_RELEVANCE: dict[str, dict[CompanyTier, Relevance]] = {
    "shares_growth_yoy":      {CompanyTier.MEGA: R, CompanyTier.LARGE: P, CompanyTier.MID: P, CompanyTier.SMALL: C, CompanyTier.MICRO: C, CompanyTier.NANO: C},
    "revenue_growth_yoy":     {CompanyTier.MEGA: C, CompanyTier.LARGE: C, CompanyTier.MID: C, CompanyTier.SMALL: C, CompanyTier.MICRO: C, CompanyTier.NANO: C},
    "rd_intensity":           {CompanyTier.MEGA: P, CompanyTier.LARGE: C, CompanyTier.MID: C, CompanyTier.SMALL: C, CompanyTier.MICRO: C, CompanyTier.NANO: P},
    "arr_growth_yoy":         {CompanyTier.MEGA: P, CompanyTier.LARGE: P, CompanyTier.MID: C, CompanyTier.SMALL: C, CompanyTier.MICRO: C, CompanyTier.NANO: C},
    "net_revenue_retention":  {CompanyTier.MEGA: C, CompanyTier.LARGE: C, CompanyTier.MID: C, CompanyTier.SMALL: C, CompanyTier.MICRO: P, CompanyTier.NANO: R},
}

TECH_QUALITY_RELEVANCE: dict[str, dict[CompanyTier, Relevance]] = {
    "quality_score":          {CompanyTier.MEGA: P, CompanyTier.LARGE: P, CompanyTier.MID: P, CompanyTier.SMALL: C, CompanyTier.MICRO: C, CompanyTier.NANO: C},
    "moat_assessment":        {CompanyTier.MEGA: C, CompanyTier.LARGE: C, CompanyTier.MID: C, CompanyTier.SMALL: C, CompanyTier.MICRO: P, CompanyTier.NANO: P},
}

SHARE_STRUCTURE_RELEVANCE: dict[str, dict[CompanyTier, Relevance]] = {
    "shares_outstanding":       {CompanyTier.MEGA: R, CompanyTier.LARGE: R, CompanyTier.MID: P, CompanyTier.SMALL: C, CompanyTier.MICRO: C, CompanyTier.NANO: C},
    "fully_diluted_shares":     {CompanyTier.MEGA: P, CompanyTier.LARGE: P, CompanyTier.MID: C, CompanyTier.SMALL: C, CompanyTier.MICRO: C, CompanyTier.NANO: C},
    "insider_ownership_pct":    {CompanyTier.MEGA: R, CompanyTier.LARGE: R, CompanyTier.MID: P, CompanyTier.SMALL: C, CompanyTier.MICRO: C, CompanyTier.NANO: C},
    "sbc_overhang_risk":        {CompanyTier.MEGA: P, CompanyTier.LARGE: C, CompanyTier.MID: C, CompanyTier.SMALL: C, CompanyTier.MICRO: C, CompanyTier.NANO: C},
    "dual_class_structure":     {CompanyTier.MEGA: P, CompanyTier.LARGE: P, CompanyTier.MID: P, CompanyTier.SMALL: R, CompanyTier.MICRO: R, CompanyTier.NANO: R},
}

EFFICIENCY_RELEVANCE: dict[str, dict[CompanyTier, Relevance]] = {
    "rule_of_x_score":        {CompanyTier.MEGA: P, CompanyTier.LARGE: C, CompanyTier.MID: C, CompanyTier.SMALL: C, CompanyTier.MICRO: P, CompanyTier.NANO: R},
    "cac_payback_months":     {CompanyTier.MEGA: R, CompanyTier.LARGE: C, CompanyTier.MID: C, CompanyTier.SMALL: C, CompanyTier.MICRO: C, CompanyTier.NANO: P},
    "fcf_conversion":         {CompanyTier.MEGA: C, CompanyTier.LARGE: C, CompanyTier.MID: C, CompanyTier.SMALL: P, CompanyTier.MICRO: R, CompanyTier.NANO: X},
}
