"""Product Pete: A Product Manager AI assistant built with Strands Agents"""

import logging
import os
from pathlib import Path
from strands import Agent
from strands.models.anthropic import AnthropicModel
from mcp.client.streamable_http import streamablehttp_client
from strands.tools.mcp.mcp_client import MCPClient

try:
    from .prompts import SYSTEM_PROMPT
except ImportError:
    from prompts import SYSTEM_PROMPT  # type: ignore

from dotenv import load_dotenv

env_loaded = False
for i in range(3):
    env_path = Path(__file__).parents[i] / ".env"
    if env_path.exists():
        load_dotenv(env_path, override=False)
        env_loaded = True
        break

if not env_loaded:
    load_dotenv(override=False)

logging.basicConfig(
    level=logging.WARNING, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def add_mcp_tools(base_tools: list, mcp_url: str):
    """Add MCP tools to the base tools list."""
    logger.info(f"Connecting to MCP server at {mcp_url}")

    try:
        mcp_client = MCPClient(lambda: streamablehttp_client(mcp_url))
        mcp_client.start()
        mcp_tools = list(mcp_client.list_tools_sync())
        base_tools.extend(mcp_tools)

        logger.info(f"Successfully added {len(mcp_tools)} MCP tools")
        return base_tools
    except Exception as e:
        logger.warning(f"Failed to connect to MCP server at {mcp_url}: {e}")
        logger.warning(
            "Agent will start without MCP tools - they may be available later"
        )
        return base_tools


def create_agent():
    """Create Product Pete agent with MCP tools."""
    tools = []
    mcp_url = os.getenv("MCP_SERVER_URL", "http://localhost:9000/mcp/")
    tools = add_mcp_tools(tools, mcp_url)

    model = AnthropicModel(
        client_args={
            "api_key": os.getenv("ANTHROPIC_API_KEY"),
        },
        model_id="claude-sonnet-4-20250514",
        max_tokens=32768,
        params={
            "temperature": 0.7,
        },
    )

    return Agent(
        model=model,
        name="Product Pete",
        description="A Product Manager AI assistant built with Strands Agents",
        tools=tools,
        system_prompt=SYSTEM_PROMPT,
    )


root_agent = create_agent()


def main():
    """Simple test function to verify Product Pete works."""
    print("Testing Product Pete...")

    try:
        response = root_agent(
            "Hello! Please list the names of available jira projects."
        )
        print(f"Agent Response: {response}")
    except Exception as e:
        logger.error(f"Test failed: {e}")
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
