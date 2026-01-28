"""
Podcast Script Generator Agent

Responsibility: Generate natural, two-host podcast scripts from source content.
Uses LLM provider (Anthropic or Ollama) with carefully crafted prompts to ensure
conversational quality, friction, and substantive teaching.
"""

from typing import Dict
from utils.llm_provider import LLMProvider
from utils.logger import get_logger

logger = get_logger(__name__)


class PodcastGenerator:
    """Generates two-host podcast scripts using LLM."""

    def __init__(self, llm_provider: LLMProvider):
        """
        Initialize the podcast generator.

        Args:
            llm_provider: LLM provider instance (Anthropic or Ollama)
        """
        self.llm_provider = llm_provider

    def generate_script(
        self,
        sections: Dict[str, str],
        target_word_count: int = 2000
    ) -> str:
        """
        Generate a podcast script from extracted sections.

        Args:
            sections: Dictionary of section name -> text content
            target_word_count: Target word count for the script

        Returns:
            Generated podcast script as string
        """
        logger.info(f"Generating podcast script from {len(sections)} sections")
        logger.info(f"Target word count: {target_word_count}")

        # Build the content summary for the prompt
        content_summary = self._build_content_summary(sections)
        logger.debug(f"Content summary:\n{content_summary}")

        # Construct the system prompt
        system_prompt = self._build_system_prompt(target_word_count)
        logger.debug(f"System prompt length: {len(system_prompt)} characters")

        # Construct the user prompt
        user_prompt = self._build_user_prompt(sections, content_summary)
        logger.debug(f"User prompt length: {len(user_prompt)} characters")

        # Call LLM provider
        logger.info("Calling LLM provider for script generation...")
        response = self.llm_provider.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=1.0,  # Higher temperature for more natural conversation
            max_tokens=8000
        )

        word_count = len(response.split())
        logger.info(f"✓ Script generated: {word_count} words")

        return response

    def _build_content_summary(self, sections: Dict[str, str]) -> str:
        """Build a summary of sections for context."""
        summary_parts = []
        for name, content in sections.items():
            word_count = len(content.split())
            summary_parts.append(f"- {name} ({word_count} words)")
        return "\n".join(summary_parts)

    def _build_system_prompt(self, target_word_count: int) -> str:
        """Build the system prompt for podcast generation."""
        return f"""You are an expert podcast script writer. Your task is to convert business document content into an engaging, educational two-host podcast script.

CRITICAL REQUIREMENTS:

1. LENGTH: Generate approximately {target_word_count} words (~10 minutes of spoken content)

2. HOSTS:
   - Use two distinct hosts: Alex (analytical, detail-oriented) and Jordan (strategic, big-picture)
   - Each should have a consistent personality and perspective
   - Format as "ALEX:" and "JORDAN:" for speaker labels

3. CONVERSATIONAL QUALITY:
   - This must sound like REAL dialogue between two people who know each other
   - Use natural speech patterns: interruptions, agreements, building on each other's points
   - NOT alternating monologues - actual conversation with back-and-forth
   - Include verbal cues: "Wait, that's interesting because...", "Hold on...", "You know what strikes me..."

4. TEACHING STYLE:
   - The goal is substantive understanding, not surface-level summary
   - Explain WHY things matter, not just WHAT they are
   - Break down complex concepts conversationally
   - Use analogies or examples when helpful

5. FRICTION (CRITICAL):
   - Include at least ONE substantive disagreement or challenge
   - One host should push back on an interpretation or raise a concern
   - This creates engagement and shows critical thinking
   - Don't force fake conflict - make it natural skepticism or alternative perspective

6. EMOTIONAL CUES:
   - Use lightweight, professional emotional markers:
     * Curiosity: "That's fascinating..."
     * Skepticism: "I'm not sure I buy that..."
     * Surprise: "Wait, really?"
     * Concern: "That worries me a bit..."
   - Keep it professional - no over-the-top reactions

7. STRUCTURE:
   - Opening: Brief, engaging hook (not "welcome to the show")
   - Body: Work through the content with natural flow
   - Closing: Clear "so what" takeaway - why this matters

8. ACCURACY:
   - Base ALL claims on the provided source material
   - Do not invent statistics, quotes, or facts
   - If you reference something, it must be traceable to the source

OUTPUT FORMAT:
Just the script with speaker labels. No meta-commentary, no [stage directions], no intro/outro music descriptions."""

    def _build_user_prompt(self, sections: Dict[str, str], summary: str) -> str:
        """Build the user prompt with source content."""
        prompt = f"""Generate a podcast script based on the following source material.

SECTIONS OVERVIEW:
{summary}

SOURCE CONTENT:

"""
        for section_name, content in sections.items():
            prompt += f"\n{'=' * 60}\n"
            prompt += f"SECTION: {section_name}\n"
            prompt += f"{'=' * 60}\n\n"
            prompt += content + "\n"

        prompt += """

Now generate the podcast script following all the requirements in your system instructions. Make it engaging, substantive, and natural."""

        return prompt
