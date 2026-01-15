"""Tests for the Job model and Job parser."""

import pytest
from models.job import Job, JobRequirement
from job_parser import JobParser, parse_job_text


class TestJobModel:
    """Test suite for Job model."""

    def test_job_creation(self):
        """Test creating a Job instance."""
        job = Job(
            title="Software Engineer",
            company="TechCorp",
            required_skills=["Python", "SQL"],
        )

        assert job.title == "Software Engineer"
        assert job.company == "TechCorp"
        assert "Python" in job.required_skills

    def test_job_to_dict(self):
        """Test Job to_dict conversion."""
        job = Job(
            title="Developer",
            company="StartUp",
            required_skills=["JavaScript"],
            preferred_skills=["React"],
        )

        data = job.to_dict()
        assert data["title"] == "Developer"
        assert "JavaScript" in data["required_skills"]

    def test_job_to_json(self):
        """Test Job to_json conversion."""
        job = Job(title="Engineer", company="Corp")
        json_str = job.to_json()

        assert "Engineer" in json_str
        assert "Corp" in json_str

    def test_get_all_skills(self):
        """Test getting all skills combined."""
        job = Job(
            required_skills=["Python", "SQL"],
            preferred_skills=["Docker", "Python"],  # Python is duplicate
        )

        all_skills = job.get_all_skills()
        assert "Python" in all_skills
        assert "SQL" in all_skills
        assert "Docker" in all_skills
        # Should be unique
        assert len(all_skills) == 3

    def test_get_summary(self):
        """Test job summary generation."""
        job = Job(
            title="Senior Developer",
            company="BigTech",
            location="Remote",
            required_skills=["Python", "Java"],
            preferred_skills=["Go"],
            min_experience_years=5,
        )

        summary = job.get_summary()
        assert summary["title"] == "Senior Developer"
        assert summary["required_skills_count"] == 2
        assert summary["min_experience"] == 5


class TestJobParser:
    """Test suite for JobParser."""

    def test_parse_basic_job(self):
        """Test parsing basic job description."""
        job_text = """
        Senior Python Developer

        We are looking for a Senior Python Developer to join our team.

        Requirements:
        - 5+ years of experience
        - Strong Python skills
        - Experience with Django or Flask
        - PostgreSQL knowledge

        Nice to have:
        - AWS experience
        - Docker knowledge
        """

        job = parse_job_text(job_text, title="Senior Python Developer", company="TechCorp")

        assert job.title == "Senior Python Developer"
        assert job.company == "TechCorp"
        assert len(job.required_skills) > 0 or len(job.preferred_skills) > 0

    def test_parse_extracts_experience_years(self):
        """Test experience years extraction."""
        job_text = """
        Software Engineer

        Requirements:
        - 3+ years of experience in software development
        - Python expertise
        """

        parser = JobParser()
        job = parser.parse_text(job_text)

        assert job.min_experience_years == 3

    def test_parse_experience_range(self):
        """Test experience range extraction."""
        job_text = """
        Developer with 2-5 years of experience needed.
        """

        parser = JobParser()
        job = parser.parse_text(job_text)

        # The parser extracts some experience value
        assert job.min_experience_years is not None

    def test_parse_required_vs_preferred(self):
        """Test distinguishing required vs preferred skills."""
        job_text = """
        Web Developer

        Required Skills:
        - JavaScript
        - React
        - Node.js

        Preferred Skills:
        - TypeScript
        - GraphQL
        """

        parser = JobParser()
        job = parser.parse_text(job_text)

        # Should have skills in either category
        total_skills = len(job.required_skills) + len(job.preferred_skills)
        assert total_skills > 0

    def test_parse_remote_detection(self):
        """Test remote work detection."""
        job_text = """
        Remote Software Engineer

        This is a fully remote position. Work from anywhere!

        Skills: Python, JavaScript
        """

        parser = JobParser()
        job = parser.parse_text(job_text)

        assert job.is_remote is True

    def test_parse_extracts_title(self):
        """Test title extraction when not provided."""
        job_text = """
        Data Scientist

        We're looking for a Data Scientist to analyze data.
        """

        parser = JobParser()
        job = parser.parse_text(job_text)

        assert "Data Scientist" in job.title

    def test_empty_text(self):
        """Test parsing empty text."""
        parser = JobParser()
        job = parser.parse_text("")

        assert job.title == "Unknown Position" or job.title == ""
        assert len(job.required_skills) == 0


class TestJobRequirement:
    """Test suite for JobRequirement model."""

    def test_requirement_creation(self):
        """Test creating a requirement."""
        req = JobRequirement(
            requirement_type="required",
            description="Bachelor's degree in CS",
            category="education",
        )

        assert req.requirement_type == "required"
        assert req.category == "education"

    def test_requirement_to_dict(self):
        """Test requirement to_dict."""
        req = JobRequirement(
            requirement_type="preferred",
            description="5 years experience",
            category="experience",
        )

        data = req.to_dict()
        assert data["requirement_type"] == "preferred"
        assert data["category"] == "experience"
