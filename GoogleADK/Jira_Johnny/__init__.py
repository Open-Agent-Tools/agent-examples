"""
Jira_Johnny Agent Package.

This package contains the Jira_Johnny agent, a specialized Jira operations agent
designed to interact with Jira and perform Jira-related tasks efficiently.

The agent is built using Google's Agent Development Kit (ADK) and uses the Gemini model.
It provides tools for Jira issue management, querying, and other Jira operations.
"""

# Expose the root agent and create_agent function at the package level for easier imports
from .agent import root_agent, create_agent

__all__ = ["root_agent", "create_agent"]
