from ..config import Mode
from ..prompts import DESTROY_SYSTEM_PROMPT
from .base import BaseMode


class DestroyMode(BaseMode):
    """
    Destroy mode: aggressively critiques ideas by finding flaws,
    risks, contradictions, and false assumptions.
    """

    mode = Mode.DESTROY

    @property
    def system_prompt(self) -> str:
        return DESTROY_SYSTEM_PROMPT
