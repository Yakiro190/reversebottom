from ..config import Mode
from ..prompts import REVERSE_SYSTEM_PROMPT
from .base import BaseMode


class ReverseMode(BaseMode):
    """
    Reverse mode: identifies the core assumption, inverts it completely,
    and builds the coherent logic of the opposite world.
    """

    mode = Mode.REVERSE

    @property
    def system_prompt(self) -> str:
        return REVERSE_SYSTEM_PROMPT
