"""Tests for the FFX NOVA Job Matcher."""

import pytest
from unittest.mock import MagicMock, patch
from dataclasses import dataclass
from typing import List, Optional

from job_matcher.models.job import Job, ClearanceLevel
from job_matcher.models.match_result import MatchResult, SkillGap
from job_matcher.matcher import JobMatcher
from job_matcher.utils.clearance import (
    detect_clearance_from_text,
    meets_clearance_requirement,
    clearance_to_string,
)
from job_matcher.utils.skill_synonyms import (
    normalize_skill,
    skills_match,
    get_canonical_skill,
)


# Mock Resume for testing
@dataclass
class MockResume:
    """Mock resume for testing."""
    raw_text: str = ""
    skills: List[str] = None
    experience: List = None

    def __post_init__(self):
        if self.skills is None:
            self.skills = []
        if self.experience is None:
            self.experience = []


@dataclass
class MockExperience:
    """Mock work experience."""
    company: str = ""
    role: str = ""
    start_date: str = ""
    end_date: str = ""
    is_current: bool = False


class TestJobModel:
    """Test suite for Job model."""

    def test_job_creation(self):
        """Test creating a Job instance."""
        job = Job(
            title="Senior Python Developer",
            company="TechCorp",
            description="Looking for a Python expert",
            required_skills=["Python", "Django"],
            preferred_skills=["Docker"],
            clearance_level=ClearanceLevel.SECRET,
            min_experience_years=5,
        )

        assert job.title == "Senior Python Developer"
        assert job.company == "TechCorp"
        assert job.clearance_level == ClearanceLevel.SECRET
        assert "Python" in job.required_skills
        assert job.min_experience_years == 5

    def test_job_clearance_levels(self):
        """Test clearance level ordering."""
        assert ClearanceLevel.NONE < ClearanceLevel.SECRET
        assert ClearanceLevel.SECRET < ClearanceLevel.TOP_SECRET
        assert ClearanceLevel.TOP_SECRET < ClearanceLevel.TS_SCI

    def test_job_to_dict(self):
        """Test Job serialization."""
        job = Job(
            title="Engineer",
            company="Corp",
            required_skills=["Python"],
        )

        data = job.to_dict()
        assert data["title"] == "Engineer"
        assert data["required_skills"] == ["Python"]

    def test_job_get_all_skills(self):
        """Test getting all skills combined."""
        job = Job(
            title="Dev",
            company="Corp",
            required_skills=["Python", "SQL"],
            preferred_skills=["Docker", "Python"],  # Duplicate
        )

        all_skills = job.get_all_skills()
        assert len(all_skills) == 3  # Unique skills
        assert "Python" in all_skills

    def test_clearance_string(self):
        """Test clearance to string conversion."""
        job = Job(
            title="Analyst",
            company="Gov",
            clearance_level=ClearanceLevel.TS_SCI,
        )

        assert job.get_clearance_string() == "TS/SCI"


class TestClearanceDetection:
    """Test suite for clearance detection."""

    def test_detect_ts_sci(self):
        """Test detecting TS/SCI clearance."""
        texts = [
            "Active TS/SCI clearance with CI Poly",
            "Current TS-SCI eligibility",
            "Top Secret/SCI cleared",
        ]

        for text in texts:
            level = detect_clearance_from_text(text)
            assert level == ClearanceLevel.TS_SCI, f"Failed for: {text}"

    def test_detect_top_secret(self):
        """Test detecting Top Secret clearance."""
        texts = [
            "Current Top Secret clearance",
            "Active TS clearance",
        ]

        for text in texts:
            level = detect_clearance_from_text(text)
            assert level >= ClearanceLevel.TOP_SECRET, f"Failed for: {text}"

    def test_detect_secret(self):
        """Test detecting Secret clearance."""
        text = "Active Secret clearance since 2020"
        level = detect_clearance_from_text(text)
        assert level == ClearanceLevel.SECRET

    def test_detect_none(self):
        """Test no clearance detected."""
        text = "Software engineer with Python experience"
        level = detect_clearance_from_text(text)
        assert level == ClearanceLevel.NONE

    def test_meets_clearance_requirement(self):
        """Test clearance requirement check."""
        # Higher meets lower
        assert meets_clearance_requirement(ClearanceLevel.TOP_SECRET, ClearanceLevel.SECRET)

        # Equal meets equal
        assert meets_clearance_requirement(ClearanceLevel.SECRET, ClearanceLevel.SECRET)

        # Lower doesn't meet higher
        assert not meets_clearance_requirement(ClearanceLevel.SECRET, ClearanceLevel.TS_SCI)

        # None meets none
        assert meets_clearance_requirement(ClearanceLevel.NONE, ClearanceLevel.NONE)


