# Changelog

## 6.0.0 — 2026-04-26

**Major release synchronising the entire Lince Investor Suite.**

### What's new across the Suite

- **lynx-fund** — brand-new mutual / index fund analysis tool, rejecting
  ETFs and stocks at the resolver level. Surfaces share classes, loads,
  12b-1 fees, manager tenure, persistence, capital-gains tax drag, and
  20-rule passive-investor checklist with tailored tips.
- **lynx-compare-fund** — head-to-head comparison for two mutual / index
  funds. Adds a Boglehead-style Passive-Investor Verdict, plus warnings
  for active-vs-passive, UCITS, soft- / hard-close, and distribution-
  policy mismatches.
- **lynx-theme** — visual theme editor for the entire Suite (GUI + TUI
  only). Edit colours, fonts, alignment, bold / italic / underline /
  blink / marquee for 15 styled areas with live preview. Three built-in
  read-only reference themes (`lynx-mocha`, `lynx-latte`,
  `lynx-high-contrast`). Sets the default theme persisted to
  `$XDG_CONFIG_HOME/lynx-theme/default.json`.
- **i18n** — every Suite CLI now accepts `--language=us|es|it|de|fr|fa`
  and persists the user's choice to `$XDG_CONFIG_HOME/lynx/language.json`.
  GUI apps mount a small bottom-right language toggle (left-click
  cycles, right-click opens a chooser); TUI apps bind `g` to cycle.
  Honours `LYNX_LANG` for ad-hoc shells.
- **Author signature footer** — every txt / html / pdf export now ends
  with the Suite-wide author block: *Borja Tarraso
  &lt;borja.tarraso@member.fsf.org&gt;*. Provided by the new
  `lynx_investor_core.author_footer` module.

### Dashboard

- Two new APP launchables (Lynx Fund, Lynx Compare Fund, Lynx Theme),
  raising the catalogue to **8 apps + 11 sector agents = 19
  launchables**.
- Per-app launch dialect (`run_mode_dialect`, `ui_mode_flags`,
  `accepts_identifier`) so the launcher emits argv each app
  understands; lynx-theme + lynx-portfolio launch correctly from every
  mode.
- `--recommend` now rejects empty queries instead of silently passing.

### Bug fixes

- `__main__.py` of every fund / compare-fund / etf / compare-etf entry
  point now propagates `run_cli`'s return code so non-zero exits are
  visible to shell scripts and CI pipelines.
- Stale-install hygiene: pyproject editable installs now overwrite
  cached site-packages copies cleanly.
- Cosmetic clean-up: remaining "ETF" labels in fund / compare-fund
  GUI / TUI / interactive prompts → "Fund".
- Validation: empty positional ticker, missing second comparison
  ticker, and `--recommend ""` now exit non-zero with a clear message.


## [4.0] - 2026-04-23

Part of **Lince Investor Suite v4.0** coordinated release.

### Added
- URL-safety enforcement for every RSS-sourced news URL and every
  `webbrowser.open(...)` site — powered by
  `lynx_investor_core.urlsafe`.
- Sector-specific ASCII art in easter-egg visuals (replaces the shared
  pickaxe motif that leaked into non-mining sectors).

### Changed
- Aligned every user-visible sector string with the package's real
  sector: titles, subtitles, app class names, splash taglines, news
  keywords, User-Agent headers, themes, export headers, and fortune
  quotes no longer carry template leftovers.
- Depends on `lynx-investor-core>=4.0`.

All notable changes to Lynx Information Technology Analysis are documented here.

## [3.0] - 2026-04-22

Part of **Lince Investor Suite v3.0** coordinated release.

### Added
- Uniform PageUp / PageDown navigation across every UI mode (GUI, TUI,
  interactive, console). Scrolling never goes above the current output
  in interactive and console mode; Shift+PageUp / Shift+PageDown remain
  reserved for the terminal emulator's own scrollback.
- Sector-mismatch warning now appends a `Suggestion: use
  'lynx-investor-<other>' instead.` line sourced from
  `lynx_investor_core.sector_registry`. The original warning text is
  preserved as-is.

### Changed
- TUI wires `lynx_investor_core.pager.PagingAppMixin` and
  `tui_paging_bindings()` into the main application.
- Graphical mode binds `<Prior>` / `<Next>` / `<Control-Home>` /
  `<Control-End>` via `bind_tk_paging()`.
- Interactive mode pages long output through `console_pager()` /
  `paged_print()`.
- Depends on `lynx-investor-core>=2.0`.

## [2.0] - 2026-04-19

