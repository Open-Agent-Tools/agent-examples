"""User Story Specialist Agent Configuration.

This module configures Story_Sage, a specialized agent for crafting
high-quality user stories and managing story-related processes in Agile development.

It can function both as a standalone root agent and as a sub-agent integrated
with other agents like Scrum_Sam for comprehensive Agile workflows.
"""

import logging
import os
import warnings

from google.adk.agents import Agent

from .prompts import agent_instruction
import basic_open_agent_tools as boat


try:
    from ..Jira_Johnny import create_agent as create_jira_agent
except ImportError:
    import sys
    from pathlib import Path

    current_file = Path(__file__)
    project_root = current_file.parent.parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    import GoogleADK.Jira_Johnny

    create_jira_agent = GoogleADK.Jira_Johnny.create_agent

from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.ERROR)
warnings.filterwarnings("ignore")


def create_agent(include_jira: bool = True) -> Agent:
    """
    Creates and returns a configured User Story agent instance.

    Args:
        include_jira: Whether to include Jira integration as a sub-agent.
                     Set to False when used as a sub-agent.

    Returns:
        Agent: Configured Story_Sage agent with appropriate tools and settings.
    """

    agent_tools = boat.merge_tool_lists(
        boat.load_all_filesystem_tools(), boat.load_all_text_tools()
    )

    sub_agents = []
    if include_jira:
        jira_johnny_agent = create_jira_agent()
        sub_agents.append(jira_johnny_agent)

    return Agent(
        model=os.environ.get("GOOGLE_MODEL") or "gemini-2.0-flash",
        name="Story_Sage",
        instruction=agent_instruction,
        description="Specialized User Story agent that crafts high-quality user stories following INVEST principles and can integrate with Jira for story management.",
        tools=agent_tools,
        sub_agents=sub_agents,
    )


root_agent = create_agent()
