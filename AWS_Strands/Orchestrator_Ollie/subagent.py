"""
Worker Sub-Agent for Orchestrator Ollie

A simple worker agent for processing individual CSV rows or other delegated tasks.
"""

import os
from pathlib import Path
from strands import Agent
from strands.models.anthropic import AnthropicModel

try:
    from dotenv import load_dotenv

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

try:
    import basic_open_agent_tools as boat

    tools = boat.helpers.merge_tool_lists(
        boat.load_all_data_tools(),
        boat.load_all_filesystem_tools(),
    )
except ImportError:
    try:
        from strands_tools.file_read import file_read
        from strands_tools.file_write import file_write
        from strands_tools.current_time import current_time

        tools = [file_read, file_write, current_time]
    except ImportError:
        tools = []

model = AnthropicModel(
    client_args={
        "api_key": os.getenv("ANTHROPIC_API_KEY"),
    },
    model_id="claude-3-5-haiku-20241022",
    max_tokens=4096,
    params={
        "temperature": 0.3,
    },
)

WORKER_SYSTEM_PROMPT = """You are a worker agent."""


def create_agent() -> Agent:
    """Create a worker sub-agent."""
    return Agent(
        name="Worker Agent",
        description="A worker agent for processing delegated tasks",
        model=model,
        system_prompt=WORKER_SYSTEM_PROMPT,
        tools=tools,
    )


root_agent = create_agent()

if __name__ == "__main__":
    agent = create_agent()
    print(f"✓ Agent: {agent.name}")
    print(f"✓ Model: {agent.model}")
    print("✓ Worker Agent ready for delegated tasks")

    try:
        response = agent("Hello! I am ready to work on tasks.")
        print(f"\nAgent Response: {response}")
    except Exception as e:
        print(f"Error: {e}")
