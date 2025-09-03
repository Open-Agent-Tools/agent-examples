"""Product Pete: A Product Manager AI assistant built with Strands Agents"""

import os
from pathlib import Path
from strands import Agent
from strands.models.anthropic import AnthropicModel
from strands_tools import calculator, current_time, file_read, file_write

# Import prompts
try:
    from .prompts import SYSTEM_PROMPT
except ImportError:
    from prompts import SYSTEM_PROMPT  # type: ignore

# Load environment variables from .env file
from dotenv import load_dotenv

# Load .env file from project root
project_root = Path(__file__).parent.parent.parent.parent
load_dotenv(project_root / ".env")

def create_agent():
    """Create Product Pete agent with Atlassian MCP tools."""
    # Basic tools
    tools = [calculator, current_time, file_read, file_write]
    
    # Add MCP tools if available
    try:
        import sys
        parent_dir = Path(__file__).parent.parent
        if str(parent_dir) not in sys.path:
            sys.path.insert(0, str(parent_dir))
        
        from utilities import add_mcp_tools, setup_agent_logging
        
        logger = setup_agent_logging("Product Pete")
        tools = add_mcp_tools(tools, "http://localhost:9000/mcp/", logger)
    except Exception as e:
        print(f"MCP tools not available: {e}")
    
    # Create the Anthropic model with Claude Sonnet 4
    model = AnthropicModel(
        client_args={
            "api_key": os.getenv("ANTHROPIC_API_KEY"),
        },
        model_id="claude-sonnet-4-20250514",
        max_tokens=1024,
        params={
            "temperature": 0.7,
        }
    )
    
    # Create the agent
    return Agent(
        model=model,
        name="Product Pete",
        description="A Product Manager AI assistant built with Strands Agents",
        tools=tools,
        system_prompt=SYSTEM_PROMPT
    )

# Create the root agent
root_agent = create_agent()

# Simple test function for local execution
def main():
    """Simple test function to verify Product Pete works."""
    print("Testing Product Pete...")
    
    try:
        response = root_agent("Hello! Please introduce yourself.")
        print(f"Agent Response: {response}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()