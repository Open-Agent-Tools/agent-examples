"""
GoogleADK (Agent Development Kit) package.

This package contains specialized AI agent examples built with Google's Agent Development Kit.
It includes:
- Butler_Basil: A generic task and facilitation agent
- Data_Daniel: A data analysis and processing agent
- FileOps_Freddy: A specialized file and directory operations agent
- Jira_Johnny: A JIRA integration and task management agent
- Scrum_Sam: A Scrum/Agile project management agent

These agents demonstrate how to build and use AI agents for various tasks.
"""

# Make the agent packages available at the top level
from . import Butler_Basil
from . import FileOps_Freddy
from . import Jira_Johnny
from . import Scrum_Sam
from . import Data_Daniel

__all__ = ["Butler_Basil", "FileOps_Freddy", "Jira_Johnny", "Scrum_Sam", "Data_Daniel"]
