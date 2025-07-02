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
from basic_open_agent_tools.file_system.tree import generate_directory_tree
from basic_open_agent_tools.file_system.operations import read_file_to_string
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters

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

    agent_tools = [
        generate_directory_tree,
        read_file_to_string,
        MCPToolset(
            connection_params=StdioServerParameters(
                command="docker",
                args=[
                    "run",
                    "-i",
                    "--rm",
                    "-e",
                    "CONFLUENCE_URL",
                    "-e",
                    "CONFLUENCE_USERNAME",
                    "-e",
                    "JIRA_URL",
                    "-e",
                    "JIRA_USERNAME",
                    "-e",
                    "CONFLUENCE_API_TOKEN",
                    "-e",
                    "CONFLUENCE_PERSONAL_TOKEN",
                    "-e",
                    "JIRA_API_TOKEN",
                    "-e",
                    "JIRA_PERSONAL_TOKEN",
                    "mcp/atlassian",
                ],
                env={
                    "CONFLUENCE_URL": os.environ.get("CONFLUENCE_URL") or "",
                    "CONFLUENCE_USERNAME": os.environ.get("ATTLASSIAN_USERNAME") or "",
                    "JIRA_URL": os.environ.get("JIRA_URL") or "",
                    "JIRA_USERNAME": os.environ.get("ATTLASSIAN_USERNAME") or "",
                    "CONFLUENCE_API_TOKEN": os.environ.get("ATTLASSIAN_KEY") or "",
                    "JIRA_API_TOKEN": os.environ.get("ATTLASSIAN_KEY") or "",
                },
            ),
            # Optional: Filter which tools from the MCP server are exposed
            # tool_filter=['list_directory', 'read_file']
        ),
    ]

    return Agent(
        model=os.environ.get("GOOGLE_MODEL") or "gemini-pro",
        name="Scrum_Sam",
        instruction=agent_instruction,
        description="Specialized Scrum Master agent that can coach the team and perform basic jira functions from the available tools.",
        tools=agent_tools,
    )


# Configure specialized Scrum Master agent
root_agent = create_agent()
