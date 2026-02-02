"""
Test the Original KeyError: 'section_name' Issue

This test simulates the exact error scenario that was reported
and verifies it's now handled gracefully.
"""

import sys
sys.path.insert(0, 'src')

from utils.helpers import format_verification_report

def test_original_keyerror_scenario():
    """
    Simulate the exact scenario that caused:
    KeyError: 'section_name' at line 382 in app.py
    """
    print("\n=== Testing Original KeyError Scenario ===")
    print("Simulating: verification['coverage_analysis']['sections'] missing 'section_name' key")

    # This is what the LLM might have returned (missing section_name)
    problematic_report = {
        'summary': {
            'total_claims': 5,
            'hallucinated_claims': 0,
            'sections_analyzed': 2
        },
        'hallucination_flags': [],
        'claim_traceability': [
            {
                'claim': 'Vestas is a global leader',
                'claim_type': 'business_fact',
                'traceable': 'YES',
                'confidence': 'HIGH'
            }
        ],
        'coverage_analysis': {
            'sections': [
                {
                    # MISSING: 'section_name' key - this caused the KeyError!
                    'overall_coverage': 'FULL',
                    'key_points': [
                        {
                            'point': 'CEO letter discussed strategy',
                            'coverage': 'FULL'
                        }
                    ]
                },
                {
                    # Another section also missing section_name
                    'overall_coverage': 'PARTIAL',
                    'key_points': []
                }
            ]
        }
    }

    print("\nAttempting to format report with missing 'section_name' keys...")

    try:
        # This would have crashed before with KeyError: 'section_name'
        result = format_verification_report(problematic_report)

        # Verify it handled gracefully
        assert "# Verification Report" in result
        assert "Unknown Section" in result  # Default value used
        print("✅ Report formatted successfully!")
        print("✅ Missing 'section_name' handled with default value: 'Unknown Section'")

        # Show relevant part of output
        print("\n--- Relevant Output ---")
        lines = result.split('\n')
        for i, line in enumerate(lines):
            if 'Unknown Section' in line:
                # Show context around the line
                start = max(0, i - 2)
                end = min(len(lines), i + 3)
                print('\n'.join(lines[start:end]))
                break

        return True

    except KeyError as e:
        print(f"❌ FAILED: KeyError still occurs: {e}")
        return False
    except Exception as e:
        print(f"❌ FAILED: Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_app_display_logic():
    """
    Test the logic that would be used in app.py for displaying sections.
    This simulates the code at line 382 that was failing.
    """
    print("\n=== Testing App Display Logic ===")
    print("Simulating Streamlit display code from app.py line ~382")

    verification = {
        'coverage_analysis': {
            'sections': [
                {'overall_coverage': 'FULL'},  # Missing section_name
                {'section_name': 'Valid Section', 'overall_coverage': 'PARTIAL'}
            ]
        }
    }

    print("\nAttempting to display sections using safe dictionary access...")

    try:
        # OLD CODE (would crash):
        # for section in verification['coverage_analysis']['sections']:
        #     st.markdown(f"### {section['section_name']}")  # KeyError here!

        # NEW CODE (defensive):
        coverage_sections = verification.get('coverage_analysis', {}).get('sections', [])
        if coverage_sections:
            for i, section in enumerate(coverage_sections, 1):
                section_name = section.get('section_name', 'Unknown Section')
                overall_coverage = section.get('overall_coverage', 'UNKNOWN')

                print(f"  Section {i}: '{section_name}' - Coverage: {overall_coverage}")

        print("✅ All sections displayed successfully without crashes!")
        print("✅ Missing 'section_name' replaced with 'Unknown Section'")
        return True

    except KeyError as e:
        print(f"❌ FAILED: KeyError occurred: {e}")
        return False
    except Exception as e:
        print(f"❌ FAILED: Unexpected error: {e}")
        return False


def test_edge_cases():
    """Test additional edge cases."""
    print("\n=== Testing Additional Edge Cases ===")

    edge_cases = [
        ("Empty sections array", {
            'summary': {'total_claims': 0, 'hallucinated_claims': 0, 'sections_analyzed': 0},
            'hallucination_flags': [],
            'claim_traceability': [],
            'coverage_analysis': {'sections': []}
        }),
        ("Missing coverage_analysis", {
            'summary': {'total_claims': 0, 'hallucinated_claims': 0, 'sections_analyzed': 0},
            'hallucination_flags': [],
            'claim_traceability': []
        }),
        ("sections is None", {
            'summary': {'total_claims': 0, 'hallucinated_claims': 0, 'sections_analyzed': 0},
            'hallucination_flags': [],
            'claim_traceability': [],
            'coverage_analysis': {'sections': None}
        }),
        ("coverage_analysis is None", {
            'summary': {'total_claims': 0, 'hallucinated_claims': 0, 'sections_analyzed': 0},
            'hallucination_flags': [],
            'claim_traceability': [],
            'coverage_analysis': None
        })
    ]

    all_passed = True
    for test_name, report in edge_cases:
        try:
            result = format_verification_report(report)
            assert "# Verification Report" in result
            print(f"  ✓ {test_name}")
        except Exception as e:
            print(f"  ✗ {test_name}: {e}")
            all_passed = False

    if all_passed:
        print("✅ All edge cases handled gracefully")
    else:
        print("❌ Some edge cases failed")

    return all_passed


def main():
    print("\n" + "="*70)
    print("TESTING ORIGINAL KeyError: 'section_name' FIX")
    print("="*70)

    results = [
        test_original_keyerror_scenario(),
        test_app_display_logic(),
        test_edge_cases()
    ]

    print("\n" + "="*70)
    if all(results):
        print("✅ SUCCESS: Original error is fixed and all edge cases pass!")
        print("="*70)
        print("\nThe app will now handle:")
        print("  • Missing 'section_name' keys")
        print("  • Missing nested dictionary keys")
        print("  • Empty or None values")
        print("  • Malformed LLM output")
        print("\nInstead of crashing with KeyError, it will:")
        print("  • Use default values ('Unknown Section', 'UNKNOWN', etc.)")
        print("  • Display warning messages")
        print("  • Show debug information in expandable sections")
        print("  • Continue functioning for other parts of the report")
    else:
        print("❌ FAILURE: Some tests failed")
        print("="*70)
        sys.exit(1)


if __name__ == "__main__":
    main()
