# cosilico-us-ca

California state tax and benefit statute encodings in Cosilico DSL.

## Overview

This repository contains machine-readable encodings of California tax law, specifically the California Revenue and Taxation Code (RTC). These encodings compile to Python, JavaScript, and WASM for use in tax calculators and microsimulation.

## Coverage

### Implemented

- **RTC 17041** - Personal Income Tax Rates (9 brackets: 1% to 12.3%)
- **RTC 17043** - Mental Health Services Tax (1% on income > $1M)
- **RTC 17054** - Standard Deduction
- **RTC 17052** - California Earned Income Tax Credit (CalEITC)
- **RTC 17052.1** - Young Child Tax Credit (YCTC)

### Planned

- RTC 17053 - Low-Income Housing Tax Credit
- RTC 17054.5 - Senior Head of Household Credit
- RTC 17131 - California Additions and Subtractions

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

## Data Sources

- [California Franchise Tax Board](https://ftb.ca.gov)
- [California Legislative Information](https://leginfo.legislature.ca.gov)
- [FTB Form 540 Booklet](https://www.ftb.ca.gov/forms/2024/2024-540-booklet.html)

## License

MIT License - See LICENSE file for details.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on adding new statutes.
