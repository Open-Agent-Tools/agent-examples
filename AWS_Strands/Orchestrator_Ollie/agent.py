"""
Orchestrator Ollie Agent

A specialized agent for coordinating and orchestrating tasks across multiple systems,
agents, and workflows. Built with AWS Strands framework.
"""

import os
from pathlib import Path
from strands import Agent, tool
from strands.models.anthropic import AnthropicModel

# Load environment variables
try:
    from dotenv import load_dotenv

    # Search current directory and up to 3 parent folders for .env
    current_path = Path(__file__).parent
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

# Import prompts and tools
try:
    from .prompts import SYSTEM_PROMPT
except ImportError:
    from prompts import SYSTEM_PROMPT

try:
    from .subagent import root_agent as worker
except ImportError:
    from subagent import root_agent as worker

# Import basic open agent tools for CSV and file operations
try:
    import basic_open_agent_tools as boat

    # Load just the essential CSV and file tools
    csv_tools = [
        boat.data.read_csv_simple,
        boat.data.write_csv_simple,
        boat.data.csv_to_dict_list,
    ]
    file_tools = boat.load_all_filesystem_tools()
    tools = boat.helpers.merge_tool_lists(csv_tools, file_tools)
except ImportError:
    # Fallback to strands_tools if basic-open-agent-tools not available
    try:
        from strands_tools.file_read import file_read
        from strands_tools.file_write import file_write
        from strands_tools.current_time import current_time

        tools = [file_read, file_write, current_time]
    except ImportError:
        tools = []

# Create the Anthropic model
model = AnthropicModel(
    client_args={
        "api_key": os.getenv("ANTHROPIC_API_KEY"),
    },
    model_id="claude-3-5-sonnet-20241022",
    max_tokens=8192,
    params={
        "temperature": 0.3,
    },
)


# Create individual worker agent tools using proper Strands @tool decorator
@tool
def worker1(task_instruction: str) -> str:
    """
    Delegate a task to worker agent #1.

    Args:
        task_instruction: Clear instruction for the worker to execute

    Returns:
        Result from worker agent #1
    """
    try:
        result = worker(task_instruction)
        return str(result)
    except Exception as e:
        return f"Worker1 error: {str(e)}"


@tool
def worker2(task_instruction: str) -> str:
    """
    Delegate a task to worker agent #2.

    Args:
        task_instruction: Clear instruction for the worker to execute

    Returns:
        Result from worker agent #2
    """
    try:
        result = worker(task_instruction)
        return str(result)
    except Exception as e:
        return f"Worker2 error: {str(e)}"


@tool
def worker3(task_instruction: str) -> str:
    """
    Delegate a task to worker agent #3.

    Args:
        task_instruction: Clear instruction for the worker to execute

    Returns:
        Result from worker agent #3
    """
    try:
        result = worker(task_instruction)
        return str(result)
    except Exception as e:
        return f"Worker3 error: {str(e)}"


@tool
def worker4(task_instruction: str) -> str:
    """
    Delegate a task to worker agent #4.

    Args:
        task_instruction: Clear instruction for the worker to execute

    Returns:
        Result from worker agent #4
    """
    try:
        result = worker(task_instruction)
        return str(result)
    except Exception as e:
        return f"Worker4 error: {str(e)}"


@tool
def worker5(task_instruction: str) -> str:
    """
    Delegate a task to worker agent #5.

    Args:
        task_instruction: Clear instruction for the worker to execute

    Returns:
        Result from worker agent #5
    """
    try:
        result = worker(task_instruction)
        return str(result)
    except Exception as e:
        return f"Worker5 error: {str(e)}"


all_tools = tools + [worker1, worker2, worker3, worker4, worker5]


def create_agent() -> Agent:
    """Create Orchestrator Ollie agent with worker delegation capability."""

    # Combine BOAT tools with worker delegation tool

    return Agent(
        name="Orchestrator Ollie",
        description="A specialized agent for coordinating and orchestrating tasks across multiple systems and workflows with worker delegation",
        model=model,
        system_prompt=SYSTEM_PROMPT,
        tools=all_tools,
    )


# Module-level agent
root_agent = create_agent()

if __name__ == "__main__":
    agent = create_agent()
    print(f"✓ Agent: {agent.name}")
    print(f"✓ Model: {agent.model}")
    print("✓ Orchestrator Ollie ready for task coordination and CSV processing")

    # Simple test
    try:
        response = agent("Hello! What can you help me orchestrate today?")
        print(f"\nAgent Response: {response}")
    except Exception as e:
        print(f"Error: {e}")
