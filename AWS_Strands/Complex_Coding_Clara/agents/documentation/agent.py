"""
Documentation Agent - Documentation generation specialist
"""

import os
import time
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
    from .prompt import DOCUMENTATION_SYSTEM_PROMPT
except ImportError:
    from prompt import DOCUMENTATION_SYSTEM_PROMPT

# Import tools
strands_tools = []
try:
    from strands_tools import file_read, file_write, editor, shell, current_time

    strands_tools = [file_read, file_write, editor, shell, current_time]
except ImportError:
    pass

boat_tools = []
try:
    import basic_open_agent_tools as boat

    # Add filesystem tools for documentation organization
    file_tools = boat.load_all_filesystem_tools()

    # Add text tools for documentation formatting
    text_tools = boat.load_all_text_tools()

    # Add data tools for doc templates (JSON, YAML, Markdown metadata)
    data_tools = [
        boat.data.safe_json_serialize,
        boat.data.safe_json_deserialize,
        boat.data.read_yaml_file,
        boat.data.write_yaml_file,
    ]

    boat_tools = file_tools + text_tools + data_tools
except ImportError:
    pass

# Build tool list
try:
    tools = strands_tools + boat_tools
except Exception:
    tools = []


# Create the Bedrock model for Documentation Agent
# Using Nova Lite for cost-effective documentation generation
model = BedrockModel(
    model_id="us.amazon.nova-lite-v1:0",  # Nova Lite (inference profile)
    region_name=os.getenv("AWS_REGION", "us-east-1"),
    max_tokens=8192,  # Increased to Nova Lite limit for comprehensive docs
    temperature=0.4,  # Slightly higher for creative documentation
)


def create_documentation_agent() -> Agent:
    """Create the Documentation agent."""
    return Agent(
        name="Documentation Agent",
        description="Docstring generation, README creation, and API documentation",
        model=model,
        system_prompt=DOCUMENTATION_SYSTEM_PROMPT,
        tools=tools,
        callback_handler=None,  # Suppress intermediate output
    )


# Create the agent instance
_documentation_agent = create_documentation_agent()


@tool
def documentation(task: str) -> str:
    """
    Delegate documentation tasks to the Documentation specialist.

    Use this for:
    - Docstring generation
    - README creation & updates
    - API documentation
    - Code comments
    - User guides
    - Technical specifications

    Args:
        task: Description of what needs to be documented (include code or file paths)

    Returns:
        Complete documentation in appropriate format (Markdown, docstring, etc.)
    """
    max_retries = 3
    retry_delay = 2  # seconds (longer for potential timeout issues)

    for attempt in range(max_retries):
        try:
            result = _documentation_agent(task)
            return str(result)
        except Exception as e:
            error_msg = str(e)

            # Check for configuration errors (don't retry)
            if "ValidationException" in error_msg or "model ID" in error_msg.lower():
                return f"Documentation Agent configuration error: {error_msg}. Please check model configuration."

            # Check for timeout errors
            if (
                "timeout" in error_msg.lower()
                or "prematurely" in error_msg.lower()
                or "ReadTimeoutError" in error_msg
            ):
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                    continue
                return f"Documentation Agent timeout error after {max_retries} attempts: {error_msg}. Try with a shorter task or simpler documentation request."

            # Retry for other transient errors
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
                continue

            # Final attempt failed
            return (
                f"Documentation Agent error after {max_retries} attempts: {error_msg}"
            )

    return "Documentation Agent error: Maximum retries exceeded"


# Export for direct use
__all__ = ["documentation", "create_documentation_agent"]
