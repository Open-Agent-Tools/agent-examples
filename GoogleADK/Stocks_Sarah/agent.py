"""Stock Trading Agent Configuration.

This module configures Stocks_Sarah, a specialized agent for handling
stock market operations and interactions with Robin Stocks through our MCP server.

It uses the specified Google model and connects to our open-stocks-mcp server
via HTTP transport to provide real-time stock market data and trading capabilities.
"""

import logging
import os
import warnings

from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.mcp_tool.mcp_toolset import (
    MCPToolset,
    StreamableHTTPConnectionParams,
)

from .prompts import agent_instruction

from basic_open_agent_tools import load_all_datetime_tools


# Initialize environment and logging
load_dotenv()
logging.basicConfig(level=logging.ERROR)
warnings.filterwarnings("ignore")


def create_agent() -> Agent:
    """
    Creates and returns a configured Stock Trading agent instance.

    Returns:
        Agent: Configured Stocks_Sarah agent with HTTP transport to MCP server.
    """

    # Use HTTP transport - server must be running separately
    http_url = os.environ.get("MCP_HTTP_URL", "http://localhost:3001/mcp")
    stock_mcp = [
        MCPToolset(
            connection_params=StreamableHTTPConnectionParams(
                url=http_url,
            ),
        )
    ]

    date_tools = load_all_datetime_tools()

    all_tools = stock_mcp + date_tools

    return Agent(
        model=os.environ.get("GOOGLE_MODEL") or "gemini-2.0-flash",
        name="Stocks_Sarah",
        instruction=agent_instruction,
        description="Specialized stock trading agent that can perform Robin Stocks operations through MCP tools.",
        tools=all_tools,
    )


# Configure specialized Stock Trading operations agent
root_agent = create_agent()
