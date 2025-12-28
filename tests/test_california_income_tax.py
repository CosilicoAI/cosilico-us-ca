"""Tests for California income tax .rac files.

TDD tests validating:
1. Cross-package imports from cosilico-us
2. California tax bracket calculations
3. Standard deduction
4. Mental Health Services Tax
"""

import pytest
from pathlib import Path
import sys

# Add cosilico-engine to path
# __file__ = .../cosilico-us-ca/tests/test_california_income_tax.py
# parents[2] = .../CosilicoAI (workspace)
engine_path = Path(__file__).parents[2] / "cosilico-engine"
sys.path.insert(0, str(engine_path / "src"))

from cosilico.dsl_parser import parse_dsl, parse_file
from cosilico.dependency_resolver import (
    DependencyResolver,
    PackageRegistry,
    extract_dependencies,
)


@pytest.fixture
def workspace_path():
    """Get workspace path containing both cosilico-us and cosilico-us-ca."""
    # __file__ = .../cosilico-us-ca/tests/test_california_income_tax.py
    # parents[0] = .../cosilico-us-ca/tests
    # parents[1] = .../cosilico-us-ca
    # parents[2] = .../CosilicoAI (workspace)
    return Path(__file__).parents[2]


@pytest.fixture
def package_registry(workspace_path):
    """Create package registry with both US and CA repos."""
    registry = PackageRegistry.from_workspace(workspace_path)
    registry.set_default("cosilico-us-ca")
    return registry


class TestCaliforniaStandardDeduction:
    """Test California standard deduction (RTC 17054)."""

    def test_parse_standard_deduction_file(self):
        """Standard deduction file parses successfully."""
        file_path = Path(__file__).parents[1] / "statute/rtc/17054.rac"
        if not file_path.exists():
            pytest.skip("statute/rtc/17054.rac not yet created")

        module = parse_file(str(file_path))

        # Should have the ca_personal_exemption_credit variable
        var_names = [v.name for v in module.variables]
        assert "ca_personal_exemption_credit" in var_names

    def test_standard_deduction_file_content(self):
        """Standard deduction file contains parameter declarations."""
        file_path = Path(__file__).parents[1] / "statute/rtc/17054.rac"
        if not file_path.exists():
            pytest.skip("statute/rtc/17054.rac not yet created")

        # Read raw file content to verify parameters are declared
        content = file_path.read_text()
        assert "ca_standard_deduction" in content
        assert "1500" in content  # base single value
        assert "3000" in content  # base joint value


class TestCaliforniaTaxBrackets:
    """Test California income tax brackets (RTC 17041/a)."""

    def test_parse_tax_brackets_file(self):
        """Tax brackets file parses successfully."""
        file_path = Path(__file__).parents[1] / "statute/rtc/17041/a.rac"
        if not file_path.exists():
            pytest.skip("statute/rtc/17041/a.rac not yet created")

        module = parse_file(str(file_path))

        # Should have the ca_income_tax variable
        var_names = [v.name for v in module.variables]
        assert "ca_income_tax" in var_names

    def test_tax_brackets_imports_federal_agi(self):
        """Tax brackets imports federal AGI from cosilico-us."""
        file_path = Path(__file__).parents[1] / "statute/rtc/17041/a.rac"
        if not file_path.exists():
            pytest.skip("statute/rtc/17041/a.rac not yet created")

        module = parse_file(str(file_path))
        deps = extract_dependencies(module)

        # Should have import from cosilico-us
        packages = [pkg for pkg, path in deps if pkg is not None]
        assert "cosilico-us" in packages

    def test_has_brackets_parameter(self):
        """California has ca_brackets parameter with thresholds and rates."""
        file_path = Path(__file__).parents[1] / "statute/rtc/17041/a.rac"
        if not file_path.exists():
            pytest.skip("statute/rtc/17041/a.rac not yet created")

        content = file_path.read_text()

        # Check for ca_brackets parameter with marginal_agg structure
        assert "parameter ca_brackets:" in content
        assert "thresholds:" in content
        assert "rates:" in content
        assert "marginal_agg" in content

    def test_uses_marginal_agg(self):
        """Formula uses marginal_agg for bracket calculations."""
        file_path = Path(__file__).parents[1] / "statute/rtc/17041/a.rac"
        if not file_path.exists():
            pytest.skip("statute/rtc/17041/a.rac not yet created")

        content = file_path.read_text()
        assert "marginal_agg(ca_taxable_income, ca_brackets, threshold_by=filing_status)" in content


