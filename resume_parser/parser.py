"""
Main Resume Parser module.

This module provides the primary ResumeParser class that orchestrates
all extraction components to parse resume files into structured data.
"""

from pathlib import Path
from typing import Union, Optional
import logging

from resume_parser.models.resume import Resume
from resume_parser.extractors.pdf_extractor import PDFExtractor
from resume_parser.extractors.docx_extractor import DOCXExtractor
from resume_parser.extractors.section_extractor import SectionExtractor
from resume_parser.extractors.contact_extractor import ContactExtractor
from resume_parser.extractors.skill_extractor import SkillExtractor
from resume_parser.extractors.experience_extractor import ExperienceExtractor
from resume_parser.extractors.education_extractor import EducationExtractor

logger = logging.getLogger(__name__)


class ResumeParser:
    """
    Main resume parser that orchestrates all extraction components.

    Parses PDF and DOCX resume files to extract structured information
    including contact details, skills, work experience, and education.

    Example:
        parser = ResumeParser()

        # Parse from file
        resume = parser.parse("path/to/resume.pdf")

        # Parse from text
        resume = parser.parse_text("... resume content ...")

        # Get JSON output
        print(resume.to_json())

    Attributes:
        include_soft_skills: Whether to extract soft skills.
        custom_skills: Additional skills to look for.
    """

    SUPPORTED_EXTENSIONS = {".pdf", ".docx"}

    def __init__(
        self,
        include_soft_skills: bool = True,
        custom_skills: Optional[list[str]] = None,
    ) -> None:
        """
        Initialize the resume parser.

        Args:
            include_soft_skills: Whether to extract soft skills.
            custom_skills: Additional custom skills to detect.
        """
        self.include_soft_skills = include_soft_skills
        self.custom_skills = custom_skills or []

        # Initialize extractors
        self._pdf_extractor = PDFExtractor()
        self._docx_extractor = DOCXExtractor()
        self._section_extractor = SectionExtractor()
        self._contact_extractor = ContactExtractor()
        self._skill_extractor = SkillExtractor(
            include_soft_skills=include_soft_skills,
            custom_skills=custom_skills,
        )
        self._experience_extractor = ExperienceExtractor()
        self._education_extractor = EducationExtractor()

    def parse(self, file_path: Union[str, Path]) -> Resume:
        """
        Parse a resume file and extract structured data.

        Args:
            file_path: Path to the resume file (PDF or DOCX).

        Returns:
            Resume object containing extracted data.

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the file type is not supported.
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"Resume file not found: {file_path}")

        extension = file_path.suffix.lower()
        if extension not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Unsupported file type: {extension}. "
                f"Supported types: {', '.join(self.SUPPORTED_EXTENSIONS)}"
            )

        # Create resume object
        resume = Resume(file_path=str(file_path), file_type=extension[1:])

        # Extract text from file
        try:
            if extension == ".pdf":
                resume.raw_text = self._pdf_extractor.extract(file_path)
            elif extension == ".docx":
                resume.raw_text = self._docx_extractor.extract(file_path)
        except Exception as e:
            error_msg = f"Failed to extract text from file: {e}"
            logger.error(error_msg)
            resume.parse_errors.append(error_msg)
            return resume

        if not resume.raw_text:
            resume.parse_errors.append("No text could be extracted from the file")
            return resume

        # Parse the extracted text
        return self._parse_content(resume)

    def parse_text(self, text: str, source: str = "text") -> Resume:
        """
        Parse resume content from a text string.

        Args:
            text: Resume text content.
            source: Optional source identifier.

        Returns:
            Resume object containing extracted data.
        """
        resume = Resume(raw_text=text, file_type=source)
        return self._parse_content(resume)

    def _parse_content(self, resume: Resume) -> Resume:
        """
        Parse all content from the resume text.

        Args:
            resume: Resume object with raw_text populated.

        Returns:
            Resume object with all fields populated.
        """
        text = resume.raw_text

        # Extract sections
        try:
            resume.sections = self._section_extractor.extract(text)
        except Exception as e:
            error_msg = f"Section extraction failed: {e}"
            logger.warning(error_msg)
            resume.parse_errors.append(error_msg)

        # Get section content if available
        contact_section = (
            resume.sections.get("contact", {}).content
            if "contact" in resume.sections
            else None
        )
        skills_section = (
            resume.sections.get("skills", {}).content
            if "skills" in resume.sections
            else None
        )
        experience_section = (
            resume.sections.get("experience", {}).content
            if "experience" in resume.sections
            else None
        )
        education_section = (
            resume.sections.get("education", {}).content
            if "education" in resume.sections
            else None
        )

        # Extract contact information
        try:
            resume.contact = self._contact_extractor.extract(
                text, contact_section
            )
        except Exception as e:
            error_msg = f"Contact extraction failed: {e}"
            logger.warning(error_msg)
            resume.parse_errors.append(error_msg)

        # Extract skills
        try:
            resume.skills = self._skill_extractor.extract(text, skills_section)
        except Exception as e:
            error_msg = f"Skill extraction failed: {e}"
            logger.warning(error_msg)
            resume.parse_errors.append(error_msg)

        # Extract work experience
        try:
            resume.experience = self._experience_extractor.extract(
                text, experience_section
            )
        except Exception as e:
            error_msg = f"Experience extraction failed: {e}"
            logger.warning(error_msg)
            resume.parse_errors.append(error_msg)

        # Extract education
        try:
            resume.education = self._education_extractor.extract(
                text, education_section
            )
        except Exception as e:
            error_msg = f"Education extraction failed: {e}"
            logger.warning(error_msg)
            resume.parse_errors.append(error_msg)

        return resume

    def get_supported_extensions(self) -> set[str]:
        """
        Get the set of supported file extensions.

        Returns:
            Set of supported extensions (e.g., {'.pdf', '.docx'}).
        """
        return self.SUPPORTED_EXTENSIONS.copy()

    def add_custom_skill(self, skill: str) -> None:
        """
        Add a custom skill to the extractor.

        Args:
            skill: Skill name to add.
        """
        self._skill_extractor.add_skill(skill)
        self.custom_skills.append(skill)

    def add_section_pattern(self, section_name: str, pattern: str) -> None:
        """
        Add a custom section pattern to the extractor.

        Args:
            section_name: Name of the section.
            pattern: Regex pattern to match the section header.
        """
        self._section_extractor.add_pattern(section_name, pattern)


def parse_resume(file_path: Union[str, Path]) -> Resume:
    """
    Convenience function to parse a resume file.

    Args:
        file_path: Path to the resume file.

    Returns:
        Parsed Resume object.
    """
    parser = ResumeParser()
    return parser.parse(file_path)


def parse_resume_text(text: str) -> Resume:
    """
    Convenience function to parse resume text.

    Args:
        text: Resume text content.

    Returns:
        Parsed Resume object.
    """
    parser = ResumeParser()
    return parser.parse_text(text)
