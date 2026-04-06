"""
Tests for the FastAPI endpoints using HTTPX TestClient.
Uses a stub LLM client injected via dependency override.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from reversebottom.api import api_app
from reversebottom.modes.base import AnalysisResult
from reversebottom.config import Mode


@pytest.fixture()
def stub_result() -> AnalysisResult:
    return AnalysisResult(
        mode=Mode.DESTROY,
        input_text="test idea",
        output="FATAL FLAWS\n───────────\nThis is a stub response.",
    )


@pytest.fixture()
def client(stub_result: AnalysisResult) -> TestClient:
    with patch("reversebottom.api.Router") as MockRouter:
        instance = MagicMock()
        instance.run.return_value = stub_result
        MockRouter.return_value = instance
        with TestClient(api_app) as c:
            yield c


def test_health_endpoint(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "provider" in data
    assert "model" in data


def test_modes_endpoint(client: TestClient) -> None:
    response = client.get("/modes")
    assert response.status_code == 200
    data = response.json()
    assert "modes" in data
    mode_names = {m["name"] for m in data["modes"]}
    assert mode_names == {"destroy", "reverse", "shadow"}


def test_analyze_destroy(client: TestClient) -> None:
    response = client.post(
        "/analyze",
        json={"text": "We should build a social network for pets.", "mode": "destroy"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["mode"] == "destroy"
    assert "output" in data
    assert len(data["output"]) > 0


def test_analyze_default_mode(client: TestClient) -> None:
    response = client.post(
        "/analyze",
        json={"text": "We should build a social network for pets."},
    )
    assert response.status_code == 200


def test_analyze_short_text_rejected(client: TestClient) -> None:
    response = client.post(
        "/analyze",
        json={"text": "hi", "mode": "destroy"},
    )
    assert response.status_code == 422  # pydantic validation


def test_analyze_invalid_mode_rejected(client: TestClient) -> None:
    response = client.post(
        "/analyze",
        json={"text": "A valid idea with enough text to pass validation.", "mode": "explode"},
    )
    assert response.status_code == 422


def test_analyze_missing_text_rejected(client: TestClient) -> None:
    response = client.post("/analyze", json={"mode": "destroy"})
    assert response.status_code == 422
