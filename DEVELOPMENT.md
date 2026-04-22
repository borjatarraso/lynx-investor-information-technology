# Development Guide

## Architecture

The application shares core architecture with other Lynx specialists (Basic Materials, Energy, etc.) but applies IT-specific domain logic end-to-end.

### Data Flow

```
User Input (ticker/ISIN/name)
    ↓
CLI/Interactive/TUI/GUI → cli.py
    ↓
analyzer.py: run_progressive_analysis()
    ↓
ticker.py: resolve_identifier() → (ticker, isin)
    ↓
storage.py: check cache → return if cached
    ↓
fetcher.py: yfinance data (profile + financials, incl. R&D, SBC, deferred revenue, goodwill)
    ↓
models.py: classify_stage / classify_category / classify_jurisdiction
    ↓
calculator.py: calc_valuation / profitability / solvency / growth / efficiency
    ↓
calculator.py: calc_share_structure + calc_tech_quality
    ↓
calculator.py: calc_market_intelligence (insider, analyst, short, technicals, QQQ + sector ETF)
    ↓
calculator.py: calc_intrinsic_value (DCF, EV/Sales peer, Reverse DCF)
    ↓
[parallel] reports.py + news.py
    ↓
conclusion.py: generate_conclusion() → verdict + 10-point tech screening
    ↓
storage.py: save_analysis_report()
    ↓
display.py / tui/app.py / gui/app.py / export/* → render with severity + impact columns
```

### Key Design Decisions

1. **Stage > Tier**: IT lifecycle stage (Startup → Growth → Scale → Mature → Platform) is the primary analysis axis. The relevance system prioritizes stage overrides.

2. **Rule of 40 as quality anchor**: Wherever a single metric is "The Headline" for SaaS-like businesses, the Rule of 40 (revenue growth % + FCF margin %) wins. It's computed in both FCF and EBITDA variants.

3. **SBC as structural dilution**: Tech-specific dilution isn't just share issuance — it's equity compensation. We compute SBC/Revenue and SBC/FCF to expose the "paper vs cash" gap.

4. **Gross margin = moat proxy**: The classification of a tech business' quality starts with gross margin (SaaS target >75%, Hardware 30-50%, Services 20-35%).

5. **Severity + Impact dual-axis display**: Every metric row shows BOTH a severity tag (how bad is this reading?) and an impact column (how much does this metric matter for this stage?). The two are independent.

6. **Progressive Rendering**: The analyzer emits progress callbacks so UIs can render sections as data arrives.

7. **Reverse DCF sanity check**: We compute the growth rate implied by the current price to spot priced-in expectations.

### Adding New Metrics

1. Add field to the appropriate dataclass in `models.py`
2. Calculate in `calculator.py` (in the relevant `calc_*` function)
3. Add relevance entry in `relevance.py` (`_STAGE_OVERRIDES` and tier tables)
4. Add explanation in `explanations.py`
5. Add display row in `display.py`, `tui/app.py`, `gui/app.py`
6. Add export row in `export/html_export.py` and `export/txt_export.py`

### Adding New Tech Categories

1. Add to `TechCategory` enum in `models.py`
2. Add keywords to `_CATEGORY_KEYWORDS`
3. Add sub-sector ETFs to `_CATEGORY_ETFS` in `calculator.py`
4. Add industry insight in `sector_insights.py`

### Adding New Stages

1. Add to `CompanyStage` enum
2. Add keywords to `_STAGE_KEYWORDS` in `models.py`
3. Add weights to `_WEIGHTS` in `conclusion.py`
4. Add relevance overrides in `relevance.py`
5. Update method selection in `calc_intrinsic_value`

## Running Tests

```bash
# Python unit tests
pytest tests/ -v --tb=short

# Robot Framework (requires robotframework)
pip install robotframework
robot --outputdir results robot/

# Syntax check all files
python -c "import py_compile, glob; [py_compile.compile(f, doraise=True) for f in glob.glob('lynx_tech/**/*.py', recursive=True)]"
```

## Code Style

- Python 3.10+ with type hints
- Dataclasses for all data models
- Rich for console rendering
- Textual for TUI
- Tkinter for GUI (dark theme)

## Severity & Impact System

The dual-axis display is implemented in `lynx_tech/display.py`:

- `_SEVERITY_FMT` → maps `Severity.*` to `[color]***CRITICAL***[/]`, `[color]*WARNING*[/]`, `[color][WATCH][/]` etc.
- `_IMPACT_DISPLAY` → maps `Relevance.*` to `[blink bold red]Critical[/]`, `[#ff8800]Important[/]`, etc.

Both are shown as separate columns in every metric table, alongside the Value and Assessment columns.
