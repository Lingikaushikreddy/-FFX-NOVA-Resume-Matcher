"""Pytest configuration and fixtures for resume parser tests."""

import pytest
from pathlib import Path
import tempfile


@pytest.fixture
def sample_resume_text() -> str:
    """Sample resume text for testing."""
    return """
John Doe
john.doe@email.com
(555) 123-4567
San Francisco, CA
linkedin.com/in/johndoe

SUMMARY
Experienced software engineer with 8+ years of experience in full-stack development.
Passionate about building scalable applications and mentoring junior developers.

EXPERIENCE

Senior Software Engineer
Tech Company Inc., San Francisco, CA
January 2020 - Present

• Led development of microservices architecture serving 10M+ users
• Implemented CI/CD pipelines using Jenkins and GitHub Actions
• Mentored team of 5 junior developers
• Technologies: Python, React, AWS, Docker, Kubernetes

Software Engineer
StartUp Corp
June 2016 - December 2019

• Built RESTful APIs using Django and Flask
• Developed React frontend applications
• Managed PostgreSQL and MongoDB databases
• Collaborated with cross-functional teams

EDUCATION

Master of Science in Computer Science
Stanford University
May 2016
GPA: 3.9/4.0

Bachelor of Science in Computer Science
UC Berkeley
May 2014
Magna Cum Laude

SKILLS

Programming Languages: Python, JavaScript, TypeScript, Java, Go
Frameworks: React, Django, Flask, Node.js, Express
Databases: PostgreSQL, MongoDB, Redis
Cloud: AWS, GCP, Docker, Kubernetes
Tools: Git, Jenkins, Jira, Agile/Scrum

CERTIFICATIONS

AWS Certified Solutions Architect
Certified Kubernetes Administrator (CKA)
"""


@pytest.fixture
def sample_resume_minimal() -> str:
    """Minimal resume text for edge case testing."""
    return """
Jane Smith
jane@company.com

Python developer with experience in data science.
Skills: Python, Pandas, NumPy, Machine Learning
"""


@pytest.fixture
def temp_pdf_file(tmp_path: Path) -> Path:
    """Create a temporary PDF file for testing."""
    # This creates an empty PDF-like file for testing file handling
    # Actual PDF content testing would require a real PDF
    pdf_path = tmp_path / "test_resume.pdf"
    pdf_path.touch()
    return pdf_path


@pytest.fixture
def temp_docx_file(tmp_path: Path) -> Path:
    """Create a temporary DOCX file for testing."""
    docx_path = tmp_path / "test_resume.docx"
    docx_path.touch()
    return docx_path
