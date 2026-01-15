"""Tests for API endpoints."""

import pytest

# Handle httpx/starlette version compatibility
try:
    from fastapi.testclient import TestClient
    from api.app import app
    _test_client = TestClient(app)
    TESTCLIENT_AVAILABLE = True
except (TypeError, ImportError) as e:
    TESTCLIENT_AVAILABLE = False
    _test_client = None


class TestHealthEndpoints:
    """Test health check endpoints."""

    @pytest.mark.skipif(not TESTCLIENT_AVAILABLE, reason="TestClient incompatible with current httpx version")
    def test_root_endpoint(self):
        """Test root endpoint returns API info."""
        from api.app import app
        from fastapi.testclient import TestClient

        client = TestClient(app)
        response = client.get("/")

        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "FFX NOVA" in data["message"]
        assert "version" in data

    @pytest.mark.skipif(not TESTCLIENT_AVAILABLE, reason="TestClient incompatible with current httpx version")
    def test_health_endpoint(self):
        """Test health check endpoint."""
        from api.app import app
        from fastapi.testclient import TestClient

        client = TestClient(app)
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data


class TestAPISchemas:
    """Test API schema validation."""

    def test_resume_upload_schema(self):
        """Test ResumeUploadRequest schema."""
        from api.schemas import ResumeUploadRequest

        request = ResumeUploadRequest(
            resume_json={
                "raw_text": "Test resume",
                "contact": {"name": "John", "email": "john@test.com"},
                "skills": ["Python"],
            }
        )

        assert request.resume_json["raw_text"] == "Test resume"

    def test_job_create_schema(self):
        """Test JobCreateRequest schema."""
        from api.schemas import JobCreateRequest

        request = JobCreateRequest(
            title="Software Engineer",
            company="TechCorp",
            raw_text="Looking for a software engineer...",
        )

        assert request.title == "Software Engineer"
        assert request.company == "TechCorp"

    def test_job_create_schema_validation(self):
        """Test JobCreateRequest validation."""
        from api.schemas import JobCreateRequest
        from pydantic import ValidationError

        # Title is required
        with pytest.raises(ValidationError):
            JobCreateRequest(company="Corp", raw_text="Description")

        # Company is required
        with pytest.raises(ValidationError):
            JobCreateRequest(title="Engineer", raw_text="Description")

        # raw_text must be at least 10 chars
        with pytest.raises(ValidationError):
            JobCreateRequest(title="Engineer", company="Corp", raw_text="Short")

    def test_match_request_schema(self):
        """Test MatchRequest schema."""
        from api.schemas import MatchRequest

        request = MatchRequest(resume_id="res123", job_id="job456")

        assert request.resume_id == "res123"
        assert request.job_id == "job456"

    def test_match_response_schema(self):
        """Test MatchResponse schema."""
        from api.schemas import MatchResponse, ExplainabilitySchema

        response = MatchResponse(
            resume_id="res123",
            job_id="job456",
            final_score=0.75,
            semantic_score=0.80,
            skill_score=0.72,
            match_tier="Strong",
            explainability=ExplainabilitySchema(
                matched_skills=["Python", "SQL"],
                missing_required_skills=["Java"],
            ),
        )

        assert response.final_score == 0.75
        assert response.match_tier == "Strong"
        assert "Python" in response.explainability.matched_skills

    def test_explainability_schema(self):
        """Test ExplainabilitySchema."""
        from api.schemas import ExplainabilitySchema

        exp = ExplainabilitySchema(
            matched_skills=["Python", "Django"],
            missing_required_skills=["Java"],
            missing_preferred_skills=["Docker"],
            skill_match_percentage=66.7,
            semantic_similarity=0.82,
        )

        assert len(exp.matched_skills) == 2
        assert exp.skill_match_percentage == 66.7


class TestAPIResponseFormats:
    """Test API response format consistency."""

    def test_resume_upload_response_format(self):
        """Test ResumeUploadResponse format."""
        from api.schemas import ResumeUploadResponse

        response = ResumeUploadResponse(
            resume_id="abc123",
            message="Success",
            candidate_name="John Doe",
            candidate_email="john@test.com",
            skills_count=5,
        )

        assert response.resume_id == "abc123"
        assert response.skills_count == 5

    def test_job_create_response_format(self):
        """Test JobCreateResponse format."""
        from api.schemas import JobCreateResponse

        response = JobCreateResponse(
            job_id="job123",
            message="Created",
            title="Engineer",
            company="Corp",
            required_skills_count=3,
            preferred_skills_count=2,
        )

        assert response.job_id == "job123"
        assert response.required_skills_count == 3

    def test_top_matches_response_format(self):
        """Test TopMatchesResponse format."""
        from api.schemas import TopMatchesResponse, MatchResponse, ExplainabilitySchema

        match = MatchResponse(
            resume_id="res1",
            job_id="job1",
            final_score=0.85,
            semantic_score=0.80,
            skill_score=0.88,
            match_tier="Excellent",
            explainability=ExplainabilitySchema(),
        )

        response = TopMatchesResponse(
            job_id="job1",
            total_matches=1,
            matches=[match],
        )

        assert response.total_matches == 1
        assert response.matches[0].final_score == 0.85


class TestConfigSettings:
    """Test configuration settings."""

    def test_settings_load(self):
        """Test settings load correctly."""
        from config import get_settings

        settings = get_settings()

        assert settings.api_port == 8000
        assert settings.semantic_weight == 0.4
        assert settings.skill_weight == 0.6

    def test_weights_valid(self):
        """Test matching weights are valid."""
        from config import get_settings

        settings = get_settings()

        assert settings.validate_weights() is True

    def test_embedding_dimension(self):
        """Test embedding dimension is set."""
        from config import get_settings

        settings = get_settings()

        assert settings.embedding_dimension == 384
