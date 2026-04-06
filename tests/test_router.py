"""
Tests for the routing layer using a stub LLM client.
These run without any API keys.
"""

from __future__ import annotations

import pytest

from reversebottom.config import Mode
from reversebottom.modes.base import AnalysisResult
from reversebottom.router import Router


class StubClient:
    """Deterministic LLM stub for testing."""

    def complete(self, system: str, user: str) -> str:
        return f"[stub] system_len={len(system)} user_len={len(user)}"


@pytest.fixture()
def router() -> Router:
    return Router(client=StubClient())


def test_destroy_mode_returns_result(router: Router) -> None:
    result = router.run("My startup idea is X", mode=Mode.DESTROY)
    assert isinstance(result, AnalysisResult)
    assert result.mode == Mode.DESTROY
    assert result.input_text == "My startup idea is X"
    assert "[stub]" in result.output


def test_reverse_mode_returns_result(router: Router) -> None:
    result = router.run("Remote work is always better", mode=Mode.REVERSE)
    assert result.mode == Mode.REVERSE
    assert "[stub]" in result.output


def test_shadow_mode_returns_result(router: Router) -> None:
    result = router.run("I should quit my job", mode=Mode.SHADOW)
    assert result.mode == Mode.SHADOW
    assert "[stub]" in result.output


def test_input_is_stripped(router: Router) -> None:
    result = router.run("  some idea  ", mode=Mode.DESTROY)
    assert result.input_text == "some idea"


def test_empty_input_raises(router: Router) -> None:
    with pytest.raises(ValueError):
        router.run("", mode=Mode.DESTROY)


def test_whitespace_only_input_raises(router: Router) -> None:
    with pytest.raises(ValueError):
        router.run("   \n\t  ", mode=Mode.DESTROY)


def test_all_modes_available(router: Router) -> None:
    assert set(router.available_modes) == {Mode.DESTROY, Mode.REVERSE, Mode.SHADOW}


def test_result_str_returns_output(router: Router) -> None:
    result = router.run("test input", mode=Mode.DESTROY)
    assert str(result) == result.output
