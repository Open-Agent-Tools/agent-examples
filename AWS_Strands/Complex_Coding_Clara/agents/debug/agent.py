"""
Debug Agent - Error analysis and troubleshooting specialist
"""

import os
from pathlib import Path
from strands import Agent, tool
from strands.models.bedrock import BedrockModel

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
    from .prompt import DEBUG_SYSTEM_PROMPT
except ImportError:
    from prompt import DEBUG_SYSTEM_PROMPT

# Import tools
strands_tools = []
try:
    from strands_tools import (
        file_read,
        file_write,
        editor,
        python_repl,
        shell,
        current_time,
    )

    strands_tools = [file_read, file_write, editor, python_repl, shell, current_time]
except ImportError:
    pass

boat_tools = []
try:
    import basic_open_agent_tools as boat

    # Add filesystem tools for navigation
    file_tools = boat.load_all_filesystem_tools()
    boat_tools = file_tools
except ImportError:
    pass

# Build tool list
try:
    tools = strands_tools + boat_tools
except Exception:
    tools = []


# Create the Bedrock model for Debug Agent
# Using Claude Sonnet 4.5 for sophisticated error analysis
model = BedrockModel(
    model_id="us.anthropic.claude-sonnet-4-5-20250929-v1:0",  # Claude Sonnet 4.5 (inference profile)
    region_name=os.getenv("AWS_REGION", "us-east-1"),
    max_tokens=8192,
    temperature=0.2,  # Lower for precise debugging
)


def create_debug_agent() -> Agent:
    """Create the Debug agent."""
    return Agent(
        name="Debug Agent",
        description="Error analysis, stack trace interpretation, and bug fixing",
        model=model,
        system_prompt=DEBUG_SYSTEM_PROMPT,
        tools=tools,
        callback_handler=None,  # Suppress intermediate output
    )


# Create the agent instance
_debug_agent = create_debug_agent()


@tool
def debug(task: str) -> str:
    """
    Delegate debugging and error analysis tasks to the Debug specialist.

    Use this for:
    - Error message interpretation
    - Stack trace analysis
    - Root cause identification
    - Fix strategy generation
    - Bug reproduction
    - Performance profiling

    Args:
        task: Description of the error or bug (include error messages, stack traces)

    Returns:
        Error analysis, root cause, fix implementation, and prevention strategies
    """
    try:
        result = _debug_agent(task)
        return str(result)
    except Exception as e:
        return f"Debug Agent error: {str(e)}"


# Export for direct use
__all__ = ["debug", "create_debug_agent"]
