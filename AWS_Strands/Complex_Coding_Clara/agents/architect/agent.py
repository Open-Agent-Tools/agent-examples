"""
Architect Agent - System design and architecture specialist
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
    from .prompt import ARCHITECT_SYSTEM_PROMPT
except ImportError:
    from prompt import ARCHITECT_SYSTEM_PROMPT

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

    # Add filesystem tools for navigation
    file_tools = boat.load_all_filesystem_tools()

    # Add data tools for architecture schemas and config templates (JSON, YAML, TOML, validation)
    data_tools = [
        boat.data.safe_json_serialize,
        boat.data.safe_json_deserialize,
        boat.data.validate_json_string,
        boat.data.read_yaml_file,
        boat.data.write_yaml_file,
        boat.data.read_toml_file,
        boat.data.write_toml_file,
        boat.data.validate_schema_simple,
    ]

    # Add system tools for environment analysis and dependency inspection
    system_tools = [
        boat.system.get_system_info,
        boat.system.get_python_module_info,
        boat.system.get_file_system_context,
        boat.system.get_network_environment,
        boat.system.inspect_runtime_environment,
    ]

    # Add text tools for diagram formatting and naming conventions
    text_tools = [
        boat.text.clean_whitespace,
        boat.text.normalize_line_endings,
        boat.text.to_snake_case,
        boat.text.to_camel_case,
    ]

    # Add datetime tools for roadmap and milestone planning
    datetime_tools = [
        boat.datetime.get_quarter_dates,
        boat.datetime.get_month_range,
        boat.datetime.calculate_days_between,
        boat.datetime.get_date_range,
    ]

    boat_tools = file_tools + data_tools + system_tools + text_tools + datetime_tools
except ImportError:
    pass

# Build tool list
try:
    tools = strands_tools + boat_tools
except Exception:
    tools = []


# Create the Bedrock model for Architect
# Using Claude Sonnet 4.5 (cost optimized from Opus)
model = BedrockModel(
    model_id="us.anthropic.claude-sonnet-4-5-20250929-v1:0",  # Claude Sonnet 4.5 (inference profile)
    region_name=os.getenv("AWS_REGION", "us-east-1"),
    max_tokens=16384,  # Increased to model limit for comprehensive architecture documents
    temperature=0.2,  # Lower for architectural decisions
)


def create_architect_agent() -> Agent:
    """Create the Architect agent."""
    return Agent(
        name="Architect",
        description="System design, architecture patterns, and technology selection",
        model=model,
        system_prompt=ARCHITECT_SYSTEM_PROMPT,
        tools=tools,
        callback_handler=None,  # Suppress intermediate output
    )


# Create the agent instance
_architect_agent = create_architect_agent()


@tool
def architect(task: str) -> str:
    """
    Delegate architecture and design tasks to the Architect specialist.

    Use this for:
    - System design & architecture patterns
    - Technology stack selection
    - Database schema design
    - API design & service boundaries
    - Scalability planning
    - Critical architectural decisions

    Args:
        task: Detailed description of the architectural challenge

    Returns:
        Architecture design with diagrams, technology recommendations, and rationale
    """
    try:
        result = _architect_agent(task)
        return str(result)
    except Exception as e:
        return f"Architect error: {str(e)}"


# Export for direct use
__all__ = ["architect", "create_architect_agent"]
