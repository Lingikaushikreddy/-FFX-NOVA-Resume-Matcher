#!/usr/bin/env python3
"""
FFX NOVA Job Matching Demo

Demonstrates the job matching system with sample data,
showing FFX-Score calculations, skill matching, and
upskilling recommendations.
"""

import sys
from dataclasses import dataclass
from typing import List, Optional

# Add project root to path
sys.path.insert(0, ".")

from job_matcher import JobMatcher, Job, ClearanceLevel


# =============================================================================
# Sample Data
# =============================================================================

@dataclass
class MockResume:
    """Mock resume for demo purposes."""
    raw_text: str
    skills: List[str]
    experience: List = None
    candidate_name: str = "John Doe"
    years_experience: int = 5

    def __post_init__(self):
        if self.experience is None:
            self.experience = []


@dataclass
class MockExperience:
    """Mock work experience."""
    company: str
    role: str
    start_date: str
    end_date: str
    is_current: bool = False


# Sample Resume
SAMPLE_RESUME = MockResume(
    candidate_name="John Doe",
    raw_text="""
    Senior Software Engineer with 5+ years of experience in Python, Django, and cloud technologies.
    Active Secret clearance. Strong background in building scalable web applications and APIs.

    Experience:
    - TechCorp (2020-Present): Senior Python Developer
    - StartupXYZ (2018-2020): Software Engineer
    - DataCo (2016-2018): Junior Developer

    Skills: Python, Django, Flask, PostgreSQL, AWS, Docker, React, JavaScript, Git, CI/CD

    Education: B.S. Computer Science, University of Virginia
    """,
    skills=[
        "Python", "Django", "Flask", "PostgreSQL", "AWS",
        "Docker", "React", "JavaScript", "Git", "CI/CD",
        "REST APIs", "SQL", "Linux"
    ],
    years_experience=5,
    experience=[
        MockExperience("TechCorp", "Senior Python Developer", "2020-01", "Present", True),
        MockExperience("StartupXYZ", "Software Engineer", "2018-01", "2020-01", False),
        MockExperience("DataCo", "Junior Developer", "2016-01", "2018-01", False),
    ]
)


# Sample Jobs
SAMPLE_JOBS = [
    Job(
        job_id="job-001",
        title="Senior Python Developer",
        company="Federal Contractor Inc",
        description="""
        We are seeking a Senior Python Developer to join our team building
        enterprise applications for government clients. The ideal candidate
        has experience with Django, cloud technologies, and working in
        cleared environments.

        Requirements:
        - 5+ years Python experience
        - Django or Flask framework expertise
        - AWS or cloud platform experience
        - Active Secret clearance

        Nice to have:
        - Kubernetes experience
        - React frontend skills
        - CI/CD pipeline experience
        """,
        clearance_level=ClearanceLevel.SECRET,
        required_skills=["Python", "Django", "AWS", "PostgreSQL"],
        preferred_skills=["Kubernetes", "React", "Docker", "CI/CD"],
        min_experience_years=5,
        location="Fairfax, VA",
        salary_min=120000,
        salary_max=160000,
        is_remote=False,
    ),
    Job(
        job_id="job-002",
        title="Full Stack Engineer",
        company="TechCorp Nova",
        description="""
        Join our innovative team building next-generation web applications.
        We're looking for a versatile engineer comfortable with both
        frontend and backend development.

        Requirements:
        - Strong JavaScript/TypeScript skills
        - React or Vue.js experience
        - Node.js backend experience

        Nice to have:
        - Python skills
        - GraphQL experience
        """,
        clearance_level=ClearanceLevel.NONE,
        required_skills=["JavaScript", "React", "Node.js"],
        preferred_skills=["TypeScript", "Python", "GraphQL"],
        min_experience_years=3,
        location="Remote",
        salary_min=100000,
        salary_max=140000,
        is_remote=True,
    ),
    Job(
        job_id="job-003",
        title="DevOps Engineer",
        company="Defense Systems LLC",
        description="""
        Looking for an experienced DevOps Engineer to manage our cloud
        infrastructure and deployment pipelines for classified systems.

        Requirements:
        - TS/SCI clearance required
        - AWS and Terraform experience
        - Kubernetes and Docker expertise
        - Strong Python scripting skills

        Nice to have:
        - Ansible experience
        - Jenkins or GitLab CI experience
        """,
        clearance_level=ClearanceLevel.TS_SCI,
        required_skills=["AWS", "Terraform", "Kubernetes", "Docker", "Python"],
        preferred_skills=["Ansible", "Jenkins", "GitLab CI", "Go"],
        min_experience_years=4,
        location="Arlington, VA",
        salary_min=140000,
        salary_max=180000,
        is_remote=False,
    ),
    Job(
        job_id="job-004",
        title="Data Engineer",
        company="Analytics Corp",
        description="""
        Seeking a Data Engineer to build and maintain data pipelines.

        Requirements:
        - Python and SQL expertise
        - Experience with Apache Spark
        - Cloud data warehouse experience

        Nice to have:
        - Machine Learning knowledge
        - Kafka experience
        """,
        clearance_level=ClearanceLevel.NONE,
        required_skills=["Python", "SQL", "Spark", "AWS"],
        preferred_skills=["Machine Learning", "Kafka", "Airflow"],
        min_experience_years=3,
        location="Reston, VA",
        salary_min=110000,
        salary_max=150000,
        is_remote=True,
    ),
]


