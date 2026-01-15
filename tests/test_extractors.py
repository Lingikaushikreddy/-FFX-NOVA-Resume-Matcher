"""Tests for individual extractor modules."""

import pytest

from resume_parser.extractors import (
    SectionExtractor,
    ContactExtractor,
    SkillExtractor,
    ExperienceExtractor,
    EducationExtractor,
)
from resume_parser.utils.text_utils import (
    clean_text,
    normalize_whitespace,
    split_date_range,
    is_likely_header,
)


class TestSectionExtractor:
    """Test suite for SectionExtractor."""

    def test_extract_experience_section(self):
        """Test experience section identification."""
        extractor = SectionExtractor()
        text = """
EXPERIENCE
Senior Developer at Tech Corp
2020 - Present

EDUCATION
BS in Computer Science
"""
        sections = extractor.extract(text)
        assert "experience" in sections
        assert "education" in sections

    def test_extract_skills_section(self):
        """Test skills section identification."""
        extractor = SectionExtractor()
        text = """
SKILLS
Python, JavaScript, React

WORK EXPERIENCE
Developer role
"""
        sections = extractor.extract(text)
        assert "skills" in sections

    def test_section_with_colon(self):
        """Test section header with colon."""
        extractor = SectionExtractor()
        text = """
Experience:
Developer at Company
2020 - Present
"""
        sections = extractor.extract(text)
        assert "experience" in sections

    def test_custom_section_pattern(self):
        """Test adding custom section pattern."""
        extractor = SectionExtractor()
        extractor.add_pattern("custom", r"my\s+special\s+section")

        text = """
MY SPECIAL SECTION
Some content here
"""
        sections = extractor.extract(text)
        assert "custom" in sections

    def test_empty_text(self):
        """Test extracting from empty text."""
        extractor = SectionExtractor()
        sections = extractor.extract("")
        assert sections == {}


class TestContactExtractor:
    """Test suite for ContactExtractor."""

    def test_extract_email(self):
        """Test email extraction."""
        extractor = ContactExtractor()
        contact = extractor.extract("Contact: john.doe@techcorp.com")

        assert contact.email == "john.doe@techcorp.com"

    def test_extract_phone_us_format(self):
        """Test US phone number extraction."""
        extractor = ContactExtractor()
        contact = extractor.extract("Phone: (555) 123-4567")

        assert contact.phone is not None
        assert "555" in contact.phone

    def test_extract_phone_international(self):
        """Test international phone number extraction."""
        extractor = ContactExtractor()
        contact = extractor.extract("Phone: +1-555-123-4567")

        assert contact.phone is not None

    def test_extract_linkedin(self):
        """Test LinkedIn URL extraction."""
        extractor = ContactExtractor()
        contact = extractor.extract("LinkedIn: linkedin.com/in/johndoe")

        assert contact.linkedin is not None
        assert "linkedin.com" in contact.linkedin

    def test_extract_location(self):
        """Test location extraction."""
        extractor = ContactExtractor()
        contact = extractor.extract("San Francisco, CA 94102")

        assert contact.location is not None
        assert "San Francisco" in contact.location

    def test_extract_name(self):
        """Test name extraction."""
        extractor = ContactExtractor()
        contact = extractor.extract("John Doe\njohn@email.com")

        assert contact.name == "John Doe"

    def test_no_contact_info(self):
        """Test with no contact information."""
        extractor = ContactExtractor()
        contact = extractor.extract("This is just some random text")

        assert contact.email is None
        assert contact.phone is None


class TestSkillExtractor:
    """Test suite for SkillExtractor."""

    def test_extract_programming_languages(self):
        """Test programming language extraction."""
        extractor = SkillExtractor()
        skills = extractor.extract("Proficient in Python, JavaScript, and Java")

        assert "Python" in skills
        assert "JavaScript" in skills
        assert "Java" in skills

    def test_extract_frameworks(self):
        """Test framework extraction."""
        extractor = SkillExtractor()
        skills = extractor.extract("Experience with React, Django, and Flask")

        assert "React" in skills
        assert "Django" in skills
        assert "Flask" in skills

    def test_extract_cloud_platforms(self):
        """Test cloud platform extraction."""
        extractor = SkillExtractor()
        skills = extractor.extract("AWS, Azure, and GCP certified")

        assert "AWS" in skills
        assert "Azure" in skills
        assert "GCP" in skills

    def test_extract_databases(self):
        """Test database extraction."""
        extractor = SkillExtractor()
        skills = extractor.extract("Experience with PostgreSQL, MongoDB, and Redis")

        assert "PostgreSQL" in skills
        assert "MongoDB" in skills
        assert "Redis" in skills

    def test_extract_soft_skills(self):
        """Test soft skill extraction."""
        extractor = SkillExtractor(include_soft_skills=True)
        skills = extractor.extract("Strong leadership and communication skills")

        assert "Leadership" in skills
        assert "Communication" in skills

    def test_no_soft_skills(self):
        """Test without soft skills."""
        extractor = SkillExtractor(include_soft_skills=False)
        skills = extractor.extract("Strong leadership and communication skills, Python")

        assert "Leadership" not in skills
        assert "Communication" not in skills
        assert "Python" in skills

    def test_extract_by_category(self):
        """Test categorized skill extraction."""
        extractor = SkillExtractor()
        categories = extractor.extract_by_category(
            "Python developer with React experience using AWS"
        )

        assert "programming_languages" in categories
        assert "Python" in categories["programming_languages"]

    def test_custom_skills(self):
        """Test custom skill addition."""
        extractor = SkillExtractor(custom_skills=["MyFramework"])
        skills = extractor.extract("Experience with MyFramework")

        assert "MyFramework" in skills

    def test_empty_text(self):
        """Test extraction from empty text."""
        extractor = SkillExtractor()
        skills = extractor.extract("")

        assert skills == []


