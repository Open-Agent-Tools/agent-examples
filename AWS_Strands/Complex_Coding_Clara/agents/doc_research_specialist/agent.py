"""
Doc Research Specialist Agent - Technical documentation research expert
"""

import logging
import os
from pathlib import Path
from strands import Agent, tool
from strands.models.bedrock import BedrockModel

# MCP imports for Context7 integration
try:
    from mcp.client.streamable_http import streamablehttp_client
    from strands.tools.mcp.mcp_client import MCPClient

    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False

# Setup logging
logger = logging.getLogger(__name__)

# Load environment
try:
    from dotenv import load_dotenv

    current_path = Path(__file__).parent.parent
    env_path = current_path / ".env"
    if env_path.exists():
        load_dotenv(env_path)
    else:
        for i in range(min(3, len(Path(__file__).parents))):
            env_path = Path(__file__).parents[i] / ".env"
            if env_path.exists():
                load_dotenv(env_path)
                break
except ImportError:
    pass

# Import prompts
try:
    from .prompt import DOC_RESEARCH_SPECIALIST_SYSTEM_PROMPT
except ImportError:
    from prompt import DOC_RESEARCH_SPECIALIST_SYSTEM_PROMPT

# Import tools
strands_tools = []
try:
    from strands_tools import file_read, file_write, current_time, http_request

    strands_tools = [file_read, file_write, current_time, http_request]
except ImportError:
    pass

boat_tools = []
try:
    import basic_open_agent_tools as boat

    # Add filesystem tools for caching research
    file_tools = boat.load_all_filesystem_tools()

    # Add data tools for structured research caching (JSON, YAML)
    data_tools = [
        boat.data.safe_json_serialize,
        boat.data.safe_json_deserialize,
        boat.data.read_yaml_file,
        boat.data.write_yaml_file,
    ]

    # Add text tools for documentation formatting
    text_tools = [
        boat.text.clean_whitespace,
        boat.text.normalize_line_endings,
        boat.text.extract_sentences,
    ]

    boat_tools = file_tools + data_tools + text_tools
except ImportError:
    pass


# MCP tools for Context7 (live library documentation) integration
def add_mcp_tools(base_tools: list, mcp_url: str) -> list:
    """Add MCP tools to base tools list - handle failures gracefully."""
    if not MCP_AVAILABLE:
        logger.warning(
            "MCP client not available - install mcp package for Context7 integration"
        )
        return base_tools

    logger.info(f"Connecting to MCP server at {mcp_url}")

    try:
        mcp_client = MCPClient(lambda: streamablehttp_client(mcp_url))
        mcp_client.start()
        mcp_tools = list(mcp_client.list_tools_sync())
        base_tools.extend(mcp_tools)

        logger.info(f"Successfully added {len(mcp_tools)} MCP tools for Context7")
        return base_tools
    except Exception as e:
        logger.warning(f"Failed to connect to MCP server at {mcp_url}: {e}")
        logger.warning(
            "Agent will start without MCP tools - Context7 documentation lookup unavailable"
        )
        return base_tools


# Build tool list
try:
    tools = strands_tools + boat_tools

    # Add Context7 MCP tools if server is configured
    mcp_url = os.getenv("MCP_SERVER_URL", "http://localhost:9000/mcp/")
    if mcp_url:
        tools = add_mcp_tools(tools, mcp_url)
except Exception:
    tools = []


# Create the Bedrock model for Doc Research Specialist
# Using Claude Haiku 3.5 (cost optimized - good for doc synthesis)
model = BedrockModel(
    model_id="us.anthropic.claude-3-5-haiku-20241022-v1:0",  # Claude Haiku 3.5 (inference profile)
    region_name=os.getenv("AWS_REGION", "us-east-1"),
    max_tokens=16384,  # Increased to Haiku limit for comprehensive research
    temperature=0.2,  # Lower for factual research
)


def create_doc_research_specialist_agent() -> Agent:
    """Create the Doc Research Specialist agent."""
    return Agent(
        name="Doc Research Specialist",
        description="Technical doc research: APIs, libraries, best practices, patterns",
        model=model,
        system_prompt=DOC_RESEARCH_SPECIALIST_SYSTEM_PROMPT,
        tools=tools,
        callback_handler=None,
    )


# Create the agent instance
_doc_research_specialist_agent = create_doc_research_specialist_agent()


@tool
def doc_research_specialist(task: str) -> str:
    """
    Delegate technical documentation research to the Doc Research Specialist.

    Use this for:
    - Library/framework documentation lookup
    - API reference research
    - Best practices and design patterns
    - Technology comparisons
    - Code example discovery
    - Architecture decision research

    Args:
        task: Detailed description of the research need

    Returns:
        Synthesized documentation with sources, examples, and actionable guidance
    """
    try:
        result = _doc_research_specialist_agent(task)
        return str(result)
    except Exception as e:
        return f"Doc Research Specialist error: {str(e)}"


# Export for direct use
__all__ = ["doc_research_specialist", "create_doc_research_specialist_agent"]