# =============================================================================
# Display Functions
# =============================================================================

def print_header(text: str, width: int = 60):
    """Print a formatted header."""
    print()
    print("=" * width)
    print(f" {text}")
    print("=" * width)


def print_subheader(text: str, width: int = 50):
    """Print a formatted subheader."""
    print()
    print(f"{'─' * width}")
    print(f"  {text}")
    print(f"{'─' * width}")


def display_result(result, rank: int):
    """Display a match result with formatting."""
    tier_colors = {
        "Excellent": "🟢",
        "Strong": "🔵",
        "Good": "🟡",
        "Fair": "🟠",
        "Weak": "🔴",
        "Disqualified": "⛔",
    }

    tier = result.get_tier()
    tier_icon = tier_colors.get(tier, "⚪")

    print(f"\nMatch #{rank}: {result.job_title} @ {result.job_company}")
    print("─" * 50)
    print(f"FFX-Score: {result.score:.1f}/100 {tier_icon} ({tier} Match)")

    if result.disqualified:
        print(f"\n⚠️  DISQUALIFIED: {result.disqualification_reason}")
        return

    # Score Breakdown
    print("\nScore Breakdown:")
    breakdown = result.get_score_breakdown()
    components = breakdown["components"]
    print(f"  • Semantic Similarity: {components['semantic']['score']:.2f} "
          f"(×0.4 = {components['semantic']['contribution']:.1f})")
    print(f"  • Skill Match: {components['skills']['score']:.2f} "
          f"(×0.4 = {components['skills']['contribution']:.1f})")
    print(f"  • Experience: {components['experience']['score']:.2f} "
          f"(×0.2 = {components['experience']['contribution']:.1f})")

    # Clearance
    if result.clearance_met:
        print(f"\n✓ Clearance: Meets requirement")

    # Skills
    if result.matched_skills:
        print(f"\nMatched Skills ({len(result.matched_skills)}): "
              f"{', '.join(result.matched_skills[:6])}"
              f"{'...' if len(result.matched_skills) > 6 else ''}")

    if result.missing_required_skills:
        print(f"Missing Required ({len(result.missing_required_skills)}): "
              f"{', '.join(result.missing_required_skills)}")

    if result.missing_preferred_skills:
        print(f"Missing Preferred ({len(result.missing_preferred_skills)}): "
              f"{', '.join(result.missing_preferred_skills)}")

    # Upskilling
    if result.upskilling_recommendations:
        print("\nUpskilling Recommendations:")
        for rec in result.upskilling_recommendations[:3]:
            print(f"  → {rec}")

    # Explanation
    print(f"\nWhy This Matches:")
    print(f"  {result.explanation}")


def display_summary(results):
    """Display summary of all matches."""
    print_subheader("Summary")

    qualified = [r for r in results if not r.disqualified]
    disqualified = [r for r in results if r.disqualified]

    print(f"Total Jobs Analyzed: {len(results)}")
    print(f"Qualified Matches: {len(qualified)}")
    print(f"Disqualified (Clearance): {len(disqualified)}")

    if qualified:
        avg_score = sum(r.score for r in qualified) / len(qualified)
        print(f"Average Score (Qualified): {avg_score:.1f}")

        excellent = len([r for r in qualified if r.score >= 85])
        strong = len([r for r in qualified if 70 <= r.score < 85])
        good = len([r for r in qualified if 55 <= r.score < 70])

        print(f"\nTier Distribution:")
        print(f"  🟢 Excellent (85+): {excellent}")
        print(f"  🔵 Strong (70-84): {strong}")
        print(f"  🟡 Good (55-69): {good}")


# =============================================================================
# Main Demo
# =============================================================================

def main():
    """Run the job matching demo."""
    print_header("FFX NOVA Job Matching Demo")

    # Initialize matcher
    print("\nInitializing JobMatcher with FFX-Score algorithm...")
    print("  • Semantic Weight: 0.4")
    print("  • Skill Weight: 0.4")
    print("  • Experience Weight: 0.2")

    matcher = JobMatcher()

    # Display resume info
    print_subheader(f"Candidate: {SAMPLE_RESUME.candidate_name}")
    print(f"Experience: {SAMPLE_RESUME.years_experience}+ years")
    print(f"Skills: {', '.join(SAMPLE_RESUME.skills[:8])}...")
    print("Clearance: Secret (detected from resume)")

    # Run matching
    print_subheader(f"Matching Against {len(SAMPLE_JOBS)} Jobs")

    results = matcher.match_batch(SAMPLE_RESUME, SAMPLE_JOBS, sort_by_score=True)

    # Display results
    for rank, result in enumerate(results, 1):
        display_result(result, rank)

    # Summary
    display_summary(results)

    # Top recommendation
    print_header("Top Recommendation")
    best = results[0]
    if not best.disqualified:
        print(f"\n🎯 Best Match: {best.job_title} @ {best.job_company}")
        print(f"   FFX-Score: {best.score:.1f}/100")
        print(f"   Location: {SAMPLE_JOBS[0].location}")
        salary = SAMPLE_JOBS[0].get_salary_range_string()
        if salary:
            print(f"   Salary: {salary}")
    else:
        # Find first non-disqualified
        for result in results:
            if not result.disqualified:
                print(f"\n🎯 Best Match: {result.job_title} @ {result.job_company}")
                print(f"   FFX-Score: {result.score:.1f}/100")
                break

    print("\n" + "=" * 60)
    print(" Demo Complete!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
