"""
Senior Coder Agent - Complex coding and algorithms specialist
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
    from .prompt import SENIOR_CODER_SYSTEM_PROMPT
except ImportError:
    from prompt import SENIOR_CODER_SYSTEM_PROMPT

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

    # Add all data tools for complex config/data handling
    data_tools = boat.load_all_data_tools()

    # Add filesystem tools
    file_tools = boat.load_all_filesystem_tools()

    # Add utilities tools for advanced debugging/profiling
    utilities_tools = boat.load_all_utilities_tools()

    # Add text tools for code formatting
    text_tools = [
        boat.text.to_snake_case,
        boat.text.to_camel_case,
        boat.text.clean_whitespace,
    ]

    boat_tools = file_tools + data_tools + utilities_tools + text_tools
except ImportError:
    pass

# Build tool list
try:
    tools = strands_tools + boat_tools
except Exception:
    tools = []


# Create the Bedrock model for Senior Coder
model = BedrockModel(
    model_id="us.anthropic.claude-sonnet-4-5-20250929-v1:0",  # Claude Sonnet 4.5 (inference profile)
    region_name=os.getenv("AWS_REGION", "us-east-1"),
    max_tokens=16384,  # Increased to Sonnet limit for complex algorithms
    temperature=0.2,  # Lower for more precise coding
)


def create_senior_coder_agent() -> Agent:
    """Create the Senior Coder agent."""
    return Agent(
        name="Senior Coder",
        description="Complex algorithms, advanced refactoring, and multi-step problem solving",
        model=model,
        system_prompt=SENIOR_CODER_SYSTEM_PROMPT,
        tools=tools,
        callback_handler=None,  # Suppress intermediate output
    )


# Create the agent instance
_senior_coder_agent = create_senior_coder_agent()


@tool
def senior_coder(task: str) -> str:
    """
    Delegate complex coding tasks to the Senior Coder specialist.

    Use this for:
    - Complex algorithms & data structures
    - Performance optimization
    - Advanced refactoring
    - Multi-step problem solving

    Args:
        task: Detailed description of the coding task

    Returns:
        Implementation with code, explanation, and recommendations
    """
    try:
        result = _senior_coder_agent(task)
        return str(result)
    except Exception as e:
        return f"Senior Coder error: {str(e)}"


# Export for direct use
__all__ = ["senior_coder", "create_senior_coder_agent"]
