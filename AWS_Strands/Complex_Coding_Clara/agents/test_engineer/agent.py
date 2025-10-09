"""
Test Engineer Agent - Test generation and quality assurance specialist
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
    from .prompt import TEST_ENGINEER_SYSTEM_PROMPT
except ImportError:
    from prompt import TEST_ENGINEER_SYSTEM_PROMPT

# Import tools
strands_tools = []
try:
    from strands_tools import file_read, file_write, python_repl, shell, current_time

    strands_tools = [file_read, file_write, python_repl, shell, current_time]
except ImportError:
    pass

boat_tools = []
try:
    import basic_open_agent_tools as boat

    # Add all data tools for test data/configs (CSV, JSON, YAML)
    data_tools = boat.load_all_data_tools()

    # Add filesystem tools
    file_tools = boat.load_all_filesystem_tools()

    # Add text tools for test formatting
    text_tools = [
        boat.text.to_snake_case,
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


# Create the Bedrock model for Test Engineer
# Using Llama 3.3 70B as specified in architecture, with fallback to Sonnet
model = BedrockModel(
    model_id="us.meta.llama3-3-70b-instruct-v1:0",  # Llama 3.3 70B (inference profile)
    region_name=os.getenv("AWS_REGION", "us-east-1"),
    max_tokens=8192,  # Increased to Llama limit for comprehensive test suites
    temperature=0.3,  # Moderate for test generation
)


def create_test_engineer_agent() -> Agent:
    """Create the Test Engineer agent."""
    return Agent(
        name="Test Engineer",
        description="Unit and integration test generation with high coverage",
        model=model,
        system_prompt=TEST_ENGINEER_SYSTEM_PROMPT,
        tools=tools,
        callback_handler=None,  # Suppress intermediate output
    )


# Create the agent instance
_test_engineer_agent = create_test_engineer_agent()


@tool
def test_engineer(task: str) -> str:
    """
    Delegate test generation tasks to the Test Engineer specialist.

    Use this for:
    - Unit test generation
    - Integration test scaffolding
    - Test case design & coverage
    - Edge case identification

    Args:
        task: Description of what needs to be tested (include code or file path)

    Returns:
        Comprehensive test suite with multiple test cases
    """
    max_retries = 3
    retry_delay = 1  # seconds

    for attempt in range(max_retries):
        try:
            result = _test_engineer_agent(task)
            return str(result)
        except Exception as e:
            error_msg = str(e)

            # Check for configuration errors (don't retry)
            if "ValidationException" in error_msg or "model ID" in error_msg.lower():
                return f"Test Engineer configuration error: {error_msg}. Please check model configuration."

            # Retry for transient errors
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
                continue

            # Final attempt failed
            return f"Test Engineer error after {max_retries} attempts: {error_msg}"

    return "Test Engineer error: Maximum retries exceeded"


# Export for direct use
__all__ = ["test_engineer", "create_test_engineer_agent"]
