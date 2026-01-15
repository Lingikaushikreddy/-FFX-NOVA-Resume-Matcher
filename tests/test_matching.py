"""Tests for the matching engine."""

import pytest
from models.job import Job
from models.match_result import MatchResult, ExplainabilityData
from resume_parser.models.resume import Resume, ContactInfo, WorkExperience, Education


class TestMatchResult:
    """Test suite for MatchResult model."""

    def test_match_result_creation(self):
        """Test creating a MatchResult."""
        result = MatchResult(
            final_score=0.75,
            semantic_score=0.80,
            skill_score=0.72,
        )

        assert result.final_score == 0.75
        assert result.semantic_score == 0.80
        assert result.skill_score == 0.72

    def test_match_result_to_dict(self):
        """Test MatchResult to_dict conversion."""
        result = MatchResult(
            resume_id="res123",
            job_id="job456",
            final_score=0.85,
        )

        data = result.to_dict()
        assert data["resume_id"] == "res123"
        assert data["job_id"] == "job456"
        assert data["final_score"] == 0.85

    def test_get_score_breakdown(self):
        """Test score breakdown calculation."""
        result = MatchResult(
            final_score=0.70,
            semantic_score=0.65,
            skill_score=0.73,
            semantic_weight=0.4,
            skill_weight=0.6,
        )

        breakdown = result.get_score_breakdown()
        assert "final_score" in breakdown
        assert "semantic_contribution" in breakdown
        assert "skill_contribution" in breakdown

    def test_is_strong_match(self):
        """Test strong match detection."""
        strong = MatchResult(final_score=0.85)
        weak = MatchResult(final_score=0.45)

        assert strong.is_strong_match(threshold=0.7) is True
        assert weak.is_strong_match(threshold=0.7) is False

    def test_get_match_tier(self):
        """Test match tier classification."""
        excellent = MatchResult(final_score=0.90)
        strong = MatchResult(final_score=0.75)
        good = MatchResult(final_score=0.60)
        fair = MatchResult(final_score=0.45)
        weak = MatchResult(final_score=0.30)

        assert excellent.get_match_tier() == "Excellent"
        assert strong.get_match_tier() == "Strong"
        assert good.get_match_tier() == "Good"
        assert fair.get_match_tier() == "Fair"
        assert weak.get_match_tier() == "Weak"


class TestExplainabilityData:
    """Test suite for ExplainabilityData."""

    def test_explainability_creation(self):
        """Test creating ExplainabilityData."""
        exp = ExplainabilityData(
            matched_skills=["Python", "SQL"],
            missing_required_skills=["Java"],
            skill_match_percentage=66.7,
            semantic_similarity=0.82,
        )

        assert "Python" in exp.matched_skills
        assert "Java" in exp.missing_required_skills
        assert exp.skill_match_percentage == 66.7

    def test_generate_explanation(self):
        """Test explanation text generation."""
        exp = ExplainabilityData(
            matched_skills=["Python", "Django", "SQL"],
            missing_required_skills=["Java"],
            semantic_similarity=0.85,
        )

        explanation = exp.generate_explanation()
        assert "Matched" in explanation
        assert "Python" in explanation or "3 skills" in explanation

    def test_to_dict(self):
        """Test ExplainabilityData to_dict."""
        exp = ExplainabilityData(
            matched_skills=["Python"],
            experience_match="Has 5 positions",
        )

        data = exp.to_dict()
        assert "matched_skills" in data
        assert "experience_match" in data


