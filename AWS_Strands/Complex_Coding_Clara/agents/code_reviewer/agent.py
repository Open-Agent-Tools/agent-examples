"""
Code Reviewer Agent - Code quality, security, and best practices specialist
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
    from .prompt import CODE_REVIEWER_SYSTEM_PROMPT
except ImportError:
    from prompt import CODE_REVIEWER_SYSTEM_PROMPT

# Import tools
strands_tools = []
try:
    from strands_tools import file_read, shell, python_repl, current_time

    strands_tools = [file_read, shell, python_repl, current_time]
except ImportError:
    pass

boat_tools = []
try:
    import basic_open_agent_tools as boat

    # Add filesystem tools for navigation
    file_tools = boat.load_all_filesystem_tools()
    boat_tools = file_tools
except ImportError:
    pass

# Build tool list
try:
    tools = strands_tools + boat_tools
except Exception:
    tools = []


# Create the Bedrock model for Code Reviewer
# Using Nova Pro as specified, with Haiku fallback
model = BedrockModel(
    model_id="amazon.nova-pro-v1:0",  # Nova Pro
    region_name=os.getenv("AWS_REGION", "us-east-1"),
    max_tokens=4096,
    temperature=0.1,  # Very low for consistent reviews
)


def create_code_reviewer_agent() -> Agent:
    """Create the Code Reviewer agent."""
    return Agent(
        name="Code Reviewer",
        description="Code quality, security scanning, and best practice enforcement",
        model=model,
        system_prompt=CODE_REVIEWER_SYSTEM_PROMPT,
        tools=tools,
        callback_handler=None,  # Suppress intermediate output
    )


# Create the agent instance
_code_reviewer_agent = create_code_reviewer_agent()


@tool
def code_reviewer(task: str) -> str:
    """
    Delegate code review tasks to the Code Reviewer specialist.

    Use this for:
    - Style & convention checks
    - Logic & correctness review
    - Security vulnerability scanning
    - Best practice enforcement

    Args:
        task: What to review (code snippet, file path, or directory)

    Returns:
        Detailed review with ratings and actionable feedback
    """
    try:
        result = _code_reviewer_agent(task)
        return str(result)
    except Exception as e:
        return f"Code Reviewer error: {str(e)}"


# Export for direct use
__all__ = ["code_reviewer", "create_code_reviewer_agent"]
