# Lynx Information Technology Analysis

> Fundamental analysis specialized for SaaS, software, cloud, cybersecurity, semiconductors, and IT-services companies.

Part of the **Lince Investor Suite**.

## Overview

Lynx Information Technology is a comprehensive fundamental analysis tool built specifically for technology investors. It evaluates companies across all lifecycle stages — from early-stage startups to dominant platforms — using IT-specific metrics, valuation methods, and risk assessments.

### Key Features

- **Stage-Aware Analysis**: Automatically classifies companies as Startup, Hyper-Growth, Scale-Up, Mature / Cash-Generative, or Dominant Platform — and adapts all metrics and scoring accordingly
- **IT-Specific Metrics**: Rule of 40 (FCF + EBITDA variants), Magic Number, ARR Growth, EV/Gross-Profit, EV/ARR, SBC/Revenue, SBC/FCF, R&D Intensity, Revenue/Employee, CAC Payback, Rule of X (Altimeter)
- **Tech Sub-Category Detection**: Automatic identification of SaaS, Infrastructure Software, Cloud, Cybersecurity, Semiconductors, Semi Equipment, IT Services, Hardware, Internet, Fintech, or Data/AI
- **5-Level Relevance System**: Critical, Important, Relevant, Informational, Irrelevant — plus an **Impact column** with colored labels (blinking red / orange / yellow / green / silver)
- **5-Level Severity System**: `***CRITICAL***` (red), `*WARNING*` (orange), `[WATCH]` (yellow), `[OK]` (green), `[STRONG]` (silver)
- **Market Intelligence**: Insider transactions (with 10b5-1 plan awareness), institutional holders, analyst consensus, short interest, price technicals with golden/death cross detection, QQQ + sub-sector ETF comparison
- **10-Point Tech Screening Checklist**: Rule-of-40 pass, moat gross margin, SBC contained, dilution, cash runway, R&D spend, debt, insider alignment, growth, jurisdiction
- **Jurisdiction Risk Classification**: Tier 1/2/3 based on IP protection, data privacy, export controls, and regulatory stability
- **Multiple Interface Modes**: Console CLI, Interactive REPL, Textual TUI, Tkinter GUI
- **Export**: TXT, HTML, and PDF report generation
- **Sector & Industry Insights**: Deep context for SaaS, Infrastructure Software, Cybersecurity, Internet Platforms, Semiconductors, Semi Equipment, IT Services, Hardware, Fintech

### Target Companies

Designed for analyzing companies like:
- **Mega-Cap Platforms**: Microsoft (MSFT), Apple (AAPL), Alphabet (GOOGL), Amazon (AMZN), Meta (META), Nvidia (NVDA)
- **SaaS**: Salesforce (CRM), ServiceNow (NOW), Snowflake (SNOW), Workday (WDAY), Datadog (DDOG)
- **Cybersecurity**: CrowdStrike (CRWD), Palo Alto Networks (PANW), Zscaler (ZS), SentinelOne (S)
- **Semiconductors**: AMD, Broadcom (AVGO), ASML, TSMC (TSM), Arm Holdings (ARM)
- **Data/AI**: Palantir (PLTR), Databricks-adjacent names

## Installation

```bash
# Clone the repository
git clone https://github.com/borjatarraso/lynx-investor-information-technology.git
cd lynx-investor-information-technology

# Install in editable mode (creates the `lynx-tech` command)
pip install -e .
```

### Dependencies

| Package        | Purpose                              |
|----------------|--------------------------------------|
| yfinance       | Financial data from Yahoo Finance    |
| requests       | HTTP calls (OpenFIGI, EDGAR, etc.)   |
| beautifulsoup4 | HTML parsing for SEC filings         |
| rich           | Terminal tables and formatting       |
| textual        | Full-screen TUI framework            |
| feedparser     | News RSS feed parsing                |
| pandas         | Data analysis                        |
| numpy          | Numerical computing                  |

All dependencies are installed automatically via `pip install -e .`.

## Usage

### Direct Execution
```bash
# Via the runner script
./lynx-investor-information-technology.py -p MSFT

# Via Python
python3 lynx-investor-information-technology.py -p NVDA

# Via pip-installed command
lynx-tech -p CRM
```

### Execution Modes

| Flag | Mode | Description |
|------|------|-------------|
| `-p` | Production | Uses `data/` for persistent cache |
| `-t` | Testing | Uses `data_test/` (isolated, always fresh) |

### Interface Modes

| Flag | Interface | Description |
|------|-----------|-------------|
| (none) | Console | Progressive CLI output |
| `-i` | Interactive | REPL with commands |
| `-tui` | TUI | Textual terminal UI with themes |
| `-x` | GUI | Tkinter graphical interface |

### Examples

```bash
# Analyze a mega-cap tech platform
lynx-tech -p MSFT

# Force fresh data download
lynx-tech -p NVDA --refresh

# Search by company name
lynx-tech -p "Palantir"

# Interactive mode
lynx-tech -p -i

# Export HTML report
lynx-tech -p CRM --export html

# Explain a metric
lynx-tech --explain rule_of_40

# Skip filings and news for faster analysis
lynx-tech -t MSFT --no-reports --no-news
```

