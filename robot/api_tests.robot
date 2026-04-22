*** Settings ***
Documentation    Python API tests for Lynx Information Technology — exercises the core functions directly.
Library          Process
Library          BuiltIn
Library          Collections
Suite Setup      Log    Starting API Tests


*** Keywords ***
I Run Python Code
    [Arguments]    ${code}
    ${result}=    Run Process    python3    -c    ${code}    stderr=STDOUT    timeout=30s
    Set Test Variable    ${PY_OUTPUT}    ${result.stdout}
    Set Test Variable    ${PY_RC}    ${result.rc}

The Output Should Contain
    [Arguments]    ${snippet}
    Should Contain    ${PY_OUTPUT}    ${snippet}

The Process Should Succeed
    Should Be Equal As Integers    ${PY_RC}    0    msg=Expected success but got ${PY_RC}: ${PY_OUTPUT}


*** Test Cases ***
Package Imports Successfully
    [Documentation]    GIVEN the package WHEN I import core classes THEN they load
    When I Run Python Code    from lynx_tech.models import AnalysisReport, CompanyProfile, CompanyStage, CompanyTier, TechCategory, JurisdictionTier, Relevance, Severity, MarketIntelligence, InsiderTransaction; print('OK')
    Then The Output Should Contain    OK
    And The Process Should Succeed

Classify Tier Mega Cap
    [Documentation]    GIVEN a 300B market cap WHEN I classify THEN Mega Cap
    When I Run Python Code    from lynx_tech.models import classify_tier; print(classify_tier(300_000_000_000).value)
    Then The Output Should Contain    Mega Cap

Classify Tier Micro Cap
    [Documentation]    GIVEN 100M market cap WHEN I classify THEN Micro Cap
    When I Run Python Code    from lynx_tech.models import classify_tier; print(classify_tier(100_000_000).value)
    Then The Output Should Contain    Micro Cap

Classify Stage Platform
    [Documentation]    GIVEN a dominant platform description WHEN I classify THEN Platform
    When I Run Python Code    from lynx_tech.models import classify_stage; print(classify_stage('dominant cloud platform', 50_000_000_000, {'marketCap': 300_000_000_000}).value)
    Then The Output Should Contain    Dominant Platform

Classify Stage Mature
    [Documentation]    GIVEN profitable tech company WHEN I classify THEN Mature
    When I Run Python Code    from lynx_tech.models import classify_stage; print(classify_stage('profitable enterprise software', 10_000_000_000, {'marketCap': 50_000_000_000, 'profitMargins': 0.25}).value)
    Then The Output Should Contain    Mature

Classify Stage Growth
    [Documentation]    GIVEN hyper-growth description WHEN I classify THEN Growth
    When I Run Python Code    from lynx_tech.models import classify_stage; print(classify_stage('hyper-growth subscription software', 100_000_000, {'revenueGrowth': 0.40}).value)
    Then The Output Should Contain    Growth

Classify Stage Startup
    [Documentation]    GIVEN pre-revenue description WHEN I classify THEN Startup
    When I Run Python Code    from lynx_tech.models import classify_stage; print(classify_stage('pre-revenue saas startup', 0).value)
    Then The Output Should Contain    Startup

Classify Category SaaS
    [Documentation]    GIVEN SaaS description WHEN I classify THEN SaaS
    When I Run Python Code    from lynx_tech.models import classify_category; print(classify_category('subscription software as a service', 'Software - Application').value)
    Then The Output Should Contain    SaaS

Classify Category Semiconductor
    [Documentation]    GIVEN semiconductor description WHEN I classify THEN Semiconductors
    When I Run Python Code    from lynx_tech.models import classify_category; print(classify_category('fabless semiconductor chip design gpu', 'Semiconductors').value)
    Then The Output Should Contain    Semiconductor

Classify Jurisdiction Tier 1 US
    [Documentation]    GIVEN United States WHEN I classify THEN Tier 1
    When I Run Python Code    from lynx_tech.models import classify_jurisdiction; print(classify_jurisdiction('United States').value)
    Then The Output Should Contain    Tier 1

Classify Jurisdiction Tier 2 India
    [Documentation]    GIVEN India WHEN I classify THEN Tier 2
    When I Run Python Code    from lynx_tech.models import classify_jurisdiction; print(classify_jurisdiction('India').value)
    Then The Output Should Contain    Tier 2

Relevance Startup PE Irrelevant
    [Documentation]    GIVEN startup stage WHEN I check P/E THEN irrelevant
    When I Run Python Code    from lynx_tech.metrics.relevance import get_relevance; from lynx_tech.models import CompanyTier, CompanyStage, Relevance; print(get_relevance('pe_trailing', CompanyTier.MICRO, 'valuation', CompanyStage.STARTUP) == Relevance.IRRELEVANT)
    Then The Output Should Contain    True

