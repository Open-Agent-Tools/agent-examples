"""
FileOps_Freddy Agent Package.

This package contains the FileOps_Freddy agent, a specialized file and directory operations agent
designed to handle file system tasks efficiently.

The agent is built using Google's Agent Development Kit (ADK) and uses the Gemini model.
It provides tools for file operations, directory management, and text processing.
"""

# Expose the root agent and create_agent function at the package level for easier imports
from .agent import root_agent, create_agent
from . import agent

__all__ = ["root_agent", "create_agent", "agent"]
