"""
Quick Research Quinten Agent

A specialized quick research agent for rapid information gathering.
"""

from .agent import QuickResearchQuinten, create_agent
from .prompts import SYSTEM_PROMPT

__all__ = [
    "QuickResearchQuinten",
    "create_agent",
    "SYSTEM_PROMPT",
]

__version__ = "1.0.0"