Relevance Growth Rule of 40 Critical
    [Documentation]    GIVEN growth stage WHEN I check Rule of 40 THEN critical
    When I Run Python Code    from lynx_tech.metrics.relevance import get_relevance; from lynx_tech.models import CompanyTier, CompanyStage, Relevance; print(get_relevance('rule_of_40', CompanyTier.MID, 'profitability', CompanyStage.GROWTH) == Relevance.CRITICAL)
    Then The Output Should Contain    True

Relevance Growth SBC To Revenue Critical
    [Documentation]    GIVEN growth stage WHEN I check SBC/Rev THEN critical
    When I Run Python Code    from lynx_tech.metrics.relevance import get_relevance; from lynx_tech.models import CompanyTier, CompanyStage, Relevance; print(get_relevance('sbc_to_revenue', CompanyTier.MID, 'profitability', CompanyStage.GROWTH) == Relevance.CRITICAL)
    Then The Output Should Contain    True

Relevance Mature ROIC Critical
    [Documentation]    GIVEN mature stage WHEN I check ROIC THEN critical
    When I Run Python Code    from lynx_tech.metrics.relevance import get_relevance; from lynx_tech.models import CompanyTier, CompanyStage, Relevance; print(get_relevance('roic', CompanyTier.MID, 'profitability', CompanyStage.MATURE) == Relevance.CRITICAL)
    Then The Output Should Contain    True

Explanations Rule Of 40 Metric Present
    [Documentation]    GIVEN explanations WHEN I look up Rule of 40 THEN it exists
    When I Run Python Code    from lynx_tech.metrics.explanations import get_explanation; e = get_explanation('rule_of_40'); print(e.category if e else 'NONE')
    Then The Output Should Contain    profitability

Explanations SBC Metric Present
    [Documentation]    GIVEN explanations WHEN I look up sbc_to_revenue THEN it exists
    When I Run Python Code    from lynx_tech.metrics.explanations import get_explanation; e = get_explanation('sbc_to_revenue'); print(e.category if e else 'NONE')
    Then The Output Should Contain    profitability

Severity Format Critical Red Bold
    [Documentation]    GIVEN CRITICAL severity WHEN I format THEN red + bold + triple stars
    When I Run Python Code    from lynx_tech.models import format_severity, Severity; s = format_severity(Severity.CRITICAL); assert '***CRITICAL***' in s and 'bold red' in s; print('OK')
    Then The Output Should Contain    OK

Severity Format Strong Silver
    [Documentation]    GIVEN STRONG severity WHEN I format THEN silver/grey
    When I Run Python Code    from lynx_tech.models import format_severity, Severity; s = format_severity(Severity.STRONG); assert '[STRONG]' in s and 'grey' in s; print('OK')
    Then The Output Should Contain    OK

Impact Format Critical Blinks Red
    [Documentation]    GIVEN CRITICAL relevance WHEN I format impact THEN blink + red
    When I Run Python Code    from lynx_tech.models import format_impact, Relevance; s = format_impact(Relevance.CRITICAL); assert 'blink' in s and 'red' in s; print('OK')
    Then The Output Should Contain    OK

Impact Format Irrelevant Silver
    [Documentation]    GIVEN IRRELEVANT relevance WHEN I format impact THEN silver/grey
    When I Run Python Code    from lynx_tech.models import format_impact, Relevance; s = format_impact(Relevance.IRRELEVANT); assert 'grey' in s; print('OK')
    Then The Output Should Contain    OK

Sector Validation Allows Technology
    [Documentation]    GIVEN a SaaS company WHEN I validate THEN allowed
    When I Run Python Code    from lynx_tech.core.analyzer import _validate_sector; from lynx_tech.models import CompanyProfile; p = CompanyProfile(ticker='CRM', name='Salesforce', sector='Technology', industry='Software - Application'); _validate_sector(p); print('ALLOWED')
    Then The Output Should Contain    ALLOWED

Conclusion Generation Returns Verdict
    [Documentation]    GIVEN a minimal report WHEN I generate conclusion THEN verdict is present
    When I Run Python Code    from lynx_tech.models import AnalysisReport, CompanyProfile; from lynx_tech.core.conclusion import generate_conclusion; r = AnalysisReport(profile=CompanyProfile(ticker='T', name='T')); c = generate_conclusion(r); print(c.verdict)
    Then The Output Should Contain    Hold

Tech Screening Checklist Present
    [Documentation]    GIVEN a report WHEN I screen THEN rule_of_40_pass key exists
    When I Run Python Code    from lynx_tech.models import AnalysisReport, CompanyProfile; from lynx_tech.core.conclusion import generate_conclusion; r = AnalysisReport(profile=CompanyProfile(ticker='T', name='T')); c = generate_conclusion(r); print('rule_of_40_pass' in c.screening_checklist)
    Then The Output Should Contain    True

Metric Explanations Tech Specific
    [Documentation]    GIVEN explanations WHEN I list THEN tech metrics present
    When I Run Python Code    from lynx_tech.metrics.explanations import list_metrics; keys = [m.key for m in list_metrics()]; print('rule_of_40' in keys and 'sbc_to_revenue' in keys and 'ev_gross_profit' in keys and 'cash_to_market_cap' in keys)
    Then The Output Should Contain    True
