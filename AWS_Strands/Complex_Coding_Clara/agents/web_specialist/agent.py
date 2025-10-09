"""
Web Specialist Agent - Modern frontend development expert
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
    from .prompt import WEB_SPECIALIST_SYSTEM_PROMPT
except ImportError:
    from prompt import WEB_SPECIALIST_SYSTEM_PROMPT

# Import tools
strands_tools = []
try:
    from strands_tools import (
        file_read,
        file_write,
        editor,
        shell,
        current_time,
        http_request,
    )

    strands_tools = [file_read, file_write, editor, shell, current_time, http_request]
except ImportError:
    pass

boat_tools = []
try:
    import basic_open_agent_tools as boat

    # Add filesystem tools
    file_tools = boat.load_all_filesystem_tools()

    # Add data tools for package.json, tsconfig.json, configs
    data_tools = [
        boat.data.safe_json_serialize,
        boat.data.safe_json_deserialize,
        boat.data.validate_json_string,
        boat.data.read_yaml_file,
        boat.data.write_yaml_file,
    ]

    # Add text tools for React/TypeScript formatting
    text_tools = [
        boat.text.to_camel_case,
        boat.text.to_snake_case,
        boat.text.clean_whitespace,
        boat.text.normalize_line_endings,
    ]

    boat_tools = file_tools + data_tools + text_tools
except ImportError:
    pass

# Build tool list
try:
    tools = strands_tools + boat_tools
except Exception:
    tools = []


# Create the Bedrock model for Web Specialist
# Using Claude Haiku 3.5 (cost optimized - good for React/TS patterns)
model = BedrockModel(
    model_id="us.anthropic.claude-3-5-haiku-20241022-v1:0",  # Claude Haiku 3.5 (inference profile)
    region_name=os.getenv("AWS_REGION", "us-east-1"),
    max_tokens=16384,  # Increased to Haiku limit for comprehensive components
    temperature=0.3,  # Moderate for web development
)


def create_web_specialist_agent() -> Agent:
    """Create the Web Specialist agent."""
    return Agent(
        name="Web Specialist",
        description="Modern frontend: React, TypeScript, performance, and accessibility",
        model=model,
        system_prompt=WEB_SPECIALIST_SYSTEM_PROMPT,
        tools=tools,
        callback_handler=None,
    )


# Create the agent instance
_web_specialist_agent = create_web_specialist_agent()


@tool
def web_specialist(task: str) -> str:
    """
    Delegate web development tasks to the Web Specialist.

    Use this for:
    - React components with TypeScript
    - Modern frontend architecture
    - Performance optimization (Core Web Vitals)
    - Accessibility (WCAG 2.1)
    - State management (Context, Zustand, Redux)
    - Build tools (Vite, Next.js, Remix)

    Args:
        task: Detailed description of the web development task

    Returns:
        Modern, accessible, performant React/TypeScript code
    """
    try:
        result = _web_specialist_agent(task)
        return str(result)
    except Exception as e:
        return f"Web Specialist error: {str(e)}"


# Export for direct use
__all__ = ["web_specialist", "create_web_specialist_agent"]
