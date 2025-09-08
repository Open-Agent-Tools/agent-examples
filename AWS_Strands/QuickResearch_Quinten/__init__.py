"""
Quick Research Quinten Agent

A specialized quick research agent for rapid information gathering.
"""

from .agent import create_agent, root_agent
from .prompts import SYSTEM_PROMPT

__all__ = [
    "create_agent",
    "SYSTEM_PROMPT",
    "root_agent",
]

__version__ = "1.0.0"