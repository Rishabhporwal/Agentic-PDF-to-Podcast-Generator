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
    md = "# Verification Report\n\n"

    # Summary
    md += "## Summary\n\n"
    md += f"- **Total Claims Analyzed**: {report['summary']['total_claims']}\n"
    md += f"- **Hallucinated Claims**: {report['summary']['hallucinated_claims']}\n"
    md += f"- **Sections Analyzed**: {report['summary']['sections_analyzed']}\n\n"

    # Hallucination Flags
    md += "## Hallucination Flags\n\n"
    if report['hallucination_flags']:
        for i, flag in enumerate(report['hallucination_flags'], 1):
            md += f"### Flag {i}\n\n"
            md += f"**Claim**: \"{flag['claim']}\"\n\n"
            md += f"**Reason**: {flag['reason']}\n\n"
    else:
        md += "*No hallucinations detected. All claims are traceable to source material.*\n\n"

    # Claim Traceability
    md += "## Claim Traceability\n\n"
    md += "Detailed mapping of claims to source material:\n\n"

    for i, claim in enumerate(report['claim_traceability'], 1):
        md += f"### Claim {i}\n\n"
        md += f"**Statement**: \"{claim['claim']}\"\n\n"
        md += f"**Type**: {claim['claim_type']}\n\n"
        md += f"**Traceable**: {claim['traceable']}\n\n"
        md += f"**Confidence**: {claim['confidence']}\n\n"

        if claim.get('source_section'):
            md += f"**Source Section**: {claim['source_section']}\n\n"

        if claim.get('source_evidence'):
            md += f"**Source Evidence**:\n> {claim['source_evidence']}\n\n"
        else:
            md += "**Source Evidence**: Not found\n\n"

        md += "---\n\n"

    # Coverage Analysis
    md += "## Coverage Analysis\n\n"
    md += "Analysis of how well each source section was covered in the podcast:\n\n"

    if 'sections' in report['coverage_analysis']:
        for section in report['coverage_analysis']['sections']:
            md += f"### {section['section_name']}\n\n"
            md += f"**Overall Coverage**: {section['overall_coverage']}\n\n"

            md += "**Key Points**:\n\n"
            for point in section['key_points']:
                coverage_icon = {
                    'FULL': '✅',
                    'PARTIAL': '⚠️',
                    'OMITTED': '❌'
                }.get(point['coverage'], '❓')

                md += f"{coverage_icon} **{point['coverage']}**: {point['point']}\n\n"

                if point.get('evidence_from_script'):
                    md += f"  *Script evidence*: \"{point['evidence_from_script']}\"\n\n"

            if section.get('omitted_points'):
                md += "\n**Omitted Information**:\n"
                for omitted in section['omitted_points']:
                    md += f"- {omitted}\n"
                md += "\n"

            md += "---\n\n"

    return md


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
    return len(text.split())
