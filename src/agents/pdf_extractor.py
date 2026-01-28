"""
PDF Extraction Agent

Responsibility: Extract text from PDF documents based on configurable page ranges.
Preserves structure and provides clean, section-separated content.
"""

import fitz  # PyMuPDF
from typing import Dict, List, Tuple
from utils.logger import get_logger

logger = get_logger(__name__)


class PDFExtractor:
    """Extracts text from PDFs with section-based configuration."""

    def __init__(self, pdf_path: str):
        """
        Initialize the PDF extractor.

        Args:
            pdf_path: Path to the PDF file
        """
        self.pdf_path = pdf_path
        self.doc = None

    def __enter__(self):
        """Context manager entry - open PDF."""
        logger.info(f"Opening PDF: {self.pdf_path}")
        self.doc = fitz.open(self.pdf_path)
        logger.debug(f"PDF opened successfully. Pages: {len(self.doc)}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - close PDF."""
        if self.doc:
            self.doc.close()

    def extract_sections(self, sections: Dict[str, List[int]]) -> Dict[str, str]:
        """
        Extract text from specified page ranges.

        Args:
            sections: Dictionary mapping section names to [start_page, end_page]
                     Pages are 1-indexed (as they appear in PDF viewers)

        Returns:
            Dictionary mapping section names to extracted text
        """
        if not self.doc:
            raise RuntimeError("PDF not opened. Use context manager (with statement).")

        logger.info(f"Extracting {len(sections)} sections from PDF")
        extracted = {}

        for section_name, page_range in sections.items():
            start_page, end_page = page_range
            logger.debug(f"Extracting section '{section_name}' (pages {start_page}-{end_page})")

            # Convert to 0-indexed for PyMuPDF
            start_idx = start_page - 1
            end_idx = end_page - 1

            section_text = []

            for page_num in range(start_idx, end_idx + 1):
                if page_num < len(self.doc):
                    page = self.doc[page_num]
                    text = page.get_text("text")
                    section_text.append(text)
                    logger.debug(f"  Extracted page {page_num + 1}: {len(text)} characters")

            # Join pages with clear separation
            extracted[section_name] = "\n\n".join(section_text)
            word_count = len(extracted[section_name].split())
            logger.info(f"✓ Section '{section_name}': {word_count} words extracted")

        return extracted

    def get_document_info(self) -> Dict[str, any]:
        """Get metadata about the PDF document."""
        if not self.doc:
            raise RuntimeError("PDF not opened. Use context manager (with statement).")

        return {
            "page_count": len(self.doc),
            "metadata": self.doc.metadata
        }
