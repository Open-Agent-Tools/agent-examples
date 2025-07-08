"""
Stocks_Sarah Agent Package.

This package contains the Stocks_Sarah agent, a specialized stock operations agent
designed to interact with stock market and perform stock-related tasks efficiently.

The agent is built using Google's Agent Development Kit (ADK) and uses the Gemini model.
It provides tools for stock management, querying, and other stock operations.
"""

# Expose the root agent and create_agent function at the package level for easier imports
from .agent import root_agent, create_agent
from . import agent

__all__ = ["root_agent", "create_agent", "agent"]
