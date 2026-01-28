"""
Main Orchestrator for PDF-to-Podcast System

Coordinates the three agents (PDF Extractor, Podcast Generator, Verifier)
using LangGraph workflow to produce a complete podcast script with verification report.
"""

import os
import json
import sys
from pathlib import Path
from dotenv import load_dotenv

from workflow import PodcastWorkflow
from utils.helpers import format_verification_report, save_json_report, count_words
from utils.llm_provider import create_llm_provider


class PodcastOrchestrator:
    """Orchestrates the end-to-end podcast generation pipeline using LangGraph."""

    def __init__(self, config_path: str):
        """
        Initialize orchestrator with configuration.

        Args:
            config_path: Path to JSON configuration file
        """
        # Load environment variables
        load_dotenv()

        # Get LLM provider configuration
        provider_type = os.getenv("LLM_PROVIDER", "ollama").lower()

        # Create LLM provider (will raise ValueError if config is invalid)
        try:
            llm_provider = create_llm_provider(provider_type=provider_type)
        except ValueError as e:
            raise ValueError(
                f"Failed to initialize LLM provider: {e}\n"
                f"Please check your .env file configuration."
            )

        # Load configuration
        with open(config_path, 'r') as f:
            self.config = json.load(f)

        self.pdf_path = self.config['pdf_path']
        self.sections = self.config['sections']
        self.target_word_count = self.config.get('target_word_count', 2000)

        # Initialize LangGraph workflow
        self.workflow = PodcastWorkflow(llm_provider)

        print(f"✓ Orchestrator initialized with LangGraph")
        print(f"  LLM Provider: {provider_type}")
        print(f"  PDF: {self.pdf_path}")
        print(f"  Sections: {len(self.sections)}")
        print(f"  Target word count: {self.target_word_count}")

    def run(self, output_dir: str = "example_output") -> dict:
        """
        Execute the complete pipeline using LangGraph workflow.

        Args:
            output_dir: Directory to save outputs

        Returns:
            Dictionary with paths to generated files
        """
        # Create output directory
        Path(output_dir).mkdir(exist_ok=True)

        # Run the LangGraph workflow
        final_state = self.workflow.run(
            pdf_path=self.pdf_path,
            sections_config=self.sections,
            target_word_count=self.target_word_count
        )

        # Check if workflow completed successfully
        if final_state["status"] != "verification_complete":
            error_msg = final_state.get("error", "Unknown error")
            raise RuntimeError(f"Workflow failed: {error_msg}")

        # Extract results from state
        script = final_state["podcast_script"]
        verification_report = final_state["verification_report"]
        script_word_count = count_words(script)

        print("\n[Saving Outputs]")

        # Save script
        script_path = os.path.join(output_dir, "podcast_script.md")
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write("# Podcast Script\n\n")
            f.write(script)
        print(f"✓ Saved script to: {script_path}")

        # Save verification report (Markdown)
        report_md = format_verification_report(verification_report)
        report_md_path = os.path.join(output_dir, "verification_report.md")
        with open(report_md_path, 'w', encoding='utf-8') as f:
            f.write(report_md)
        print(f"✓ Saved markdown report to: {report_md_path}")

        # Save verification report (JSON)
        report_json_path = os.path.join(output_dir, "verification_report.json")
        save_json_report(verification_report, report_json_path)
        print(f"✓ Saved JSON report to: {report_json_path}")

        return {
            "script_path": script_path,
            "report_md_path": report_md_path,
            "report_json_path": report_json_path,
            "script_word_count": script_word_count
        }


def main():
    """Main entry point."""
    # Default config path
    config_path = "config.json"

    # Allow config path as command line argument
    if len(sys.argv) > 1:
        config_path = sys.argv[1]

    # Check if config exists
    if not os.path.exists(config_path):
        print(f"Error: Configuration file not found: {config_path}")
        print("\nUsage: python src/main.py [config.json]")
        sys.exit(1)

    # Check if PDF exists
    with open(config_path, 'r') as f:
        config = json.load(f)

    pdf_path = config['pdf_path']
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file not found: {pdf_path}")
        print(f"\nPlease ensure the PDF exists at the path specified in {config_path}")
        sys.exit(1)

    try:
        # Run orchestrator
        orchestrator = PodcastOrchestrator(config_path)
        results = orchestrator.run()

        print("\n✅ All outputs generated successfully!")
        print(f"\nScript: {results['script_path']}")
        print(f"Verification Report: {results['report_md_path']}")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
