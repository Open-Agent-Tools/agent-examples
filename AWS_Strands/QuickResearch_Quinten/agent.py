"""
Quick Research Quinten Agent - Minimal Implementation

Provides atomic tools and lets the agent decide how to use them.
"""

import os
from pathlib import Path
from strands import Agent
from strands.models.anthropic import AnthropicModel

# Load .env file
try:
    from dotenv import load_dotenv
    for i in range(4):
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


def create_agent() -> Agent:
    """Create Quick Research Quinten agent with atomic tools."""
    
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
    
    # # Import tools
    # try:
    #     from .tools import ...
    # except ImportError:
    #     from tools import ...
    
    # Create agent with atomic tools
    return Agent(
        name="Quick Research Quinten",
        description="Research agent with URL generation and web crawling tools",
        model=model,
        system_prompt=SYSTEM_PROMPT,
        tools=[

        ]
    )


# Module-level agent
root_agent = create_agent()

if __name__ == "__main__":
    agent = create_agent()
    print(f"✓ Agent: {agent.name}")
    print(f"✓ Model: {agent.model}")
    
    # Test a simple tool
    from tools import get_search_urls
    urls = get_search_urls("test query", ["google", "wikipedia"])
    print(f"✓ Generated {len(urls)} search URLs")