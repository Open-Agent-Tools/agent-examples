"""Butler/Generic Task Agent Configuration.

This module configures Basil, the main generic task and facilitation agent
responsible for general task coordination and file management operations.
"""

import logging
import warnings

from google.adk.agents import Agent

from .prompts import agent_instruction
import basic_open_agent_tools as boat  # type: ignore

from dotenv import load_dotenv

# Initialize environment and logging
load_dotenv() # or load_dotenv(dotenv_path="/env_path")
logging.basicConfig(level=logging.ERROR)
warnings.filterwarnings("ignore")


fs_tools = boat.load_all_filesystem_tools()

agent_tools = boat.merge_tool_lists(fs_tools)


# Configure agent with comprehensive file system tools
root_agent = Agent(
    model="gemini-2.0-flash",
    name="Basil",
    instruction=agent_instruction,
    description="A generic task and facilitation agent.",
    tools=agent_tools,
)
