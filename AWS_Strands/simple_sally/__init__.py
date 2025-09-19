"""
Simple Sally Agent

A minimal example of a Strands agent with basic functionality.
"""

from .agent import create_agent, root_agent
from .prompts import SYSTEM_PROMPT

__all__ = [
    "create_agent",
    "SYSTEM_PROMPT",
    "root_agent",
]

__version__ = "1.0.0"