"""
GoogleADK (Agent Development Kit) package.

This package contains specialized AI agent examples built with Google's Agent Development Kit.
It includes:
- Butler_Basil: A generic task and facilitation agent
- FileOps_Freddy: A specialized file and directory operations agent

These agents demonstrate how to build and use AI agents for various tasks.
"""

# Make the agent packages available at the top level
from . import Butler_Basil
from . import FileOps_Freddy

__all__ = ["Butler_Basil", "FileOps_Freddy"]
