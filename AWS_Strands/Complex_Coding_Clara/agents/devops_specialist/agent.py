"""
DevOps Specialist Agent - Infrastructure and deployment expert
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
    from .prompt import DEVOPS_SPECIALIST_SYSTEM_PROMPT
except ImportError:
    from prompt import DEVOPS_SPECIALIST_SYSTEM_PROMPT

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


# Create the Bedrock model for DevOps Specialist
model = BedrockModel(
    model_id="us.amazon.nova-pro-v1:0",  # Nova Pro - cost-effective for infra
    region_name=os.getenv("AWS_REGION", "us-east-1"),
    max_tokens=8192,
    temperature=0.2,  # Lower for infrastructure code
)


def create_devops_specialist_agent() -> Agent:
    """Create the DevOps Specialist agent."""
    return Agent(
        name="DevOps Specialist",
        description="Infrastructure expert: Docker, Kubernetes, CI/CD, IaC",
        model=model,
        system_prompt=DEVOPS_SPECIALIST_SYSTEM_PROMPT,
        tools=tools,
        callback_handler=None,
    )


# Create the agent instance
_devops_specialist_agent = create_devops_specialist_agent()


@tool
def devops_specialist(task: str) -> str:
    """
    Delegate DevOps tasks to the DevOps Specialist.

    Use this for:
    - Docker and containerization
    - Kubernetes deployments
    - CI/CD pipelines (GitHub Actions, GitLab CI)
    - Infrastructure as Code (Terraform, CloudFormation)
    - Monitoring and observability
    - Security and compliance

    Args:
        task: Detailed description of the DevOps task

    Returns:
        Production-ready infrastructure code and configurations
    """
    try:
        result = _devops_specialist_agent(task)
        return str(result)
    except Exception as e:
        return f"DevOps Specialist error: {str(e)}"


# Export for direct use
__all__ = ["devops_specialist", "create_devops_specialist_agent"]
