#!/usr/bin/env python3
"""Generate test coverage report for .rac files."""

import re
from pathlib import Path

def analyze_rac_file(path):
    """Analyze a .rac file for variables and tests."""
    content = path.read_text()

    # Find all variable definitions
    var_pattern = r'^variable\s+(\w+):'
    variables = re.findall(var_pattern, content, re.MULTILINE)

    # Check if tests exist
    has_tests = 'tests:' in content

    # Count test cases
    test_count = len(re.findall(r'^\s+- name:', content, re.MULTILINE))

    return {
        'path': str(path),
        'variables': variables,
        'has_tests': has_tests,
        'test_count': test_count
    }

def main():
    root = Path('statute/rtc')
    rac_files = sorted(root.glob('**/*.rac'))

    total_vars = 0
    tested_vars = 0
    total_tests = 0

    print("=" * 70)
    print("VARIABLE TEST COVERAGE REPORT")
    print("=" * 70)
    print()

    for f in rac_files:
        info = analyze_rac_file(f)
        if info['variables']:
            for var in info['variables']:
                total_vars += 1
                status = "✓" if info['has_tests'] else "✗"
                if info['has_tests']:
                    tested_vars += 1
                    total_tests += info['test_count']
                print(f"{status} {var:40} {f} ({info['test_count']} tests)")

    print()
    print("=" * 70)
    pct = (tested_vars / total_vars * 100) if total_vars else 0
    print(f"COVERAGE: {tested_vars}/{total_vars} variables tested ({pct:.0f}%)")
    print(f"TOTAL TESTS: {total_tests}")
    print("=" * 70)

if __name__ == '__main__':
    main()
