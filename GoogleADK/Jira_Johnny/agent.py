"""Jira Operations Agent Configuration.

This module configures Jira_Johnny, a specialized agent for handling
Jira operations and interactions with Atlassian tools.

It uses the specified Google model and connects to Atlassian services
through a Docker container with the necessary credentials.
"""
import logging
import os
import warnings

from google.adk.agents import Agent

from .prompts import agent_instruction
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StreamableHTTPConnectionParams
from dotenv import load_dotenv

# Initialize environment and logging
load_dotenv()  # or load_dotenv(dotenv_path="/env_path")
logging.basicConfig(level=logging.ERROR)
warnings.filterwarnings("ignore")


def create_agent() -> Agent:
    """
    Creates and returns a configured Jira agent instance.

    Args:

    Returns:
        Agent: Configured Jira agent with appropriate tools and settings.
    """

    agent_tools = [
        MCPToolset(
            connection_params=StreamableHTTPConnectionParams(
                url="http://localhost:9000/mcp",
            ),
            # Optional: Filter which tools from the MCP server are exposed
            # tool_filter=['list_directory', 'read_file']
        ),
    ]

    return Agent(
        model=os.environ.get("GOOGLE_MODEL"),
        name="Jira_Johnny",
        instruction=agent_instruction,
        description="Specialized Jira agent that can perform basic jira functions from the available tools.",
        tools=agent_tools,
    )


# Configure specialized Jira operations agent
root_agent = create_agent()
