*** Settings ***
Documentation    CLI integration tests for lynx-tech
Library          Process
Library          OperatingSystem

*** Variables ***
${PYTHON}        python3
${MODULE}        lynx_tech

*** Keywords ***
Run App
    [Arguments]    @{args}
    ${result}=    Run Process    ${PYTHON}    -m    ${MODULE}    @{args}    timeout=120s
    Set Test Variable    ${OUTPUT}    ${result.stdout}${result.stderr}
    Set Test Variable    ${RC}    ${result.rc}

Given The Application Is Available
    Run App    --version
    Should Contain    ${OUTPUT}    lynx-tech

When I Run The Help Command
    Run App    -p    --help

When I Run About
    Run App    --about

When I Run Version
    Run App    --version

When I Explain Metric "${metric}"
    Run App    --explain    ${metric}

When I List All Metrics
    Run App    --explain

When I Explain Section "${section}"
    Run App    --explain-section    ${section}

When I Explain Conclusion "${category}"
    Run App    --explain-conclusion    ${category}

When I Search For "${query}"
    Run App    -p    -s    ${query}

When I List Cache In Testing Mode
    Run App    -t    --list-cache

When I Drop All Cache In Testing Mode
    Run App    -t    --drop-cache    ALL

Then The Exit Code Should Be ${expected}
    Should Be Equal As Integers    ${RC}    ${expected}

Then The Output Should Contain "${text}"
    Should Contain    ${OUTPUT}    ${text}

*** Test Cases ***
Show Help
    [Documentation]    GIVEN the app is available WHEN I run help THEN it shows usage
    Given The Application Is Available
    When I Run The Help Command
    Then The Exit Code Should Be 0
    Then The Output Should Contain "lynx-tech"
    Then The Output Should Contain "production-mode"
    Then The Output Should Contain "testing-mode"
    Then The Output Should Contain "--gui"
    Then The Output Should Contain "--export"

Show Version
    [Documentation]    GIVEN the app WHEN I run version THEN it shows version info
    Given The Application Is Available
    When I Run Version
    Then The Exit Code Should Be 0
    Then The Output Should Contain "lynx-tech"
    Then The Output Should Contain "3.0"

Show About
    [Documentation]    GIVEN the app WHEN I run about THEN it shows author and license
    Given The Application Is Available
    When I Run About
    Then The Exit Code Should Be 0
    Then The Output Should Contain "Lynx Information Technology Analysis"
    Then The Output Should Contain "Borja Tarraso"
    Then The Output Should Contain "BSD-3-Clause"

Explain A Valuation Metric
    [Documentation]    GIVEN the app WHEN I explain cash_to_market_cap THEN it shows details
    Given The Application Is Available
    When I Explain Metric "cash_to_market_cap"
    Then The Exit Code Should Be 0
    Then The Output Should Contain "Cash-to-Market-Cap"

Explain A Tech-Specific Metric Rule Of 40
    [Documentation]    GIVEN the app WHEN I explain rule_of_40 THEN it shows details
    Given The Application Is Available
    When I Explain Metric "rule_of_40"
    Then The Exit Code Should Be 0
    Then The Output Should Contain "Rule of 40"

Explain A Tech-Specific Metric SBC
    [Documentation]    GIVEN the app WHEN I explain sbc_to_revenue THEN it shows SBC info
    Given The Application Is Available
    When I Explain Metric "sbc_to_revenue"
    Then The Exit Code Should Be 0
    Then The Output Should Contain "Stock-Based Compensation"

List All Available Metrics
    [Documentation]    GIVEN the app WHEN I list metrics THEN it shows the full table
    Given The Application Is Available
    When I List All Metrics
    Then The Exit Code Should Be 0
    Then The Output Should Contain "pe_trailing"
    Then The Output Should Contain "cash_to_market_cap"
    Then The Output Should Contain "quality_score"

Explain A Section
    [Documentation]    GIVEN the app WHEN I explain a section THEN it shows section description
    Given The Application Is Available
    When I Explain Section "tech_quality"
    Then The Exit Code Should Be 0
    Then The Output Should Contain "Tech Quality"

Explain Conclusion Methodology
    [Documentation]    GIVEN the app WHEN I explain conclusion THEN it shows scoring method
    Given The Application Is Available
    When I Explain Conclusion "overall"
    Then The Exit Code Should Be 0
    Then The Output Should Contain "tech quality"

Search For A Tech Company
    [Documentation]    GIVEN the app WHEN I search for a tech company THEN results are shown
    Given The Application Is Available
    When I Search For "Microsoft"
    Then The Exit Code Should Be 0
    Then The Output Should Contain "Search Results"

Drop All Test Cache
    [Documentation]    GIVEN the app WHEN I drop all test cache THEN it confirms
    Given The Application Is Available
    When I Drop All Cache In Testing Mode
    Then The Exit Code Should Be 0
    Then The Output Should Contain "Removed"

Invalid Ticker Shows Error
    [Documentation]    GIVEN the app WHEN I analyze a nonsense ticker THEN it shows an error
    Given The Application Is Available
    Run App    -t    ZZZZZZZZZZZZZ999    --no-reports    --no-news
    Then The Exit Code Should Be 1
    Then The Output Should Contain "Error"

No Identifier Shows Help
    [Documentation]    GIVEN the app WHEN I provide no identifier THEN it shows help
    Given The Application Is Available
    Run App    -p
    Then The Exit Code Should Be 1
