"""Data Processing Sub-Agent Configuration.

This module configures Data_Daniel, a specialized sub-agent for handling
data processing operations delegated from the main Python developer agent.
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
    Creates and returns a configured Data Processing agent instance.

    Returns:
        Agent: Configured Data Processing agent with appropriate tools and settings.
    """

    data_tools = boat.load_all_data_tools()
    agent_tools = boat.merge_tool_lists(data_tools)

    return Agent(
        model=os.environ.get("GOOGLE_MODEL") or "gemini-2.0-flash",
        name="Data_Daniel",
        instruction=agent_instruction,
        description="Specialized data processing agent that can analyze, transform, and visualize data.",
        tools=agent_tools,
    )


root_agent = create_agent()