class TestMentalHealthServicesTax:
    """Test Mental Health Services Tax (RTC 17043/a)."""

    def test_parse_mhs_tax_file(self):
        """MHS tax file parses successfully."""
        file_path = Path(__file__).parents[1] / "statute/rtc/17043/a.rac"
        if not file_path.exists():
            pytest.skip("statute/rtc/17043/a.rac not yet created")

        module = parse_file(str(file_path))

        # Should have the mhs_tax variable
        var_names = [v.name for v in module.variables]
        assert "ca_mental_health_services_tax" in var_names

    def test_mhs_threshold_is_one_million(self):
        """MHS tax threshold is $1 million."""
        file_path = Path(__file__).parents[1] / "statute/rtc/17043/a.rac"
        if not file_path.exists():
            pytest.skip("statute/rtc/17043/a.rac not yet created")

        content = file_path.read_text()
        assert "ca_mhs_threshold" in content
        assert "1000000" in content

    def test_mhs_rate_is_one_percent(self):
        """MHS tax rate is 1%."""
        file_path = Path(__file__).parents[1] / "statute/rtc/17043/a.rac"
        if not file_path.exists():
            pytest.skip("statute/rtc/17043/a.rac not yet created")

        content = file_path.read_text()
        assert "ca_mhs_rate" in content
        assert "0.01" in content


class TestExemptionCredits:
    """Test Personal Exemption Credits (RTC 17054 subsections)."""

    def test_single_exemption_base(self):
        """Single exemption base is $52."""
        file_path = Path(__file__).parents[1] / "statute/rtc/17054/a.rac"
        if not file_path.exists():
            pytest.skip("statute/rtc/17054/a.rac not yet created")

        content = file_path.read_text()
        assert "ca_personal_exemption_single_base" in content
        assert "52" in content

    def test_joint_exemption_base(self):
        """Joint exemption base is $104."""
        file_path = Path(__file__).parents[1] / "statute/rtc/17054/b.rac"
        if not file_path.exists():
            pytest.skip("statute/rtc/17054/b.rac not yet created")

        content = file_path.read_text()
        assert "ca_personal_exemption_joint_base" in content
        assert "104" in content

    def test_dependent_exemption_base(self):
        """Dependent exemption base is $227."""
        file_path = Path(__file__).parents[1] / "statute/rtc/17054/d.rac"
        if not file_path.exists():
            pytest.skip("statute/rtc/17054/d.rac not yet created")

        content = file_path.read_text()
        assert "ca_dependent_exemption_base" in content
        assert "227" in content


class TestCrossPackageDependencyResolution:
    """Test that CA files correctly resolve federal dependencies."""

    def test_resolve_ca_tax_with_federal_agi(self, package_registry):
        """CA tax resolves federal AGI dependency."""
        file_path = Path(__file__).parents[1] / "statute/rtc/17041/a.rac"
        if not file_path.exists():
            pytest.skip("statute/rtc/17041/a.rac not yet created")

        resolver = DependencyResolver(registry=package_registry)
        modules = resolver.resolve_all("statute/rtc/17041/a")

        # Should have both CA and federal modules
        paths = [m.path for m in modules]
        assert any("17041" in p for p in paths), f"CA tax file not found in {paths}"

        # Federal AGI should be in dependencies (cache key includes package)
        has_federal = any("cosilico-us" in p for p in paths)
        assert has_federal, f"Federal AGI not in dependencies: {paths}"

    def test_topological_order_federal_before_state(self, package_registry):
        """Federal dependencies come before state dependents in execution order."""
        file_path = Path(__file__).parents[1] / "statute/rtc/17041/a.rac"
        if not file_path.exists():
            pytest.skip("statute/rtc/17041/a.rac not yet created")

        resolver = DependencyResolver(registry=package_registry)
        modules = resolver.resolve_all("statute/rtc/17041/a")

        # Find indices
        fed_idx = None
        ca_idx = None
        for i, m in enumerate(modules):
            if "cosilico-us" in m.path:
                fed_idx = i
            if "17041" in m.path:
                ca_idx = i

        if fed_idx is not None and ca_idx is not None:
            assert fed_idx < ca_idx, "Federal AGI should come before CA tax"


class TestCaliforniaTaxCalculation:
    """Integration tests for actual tax calculations."""

    @pytest.mark.skip(reason="VectorizedExecutor integration pending")
    def test_single_filer_tax_calculation(self, package_registry):
        """Calculate tax for single filer with various incomes."""
        import numpy as np
        from cosilico.vectorized_executor import VectorizedExecutor

        resolver = DependencyResolver(registry=package_registry)
        executor = VectorizedExecutor(dependency_resolver=resolver)

        # Test cases: federal AGI -> expected CA tax (approximate)
        inputs = {
            "gross_income": np.array([50000, 100000, 200000]),
            "weight": np.array([1.0, 1.0, 1.0]),
            "filing_status": np.array(["single", "single", "single"]),
        }

        results = executor.execute_with_dependencies(
            entry_point="statute/rtc/17041/a",
            inputs=inputs,
            output_variables=["ca_income_tax"],
            tax_year=2024,
        )

        # Verify reasonable tax amounts
        assert all(results["ca_income_tax"] > 0)
        # Higher income should have higher tax
        assert results["ca_income_tax"][1] > results["ca_income_tax"][0]
        assert results["ca_income_tax"][2] > results["ca_income_tax"][1]
