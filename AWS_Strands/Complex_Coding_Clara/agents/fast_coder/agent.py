"""
Fast Coder Agent - Rapid implementation for standard coding tasks
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
    from .prompt import FAST_CODER_SYSTEM_PROMPT
except ImportError:
    from prompt import FAST_CODER_SYSTEM_PROMPT

# Import tools
strands_tools = []
try:
    from strands_tools import (
        file_read,
        file_write,
        editor,
        python_repl,
        shell,
        calculator,
        current_time,
    )

    strands_tools = [
        file_read,
        file_write,
        editor,
        python_repl,
        shell,
        calculator,
        current_time,
    ]
except ImportError:
    pass

boat_tools = []
try:
    import basic_open_agent_tools as boat

    # Add all data tools for config/API handling (CSV, JSON, YAML, validation)
    data_tools = boat.load_all_data_tools()

    # Add filesystem tools
    file_tools = boat.load_all_filesystem_tools()

    # Add text tools for boilerplate formatting
    text_tools = [
        boat.text.to_snake_case,
        boat.text.to_camel_case,
        boat.text.clean_whitespace,
    ]

    boat_tools = file_tools + data_tools + text_tools
except ImportError:
    pass

# Build tool list
try:
    tools = strands_tools + boat_tools
except Exception:
    tools = []


# Create the Bedrock model for Fast Coder
# Using Nova Pro for speed and cost-effectiveness
model = BedrockModel(
    model_id="us.amazon.nova-pro-v1:0",  # Nova Pro (inference profile)
    region_name=os.getenv("AWS_REGION", "us-east-1"),
    max_tokens=5120,  # Increased to Nova Pro limit for comprehensive implementations
    temperature=0.3,  # Moderate for standard coding
)


def create_fast_coder_agent() -> Agent:
    """Create the Fast Coder agent."""
    return Agent(
        name="Fast Coder",
        description="Rapid implementation of CRUD, API endpoints, and boilerplate code",
        model=model,
        system_prompt=FAST_CODER_SYSTEM_PROMPT,
        tools=tools,
        callback_handler=None,  # Suppress intermediate output
    )


# Create the agent instance
_fast_coder_agent = create_fast_coder_agent()


@tool
def fast_coder(task: str) -> str:
    """
    Delegate simple, standard coding tasks to the Fast Coder specialist.

    Use this for:
    - CRUD operations & API endpoints
    - Boilerplate code generation
    - Standard design patterns
    - Simple function implementations
    - Basic data transformations
    - Common utility functions

    Args:
        task: Detailed description of the coding task

    Returns:
        Working code implementation with basic examples
    """
    try:
        result = _fast_coder_agent(task)
        return str(result)
    except Exception as e:
        return f"Fast Coder error: {str(e)}"


# Export for direct use
__all__ = ["fast_coder", "create_fast_coder_agent"]