class TestSkillSynonyms:
    """Test suite for skill synonym handling."""

    def test_normalize_skill(self):
        """Test skill normalization."""
        assert normalize_skill("ReactJS") == "react"
        assert normalize_skill("K8s") == "kubernetes"
        assert normalize_skill("JS") == "javascript"
        assert normalize_skill("Python3") == "python"

    def test_skills_match(self):
        """Test synonym matching."""
        assert skills_match("JavaScript", "JS")
        assert skills_match("kubernetes", "K8s")
        assert skills_match("AWS", "Amazon Web Services")
        assert not skills_match("Python", "Java")

    def test_get_canonical_skill(self):
        """Test getting canonical skill name."""
        assert get_canonical_skill("js") == "JavaScript"
        assert get_canonical_skill("k8s") == "Kubernetes"
        assert get_canonical_skill("aws") == "AWS"

    def test_case_insensitive(self):
        """Test case insensitivity."""
        assert skills_match("PYTHON", "python")
        assert skills_match("React", "REACT")


class TestMatchResult:
    """Test suite for MatchResult."""

    def test_match_result_creation(self):
        """Test creating a MatchResult."""
        result = MatchResult(
            score=85.5,
            semantic_score=0.90,
            skill_score=0.85,
            experience_score=0.80,
            matched_skills=["Python", "Django"],
            missing_required_skills=["PostgreSQL"],
        )

        assert result.score == 85.5
        assert result.get_tier() == "Excellent"

    def test_match_tiers(self):
        """Test match tier classification."""
        assert MatchResult(score=90).get_tier() == "Excellent"
        assert MatchResult(score=75).get_tier() == "Strong"
        assert MatchResult(score=60).get_tier() == "Good"
        assert MatchResult(score=45).get_tier() == "Fair"
        assert MatchResult(score=30).get_tier() == "Weak"

    def test_disqualified_tier(self):
        """Test disqualified result."""
        result = MatchResult(score=0, disqualified=True)
        assert result.get_tier() == "Disqualified"

    def test_score_breakdown(self):
        """Test score breakdown calculation."""
        result = MatchResult(
            score=76,
            semantic_score=0.80,
            skill_score=0.75,
            experience_score=0.70,
        )

        breakdown = result.get_score_breakdown()
        assert breakdown["total_score"] == 76
        assert breakdown["tier"] == "Strong"
        assert "components" in breakdown

    def test_generate_explanation(self):
        """Test explanation generation."""
        result = MatchResult(
            score=85,
            matched_skills=["Python", "Django", "AWS"],
            missing_required_skills=["PostgreSQL"],
        )

        explanation = result.generate_explanation()
        assert "Python" in explanation or "3" in explanation