Initial release of **Lynx Information Technology Analysis**, part of the **Lince Investor Suite v2.0**.

### Added
- **IT-specific lifecycle stages**: Startup / Hyper-Growth / Scale-Up / Mature / Dominant Platform (replaces mining stages)
- **IT sub-category classification**: SaaS, Infrastructure Software, Cloud, Cybersecurity, Semiconductors, Semi Equipment, IT Services, Hardware, Internet, Fintech, Data/AI
- **IT-specific valuation metrics**: EV/Gross-Profit, EV/ARR (approx), EV/Employee, Rule-of-40-Adjusted EV/Revenue
- **IT-specific profitability metrics**: Rule of 40 (FCF & EBITDA variants), Magic Number (sales efficiency), SBC/Revenue, SBC/FCF, GAAP-vs-Adjusted gap
- **IT-specific growth metrics**: ARR Growth (approx via deferred revenue), R&D intensity, R&D growth, S&M intensity, Revenue per Employee, slots for NRR and GRR
- **IT-specific solvency metrics**: Capex/Revenue, Deferred Revenue Ratio, RPO Coverage, Goodwill-to-Assets (impairment risk), Cash Coverage (months)
- **IT-specific efficiency metrics**: Rule of X (Altimeter), CAC Payback Months, FCF Conversion
- **Tech Quality scoring**: Moat/Gross-Margin (20pts), Rule-of-40 (20pts), Financial Position (15pts), Dilution+SBC (15pts), R&D Efficiency (10pts), Unit Economics (10pts), Revenue Predictability (10pts)
- **Severity system with 5 levels**: `***CRITICAL***` (red uppercase), `*WARNING*` (orange), `[WATCH]` (yellow), `[OK]` (green), `[STRONG]` (silver)
- **Impact column** on every metric table: Critical (blinking red), Important (orange), Relevant (yellow), Informational (green), Irrelevant (silver)
- **IT sector validation gate**: refuses to analyze non-IT companies with prominent red-blinking warning
- **Tech benchmark context**: QQQ headline benchmark + sub-sector ETFs (IGV, WCLD, CIBR, SMH, SOXX, FDN, etc.) based on detected tech category
- **Tech investment disclaimers**: SBC dilution, rate-sensitivity, churn/retention risks, semiconductor cyclicality, early-stage PMF risk
- **Intrinsic value adapted per stage**: DCF for platform/mature, EV/Gross-Profit for scale-up/growth, Reverse DCF for all, Cash + Option Value for startup
- **Comprehensive unit tests** (169 passing): models, calculator, relevance, conclusion, explanations, export, sector validation, storage, edge cases
- **IT-specific test fixtures** (Software Corp, SaaS profile, Hyper-Growth stage)

### Changed (vs Basic Materials predecessor)
- Package renamed `lynx_mining` → `lynx_tech`
- CLI command renamed `lynx-mining` → `lynx-tech`
- `CompanyStage` enum replaced (Grassroots/Explorer/Developer/Producer/Royalty → Startup/Growth/Scale/Mature/Platform)
- `Commodity` enum replaced with `TechCategory`
- `MiningQualityIndicators` dataclass renamed to `TechQualityIndicators` with IT-specific fields
- `primary_commodity` field renamed to `tech_category`
- Jurisdiction tiers adapted to IT lens (IP protection, data privacy, export controls): Tier 1 includes US, Canada, UK, Ireland, Japan, Korea, Singapore, Israel, Taiwan
- Commodity context in Market Intelligence replaced with Tech Benchmark context (QQQ + sub-sector ETFs)
- Mining-specific metrics removed: AISC, Cash Cost per Unit, EV per Resource oz/lb, P/NAV, NAV per Share, EV Resource Implied Price, Production Growth, Exploration Ratio, Capex Intensity, Geological Quality, Resource Grade/Scale, Jurisdiction Assessment, Insider Alignment, Asset Backing, Niche Position, Warrant Overhang Risk
- Screening checklist rewritten for IT (Rule-of-40 pass, moat gross margin, SBC contained, R&D spend, etc.)

### Retained (from common architecture)
- Progressive rendering across four UI modes (Console, Interactive REPL, Textual TUI, Tkinter GUI)
- Rich-powered tables with relevance-based styling
- TXT / HTML / PDF export (with IT-adapted tables and sections)
- Local caching (production mode) and isolated testing mode (`data/` vs `data_test/`)
- SEC filings fetcher
- News fetcher (Yahoo Finance + Google News RSS)
- ISIN resolution, exchange-suffix search, and ticker validation
- BSD-3-Clause license, suite branding, ASCII logo support
