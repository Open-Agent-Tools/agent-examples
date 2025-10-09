"""
Data Science Specialist Agent - Machine learning and data analysis expert
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
    from .prompt import DATA_SCIENCE_SPECIALIST_SYSTEM_PROMPT
except ImportError:
    from prompt import DATA_SCIENCE_SPECIALIST_SYSTEM_PROMPT

# Import tools
strands_tools = []
try:
    from strands_tools import (
        file_read,
        file_write,
        editor,
        python_repl,
        shell,
        current_time,
    )

    strands_tools = [file_read, file_write, editor, python_repl, shell, current_time]
except ImportError:
    pass

boat_tools = []
try:
    import basic_open_agent_tools as boat

    # Add all data tools for ML pipelines (CSV, JSON, YAML, validation)
    data_tools = boat.load_all_data_tools()

    # Add filesystem tools for organizing ML projects
    file_tools = boat.load_all_filesystem_tools()

    # Add archive tools for dataset compression/extraction
    archive_tools = boat.load_all_archive_tools()

    # Add crypto tools for dataset hashing and checksum verification
    crypto_tools = [
        boat.crypto.hash_sha256,
        boat.crypto.hash_md5,
        boat.crypto.verify_checksum,
    ]

    # Add datetime tools for time series analysis
    datetime_tools = [
        boat.datetime.get_date_range,
        boat.datetime.calculate_days_between,
        boat.datetime.get_business_days_in_range,
        boat.datetime.is_business_day,
    ]

    boat_tools = file_tools + data_tools + archive_tools + crypto_tools + datetime_tools
except ImportError:
    pass

# Build tool list
try:
    tools = strands_tools + boat_tools
except Exception:
    tools = []


# Create the Bedrock model for Data Science Specialist
# Using Nova Pro (cost optimized - good for ML templates)
model = BedrockModel(
    model_id="us.amazon.nova-pro-v1:0",  # Amazon Nova Pro (inference profile)
    region_name=os.getenv("AWS_REGION", "us-east-1"),
    max_tokens=5120,  # Increased to Nova Pro limit for comprehensive ML pipelines
    temperature=0.2,  # Lower for data science precision
)


def create_data_science_specialist_agent() -> Agent:
    """Create the Data Science Specialist agent."""
    return Agent(
        name="Data Science Specialist",
        description="ML expert: data preprocessing, model training, evaluation, MLOps",
        model=model,
        system_prompt=DATA_SCIENCE_SPECIALIST_SYSTEM_PROMPT,
        tools=tools,
        callback_handler=None,
    )


# Create the agent instance
_data_science_specialist_agent = create_data_science_specialist_agent()


@tool
def data_science_specialist(task: str) -> str:
    """
    Delegate data science tasks to the Data Science Specialist.

    Use this for:
    - Data preprocessing and feature engineering
    - Model selection and training
    - Hyperparameter tuning
    - Model evaluation and metrics
    - Deep learning (PyTorch, TensorFlow)
    - MLOps and experiment tracking

    Args:
        task: Detailed description of the data science task

    Returns:
        Complete ML pipeline with preprocessing, training, and evaluation
    """
    try:
        result = _data_science_specialist_agent(task)
        return str(result)
    except Exception as e:
        return f"Data Science Specialist error: {str(e)}"


# Export for direct use
__all__ = ["data_science_specialist", "create_data_science_specialist_agent"]