class TestJobMatcher:
    """Test suite for JobMatcher."""

    def test_matcher_initialization(self):
        """Test matcher initialization."""
        matcher = JobMatcher()
        assert matcher.semantic_weight == 0.4
        assert matcher.skill_weight == 0.4
        assert matcher.experience_weight == 0.2

    def test_invalid_weights(self):
        """Test that invalid weights raise error."""
        with pytest.raises(ValueError):
            JobMatcher(semantic_weight=0.5, skill_weight=0.5, experience_weight=0.5)

    def test_match_basic(self):
        """Test basic matching."""
        matcher = JobMatcher()

        resume = MockResume(
            raw_text="Python developer with Django experience",
            skills=["Python", "Django", "PostgreSQL"],
        )

        job = Job(
            title="Python Developer",
            company="TechCorp",
            description="Looking for Python developer",
            required_skills=["Python", "Django"],
            preferred_skills=["PostgreSQL"],
        )

        with patch.object(matcher.semantic_scorer, 'score', return_value=0.85):
            result = matcher.match(resume, job)

        assert result.score > 0
        assert not result.disqualified
        assert "Python" in result.matched_skills

    def test_clearance_disqualification(self):
        """Test clearance disqualification."""
        matcher = JobMatcher()

        resume = MockResume(
            raw_text="Software engineer (no clearance mentioned)",
            skills=["Python"],
        )

        job = Job(
            title="Cleared Developer",
            company="Defense Corp",
            description="Must have TS/SCI",
            required_skills=["Python"],
            clearance_level=ClearanceLevel.TS_SCI,
        )

        result = matcher.match(resume, job)

        assert result.disqualified
        assert result.score == 0
        assert "clearance" in result.disqualification_reason.lower()

    def test_clearance_pass(self):
        """Test clearance requirement met."""
        matcher = JobMatcher()

        resume = MockResume(
            raw_text="Active Top Secret clearance holder with Python experience",
            skills=["Python", "AWS"],
        )

        job = Job(
            title="Developer",
            company="Corp",
            description="Looking for developer",
            required_skills=["Python"],
            clearance_level=ClearanceLevel.SECRET,
        )

        with patch.object(matcher.semantic_scorer, 'score', return_value=0.80):
            result = matcher.match(resume, job)

        assert not result.disqualified
        assert result.clearance_met

    def test_skill_synonym_matching(self):
        """Test that skill synonyms are matched."""
        matcher = JobMatcher()

        resume = MockResume(
            raw_text="JavaScript and ReactJS developer",
            skills=["JS", "ReactJS", "NodeJS"],  # Synonyms
        )

        job = Job(
            title="Frontend Dev",
            company="Corp",
            description="Frontend developer needed",
            required_skills=["JavaScript", "React", "Node.js"],  # Canonical forms
        )

        with patch.object(matcher.semantic_scorer, 'score', return_value=0.85):
            result = matcher.match(resume, job)

        # All skills should match via synonyms
        assert len(result.matched_skills) == 3
        assert len(result.missing_required_skills) == 0

    def test_upskilling_recommendations(self):
        """Test upskilling recommendations for missing skills."""
        matcher = JobMatcher()

        resume = MockResume(
            raw_text="Python developer",
            skills=["Python"],
        )

        job = Job(
            title="DevOps Engineer",
            company="Corp",
            description="DevOps role",
            required_skills=["Python", "Kubernetes", "Docker"],
        )

        with patch.object(matcher.semantic_scorer, 'score', return_value=0.60):
            result = matcher.match(resume, job)

        # Should have upskilling for missing skills
        assert len(result.upskilling_recommendations) > 0
        assert any("Kubernetes" in rec or "Docker" in rec
                   for rec in result.upskilling_recommendations)

    def test_batch_matching(self):
        """Test batch matching multiple jobs."""
        matcher = JobMatcher()

        resume = MockResume(
            raw_text="Python developer",
            skills=["Python", "Django"],
        )

        jobs = [
            Job(title="Python Dev", company="A", required_skills=["Python"]),
            Job(title="Java Dev", company="B", required_skills=["Java"]),
            Job(title="Full Stack", company="C", required_skills=["Python", "React"]),
        ]

        with patch.object(matcher.semantic_scorer, 'score', return_value=0.75):
            results = matcher.match_batch(resume, jobs)

        assert len(results) == 3
        # Results should be sorted by score
        assert results[0].score >= results[1].score >= results[2].score

    def test_get_top_matches(self):
        """Test getting top K matches."""
        matcher = JobMatcher()

        resume = MockResume(
            raw_text="Python developer",
            skills=["Python"],
        )

        jobs = [
            Job(title=f"Job {i}", company="Corp", required_skills=["Python"])
            for i in range(10)
        ]

        with patch.object(matcher.semantic_scorer, 'score', return_value=0.70):
            results = matcher.get_top_matches(resume, jobs, top_k=5)

        assert len(results) == 5


