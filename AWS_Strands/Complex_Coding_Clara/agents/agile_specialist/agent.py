"""
Agile Specialist Agent - Scrum and user story expert for SDLC
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
    from .prompt import AGILE_SPECIALIST_SYSTEM_PROMPT
except ImportError:
    from prompt import AGILE_SPECIALIST_SYSTEM_PROMPT

# Import tools
strands_tools = []
try:
    from strands_tools import file_read, file_write, shell, current_time

    strands_tools = [file_read, file_write, shell, current_time]
except ImportError:
    pass

boat_tools = []
try:
    import basic_open_agent_tools as boat

    # Add filesystem tools for templates/PRDs
    file_tools = boat.load_all_filesystem_tools()

    # Add data tools for structured story/epic management (JSON, YAML, CSV, validation)
    data_tools = boat.load_all_data_tools()

    # Add text tools for template formatting (case conversion, whitespace, Oxford comma)
    text_tools = boat.load_all_text_tools()

    # Add todo tools for sprint task management
    todo_tools = boat.load_all_todo_tools()

    boat_tools = file_tools + data_tools + text_tools + todo_tools
except ImportError:
    pass

# Build tool list
try:
    tools = strands_tools + boat_tools
except Exception:
    tools = []


# Create the Bedrock model for Agile Specialist
# Using Claude Haiku 3.5 (cost optimized - good for templates/stories)
model = BedrockModel(
    model_id="us.anthropic.claude-3-5-haiku-20241022-v1:0",  # Claude Haiku 3.5 (inference profile)
    region_name=os.getenv("AWS_REGION", "us-east-1"),
    max_tokens=8192,
    temperature=0.5,  # Moderate for creative story writing
)


def create_agile_specialist_agent() -> Agent:
    """Create the Agile Specialist agent."""
    return Agent(
        name="Agile Specialist",
        description="Scrum master: user stories, epics, sprint planning, INVEST/V.A.S.T.",
        model=model,
        system_prompt=AGILE_SPECIALIST_SYSTEM_PROMPT,
        tools=tools,
        callback_handler=None,
    )


# Create the agent instance
_agile_specialist_agent = create_agile_specialist_agent()


@tool
def agile_specialist(task: str) -> str:
    """
    Delegate Agile/Scrum tasks to the Agile Specialist.

    Use this for:
    - User story creation (INVEST criteria)
    - Epic definition (V.A.S.T. criteria)
    - Sprint planning and estimation
    - Backlog grooming and prioritization
    - Acceptance criteria generation
    - Agile ceremony facilitation

    Args:
        task: Detailed description of the Agile/Scrum task

    Returns:
        User stories, epics, or Agile process guidance following best practices
    """
    try:
        result = _agile_specialist_agent(task)
        return str(result)
    except Exception as e:
        return f"Agile Specialist error: {str(e)}"


# Export for direct use
__all__ = ["agile_specialist", "create_agile_specialist_agent"]
