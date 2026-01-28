"""
Verification Agent

Responsibility: Verify podcast script accuracy against source material.
- Extract and trace factual claims
- Detect hallucinations
- Analyze coverage of key information
"""

import json
from typing import Dict, List, Any
from utils.llm_provider import LLMProvider
from utils.logger import get_logger

logger = get_logger(__name__)


class Verifier:
    """Verifies podcast script accuracy and coverage."""

    def __init__(self, llm_provider: LLMProvider):
        """
        Initialize the verifier.

        Args:
            llm_provider: LLM provider instance (Anthropic or Ollama)
        """
        self.llm_provider = llm_provider

    def verify_script(
        self,
        script: str,
        source_sections: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Verify the podcast script against source material.

        Args:
            script: The generated podcast script
            source_sections: Original source content by section

        Returns:
            Verification report as dictionary
        """
        logger.info(f"Verifying script against {len(source_sections)} source sections")

        # Step 1: Extract and trace claims
        logger.info("Step 1: Extracting and tracing claims...")
        claims_analysis = self._extract_and_trace_claims(script, source_sections)

        # Step 2: Analyze coverage
        logger.info("Step 2: Analyzing coverage...")
        coverage_analysis = self._analyze_coverage(script, source_sections)

        # Combine results (use .get() for safety)
        claims = claims_analysis.get("claims", [])
        hallucinations = claims_analysis.get("hallucinations", [])

        logger.info(f"✓ Verification complete: {len(claims)} claims, {len(hallucinations)} hallucinations")

        report = {
            "claim_traceability": claims,
            "hallucination_flags": hallucinations,
            "coverage_analysis": coverage_analysis,
            "summary": {
                "total_claims": len(claims),
                "hallucinated_claims": len(hallucinations),
                "sections_analyzed": len(source_sections)
            }
        }

        # Add error info if parsing failed
        if "error" in claims_analysis:
            logger.warning(f"Claim extraction had errors: {claims_analysis['error']}")
            report["verification_error"] = claims_analysis["error"]
        if "error" in coverage_analysis:
            logger.warning(f"Coverage analysis had errors: {coverage_analysis['error']}")
            report["coverage_error"] = coverage_analysis["error"]

        return report

    def _extract_and_trace_claims(
        self,
        script: str,
        source_sections: Dict[str, str]
    ) -> Dict[str, Any]:
        """Extract claims from script and trace them to source."""

        system_prompt = """You are a fact-checking expert. Your task is to extract factual claims from a podcast script and trace each claim back to source material.

WHAT COUNTS AS A FACTUAL CLAIM:
- Business facts (e.g., "the company operates in 80 countries")
- Market conditions (e.g., "offshore wind demand is growing")
- Strategy statements (e.g., "they're focusing on modular turbines")
- Numbers and statistics (e.g., "revenue grew by 15%")
- Stated intentions or plans (e.g., "they plan to expand in Asia")

WHAT TO EXCLUDE:
- Host opinions or interpretations (e.g., "I think this is smart")
- Conversational banter (e.g., "That's interesting")
- Rhetorical questions
- General context-setting without specific facts

FOR EACH CLAIM:
1. Extract the exact claim (quote from script)
2. Identify which source passage(s) support it
3. Assess if it's traceable (YES/NO/PARTIAL)
4. If NOT traceable or only PARTIAL, flag as potential hallucination

OUTPUT FORMAT:
Return a JSON object with this structure:
{
  "claims": [
    {
      "claim": "exact quote from script",
      "claim_type": "business_fact|market_condition|strategy|number|intention",
      "traceable": "YES|NO|PARTIAL",
      "source_evidence": "relevant quote from source material (or null if not found)",
      "source_section": "section name where found (or null)",
      "confidence": "HIGH|MEDIUM|LOW"
    }
  ],
  "hallucinations": [
    {
      "claim": "the untraceable claim",
      "reason": "why this is flagged as potential hallucination"
    }
  ]
}"""

        # Build source material context
        source_context = "SOURCE MATERIAL:\n\n"
        for section_name, content in source_sections.items():
            source_context += f"\n{'='*60}\n"
            source_context += f"SECTION: {section_name}\n"
            source_context += f"{'='*60}\n\n"
            source_context += content[:3000] + ("..." if len(content) > 3000 else "") + "\n"

        user_prompt = f"""{source_context}

PODCAST SCRIPT TO VERIFY:

{script}

Now extract all factual claims and trace them to the source material. Return ONLY the JSON output, no other text."""

        response_text = self.llm_provider.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.0,  # Low temperature for analytical task
            max_tokens=8000
        )

        # Extract JSON from response (may be wrapped in markdown)
        if "```json" in response_text:
            json_start = response_text.find("```json") + 7
            json_end = response_text.find("```", json_start)
            response_text = response_text[json_start:json_end].strip()
        elif "```" in response_text:
            json_start = response_text.find("```") + 3
            json_end = response_text.find("```", json_start)
            response_text = response_text[json_start:json_end].strip()

        try:
            result = json.loads(response_text)
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            result = {
                "claims": [],
                "hallucinations": [],
                "error": "Failed to parse verification output"
            }

        return result

    def _analyze_coverage(
        self,
        script: str,
        source_sections: Dict[str, str]
    ) -> Dict[str, Any]:
        """Analyze how well the script covers the source material."""

        system_prompt = """You are analyzing how well a podcast script covers the key information from source documents.

For each source section, assess:
1. What are the KEY POINTS in this section (2-5 main points)
2. Which key points made it into the podcast script
3. Coverage level: FULL / PARTIAL / OMITTED

Be realistic - a podcast is a summary medium. "FULL" means the main idea is conveyed even if details are omitted. "PARTIAL" means some aspect is mentioned but incomplete. "OMITTED" means the key point is not addressed at all.

OUTPUT FORMAT:
Return a JSON object:
{
  "sections": [
    {
      "section_name": "name of section",
      "key_points": [
        {
          "point": "description of key point",
          "coverage": "FULL|PARTIAL|OMITTED",
          "evidence_from_script": "quote from script showing coverage (or null if omitted)"
        }
      ],
      "overall_coverage": "FULL|PARTIAL|MINIMAL",
      "omitted_points": ["list of important omitted information"]
    }
  ]
}"""

        # Build source context
        source_context = "SOURCE MATERIAL:\n\n"
        for section_name, content in source_sections.items():
            source_context += f"\n{'='*60}\n"
            source_context += f"SECTION: {section_name}\n"
            source_context += f"{'='*60}\n\n"
            source_context += content + "\n"

        user_prompt = f"""{source_context}

PODCAST SCRIPT:

{script}

Now analyze the coverage. Return ONLY the JSON output, no other text."""

        response_text = self.llm_provider.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.0,
            max_tokens=8000
        )

        # Extract JSON from response
        if "```json" in response_text:
            json_start = response_text.find("```json") + 7
            json_end = response_text.find("```", json_start)
            response_text = response_text[json_start:json_end].strip()
        elif "```" in response_text:
            json_start = response_text.find("```") + 3
            json_end = response_text.find("```", json_start)
            response_text = response_text[json_start:json_end].strip()

        try:
            result = json.loads(response_text)
        except json.JSONDecodeError:
            result = {
                "sections": [],
                "error": "Failed to parse coverage analysis"
            }

        return result
