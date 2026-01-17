"""Tests for scoring components."""

import pytest
from job_matcher.scoring.semantic_scorer import SemanticScorer
from job_matcher.scoring.skill_scorer import SkillScorer, SkillMatchResult
from job_matcher.scoring.experience_scorer import ExperienceScorer


class TestSemanticScorer:
    """Test suite for semantic scorer."""

    def test_scorer_initialization(self):
        """Test scorer initialization."""
        scorer = SemanticScorer()
        assert scorer is not None

    def test_empty_text_returns_zero(self):
        """Test empty text returns zero score."""
        scorer = SemanticScorer()
        score = scorer.score("", "Some job description")
        assert score == 0.0

        score = scorer.score("Some resume", "")
        assert score == 0.0

    def test_score_range(self):
        """Test score is in valid range."""
        scorer = SemanticScorer()

        # Mock the embedding service to avoid loading model
        from unittest.mock import patch, MagicMock

        mock_service = MagicMock()
        mock_service.encode.return_value = [0.1] * 384
        mock_service.cosine_similarity.return_value = 0.75

        with patch.object(scorer, '_embedding_service', mock_service):
            score = scorer.score("Python developer", "Python job")

        assert 0.0 <= score <= 1.0


class TestSkillScorer:
    """Test suite for skill scorer."""

    def test_scorer_initialization(self):
        """Test scorer initialization."""
        scorer = SkillScorer()
        assert scorer.required_weight == 2.0
        assert scorer.preferred_weight == 1.0

    def test_perfect_match(self):
        """Test perfect skill match."""
        scorer = SkillScorer()
        result = scorer.score(
            resume_skills=["Python", "Django", "PostgreSQL"],
            required_skills=["Python", "Django"],
            preferred_skills=["PostgreSQL"],
        )

        assert result.score == 1.0
        assert len(result.matched_skills) == 3

    def test_no_match(self):
        """Test no skill match."""
        scorer = SkillScorer()
        result = scorer.score(
            resume_skills=["Java", "Spring"],
            required_skills=["Python", "Django"],
            preferred_skills=["PostgreSQL"],
        )

        assert result.score == 0.0
        assert len(result.matched_skills) == 0

    def test_partial_match(self):
        """Test partial skill match."""
        scorer = SkillScorer()
        result = scorer.score(
            resume_skills=["Python", "Flask"],
            required_skills=["Python", "Django"],
            preferred_skills=["PostgreSQL"],
        )

        # Python matched (2 pts), Django missing (0 pts), PostgreSQL missing (0 pts)
        # Total possible: 2*2 + 1 = 5
        # Matched: 2
        # Score: 2/5 = 0.4
        assert abs(result.score - 0.4) < 0.01
        assert "Python" in result.matched_skills
        assert "Django" in result.missing_required

    def test_synonym_matching(self):
        """Test synonym skill matching."""
        scorer = SkillScorer()
        result = scorer.score(
            resume_skills=["JS", "ReactJS"],
            required_skills=["JavaScript", "React"],
            preferred_skills=[],
        )

        assert result.score == 1.0
        assert len(result.matched_skills) == 2

    def test_case_insensitive(self):
        """Test case insensitive matching."""
        scorer = SkillScorer()
        result = scorer.score(
            resume_skills=["PYTHON", "django"],
            required_skills=["python", "Django"],
            preferred_skills=[],
        )

        assert result.score == 1.0

    def test_empty_job_skills(self):
        """Test when job has no skills listed."""
        scorer = SkillScorer()
        result = scorer.score(
            resume_skills=["Python"],
            required_skills=[],
            preferred_skills=[],
        )

        assert result.score == 0.5  # Neutral score

    def test_skill_gaps(self):
        """Test skill gap analysis."""
        scorer = SkillScorer()
        result = scorer.score(
            resume_skills=["Python"],
            required_skills=["Python", "Kubernetes"],
            preferred_skills=["Docker"],
        )

        assert len(result.gaps) == 2
        gap_skills = [g.skill for g in result.gaps]
        assert "Kubernetes" in gap_skills
        assert "Docker" in gap_skills

    def test_overlap_percentage(self):
        """Test skill overlap percentage."""
        scorer = SkillScorer()
        percentage = scorer.get_skill_overlap_percentage(
            resume_skills=["Python", "Django"],
            job_skills=["Python", "Django", "PostgreSQL", "Docker"],
        )

        assert percentage == 50.0  # 2/4 = 50%


