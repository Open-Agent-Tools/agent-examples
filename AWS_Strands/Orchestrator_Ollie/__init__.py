"""
Orchestrator Ollie Agent

A specialized agent for coordinating and orchestrating tasks across
multiple systems, agents, and workflows.
"""

from .agent import create_agent, root_agent
from .prompts import SYSTEM_PROMPT

__all__ = [
    "create_agent",
    "root_agent",
    "SYSTEM_PROMPT",
]

__version__ = "1.0.0"