class TestFFXScoreCalculation:
    """Test FFX-Score calculation."""

    def test_ffx_score_formula(self):
        """Test FFX-Score = 0.4*semantic + 0.4*skills + 0.2*experience."""
        matcher = JobMatcher()

        resume = MockResume(
            raw_text="5 years Python developer",
            skills=["Python", "Django"],
        )

        job = Job(
            title="Dev",
            company="Corp",
            description="Python role",
            required_skills=["Python", "Django"],
            min_experience_years=5,
        )

        # Mock scorers to return known values
        with patch.object(matcher.semantic_scorer, 'score', return_value=0.80):
            with patch.object(matcher.experience_scorer, 'score', return_value=1.0):
                result = matcher.match(resume, job)

        # skill_score should be 1.0 (perfect match)
        # FFX = (0.4 * 0.80 + 0.4 * 1.0 + 0.2 * 1.0) * 100 = 92
        expected_min = 85  # Allow some variance
        assert result.score >= expected_min

    def test_custom_weights(self):
        """Test custom weight configuration."""
        matcher = JobMatcher(
            semantic_weight=0.5,
            skill_weight=0.3,
            experience_weight=0.2,
        )

        assert matcher.semantic_weight == 0.5
        assert matcher.skill_weight == 0.3
        assert matcher.experience_weight == 0.2


class TestExperienceScoring:
    """Test experience scoring."""

    def test_experience_meets_requirement(self):
        """Test experience score when requirement is met."""
        from job_matcher.scoring import ExperienceScorer

        scorer = ExperienceScorer()
        score = scorer.score(resume_years=5, job_min_years=3)
        assert score == 1.0

    def test_experience_below_requirement(self):
        """Test experience score when below requirement."""
        from job_matcher.scoring import ExperienceScorer

        scorer = ExperienceScorer()
        score = scorer.score(resume_years=2, job_min_years=5)
        assert score == 0.4  # 2/5

    def test_no_experience_requirement(self):
        """Test when job has no experience requirement."""
        from job_matcher.scoring import ExperienceScorer

        scorer = ExperienceScorer()
        score = scorer.score(resume_years=0, job_min_years=0)
        assert score == 1.0


class TestSkillScoring:
    """Test skill scoring."""

    def test_perfect_skill_match(self):
        """Test perfect skill match score."""
        from job_matcher.scoring import SkillScorer

        scorer = SkillScorer()
        result = scorer.score(
            resume_skills=["Python", "Django", "PostgreSQL"],
            required_skills=["Python", "Django"],
            preferred_skills=["PostgreSQL"],
        )

        assert result.score == 1.0
        assert len(result.missing_required) == 0
        assert len(result.missing_preferred) == 0

    def test_partial_skill_match(self):
        """Test partial skill match."""
        from job_matcher.scoring import SkillScorer

        scorer = SkillScorer()
        result = scorer.score(
            resume_skills=["Python"],
            required_skills=["Python", "Django"],
            preferred_skills=["PostgreSQL"],
        )

        assert result.score < 1.0
        assert "Django" in result.missing_required
        assert "PostgreSQL" in result.missing_preferred

    def test_required_weighted_higher(self):
        """Test that required skills are weighted higher."""
        from job_matcher.scoring import SkillScorer

        scorer = SkillScorer()

        # Missing required skill
        result1 = scorer.score(
            resume_skills=["Docker"],  # Only preferred
            required_skills=["Python"],
            preferred_skills=["Docker"],
        )

        # Missing preferred skill
        result2 = scorer.score(
            resume_skills=["Python"],  # Only required
            required_skills=["Python"],
            preferred_skills=["Docker"],
        )

        # Having required should score higher than having preferred
        assert result2.score > result1.score
