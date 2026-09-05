# config/__init__.py
"""
Config package for AI Resume Analysis & Router Engine.
Exports centralized prompts and menu configurations.
"""

from .prompts import (
    PROMPT_CASE_1,
    PROMPT_CASE_2,
    PROMPT_CASE_3,
    PROMPT_CASE_4,
    PROMPT_CASE_5,
    GATEKEEPER_SYSTEM_PROMPT,
)
from .menu import MENU_OPTIONS, display_menu
from .schemas import CandidateEvaluationSchema

__all__ = [
    "PROMPT_CASE_1",
    "PROMPT_CASE_2",
    "PROMPT_CASE_3",
    "PROMPT_CASE_4",
    "PROMPT_CASE_5",
    "GATEKEEPER_SYSTEM_PROMPT",
    "MENU_OPTIONS",
    "display_menu",
    "CandidateEvaluationSchema",
]