"""
Data_Daniel Agent Package.

This package contains the Data_Daniel agent, a specialized data processing agent
designed to analyze, transform, and visualize data efficiently.

The agent is built using Google's Agent Development Kit (ADK) and uses the Gemini model.
It provides tools for data analysis, transformation, and visualization.
"""

# Expose the root agent and create_agent function at the package level for easier imports
from .agent import root_agent, create_agent
from . import agent

__all__ = ["root_agent", "create_agent", "agent"]
