"""
Utility helper functions for the podcast generation system.
"""

from typing import Dict, Any
import json


def format_verification_report(report: Dict[str, Any]) -> str:
    """
    Format verification report as readable Markdown.

    Args:
        report: Verification report dictionary

    Returns:
        Formatted markdown string
    """
    try:
        md = "# Verification Report\n\n"

        # Summary
        md += "## Summary\n\n"
        summary = report.get('summary', {})
        md += f"- **Total Claims Analyzed**: {summary.get('total_claims', 0)}\n"
        md += f"- **Hallucinated Claims**: {summary.get('hallucinated_claims', 0)}\n"
        md += f"- **Sections Analyzed**: {summary.get('sections_analyzed', 0)}\n\n"

        # Show any errors
        if 'verification_error' in report:
            md += f"⚠️ **Verification Warning**: {report['verification_error']}\n\n"
        if 'coverage_error' in report:
            md += f"⚠️ **Coverage Analysis Warning**: {report['coverage_error']}\n\n"

        # Hallucination Flags
        md += "## Hallucination Flags\n\n"
        hallucination_flags = report.get('hallucination_flags', [])
        if hallucination_flags:
            for i, flag in enumerate(hallucination_flags, 1):
                md += f"### Flag {i}\n\n"
                md += f"**Claim**: \"{flag.get('claim', 'Unknown')}\"\n\n"
                md += f"**Reason**: {flag.get('reason', 'No reason provided')}\n\n"
        else:
            md += "*No hallucinations detected. All claims are traceable to source material.*\n\n"

        # Claim Traceability
        md += "## Claim Traceability\n\n"
        claims = report.get('claim_traceability', [])
        if claims:
            md += "Detailed mapping of claims to source material:\n\n"
            for i, claim in enumerate(claims, 1):
                md += f"### Claim {i}\n\n"
                md += f"**Statement**: \"{claim.get('claim', 'Unknown')}\"\n\n"
                md += f"**Type**: {claim.get('claim_type', 'unknown')}\n\n"
                md += f"**Traceable**: {claim.get('traceable', 'UNKNOWN')}\n\n"
                md += f"**Confidence**: {claim.get('confidence', 'UNKNOWN')}\n\n"

                if claim.get('source_section'):
                    md += f"**Source Section**: {claim['source_section']}\n\n"

                if claim.get('source_evidence'):
                    md += f"**Source Evidence**:\n> {claim['source_evidence']}\n\n"
                else:
                    md += "**Source Evidence**: Not found\n\n"

                md += "---\n\n"
        else:
            md += "*No claims extracted from script.*\n\n"

        # Coverage Analysis
        md += "## Coverage Analysis\n\n"
        coverage_analysis = report.get('coverage_analysis', {})
        sections = coverage_analysis.get('sections', [])

        if sections:
            md += "Analysis of how well each source section was covered in the podcast:\n\n"
            for section in sections:
                section_name = section.get('section_name', 'Unknown Section')
                overall_coverage = section.get('overall_coverage', 'UNKNOWN')

                md += f"### {section_name}\n\n"
                md += f"**Overall Coverage**: {overall_coverage}\n\n"

                key_points = section.get('key_points', [])
                if key_points:
                    md += "**Key Points**:\n\n"
                    for point in key_points:
                        coverage = point.get('coverage', 'UNKNOWN')
                        point_text = point.get('point', 'Unknown point')
                        coverage_icon = {
                            'FULL': '✅',
                            'PARTIAL': '⚠️',
                            'OMITTED': '❌'
                        }.get(coverage, '❓')

                        md += f"{coverage_icon} **{coverage}**: {point_text}\n\n"

                        if point.get('evidence_from_script'):
                            md += f"  *Script evidence*: \"{point['evidence_from_script']}\"\n\n"

                omitted_points = section.get('omitted_points', [])
                if omitted_points:
                    md += "\n**Omitted Information**:\n"
                    for omitted in omitted_points:
                        md += f"- {omitted}\n"
                    md += "\n"

                md += "---\n\n"
        else:
            md += "*No coverage analysis available.*\n\n"

        return md

    except Exception as e:
        # Return error report if formatting fails
        return f"# Verification Report\n\n**Error**: Failed to format report - {str(e)}\n\n**Raw Report**:\n```json\n{json.dumps(report, indent=2)}\n```"


def save_json_report(report: Dict[str, Any], filepath: str):
    """
    Save verification report as JSON.

    Args:
        report: Verification report dictionary
        filepath: Path to save JSON file
    """
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)


def count_words(text: str) -> int:
    """
    Count words in text.

    Args:
        text: Input text

    Returns:
        Word count
    """
    if not text or not isinstance(text, str):
        return 0
    return len(text.split())
