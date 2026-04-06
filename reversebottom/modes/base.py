from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from ..client import LLMClient, build_client
from ..config import Mode


@dataclass
class AnalysisResult:
    mode: Mode
    input_text: str
    output: str

    def __str__(self) -> str:
        return self.output


class BaseMode(ABC):
    """Base class for all ReverseBottom operating modes."""

    mode: Mode

    def __init__(self, client: LLMClient | None = None) -> None:
        self._client = client or build_client()

    @property
    @abstractmethod
    def system_prompt(self) -> str:
        """The system prompt that defines this mode's behavior."""
        ...

    def run(self, text: str) -> AnalysisResult:
        """
        Run analysis on the input text.

        Args:
            text: The idea, argument, or decision to analyze.

        Returns:
            AnalysisResult containing the mode, input, and model output.
        """
        if not text or not text.strip():
            raise ValueError("Input text cannot be empty.")

        output = self._client.complete(
            system=self.system_prompt,
            user=text.strip(),
        )

        return AnalysisResult(
            mode=self.mode,
            input_text=text.strip(),
            output=output,
        )
