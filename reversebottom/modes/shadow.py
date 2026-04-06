from ..config import Mode
from ..prompts import SHADOW_SYSTEM_PROMPT
from .base import BaseMode


class ShadowMode(BaseMode):
    """
    Shadow mode: surfaces hidden motives, cognitive biases, and blind spots
    in the way an idea or question was framed.
    """

    mode = Mode.SHADOW

    @property
    def system_prompt(self) -> str:
        return SHADOW_SYSTEM_PROMPT
