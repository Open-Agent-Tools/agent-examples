"""
Scrum_Sam Agent Package.

This package contains the Scrum_Sam agent, a specialized Scrum Master agent
designed to coach teams and interact with Jira for Scrum-related tasks.

The agent is built using Google's Agent Development Kit (ADK) and uses the Gemini model.
It provides tools for Scrum coaching, Jira integration, and team facilitation.
"""

# Expose the root agent and create_agent function at the package level for easier imports
from .agent import root_agent, create_agent

__all__ = ["root_agent", "create_agent"]