## Severity & Impact System

Every metric displays a **Severity tag** and an **Impact column**.

### Severity Levels

| Severity        | Marker          | Color           | Meaning                  |
|-----------------|-----------------|-----------------|--------------------------|
| `***CRITICAL***` | uppercase, red bold | Red             | Urgent red flag          |
| `*WARNING*`     | italic          | Orange          | Significant concern      |
| `[WATCH]`       | bracketed       | Yellow          | Needs monitoring         |
| `[OK]`          | bracketed       | Green           | Normal range             |
| `[STRONG]`      | bracketed       | Silver / Grey   | Excellent signal         |

### Impact Column

| Impact          | Color (text)      |
|-----------------|-------------------|
| Critical        | Blinking red      |
| Important       | Orange            |
| Relevant        | Yellow            |
| Informational   | Green             |
| Irrelevant      | Grey / Silver     |

## Analysis Sections

1. **Company Profile** — Tier, stage, tech category, jurisdiction classification
2. **Sector & Industry Insights** — IT-specific context and benchmarks
3. **Valuation Metrics** — Traditional + IT-specific (EV/GP, EV/ARR, EV/Employee, R40-Adj EV/Rev)
4. **Profitability Metrics** — ROE/ROIC/margins + Rule of 40, Magic Number, SBC/Revenue, SBC/FCF, GAAP-vs-Adjusted gap
5. **Solvency & Survival** — Cash runway, burn rate, Capex/Revenue, Deferred Rev ratio, Goodwill/Assets
6. **Growth & Retention** — Revenue/ARR growth, R&D intensity, S&M intensity, Revenue/Employee, NRR/GRR slots
7. **Share Structure** — Outstanding/diluted shares, insider/institutional ownership, SBC Overhang Risk, Dual-Class flag
8. **Tech Quality** — Moat, Rule-of-40 verdict, Unit Economics, R&D Efficiency, Platform Position, Founder-Led Signal
9. **Intrinsic Value** — DCF, Graham Number, EV/Sales Implied, Reverse DCF (method selection by stage)
10. **Market Intelligence** — Analysts, short interest, technicals, insider trades, tech benchmark (QQQ + sub-sector ETF)
11. **Financial Statements** — 5-year annual summary with R&D, SBC, deferred revenue
12. **SEC Filings** — Downloadable regulatory filings
13. **News** — Yahoo Finance + Google News RSS
14. **Assessment Conclusion** — Weighted score, verdict, strengths/risks, 10-point tech screening checklist
15. **Tech Disclaimers** — Stage-specific risk disclosures

## Relevance System

Each metric is classified by importance for the company's lifecycle stage:

| Level | Prefix | Impact Column    | Meaning |
|-------|--------|------------------|---------|
| **Critical**    | `*`      | Blinking Red    | Must-check for this stage |
| **Important**   | `!`      | Orange          | Primary metric |
| **Relevant**    | normal   | Yellow          | Important context |
| **Informational** (Contextual) | dimmed | Green | Background only |
| **Irrelevant**  | hidden   | Silver          | Not meaningful for this stage |

Example: For a Hyper-Growth SaaS company, Rule of 40 is **Critical** while traditional P/E is **Irrelevant**.

## Scoring Methodology

The overall score (0-100) is a weighted average of 5 categories, with weights adapted by both company tier AND lifecycle stage:

| Stage | Valuation | Profitability | Solvency | Growth | Tech Quality |
|-------|-----------|---------------|----------|--------|--------------|
| Startup | 5-10% | 5% | 35-40% | 15-20% | 30-35% |
| Hyper-Growth | 10-15% | 10-15% | 15-25% | 30% | 25% |
| Scale-Up | 15-20% | 15-20% | 15-20% | 20-25% | 25% |
| Mature / Cash-Generative | 20-25% | 20-25% | 10-15% | 15-20% | 25% |
| Dominant Platform | 25% | 25% | 10% | 15% | 25% |

Verdicts: Strong Buy (>=75), Buy (>=60), Hold (>=45), Caution (>=30), Avoid (<30).

## Project Structure

```
lynx-investor-information-technology/
├── lynx-investor-information-technology.py  # Runner script
├── pyproject.toml                            # Build configuration
├── requirements.txt                          # Dependencies
├── img/                                      # Logo images
├── data/                                     # Production cache
├── data_test/                                # Testing cache
├── docs/                                     # Documentation
│   └── API.md                                # API reference
├── robot/                                    # Robot Framework tests
│   ├── cli_tests.robot
│   ├── api_tests.robot
│   └── export_tests.robot
├── tests/                                    # Unit tests
└── lynx_tech/                                # Main package
```

## Testing

```bash
# Unit tests
pytest tests/ -v

# Robot Framework acceptance tests
robot robot/
```

## License

BSD 3-Clause License. See LICENSE in source.

## Author

**Borja Tarraso** — borja.tarraso@member.fsf.org