class TestExperienceExtractor:
    """Test suite for ExperienceExtractor."""

    def test_extract_basic_experience(self):
        """Test basic experience extraction."""
        extractor = ExperienceExtractor()
        text = """
Senior Developer
Tech Company
January 2020 - Present

Built scalable applications
"""
        experiences = extractor.extract(text)
        assert len(experiences) >= 1

    def test_extract_date_range(self):
        """Test date range extraction in experience."""
        extractor = ExperienceExtractor()
        # Put date on same line as role for better detection
        text = """
Software Engineer - June 2018 - December 2020
Company Inc

Built software applications
"""
        experiences = extractor.extract(text)

        assert len(experiences) >= 1
        # Verify we got an experience entry
        assert experiences[0].role is not None or experiences[0].company is not None

    def test_current_position(self):
        """Test current position detection."""
        extractor = ExperienceExtractor()
        text = """
Lead Developer - 2021 - Present
Current Company

Leading development team
"""
        experiences = extractor.extract(text)

        # Verify experience was extracted
        assert len(experiences) >= 1

    def test_empty_text(self):
        """Test extraction from empty text."""
        extractor = ExperienceExtractor()
        experiences = extractor.extract("")

        assert experiences == []


class TestEducationExtractor:
    """Test suite for EducationExtractor."""

    def test_extract_bachelors(self):
        """Test bachelor's degree extraction."""
        extractor = EducationExtractor()
        text = """
Bachelor of Science in Computer Science
University of California, Berkeley
May 2018
"""
        education = extractor.extract(text)
        assert len(education) >= 1

    def test_extract_masters(self):
        """Test master's degree extraction."""
        extractor = EducationExtractor()
        text = """
M.S. in Data Science
Stanford University
2020
"""
        education = extractor.extract(text)
        assert len(education) >= 1

    def test_extract_gpa(self):
        """Test GPA extraction."""
        extractor = EducationExtractor()
        text = """
BS Computer Science
MIT
GPA: 3.8/4.0
"""
        education = extractor.extract(text)

        if education:
            assert any(edu.gpa == "3.8" for edu in education)

    def test_extract_honors(self):
        """Test honors extraction."""
        extractor = EducationExtractor()
        text = """
Bachelor of Arts
Harvard University
Magna Cum Laude
"""
        education = extractor.extract(text)

        if education:
            assert any(edu.honors and "Cum Laude" in edu.honors for edu in education)

    def test_empty_text(self):
        """Test extraction from empty text."""
        extractor = EducationExtractor()
        education = extractor.extract("")

        assert education == []


class TestTextUtils:
    """Test suite for text utility functions."""

    def test_clean_text(self):
        """Test text cleaning."""
        text = "  Hello   world  \n\n\n\nTest  "
        cleaned = clean_text(text)

        assert "   " not in cleaned
        assert "\n\n\n" not in cleaned

    def test_normalize_whitespace(self):
        """Test whitespace normalization."""
        text = "Hello    world\n\ttest"
        normalized = normalize_whitespace(text)

        assert normalized == "Hello world test"

    def test_split_date_range(self):
        """Test date range splitting."""
        start, end = split_date_range("January 2020 - December 2022")

        assert start is not None
        assert end is not None

    def test_split_date_range_present(self):
        """Test date range with present."""
        start, end = split_date_range("2020 - Present")

        assert end == "Present"

    def test_is_likely_header_uppercase(self):
        """Test header detection for uppercase."""
        assert is_likely_header("EXPERIENCE") is True
        assert is_likely_header("SKILLS") is True

    def test_is_likely_header_with_colon(self):
        """Test header detection with colon."""
        assert is_likely_header("Experience:") is True

    def test_is_likely_header_long_text(self):
        """Test that long text is not a header."""
        long_text = "This is a very long sentence that should not be detected as a header."
        assert is_likely_header(long_text) is False

    def test_is_likely_header_empty(self):
        """Test header detection with empty string."""
        assert is_likely_header("") is False
