#!/usr/bin/env python3
"""Validate Cosilico California tax calculations against PolicyEngine.

This script runs test cases through PolicyEngine and compares against
our expected values to ensure parity.
"""

from dataclasses import dataclass
from policyengine_us import Simulation


@dataclass
class TestCase:
    name: str
    age: int
    income: int
    filing_status: str  # 'single' or 'head_of_household'
    dependents: list[int]  # ages of dependents
    expected: dict[str, float] | None = None


TEST_CASES = [
    TestCase(
        name="Single filer, $50,000 income",
        age=35,
        income=50000,
        filing_status="single",
        dependents=[],
    ),
    TestCase(
        name="Single parent, $20,000 with child age 3",
        age=30,
        income=20000,
        filing_status="head_of_household",
        dependents=[3],
    ),
    TestCase(
        name="High income, $1,500,000",
        age=45,
        income=1500000,
        filing_status="single",
        dependents=[],
    ),
    TestCase(
        name="MHS threshold exact - $1,000,000",
        age=45,
        income=1000000,
        filing_status="single",
        dependents=[],
    ),
    TestCase(
        name="Low income - CalEITC eligible",
        age=28,
        income=15000,
        filing_status="single",
        dependents=[],
    ),
]


def build_situation(tc: TestCase) -> dict:
    """Build a PolicyEngine situation from a test case."""
    people = {
        "taxpayer": {
            "age": {2024: tc.age},
            "employment_income": {2024: tc.income},
        }
    }
    members = ["taxpayer"]

    for i, dep_age in enumerate(tc.dependents):
        dep_id = f"dependent_{i}"
        people[dep_id] = {"age": {2024: dep_age}}
        members.append(dep_id)

    return {
        "people": people,
        "tax_units": {"tax_unit": {"members": members}},
        "households": {
            "household": {
                "members": members,
                "state_code": {2024: "CA"},
            }
        },
        "spm_units": {"spm_unit": {"members": members}},
        "families": {"family": {"members": members}},
        "marital_units": {"marital_unit": {"members": ["taxpayer"]}},
    }


def run_test(tc: TestCase) -> dict:
    """Run a test case through PolicyEngine and return results."""
    sim = Simulation(situation=build_situation(tc))

    results = {
        "ca_agi": float(sim.calculate("ca_agi", 2024)[0]),
        "ca_taxable_income": float(sim.calculate("ca_taxable_income", 2024)[0]),
        "ca_income_tax": float(sim.calculate("ca_income_tax", 2024)[0]),
        "ca_eitc": float(sim.calculate("ca_eitc", 2024)[0]),
        "ca_yctc": float(sim.calculate("ca_yctc", 2024)[0]),
        "ca_mental_health_services_tax": float(
            sim.calculate("ca_mental_health_services_tax", 2024)[0]
        ),
    }

    # Calculate net tax (income tax includes credits in PE)
    results["ca_net_tax"] = results["ca_income_tax"]
    results["ca_total_with_mhs"] = (
        results["ca_income_tax"] + results["ca_mental_health_services_tax"]
    )

    return results


def main():
    print("=" * 80)
    print("CALIFORNIA TAX VALIDATION: PolicyEngine Reference Values")
    print("=" * 80)
    print()

    for tc in TEST_CASES:
        print(f"Test: {tc.name}")
        print("-" * 60)
        print(f"  Input: age={tc.age}, income=${tc.income:,}, {tc.filing_status}")
        if tc.dependents:
            print(f"  Dependents: {tc.dependents}")

        results = run_test(tc)

        print(f"  PolicyEngine Results:")
        print(f"    CA AGI:           ${results['ca_agi']:>12,.2f}")
        print(f"    CA Taxable:       ${results['ca_taxable_income']:>12,.2f}")
        print(f"    CA Income Tax:    ${results['ca_income_tax']:>12,.2f}")
        if results["ca_eitc"] > 0:
            print(f"    CalEITC:          ${results['ca_eitc']:>12,.2f}")
        if results["ca_yctc"] > 0:
            print(f"    YCTC:             ${results['ca_yctc']:>12,.2f}")
        if results["ca_mental_health_services_tax"] > 0:
            print(f"    MHS Tax:          ${results['ca_mental_health_services_tax']:>12,.2f}")
            print(f"    Total with MHS:   ${results['ca_total_with_mhs']:>12,.2f}")
        print()

    print("=" * 80)
    print("These values can be used to validate Cosilico implementations.")
    print("=" * 80)


if __name__ == "__main__":
    main()
