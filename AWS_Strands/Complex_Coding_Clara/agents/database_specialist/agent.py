"""
Database Specialist Agent - Database design and optimization expert
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
    from .prompt import DATABASE_SPECIALIST_SYSTEM_PROMPT
except ImportError:
    from prompt import DATABASE_SPECIALIST_SYSTEM_PROMPT

# Import tools
strands_tools = []
try:
    from strands_tools import (
        file_read,
        file_write,
        editor,
        shell,
        python_repl,
        current_time,
    )

    strands_tools = [file_read, file_write, editor, shell, python_repl, current_time]
except ImportError:
    pass

boat_tools = []
try:
    import basic_open_agent_tools as boat

    # Add filesystem tools
    file_tools = boat.load_all_filesystem_tools()

    # Add all data tools for schema/config management (SQL, JSON, YAML, CSV)
    data_tools = boat.load_all_data_tools()

    # Add text tools for SQL formatting and naming conventions
    text_tools = [
        boat.text.clean_whitespace,
        boat.text.normalize_line_endings,
        boat.text.to_snake_case,
    ]

    # Add crypto tools for connection string hashing, checksums
    crypto_tools = [
        boat.crypto.hash_sha256,
        boat.crypto.generate_uuid,
    ]

    boat_tools = file_tools + data_tools + text_tools + crypto_tools
except ImportError:
    pass

# Build tool list
try:
    tools = strands_tools + boat_tools
except Exception:
    tools = []


# Create the Bedrock model for Database Specialist
# Using Claude Haiku 3.5 (cost optimized - good for query patterns)
model = BedrockModel(
    model_id="us.anthropic.claude-3-5-haiku-20241022-v1:0",  # Claude Haiku 3.5 (inference profile)
    region_name=os.getenv("AWS_REGION", "us-east-1"),
    max_tokens=16384,  # Increased to Haiku limit for comprehensive schemas
    temperature=0.2,  # Lower for precise database work
)


def create_database_specialist_agent() -> Agent:
    """Create the Database Specialist agent."""
    return Agent(
        name="Database Specialist",
        description="Database expert: schema design, query optimization, SQL/NoSQL",
        model=model,
        system_prompt=DATABASE_SPECIALIST_SYSTEM_PROMPT,
        tools=tools,
        callback_handler=None,
    )


# Create the agent instance
_database_specialist_agent = create_database_specialist_agent()


@tool
def database_specialist(task: str) -> str:
    """
    Delegate database tasks to the Database Specialist.

    Use this for:
    - Schema design and normalization
    - Query optimization with EXPLAIN
    - Index strategy
    - SQL and NoSQL patterns
    - Migration scripts
    - Performance tuning

    Args:
        task: Detailed description of the database task

    Returns:
        Optimized database schemas, queries, and migration scripts
    """
    try:
        result = _database_specialist_agent(task)
        return str(result)
    except Exception as e:
        return f"Database Specialist error: {str(e)}"


# Export for direct use
__all__ = ["database_specialist", "create_database_specialist_agent"]
