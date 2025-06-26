"""
Butler_Basil Agent Package.

This package contains the Butler_Basil agent, a generic task and facilitation agent
designed to assist with various tasks and provide information.

The agent is built using Google's Agent Development Kit (ADK) and uses the Gemini model.
"""

# Expose the root agent at the package level for easier imports
from .agent import root_agent
