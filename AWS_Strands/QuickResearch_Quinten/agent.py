"""
Quick Research Quinten Agent - Minimal Implementation

Provides atomic tools and lets the agent decide how to use them.
"""

import os
from pathlib import Path
from strands import Agent
from strands.models.anthropic import AnthropicModel

try:
    from dotenv import load_dotenv

    env_loaded = False
    for i in range(3):
        env_path = Path(__file__).parents[i] / ".env"
        if env_path.exists():
            load_dotenv(env_path, override=False)
            env_loaded = True
            break

    if not env_loaded:
        load_dotenv(override=False)
except ImportError:
    pass

try:
    from .prompts import SYSTEM_PROMPT
except ImportError:
    from prompts import SYSTEM_PROMPT

try:
    from .tools import (
        generate_search_url,
        process_web_content,
        extract_urls_from_content,
        extract_contact_info,
    )
except ImportError:
    from tools import (
        generate_search_url,
        process_web_content,
        extract_urls_from_content,
        extract_contact_info,
    )

try:
    from strands_tools.file_read import file_read
    from strands_tools.file_write import file_write
    from strands_tools.current_time import current_time

    tools = [
        file_read,
        file_write,
        current_time,
        generate_search_url,
        process_web_content,
        extract_urls_from_content,
        extract_contact_info,
    ]
except ImportError:
    tools = [
        generate_search_url,
        process_web_content,
        extract_urls_from_content,
        extract_contact_info,
    ]

model = AnthropicModel(
    client_args={
        "api_key": os.getenv("ANTHROPIC_API_KEY"),
    },
    model_id="claude-3-5-sonnet-20241022",
    max_tokens=4096,
    params={
        "temperature": 0.1,
    },
)


def create_agent() -> Agent:
    """Create Quick Research Quinten agent with atomic tools."""
    return Agent(
        name="Quick Research Quinten",
        description="Research agent with URL generation, web fetching, and file management tools",
        model=model,
        system_prompt=SYSTEM_PROMPT,
        tools=tools,
    )


root_agent = create_agent()

if __name__ == "__main__":
    agent = create_agent()
    print(f"✓ Agent: {agent.name}")
    print(f"✓ Model: {agent.model}")

    print("✓ Agent ready for tool integration")
