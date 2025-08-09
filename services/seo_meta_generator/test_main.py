"""Unit tests for the SEO Meta Description Generator service."""

from fastapi.testclient import TestClient
from services.seo_meta_generator.main import app, truncate_description, generate_meta_with_openai

client = TestClient(app)


def test_generate_meta_endpoint_valid_input():
    """Ensure the /generate endpoint returns a meta description."""
    payload = {"title": "Test Page", "description": "This is a short test description."}
    response = client.post("/generate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "meta_description" in data
    # The meta description should be non-empty and not exceed 160 characters
    assert 0 < len(data["meta_description"]) <= 160


def test_generate_meta_endpoint_missing_fields():
    """Ensure the endpoint validates missing fields appropriately."""
    response = client.post("/generate", json={"title": "Only title"})
    assert response.status_code == 422  # FastAPI validates missing description field


def test_truncate_description_short():
    """truncate_description should return the original description when under limit."""
    desc = "Short description"
    assert truncate_description(desc) == desc


def test_truncate_description_long():
    """truncate_description should truncate descriptions longer than 160 characters."""
    long_desc = "A" * 200
    truncated = truncate_description(long_desc)
    assert len(truncated) == 160
    assert truncated.endswith("...")
