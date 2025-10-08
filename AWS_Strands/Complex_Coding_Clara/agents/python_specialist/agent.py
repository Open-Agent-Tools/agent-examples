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

    csv_tools = [
        boat.data.read_csv_simple,
        boat.data.write_csv_simple,
        boat.data.csv_to_dict_list,
    ]
    file_tools = boat.load_all_filesystem_tools()
    boat_tools = csv_tools + file_tools
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
    max_tokens=8192,
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
