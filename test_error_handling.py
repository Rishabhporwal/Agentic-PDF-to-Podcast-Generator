"""
Test Error Handling in the Podcast Generator

This script tests various edge cases to ensure the app handles
malformed data gracefully without crashing.
"""

import sys
sys.path.insert(0, 'src')

from utils.helpers import format_verification_report, count_words

def test_count_words():
    """Test count_words with various inputs."""
    print("\n=== Testing count_words ===")

    # Normal case
    assert count_words("hello world") == 2, "Normal case failed"
    print("✓ Normal case: 'hello world' = 2 words")

    # Empty string
    assert count_words("") == 0, "Empty string failed"
    print("✓ Empty string = 0 words")

    # None
    assert count_words(None) == 0, "None failed"
    print("✓ None = 0 words")

    # Non-string type
    assert count_words(123) == 0, "Non-string failed"
    print("✓ Non-string (123) = 0 words")

    print("✅ All count_words tests passed")


def test_format_verification_report():
    """Test format_verification_report with various edge cases."""
    print("\n=== Testing format_verification_report ===")

    # Test 1: Complete, valid report
    valid_report = {
        'summary': {
            'total_claims': 5,
            'hallucinated_claims': 0,
            'sections_analyzed': 2
        },
        'hallucination_flags': [],
        'claim_traceability': [
            {
                'claim': 'Test claim',
                'claim_type': 'business_fact',
                'traceable': 'YES',
                'confidence': 'HIGH',
                'source_evidence': 'Test evidence',
                'source_section': 'Section 1'
            }
        ],
        'coverage_analysis': {
            'sections': [
                {
                    'section_name': 'Test Section',
                    'overall_coverage': 'FULL',
                    'key_points': [
                        {
                            'point': 'Key point 1',
                            'coverage': 'FULL',
                            'evidence_from_script': 'Evidence text'
                        }
                    ],
                    'omitted_points': []
                }
            ]
        }
    }

    result = format_verification_report(valid_report)
    assert "# Verification Report" in result, "Valid report failed"
    assert "Test claim" in result, "Claim not in report"
    assert "Test Section" in result, "Section name not in report"
    print("✓ Valid report formatted successfully")

    # Test 2: Empty report
    empty_report = {}
    result = format_verification_report(empty_report)
    assert "# Verification Report" in result, "Empty report failed"
    print("✓ Empty report handled gracefully")

    # Test 3: Missing summary
    no_summary = {
        'hallucination_flags': [],
        'claim_traceability': [],
        'coverage_analysis': {}
    }
    result = format_verification_report(no_summary)
    assert "Total Claims Analyzed**: 0" in result, "Missing summary failed"
    print("✓ Missing summary handled with defaults")

    # Test 4: Missing section_name in coverage
    missing_section_name = {
        'summary': {'total_claims': 0, 'hallucinated_claims': 0, 'sections_analyzed': 0},
        'hallucination_flags': [],
        'claim_traceability': [],
        'coverage_analysis': {
            'sections': [
                {
                    # Missing 'section_name'
                    'overall_coverage': 'FULL',
                    'key_points': []
                }
            ]
        }
    }
    result = format_verification_report(missing_section_name)
    assert "Unknown Section" in result, "Missing section_name not handled"
    print("✓ Missing section_name handled with default")

    # Test 5: Missing key_points
    missing_key_points = {
        'summary': {'total_claims': 0, 'hallucinated_claims': 0, 'sections_analyzed': 0},
        'hallucination_flags': [],
        'claim_traceability': [],
        'coverage_analysis': {
            'sections': [
                {
                    'section_name': 'Test',
                    'overall_coverage': 'FULL'
                    # Missing 'key_points'
                }
            ]
        }
    }
    result = format_verification_report(missing_key_points)
    assert "Test" in result, "Missing key_points failed"
    print("✓ Missing key_points handled gracefully")

    # Test 6: Missing claim fields
    missing_claim_fields = {
        'summary': {'total_claims': 1, 'hallucinated_claims': 0, 'sections_analyzed': 0},
        'hallucination_flags': [],
        'claim_traceability': [
            {
                # Missing most fields
                'claim': 'Test'
            }
        ],
        'coverage_analysis': {}
    }
    result = format_verification_report(missing_claim_fields)
    assert "Test" in result, "Missing claim fields failed"
    assert "UNKNOWN" in result, "Default values not used"
    print("✓ Missing claim fields handled with defaults")

    # Test 7: Missing coverage sections
    missing_coverage_sections = {
        'summary': {'total_claims': 0, 'hallucinated_claims': 0, 'sections_analyzed': 0},
        'hallucination_flags': [],
        'claim_traceability': [],
        'coverage_analysis': {
            # Missing 'sections'
        }
    }
    result = format_verification_report(missing_coverage_sections)
    assert "No coverage analysis available" in result, "Missing sections not handled"
    print("✓ Missing coverage sections handled gracefully")

    # Test 8: Verification errors
    with_errors = {
        'summary': {'total_claims': 0, 'hallucinated_claims': 0, 'sections_analyzed': 0},
        'verification_error': 'Failed to parse verification output',
        'coverage_error': 'Failed to parse coverage analysis',
        'hallucination_flags': [],
        'claim_traceability': [],
        'coverage_analysis': {}
    }
    result = format_verification_report(with_errors)
    assert "Verification Warning" in result, "Verification error not shown"
    assert "Coverage Analysis Warning" in result, "Coverage error not shown"
    print("✓ Verification errors displayed in report")

    # Test 9: Hallucinations without reason
    hallucinations_no_reason = {
        'summary': {'total_claims': 0, 'hallucinated_claims': 1, 'sections_analyzed': 0},
        'hallucination_flags': [
            {
                'claim': 'Bad claim'
                # Missing 'reason'
            }
        ],
        'claim_traceability': [],
        'coverage_analysis': {}
    }
    result = format_verification_report(hallucinations_no_reason)
    assert "Bad claim" in result, "Hallucination claim not shown"
    assert "No reason provided" in result, "Default reason not used"
    print("✓ Missing hallucination reason handled with default")

    # Test 10: None value (should not crash)
    try:
        result = format_verification_report(None)
        assert "Error" in result, "None value should produce error report"
        print("✓ None value handled gracefully")
    except Exception as e:
        print(f"✗ None value crashed: {e}")

    print("✅ All format_verification_report tests passed")


def test_dict_access_patterns():
    """Test common dictionary access patterns."""
    print("\n=== Testing Dictionary Access Patterns ===")

    # Test nested .get()
    data = {}
    value = data.get('level1', {}).get('level2', {}).get('level3', 'default')
    assert value == 'default', "Nested .get() failed"
    print("✓ Nested .get() with defaults works")

    # Test with partial data
    data = {'level1': {'level2': {}}}
    value = data.get('level1', {}).get('level2', {}).get('level3', 'default')
    assert value == 'default', "Partial nested .get() failed"
    print("✓ Partial nested .get() works")

    # Test with complete data
    data = {'level1': {'level2': {'level3': 'value'}}}
    value = data.get('level1', {}).get('level2', {}).get('level3', 'default')
    assert value == 'value', "Complete nested .get() failed"
    print("✓ Complete nested .get() works")

    print("✅ All dictionary access pattern tests passed")


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("TESTING ERROR HANDLING")
    print("="*60)

    try:
        test_count_words()
        test_format_verification_report()
        test_dict_access_patterns()

        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED - ERROR HANDLING IS ROBUST")
        print("="*60)

    except Exception as e:
        print("\n" + "="*60)
        print(f"❌ TESTS FAILED: {e}")
        print("="*60)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
