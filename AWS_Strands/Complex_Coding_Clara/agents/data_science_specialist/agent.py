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

    csv_tools = [
        boat.data.read_csv_simple,
        boat.data.write_csv_simple,
        boat.data.csv_to_dict_list,
    ]
    file_tools = boat.load_all_filesystem_tools()
    boat_tools = csv_tools + file_tools
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
    max_tokens=8192,
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