class TestExperienceScorer:
    """Test suite for experience scorer."""

    def test_scorer_initialization(self):
        """Test scorer initialization."""
        scorer = ExperienceScorer()
        assert scorer is not None

    def test_meets_requirement(self):
        """Test score when experience meets requirement."""
        scorer = ExperienceScorer()
        score = scorer.score(resume_years=5, job_min_years=3)
        assert score == 1.0

    def test_exceeds_requirement(self):
        """Test score when experience exceeds requirement."""
        scorer = ExperienceScorer()
        score = scorer.score(resume_years=10, job_min_years=5)
        assert score == 1.0  # Capped at 1.0

    def test_below_requirement(self):
        """Test score when experience below requirement."""
        scorer = ExperienceScorer()
        score = scorer.score(resume_years=2, job_min_years=5)
        assert score == 0.4  # 2/5

    def test_no_requirement(self):
        """Test score when no experience required."""
        scorer = ExperienceScorer()
        score = scorer.score(resume_years=0, job_min_years=0)
        assert score == 1.0

    def test_no_resume_experience(self):
        """Test when resume has no experience info."""
        scorer = ExperienceScorer()
        score = scorer.score(resume_years=None, job_min_years=5)
        assert score == 0.5  # Partial score

    def test_estimate_from_text(self):
        """Test extracting years from text."""
        scorer = ExperienceScorer()

        tests = [
            ("5 years of experience in Python", 5),
            ("Over 10 years of software development", 10),
            ("3+ years experience required", 3),
        ]

        for text, expected in tests:
            years = scorer.estimate_years_from_text(text)
            assert years == expected, f"Failed for: {text}"

    def test_estimate_from_positions(self):
        """Test estimating years from position count."""
        scorer = ExperienceScorer()

        # 3 positions × 2.5 years average = 7.5 years
        years = scorer.estimate_from_positions(3)
        assert years == 7.5

    def test_estimate_from_entries(self):
        """Test estimating from work entries."""
        scorer = ExperienceScorer()

        entries = [
            {"start_date": "2020-01", "end_date": "2022-01", "is_current": False},
            {"start_date": "2022-01", "end_date": None, "is_current": True},
        ]

        years = scorer.estimate_years_from_entries(entries)
        assert years >= 2.0  # At least 2 years from first entry


class TestSkillMatchResult:
    """Test SkillMatchResult dataclass."""

    def test_default_values(self):
        """Test default values."""
        result = SkillMatchResult()
        assert result.score == 0.0
        assert result.matched_skills == []
        assert result.missing_required == []

    def test_with_values(self):
        """Test with values."""
        result = SkillMatchResult(
            score=0.75,
            matched_skills=["Python", "Django"],
            missing_required=["PostgreSQL"],
            missing_preferred=["Docker"],
        )

        assert result.score == 0.75
        assert len(result.matched_skills) == 2
        assert len(result.missing_required) == 1


class TestEdgeCases:
    """Test edge cases for scorers."""

    def test_empty_skills_lists(self):
        """Test with empty skill lists."""
        scorer = SkillScorer()
        result = scorer.score([], [], [])
        assert result.score == 0.5  # Neutral

    def test_duplicate_skills(self):
        """Test handling of duplicate skills."""
        scorer = SkillScorer()
        result = scorer.score(
            resume_skills=["Python", "Python", "python"],
            required_skills=["Python"],
            preferred_skills=[],
        )

        assert result.score == 1.0
        assert len(result.matched_skills) == 1

    def test_none_values(self):
        """Test handling of None values."""
        scorer = ExperienceScorer()
        score = scorer.score(resume_years=None, job_min_years=5)
        assert 0 <= score <= 1

    def test_negative_experience(self):
        """Test handling of edge case values."""
        scorer = ExperienceScorer()
        score = scorer.score(resume_years=-1, job_min_years=5)
        assert score == 0.0

    def test_very_long_skill_list(self):
        """Test with many skills."""
        scorer = SkillScorer()

        resume_skills = [f"Skill{i}" for i in range(100)]
        required_skills = [f"Skill{i}" for i in range(50)]
        preferred_skills = [f"Skill{i}" for i in range(50, 75)]

        result = scorer.score(resume_skills, required_skills, preferred_skills)
        assert result.score == 1.0
