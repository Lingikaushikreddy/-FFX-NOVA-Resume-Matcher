"""
PDF text extraction module.

This module provides functionality to extract text content from PDF files
using PyPDF2.
"""

from pathlib import Path
from typing import Union
import logging

from resume_parser.utils.text_utils import clean_text

logger = logging.getLogger(__name__)


class PDFExtractor:
    """
    Extract text content from PDF files.

    Uses PyPDF2 for PDF parsing with fallback error handling
    for corrupted or protected PDFs.

    Example:
        extractor = PDFExtractor()
        text = extractor.extract("resume.pdf")
    """

    def __init__(self) -> None:
        """Initialize the PDF extractor."""
        self._check_dependencies()

    def _check_dependencies(self) -> None:
        """Verify that PyPDF2 is installed."""
        try:
            import PyPDF2  # noqa: F401
        except ImportError as e:
            raise ImportError(
                "PyPDF2 is required for PDF extraction. "
                "Install it with: pip install PyPDF2"
            ) from e

    def extract(self, file_path: Union[str, Path]) -> str:
        """
        Extract text from a PDF file.

        Args:
            file_path: Path to the PDF file.

        Returns:
            Extracted and cleaned text content.

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the file is not a valid PDF.
            RuntimeError: If text extraction fails.
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"PDF file not found: {file_path}")

        if file_path.suffix.lower() != ".pdf":
            raise ValueError(f"File is not a PDF: {file_path}")

        return self._extract_text(file_path)

    def _extract_text(self, file_path: Path) -> str:
        """
        Perform the actual text extraction from PDF.

        Args:
            file_path: Path to the PDF file.

        Returns:
            Extracted text content.

        Raises:
            RuntimeError: If extraction fails.
        """
        import PyPDF2

        text_parts: list[str] = []

        try:
            with open(file_path, "rb") as pdf_file:
                reader = PyPDF2.PdfReader(pdf_file)

                # Check for encryption
                if reader.is_encrypted:
                    try:
                        # Try empty password first
                        if not reader.decrypt(""):
                            raise RuntimeError(
                                "PDF is password-protected and cannot be read"
                            )
                    except Exception as e:
                        raise RuntimeError(
                            f"Cannot decrypt PDF: {e}"
                        ) from e

                # Extract text from each page
                for page_num, page in enumerate(reader.pages):
                    try:
                        page_text = page.extract_text()
                        if page_text:
                            text_parts.append(page_text)
                    except Exception as e:
                        logger.warning(
                            f"Failed to extract text from page {page_num + 1}: {e}"
                        )
                        continue

        except PyPDF2.errors.PdfReadError as e:
            raise RuntimeError(f"Invalid or corrupted PDF file: {e}") from e
        except Exception as e:
            raise RuntimeError(f"Failed to read PDF: {e}") from e

        if not text_parts:
            logger.warning(f"No text extracted from PDF: {file_path}")
            return ""

        # Join all pages and clean the text
        full_text = "\n\n".join(text_parts)
        return clean_text(full_text)

    def get_page_count(self, file_path: Union[str, Path]) -> int:
        """
        Get the number of pages in a PDF file.

        Args:
            file_path: Path to the PDF file.

        Returns:
            Number of pages in the PDF.

        Raises:
            FileNotFoundError: If the file does not exist.
            RuntimeError: If reading fails.
        """
        import PyPDF2

        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"PDF file not found: {file_path}")

        try:
            with open(file_path, "rb") as pdf_file:
                reader = PyPDF2.PdfReader(pdf_file)
                return len(reader.pages)
        except Exception as e:
            raise RuntimeError(f"Failed to read PDF: {e}") from e

    def extract_metadata(self, file_path: Union[str, Path]) -> dict:
        """
        Extract metadata from a PDF file.

        Args:
            file_path: Path to the PDF file.

        Returns:
            Dictionary containing PDF metadata.

        Raises:
            FileNotFoundError: If the file does not exist.
            RuntimeError: If reading fails.
        """
        import PyPDF2

        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"PDF file not found: {file_path}")

        try:
            with open(file_path, "rb") as pdf_file:
                reader = PyPDF2.PdfReader(pdf_file)
                metadata = reader.metadata

                if metadata is None:
                    return {}

                return {
                    "title": metadata.get("/Title"),
                    "author": metadata.get("/Author"),
                    "subject": metadata.get("/Subject"),
                    "creator": metadata.get("/Creator"),
                    "producer": metadata.get("/Producer"),
                    "creation_date": metadata.get("/CreationDate"),
                    "modification_date": metadata.get("/ModDate"),
                }
        except Exception as e:
            raise RuntimeError(f"Failed to read PDF metadata: {e}") from e
