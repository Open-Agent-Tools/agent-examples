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


# Import Jira_Johnny and Story_Sage with fallback for different execution contexts
try:
    from ..Jira_Johnny import create_agent as create_jira_agent
    from ..Story_Sage import create_agent as create_story_agent
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
    import GoogleADK.Story_Sage

    create_jira_agent = GoogleADK.Jira_Johnny.create_agent
    create_story_agent = GoogleADK.Story_Sage.create_agent

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

    # Create fresh sub-agent instances for this Scrum_Sam agent
    jira_johnny_agent = create_jira_agent()
    # Create Story_Sage without Jira integration to prevent circular dependencies
    story_sage_agent = create_story_agent(include_jira=False)

    return Agent(
        model=os.environ.get("GOOGLE_MODEL") or "gemini-2.0-flash",
        name="Scrum_Sam",
        instruction=agent_instruction,
        description="Specialized Scrum Master agent that can coach the team, perform Jira functions, and craft high-quality user stories following INVEST principles.",
        tools=agent_tools,
        sub_agents=[jira_johnny_agent, story_sage_agent],
    )


# Configure specialized Scrum Master agent
root_agent = create_agent()
