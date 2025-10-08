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
    from strands_tools import file_read, file_write, editor, shell, current_time

    strands_tools = [file_read, file_write, editor, shell, current_time]
except ImportError:
    pass

boat_tools = []
try:
    import basic_open_agent_tools as boat

    file_tools = boat.load_all_filesystem_tools()
    boat_tools = file_tools
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
    max_tokens=8192,
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