class TestHybridMatcherLogic:
    """Test suite for matching logic (without loading model)."""

    def test_skill_normalization(self):
        """Test that skill matching is case-insensitive."""
        resume_skills = ["Python", "javascript", "SQL"]
        job_required = ["python", "JavaScript", "sql"]

        # Normalize for comparison
        resume_normalized = {s.lower() for s in resume_skills}
        job_normalized = {s.lower() for s in job_required}

        matched = resume_normalized & job_normalized
        assert len(matched) == 3

    def test_skill_score_calculation(self):
        """Test skill score calculation logic."""
        # Perfect match
        resume_skills = {"python", "sql", "docker"}
        required = {"python", "sql"}
        preferred = {"docker"}

        matched_required = resume_skills & required
        matched_preferred = resume_skills & preferred

        # Required skills worth 2 points, preferred worth 1
        total_possible = len(required) * 2 + len(preferred)
        matched_points = len(matched_required) * 2 + len(matched_preferred)
        score = matched_points / total_possible

        assert score == 1.0  # Perfect match

    def test_skill_score_partial_match(self):
        """Test partial skill match scoring."""
        resume_skills = {"python", "sql"}
        required = {"python", "sql", "java"}  # Missing java
        preferred = {"docker"}  # Missing docker

        matched_required = resume_skills & required
        matched_preferred = resume_skills & preferred

        total_possible = len(required) * 2 + len(preferred)  # 6 + 1 = 7
        matched_points = len(matched_required) * 2 + len(matched_preferred)  # 4 + 0 = 4
        score = matched_points / total_possible

        assert score == 4 / 7  # About 0.57

    def test_weighted_final_score(self):
        """Test weighted final score calculation."""
        semantic_score = 0.80
        skill_score = 0.60
        semantic_weight = 0.4
        skill_weight = 0.6

        final_score = (semantic_weight * semantic_score) + (skill_weight * skill_score)

        expected = (0.4 * 0.80) + (0.6 * 0.60)  # 0.32 + 0.36 = 0.68
        assert abs(final_score - expected) < 0.001

    def test_weights_sum_to_one(self):
        """Test that default weights sum to 1.0."""
        from config import get_settings

        settings = get_settings()
        total = settings.semantic_weight + settings.skill_weight

        assert abs(total - 1.0) < 0.01


class TestMatchingScenarios:
    """Test various matching scenarios."""

    def test_perfect_skill_match_scenario(self):
        """Test scenario with perfect skill overlap."""
        resume_skills = {"Python", "Django", "PostgreSQL", "Docker", "AWS"}
        job_required = {"Python", "Django", "PostgreSQL"}
        job_preferred = {"Docker", "AWS"}

        matched_req = {s.lower() for s in resume_skills} & {s.lower() for s in job_required}
        matched_pref = {s.lower() for s in resume_skills} & {s.lower() for s in job_preferred}

        assert len(matched_req) == 3
        assert len(matched_pref) == 2

    def test_no_skill_match_scenario(self):
        """Test scenario with no skill overlap."""
        resume_skills = {"Java", "Spring", "Oracle"}
        job_required = {"Python", "Django", "PostgreSQL"}

        matched = {s.lower() for s in resume_skills} & {s.lower() for s in job_required}

        assert len(matched) == 0

    def test_partial_skill_match_scenario(self):
        """Test scenario with partial skill overlap."""
        resume_skills = {"Python", "Flask", "MySQL", "Git"}
        job_required = {"Python", "Django", "PostgreSQL"}

        matched = {s.lower() for s in resume_skills} & {s.lower() for s in job_required}

        assert len(matched) == 1  # Only Python matches
        assert "python" in matched


class TestResumeJobCompatibility:
    """Test Resume and Job model compatibility."""

    def test_resume_skills_format(self):
        """Test Resume skills are list of strings."""
        resume = Resume(skills=["Python", "JavaScript", "SQL"])

        assert isinstance(resume.skills, list)
        assert all(isinstance(s, str) for s in resume.skills)

    def test_job_skills_format(self):
        """Test Job skills are list of strings."""
        job = Job(
            required_skills=["Python", "Django"],
            preferred_skills=["Docker"],
        )

        assert isinstance(job.required_skills, list)
        assert isinstance(job.preferred_skills, list)

    def test_models_serializable(self):
        """Test both models serialize to JSON."""
        resume = Resume(
            raw_text="Software Engineer",
            skills=["Python"],
            contact=ContactInfo(name="John"),
        )

        job = Job(
            title="Developer",
            company="Corp",
            required_skills=["Python"],
        )

        # Both should serialize without error
        resume_json = resume.to_json()
        job_json = job.to_json()

        assert "Python" in resume_json
        assert "Python" in job_json
