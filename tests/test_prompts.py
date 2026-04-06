"""
Sanity checks on the prompt strings — they should be non-empty,
contain the required section headers, and not contain forbidden phrases.
"""

from __future__ import annotations

import pytest

from reversebottom.prompts import DESTROY_SYSTEM_PROMPT, REVERSE_SYSTEM_PROMPT, SHADOW_SYSTEM_PROMPT


FORBIDDEN_PHRASES = [
    "great question",
    "certainly",
    "absolutely",
    "happy to help",
    "of course",
    "I'd be happy",
    "let me help",
]


@pytest.mark.parametrize(
    "prompt",
    [DESTROY_SYSTEM_PROMPT, REVERSE_SYSTEM_PROMPT, SHADOW_SYSTEM_PROMPT],
    ids=["destroy", "reverse", "shadow"],
)
def test_prompt_not_empty(prompt: str) -> None:
    assert len(prompt.strip()) > 200


@pytest.mark.parametrize(
    "phrase",
    FORBIDDEN_PHRASES,
)
@pytest.mark.parametrize(
    "prompt",
    [DESTROY_SYSTEM_PROMPT, REVERSE_SYSTEM_PROMPT, SHADOW_SYSTEM_PROMPT],
    ids=["destroy", "reverse", "shadow"],
)
def test_prompt_no_sycophantic_phrases(prompt: str, phrase: str) -> None:
    assert phrase.lower() not in prompt.lower(), (
        f"Sycophantic phrase '{phrase}' found in prompt"
    )


def test_destroy_prompt_contains_required_sections() -> None:
    required = ["FATAL FLAWS", "WORST-CASE SCENARIO", "VERDICT", "WHAT YOU MISSED"]
    for section in required:
        assert section in DESTROY_SYSTEM_PROMPT, f"Missing section: {section}"


def test_reverse_prompt_contains_required_sections() -> None:
    required = ["CORE ASSUMPTION", "INVERSION", "MIRROR WORLD", "STRESS TEST", "REVEALS"]
    for section in required:
        assert section.upper() in REVERSE_SYSTEM_PROMPT.upper(), f"Missing section: {section}"


def test_shadow_prompt_contains_required_sections() -> None:
    required = ["COGNITIVE BIASES", "HIDDEN ASSUMPTIONS", "EMOTIONAL INVESTMENT"]
    for section in required:
        assert section.upper() in SHADOW_SYSTEM_PROMPT.upper(), f"Missing section: {section}"
