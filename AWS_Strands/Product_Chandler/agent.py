"""
Product Chandler: A Product Manager AI assistant built with Strands Agents
Includes Atlassian MCP server for Jira/Confluence integration
"""

import os
from pathlib import Path
from strands import Agent
from strands_tools import calculator, current_time, file_read, file_write
from prompts import SYSTEM_PROMPT

# Load .env file
try:
    from dotenv import load_dotenv
    for i in range(4):
        env_path = Path(__file__).parents[i] / '.env'
        if env_path.exists():
            load_dotenv(env_path)
            break
except ImportError:
    pass

# Create agent
if os.getenv('ANTHROPIC_API_KEY'):
    try:
        from strands.models.anthropic import AnthropicModel
        model = AnthropicModel(
            model_id="claude-3-5-sonnet-20241022",
            max_tokens=4096
        )
    except ImportError:
        model = "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
else:
    model = "us.anthropic.claude-3-7-sonnet-20250219-v1:0"

# Setup basic tools
tools = [calculator, current_time, file_read, file_write]

# Add Atlassian MCP tools
try:
    from mcp.client.streamable_http import streamablehttp_client
    from strands.tools.mcp.mcp_client import MCPClient

    def create_streamable_http_transport():
        return streamablehttp_client('http://localhost:9000/mcp/')

    streamable_http_mcp_client = MCPClient(create_streamable_http_transport)

    # Use the MCP server in a context manager
    with streamable_http_mcp_client:
        # Get the tools from the MCP server
        mcp_tools = streamable_http_mcp_client.list_tools_sync()
        tools.extend(mcp_tools)
        print(f"Connected to Atlassian MCP server ({len(mcp_tools)} tools)")

except Exception as e:
    print(f"Failed to connect to Atlassian MCP server: {e}")



agent = Agent(
    model=model,
    tools=tools,
    system_prompt=SYSTEM_PROMPT
)

if __name__ == "__main__":
    print("Product Chandler Agent")
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            if user_input.lower() in ['exit', 'quit', 'bye']:
                break
            if user_input:
                print("\nChandler:")
                agent(user_input)
        except (KeyboardInterrupt, EOFError):
            break
    
    print("\nGoodbye!")
    
