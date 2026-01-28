"""
LangGraph Workflow for Podcast Generation

Uses LangGraph to orchestrate the agentic workflow:
PDF Extraction -> Podcast Generation -> Verification
"""

from typing import TypedDict, Dict, Any
from langgraph.graph import StateGraph, END
from agents.pdf_extractor import PDFExtractor
from agents.podcast_generator import PodcastGenerator
from agents.verifier import Verifier
from utils.llm_provider import LLMProvider
from utils.logger import get_logger

logger = get_logger(__name__)


class PodcastState(TypedDict):
    """State object that flows through the workflow."""
    # Input
    pdf_path: str
    sections_config: Dict[str, list]
    target_word_count: int

    # Agent outputs
    extracted_sections: Dict[str, str]
    podcast_script: str
    verification_report: Dict[str, Any]

    # Metadata
    error: str
    status: str


class PodcastWorkflow:
    """LangGraph workflow for podcast generation pipeline."""

    def __init__(self, llm_provider: LLMProvider):
        """
        Initialize workflow with LLM provider.

        Args:
            llm_provider: LLM provider instance for agents
        """
        self.llm_provider = llm_provider

        # Initialize agents
        self.podcast_generator = PodcastGenerator(llm_provider)
        self.verifier = Verifier(llm_provider)

        # Build the workflow graph
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        """
        Build the LangGraph workflow.

        Flow: extract_pdf -> generate_podcast -> verify_script -> end
        """
        # Create the graph
        workflow = StateGraph(PodcastState)

        # Add nodes (agent steps)
        workflow.add_node("extract_pdf", self._extract_pdf_node)
        workflow.add_node("generate_podcast", self._generate_podcast_node)
        workflow.add_node("verify_script", self._verify_script_node)

        # Define edges (flow)
        workflow.set_entry_point("extract_pdf")
        workflow.add_edge("extract_pdf", "generate_podcast")
        workflow.add_edge("generate_podcast", "verify_script")
        workflow.add_edge("verify_script", END)

        # Compile the graph
        return workflow.compile()

    def _extract_pdf_node(self, state: PodcastState) -> PodcastState:
        """
        Node: Extract PDF content.

        Args:
            state: Current workflow state

        Returns:
            Updated state with extracted sections
        """
        print("\n[Agent: PDF Extractor] Extracting content from PDF...")

        try:
            with PDFExtractor(state["pdf_path"]) as extractor:
                extracted = extractor.extract_sections(state["sections_config"])

            print(f"✓ Extracted {len(extracted)} sections")
            for name, content in extracted.items():
                word_count = len(content.split())
                print(f"  - {name}: {word_count} words")

            state["extracted_sections"] = extracted
            state["status"] = "extraction_complete"

        except Exception as e:
            print(f"✗ Extraction failed: {e}")
            state["error"] = str(e)
            state["status"] = "extraction_failed"

        return state

    def _generate_podcast_node(self, state: PodcastState) -> PodcastState:
        """
        Node: Generate podcast script.

        Args:
            state: Current workflow state

        Returns:
            Updated state with podcast script
        """
        print("\n[Agent: Podcast Generator] Generating podcast script...")

        # Check if extraction succeeded
        if state.get("status") == "extraction_failed":
            print("✗ Skipping generation due to extraction failure")
            state["status"] = "generation_skipped"
            return state

        try:
            script = self.podcast_generator.generate_script(
                sections=state["extracted_sections"],
                target_word_count=state["target_word_count"]
            )

            word_count = len(script.split())
            print(f"✓ Generated script: {word_count} words")

            state["podcast_script"] = script
            state["status"] = "generation_complete"

        except Exception as e:
            print(f"✗ Generation failed: {e}")
            state["error"] = str(e)
            state["status"] = "generation_failed"

        return state

    def _verify_script_node(self, state: PodcastState) -> PodcastState:
        """
        Node: Verify podcast script.

        Args:
            state: Current workflow state

        Returns:
            Updated state with verification report
        """
        print("\n[Agent: Verifier] Verifying script accuracy...")

        # Check if generation succeeded
        if state.get("status") == "generation_failed":
            print("✗ Skipping verification due to generation failure")
            state["status"] = "verification_skipped"
            return state

        try:
            report = self.verifier.verify_script(
                script=state["podcast_script"],
                source_sections=state["extracted_sections"]
            )

            print(f"✓ Verification complete")
            print(f"  - Claims analyzed: {report['summary']['total_claims']}")
            print(f"  - Hallucinations: {report['summary']['hallucinated_claims']}")

            state["verification_report"] = report
            state["status"] = "verification_complete"

        except Exception as e:
            print(f"✗ Verification failed: {e}")
            state["error"] = str(e)
            state["status"] = "verification_failed"

        return state

    def run(
        self,
        pdf_path: str,
        sections_config: Dict[str, list],
        target_word_count: int = 2000
    ) -> PodcastState:
        """
        Execute the workflow.

        Args:
            pdf_path: Path to PDF file
            sections_config: Section configuration (name -> [start, end])
            target_word_count: Target word count for script

        Returns:
            Final workflow state with all outputs
        """
        # Initialize state
        initial_state: PodcastState = {
            "pdf_path": pdf_path,
            "sections_config": sections_config,
            "target_word_count": target_word_count,
            "extracted_sections": {},
            "podcast_script": "",
            "verification_report": {},
            "error": "",
            "status": "initialized"
        }

        print("\n" + "=" * 60)
        print("STARTING LANGGRAPH WORKFLOW")
        print("=" * 60)

        # Run the workflow
        final_state = self.graph.invoke(initial_state)

        print("\n" + "=" * 60)
        print("WORKFLOW COMPLETE")
        print(f"Final Status: {final_state['status']}")
        print("=" * 60)

        return final_state

    def visualize(self, output_path: str = "workflow_graph.png"):
        """
        Generate a visualization of the workflow graph.

        Args:
            output_path: Path to save the graph visualization
        """
        try:
            from IPython.display import Image, display
            display(Image(self.graph.get_graph().draw_mermaid_png()))
        except Exception as e:
            print(f"Visualization requires graphviz and IPython: {e}")
