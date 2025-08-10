"""Story_Sage User Story Specialist Agent Module.

This module provides Story_Sage, a specialized agent for crafting high-quality
user stories following INVEST principles and integrating with Agile workflows.
"""

# Expose the root agent and create_agent function at the package level for easier imports
from .agent import create_agent, root_agent
from . import agent

__all__ = ["create_agent", "root_agent", "agent"]
