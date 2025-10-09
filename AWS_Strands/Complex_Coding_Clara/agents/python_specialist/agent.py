"""
Python Specialist Agent - Python language and ecosystem expert
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
    from .prompt import PYTHON_SPECIALIST_SYSTEM_PROMPT
except ImportError:
    from prompt import PYTHON_SPECIALIST_SYSTEM_PROMPT

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

    # Add all data tools for Python configs (TOML, JSON, YAML, CSV)
    data_tools = boat.load_all_data_tools()

    # Add filesystem tools
    file_tools = boat.load_all_filesystem_tools()

    # Add text tools for Pythonic naming conventions
    text_tools = [
        boat.text.to_snake_case,
        boat.text.clean_whitespace,
        boat.text.normalize_line_endings,
    ]

    # Add system tools for Python environment inspection
    system_tools = [
        boat.system.get_python_module_info,
        boat.system.inspect_runtime_environment,
    ]

    boat_tools = file_tools + data_tools + text_tools + system_tools
except ImportError:
    pass

# Build tool list
try:
    tools = strands_tools + boat_tools
except Exception:
    tools = []


# Create the Bedrock model for Python Specialist
# Using Claude Haiku 3.5 (cost optimized - good for patterns/templates)
model = BedrockModel(
    model_id="us.anthropic.claude-3-5-haiku-20241022-v1:0",  # Claude Haiku 3.5 (inference profile)
    region_name=os.getenv("AWS_REGION", "us-east-1"),
    max_tokens=16384,  # Increased to Haiku limit for comprehensive Python code
    temperature=0.2,  # Lower for precise Python code
)


def create_python_specialist_agent() -> Agent:
    """Create the Python Specialist agent."""
    return Agent(
        name="Python Specialist",
        description="Python language expert: PEP standards, idioms, type hints, and ecosystem",
        model=model,
        system_prompt=PYTHON_SPECIALIST_SYSTEM_PROMPT,
        tools=tools,
        callback_handler=None,
    )


# Create the agent instance
_python_specialist_agent = create_python_specialist_agent()


@tool
def python_specialist(task: str) -> str:
    """
    Delegate Python-specific tasks to the Python Specialist.

    Use this for:
    - Writing idiomatic Python code (Pythonic patterns)
    - Type hints and mypy integration
    - Python-specific optimizations
    - Async/await patterns
    - PEP standards compliance
    - Python ecosystem tools (pytest, ruff, poetry)

    Args:
        task: Detailed description of the Python task

    Returns:
        Idiomatic Python code with type hints, tests, and best practices
    """
    try:
        result = _python_specialist_agent(task)
        return str(result)
    except Exception as e:
        return f"Python Specialist error: {str(e)}"


# Export for direct use
__all__ = ["python_specialist", "create_python_specialist_agent"]
