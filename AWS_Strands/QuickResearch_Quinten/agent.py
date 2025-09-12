"""
Quick Research Quinten Agent - Minimal Implementation

Provides atomic tools and lets the agent decide how to use them.
"""

import os
from pathlib import Path
from strands import Agent
from strands.models.anthropic import AnthropicModel

# Load .env file - search current directory and up to 3 parent folders
try:
    from dotenv import load_dotenv
    
    # Start with current file directory
    current_path = Path(__file__).parent
    env_path = current_path / ".env"
    if env_path.exists():
        load_dotenv(env_path)
    else:
        # Search up to 3 parent directories safely
        for i in range(min(3, len(Path(__file__).parents))):
            env_path = Path(__file__).parents[i] / ".env"
            if env_path.exists():
                load_dotenv(env_path)
                break
except ImportError:
    pass

try:
    from .prompts import SYSTEM_PROMPT
except ImportError:
    from prompts import SYSTEM_PROMPT

try:
    from .tools import generate_search_url, process_web_content, extract_urls_from_content, extract_contact_info
except ImportError:
    from tools import generate_search_url, process_web_content, extract_urls_from_content, extract_contact_info

# Import strands_tools
try:
    from strands_tools.file_read import file_read
    from strands_tools.file_write import file_write
    from strands_tools.current_time import current_time
    tools = [file_read, file_write, current_time, generate_search_url, process_web_content, extract_urls_from_content, extract_contact_info]
except ImportError:
    # Fallback without strands_tools
    tools = [generate_search_url, process_web_content, extract_urls_from_content, extract_contact_info]

# Create the Anthropic model
model = AnthropicModel(
    client_args={
        "api_key": os.getenv("ANTHROPIC_API_KEY"),
    },
    model_id="claude-3-5-sonnet-20241022",
    max_tokens=4096,
    params={
        "temperature": 0.1,
    }
)

def create_agent() -> Agent:
    """Create Quick Research Quinten agent with atomic tools."""
    return Agent(
        name="Quick Research Quinten",
        description="Research agent with URL generation, web fetching, and file management tools",
        model=model,
        system_prompt=SYSTEM_PROMPT,
        tools=tools
    )


# Module-level agent
root_agent = create_agent()

if __name__ == "__main__":
    agent = create_agent()
    print(f"✓ Agent: {agent.name}")
    print(f"✓ Model: {agent.model}")
    
    # Agent ready for tool integration
    print("✓ Agent ready for tool integration")