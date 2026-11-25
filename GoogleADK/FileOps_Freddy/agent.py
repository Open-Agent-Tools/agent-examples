"""File Operations Sub-Agent Configuration.

This module configures FileOps_Freddy, a specialized sub-agent for handling
file and directory operations delegated from the main Python developer agent.
"""

import logging
import os
import warnings

from google.adk.agents import Agent

from .prompts import agent_instruction
import basic_open_agent_tools as boat  # type: ignore

from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.ERROR)
warnings.filterwarnings("ignore")


def create_agent() -> Agent:
    """
    Creates and returns a configured FileOps agent instance.

    Returns:
        Agent: Configured FileOps agent with appropriate tools and settings.
    """

    fs_tools = boat.load_all_filesystem_tools()
    text_tools = boat.load_all_text_tools()
    agent_tools = boat.merge_tool_lists(fs_tools, text_tools)

    return Agent(
        model=os.environ.get("GOOGLE_MODEL") or "gemini-2.0-flash",
        name="FileOps_Freddy",
        instruction=agent_instruction,
        description="Specialized file and directory operations agent that can enumerate directories and files, write to files, and perform basic text processing.",
        tools=agent_tools,
    )


root_agent = create_agent()
