# cosilico-us-ca

California state tax and benefit statute encodings in Cosilico DSL.

## Overview

This repository contains machine-readable encodings of California tax law, specifically the California Revenue and Taxation Code (RTC). These encodings compile to Python, JavaScript, and WASM for use in tax calculators and microsimulation.

## Coverage

### Implemented

| Statute | Description | Status |
|---------|-------------|--------|
| **RTC 17041** | Personal Income Tax Rates (9 brackets: 1% to 12.3%) | Complete |
| **RTC 17043** | Mental Health Services Tax (1% on income > $1M) | Complete |
| **RTC 17054** | Standard Deduction | Complete |
| **RTC 17052** | California Earned Income Tax Credit (CalEITC) | Complete |
| **RTC 17052.1** | Young Child Tax Credit (YCTC) | Complete |
| **RTC 17081** | Renter's Credit | Complete |

### Planned

- RTC 17053 - Low-Income Housing Tax Credit
- RTC 17054.5 - Personal Exemption Credits
- RTC 17131-17145 - California Additions and Subtractions to AGI
- RTC 17062 - Alternative Minimum Tax (AMT)

## Structure

```
cosilico-us-ca/
├── statute/                    # All enacted statutes
│   └── rtc/                   # Revenue and Taxation Code
│       ├── 17041/             # Section 17041 - Personal Income Tax Rates
│       │   ├── income_tax.cosilico
│       │   └── parameters.yaml
│       ├── 17043/             # Section 17043 - Mental Health Services Tax
│       │   ├── mhs_tax.cosilico
│       │   └── parameters.yaml
│       ├── 17052/             # Section 17052 - CalEITC
│       │   ├── caleitc.cosilico
│       │   └── parameters.yaml
│       ├── 17052.1/           # Section 17052.1 - Young Child Tax Credit
│       │   ├── yctc.cosilico
│       │   └── parameters.yaml
│       ├── 17054/             # Section 17054 - Standard Deduction
│       │   ├── standard_deduction.cosilico
│       │   └── parameters.yaml
│       └── 17081/             # Section 17081 - Renter's Credit
│           ├── renters_credit.cosilico
│           └── parameters.yaml
│
├── ftb/                       # Franchise Tax Board consolidated parameters
│   ├── 2024/
│   │   └── parameters.yaml    # 2024 tax year (official)
│   ├── 2025/
│   │   └── parameters.yaml    # 2025 tax year (projected)
│   └── 2026/
│       └── parameters.yaml    # 2026 tax year (projected)
│
└── tests/                     # Validation test cases
    └── integration/
        ├── test_income_tax.yaml
        └── test_caleitc.yaml
```

## Usage

```python
from cosilico_engine import load_statute

ca_income_tax = load_statute("cosilico-us-ca/statute/rtc/17041/income_tax")

# Calculate California income tax
tax = ca_income_tax.calculate(
    taxable_income=75000,
    filing_status="single"
)
```

## Key Features

### Tax Rates (RTC 17041)
California has 9 marginal tax brackets:
- 1%, 2%, 4%, 6%, 8%, 9.3%, 10.3%, 11.3%, 12.3%
- Thresholds vary by filing status and are adjusted annually for inflation

### Mental Health Services Tax (RTC 17043)
- 1% surtax on taxable income exceeding $1 million
- Enacted via Proposition 63 (2004)
- Brings top marginal rate to **13.3%** for high earners
- Threshold NOT indexed for inflation

### CalEITC (RTC 17052)
- Refundable credit for low-income workers
- Maximum credit: $3,644 (3+ children, 2024)
- Income limit: $31,950 (2024)
- Includes self-employment income

### Young Child Tax Credit (RTC 17052.1)
- Additional refundable credit for families with children under 6
- Maximum credit: $1,154 (2024)
- Must qualify for CalEITC

### Renter's Credit (RTC 17081)
- Nonrefundable credit for qualifying renters
- $60 single / $120 joint (frozen since 1979)
- AGI limits indexed annually

## Data Sources

- [California Franchise Tax Board](https://ftb.ca.gov)
- [California Legislative Information](https://leginfo.legislature.ca.gov)
- [FTB Form 540 Booklet](https://www.ftb.ca.gov/forms/2024/2024-540-booklet.html)
- [FTB Form 3514 (CalEITC/YCTC)](https://www.ftb.ca.gov/forms/2024/2024-3514.html)

## Parameter Years

| Year | Status | Notes |
|------|--------|-------|
| 2024 | Official | Published by FTB |
| 2025 | Projected | ~3.1% CCPI adjustment |
| 2026 | Projected | ~2.5% inflation estimate |

## Related Repos

- **cosilico-us** - Federal tax statutes (Title 26 IRC)
- **cosilico-engine** - DSL compiler and runtime
- **cosilico-validators** - Validation against external calculators

## License

MIT License - See LICENSE file for details.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on adding new statutes.
