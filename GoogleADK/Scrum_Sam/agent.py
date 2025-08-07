"""Scrum Master Agent Configuration.

This module configures Scrum_Sam, a specialized agent for handling
Scrum Master responsibilities and interactions with Atlassian tools.

It uses the specified Google model and connects to Atlassian services
through a Docker container with the necessary credentials.
"""

import logging
import os
import warnings

from google.adk.agents import Agent

from .prompts import agent_instruction
import basic_open_agent_tools as boat


# Import Jira_Johnny with fallback for different execution contexts
try:
    from ..Jira_Johnny import create_agent as create_jira_agent
except ImportError:
    # Fallback for when running via ADK eval or other contexts
    import sys
    from pathlib import Path

    # Add parent directory to Python path
    current_file = Path(__file__)
    project_root = current_file.parent.parent.parent  # Go up to agent-examples
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    import GoogleADK.Jira_Johnny

    create_jira_agent = GoogleADK.Jira_Johnny.create_agent

from dotenv import load_dotenv

# Initialize environment and logging
load_dotenv()  # or load_dotenv(dotenv_path="/env_path")
logging.basicConfig(level=logging.ERROR)
warnings.filterwarnings("ignore")


def create_agent() -> Agent:
    """
    Creates and returns a configured Scrum Master agent instance.

    Returns:
        Agent: Configured Scrum Master agent with appropriate tools and settings.
    """

    agent_tools = boat.merge_tool_lists(
        boat.load_all_filesystem_tools(), boat.load_all_text_tools()
    )

    # Create fresh Jira_Johnny instance for this Scrum_Sam agent
    jira_johnny_agent = create_jira_agent()

    return Agent(
        model=os.environ.get("GOOGLE_MODEL") or "gemini-2.0-flash",
        name="Scrum_Sam",
        instruction=agent_instruction,
        description="Specialized Scrum Master agent that can coach the team and perform basic jira functions from the available tools.",
        tools=agent_tools,
        sub_agents=[jira_johnny_agent],
    )


# Configure specialized Scrum Master agent
root_agent = create_agent()
