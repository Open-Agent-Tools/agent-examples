"""Butler/Generic Task Agent Configuration.

This module configures Basil, the main generic task and facilitation agent
responsible for general task coordination and file management operations.
"""

import logging
import os
import warnings

from google.adk.agents import Agent

from .prompts import agent_instruction

import basic_open_agent_tools as boat  # type: ignore
# from basic_open_agent_tools import load_all_filesystem_tools

from dotenv import load_dotenv

# Initialize environment and logging
load_dotenv()  # or load_dotenv(dotenv_path="/env_path")
logging.basicConfig(level=logging.ERROR)
warnings.filterwarnings("ignore")


agent_tools = boat.load_all_filesystem_tools()


def create_agent() -> Agent:
    """
    Creates and returns a configured Butler agent instance.

    Returns:
        Agent: Configured Butler agent with appropriate tools and settings.
    """

    return Agent(
        model=os.environ.get("GOOGLE_MODEL") or "gemini-2.0-flash",
        name="Basil",
        instruction=agent_instruction,
        description="A generic task and facilitation agent.",
        tools=agent_tools,
    )


# Configure agent with comprehensive file system tools
root_agent = create_agent()
