"""
Mode routing: maps Mode enum values to their handler instances.
To add a new mode, register it in REGISTRY.
"""

from __future__ import annotations

from .client import LLMClient
from .config import Mode
from .modes.base import AnalysisResult, BaseMode
from .modes.destroy import DestroyMode
from .modes.reverse import ReverseMode
from .modes.shadow import ShadowMode


def _build_registry(client: LLMClient | None = None) -> dict[Mode, BaseMode]:
    return {
        Mode.DESTROY: DestroyMode(client),
        Mode.REVERSE: ReverseMode(client),
        Mode.SHADOW: ShadowMode(client),
    }


class Router:
    """
    Routes analysis requests to the appropriate mode handler.

    Example:
        router = Router()
        result = router.run("My startup idea is...", mode=Mode.DESTROY)
        print(result.output)
    """

    def __init__(self, client: LLMClient | None = None) -> None:
        self._registry = _build_registry(client)

    def run(self, text: str, mode: Mode) -> AnalysisResult:
        """
        Run the specified mode against the input text.

        Args:
            text: The idea, argument, or decision to analyze.
            mode: Which operating mode to use.

        Returns:
            AnalysisResult with the mode, input, and output.

        Raises:
            ValueError: If the mode is not registered.
        """
        handler = self._registry.get(mode)
        if handler is None:
            registered = ", ".join(m.value for m in self._registry)
            raise ValueError(
                f"Unknown mode '{mode}'. Registered modes: {registered}"
            )
        return handler.run(text)

    @property
    def available_modes(self) -> list[Mode]:
        return list(self._registry.keys())
