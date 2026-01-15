"""Tests for the main ResumeParser class."""

import pytest
from pathlib import Path

from resume_parser import ResumeParser, Resume
from resume_parser.parser import parse_resume_text


class TestResumeParser:
    """Test suite for ResumeParser class."""

    def test_parser_initialization(self):
        """Test parser initializes correctly."""
        parser = ResumeParser()
        assert parser is not None
        assert parser.include_soft_skills is True
        assert parser.custom_skills == []

    def test_parser_with_custom_skills(self):
        """Test parser with custom skills."""
        custom = ["CustomFramework", "SpecialTool"]
        parser = ResumeParser(custom_skills=custom)
        assert parser.custom_skills == custom

    def test_parser_without_soft_skills(self):
        """Test parser without soft skills extraction."""
        parser = ResumeParser(include_soft_skills=False)
        assert parser.include_soft_skills is False

    def test_supported_extensions(self):
        """Test supported file extensions."""
        parser = ResumeParser()
        extensions = parser.get_supported_extensions()
        assert ".pdf" in extensions
        assert ".docx" in extensions

    def test_parse_text_basic(self, sample_resume_text: str):
        """Test basic text parsing."""
        parser = ResumeParser()
        resume = parser.parse_text(sample_resume_text)

        assert isinstance(resume, Resume)
        assert resume.raw_text == sample_resume_text
        assert resume.file_type == "text"

    def test_parse_text_extracts_contact(self, sample_resume_text: str):
        """Test contact extraction from parsed text."""
        parser = ResumeParser()
        resume = parser.parse_text(sample_resume_text)

        assert resume.contact.email == "john.doe@email.com"
        assert resume.contact.phone is not None
        assert "555" in resume.contact.phone
        assert resume.contact.name == "John Doe"

    def test_parse_text_extracts_skills(self, sample_resume_text: str):
        """Test skill extraction from parsed text."""
        parser = ResumeParser()
        resume = parser.parse_text(sample_resume_text)

        assert len(resume.skills) > 0
        assert "Python" in resume.skills
        assert "React" in resume.skills
        assert "AWS" in resume.skills

    def test_parse_text_extracts_experience(self, sample_resume_text: str):
        """Test experience extraction from parsed text."""
        parser = ResumeParser()
        resume = parser.parse_text(sample_resume_text)

        assert len(resume.experience) >= 1

    def test_parse_text_extracts_education(self, sample_resume_text: str):
        """Test education extraction from parsed text."""
        parser = ResumeParser()
        resume = parser.parse_text(sample_resume_text)

        assert len(resume.education) >= 1

    def test_parse_text_identifies_sections(self, sample_resume_text: str):
        """Test section identification from parsed text."""
        parser = ResumeParser()
        resume = parser.parse_text(sample_resume_text)

        assert len(resume.sections) > 0
        section_names = list(resume.sections.keys())
        assert any(s in section_names for s in ["experience", "education", "skills"])

    def test_parse_file_not_found(self):
        """Test parsing non-existent file raises error."""
        parser = ResumeParser()

        with pytest.raises(FileNotFoundError):
            parser.parse("/nonexistent/path/resume.pdf")

    def test_parse_unsupported_extension(self, tmp_path: Path):
        """Test parsing unsupported file type raises error."""
        txt_file = tmp_path / "resume.txt"
        txt_file.touch()

        parser = ResumeParser()
        with pytest.raises(ValueError) as exc_info:
            parser.parse(txt_file)

        assert "Unsupported file type" in str(exc_info.value)

    def test_resume_to_json(self, sample_resume_text: str):
        """Test JSON output generation."""
        parser = ResumeParser()
        resume = parser.parse_text(sample_resume_text)

        json_output = resume.to_json()
        assert isinstance(json_output, str)
        assert "john.doe@email.com" in json_output
        assert "Python" in json_output

    def test_resume_to_dict(self, sample_resume_text: str):
        """Test dictionary output generation."""
        parser = ResumeParser()
        resume = parser.parse_text(sample_resume_text)

        data = resume.to_dict()
        assert isinstance(data, dict)
        assert "contact" in data
        assert "skills" in data
        assert "experience" in data
        assert "education" in data

    def test_resume_get_summary(self, sample_resume_text: str):
        """Test resume summary generation."""
        parser = ResumeParser()
        resume = parser.parse_text(sample_resume_text)

        summary = resume.get_summary()
        assert "name" in summary
        assert "email" in summary
        assert "skills_count" in summary
        assert summary["skills_count"] > 0

    def test_minimal_resume(self, sample_resume_minimal: str):
        """Test parsing minimal resume."""
        parser = ResumeParser()
        resume = parser.parse_text(sample_resume_minimal)

        assert resume.contact.email == "jane@company.com"
        assert resume.contact.name == "Jane Smith"
        assert "Python" in resume.skills

    def test_add_custom_skill(self, sample_resume_text: str):
        """Test adding custom skill."""
        parser = ResumeParser()
        parser.add_custom_skill("SpecialTech")

        assert "SpecialTech" in parser.custom_skills

    def test_convenience_function(self, sample_resume_text: str):
        """Test parse_resume_text convenience function."""
        resume = parse_resume_text(sample_resume_text)

        assert isinstance(resume, Resume)
        assert resume.contact.email == "john.doe@email.com"

    def test_empty_text(self):
        """Test parsing empty text."""
        parser = ResumeParser()
        resume = parser.parse_text("")

        assert resume.raw_text == ""
        assert len(resume.skills) == 0

    def test_parse_errors_tracked(self):
        """Test that parse errors are tracked."""
        parser = ResumeParser()
        resume = parser.parse_text("")

        # Empty text shouldn't cause errors, but verify the mechanism exists
        assert isinstance(resume.parse_errors, list)
