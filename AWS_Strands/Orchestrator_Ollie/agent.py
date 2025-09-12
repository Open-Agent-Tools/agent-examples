"""
Orchestrator Ollie Agent

A specialized agent for coordinating and orchestrating tasks across multiple systems,
agents, and workflows. Built with AWS Strands framework.
"""

import os
from pathlib import Path
from strands import Agent, tool
from strands.models.anthropic import AnthropicModel

# Load environment variables
try:
    from dotenv import load_dotenv
    
    # Search current directory and up to 3 parent folders for .env
    current_path = Path(__file__).parent
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

# Import prompts and tools
try:
    from .prompts import SYSTEM_PROMPT
except ImportError:
    from prompts import SYSTEM_PROMPT

# Import basic open agent tools for CSV and file operations
try:
    import basic_open_agent_tools as boat
    # Use the helper to merge tools lists
    tools = boat.helpers.merge_tool_lists(
        boat.load_all_data_tools(),              # 27 CSV/data tools
        boat.load_all_filesystem_tools()        # 18 file system tools
    )
except ImportError:
    # Fallback to strands_tools if basic-open-agent-tools not available
    try:
        from strands_tools.file_read import file_read
        from strands_tools.file_write import file_write
        from strands_tools.current_time import current_time
        tools = [file_read, file_write, current_time]
    except ImportError:
        tools = []

# Create the Anthropic model
model = AnthropicModel(
    client_args={
        "api_key": os.getenv("ANTHROPIC_API_KEY"),
    },
    model_id="claude-3-5-sonnet-20241022",
    max_tokens=8192,
    params={
        "temperature": 0.3,
    }
)

# Import the worker sub-agent
try:
    from .subagent import create_agent as create_worker_agent
except ImportError:
    from subagent import create_agent as create_worker_agent

# Define worker agent tool that uses the external worker agent
@tool
def worker_agent(task_data: str, instruction: str) -> str:
    """
    Delegate a task to a worker sub-agent.
    
    Args:
        task_data: Data for the worker to process
        instruction: Instructions for the worker
        
    Returns:
        Processed result from the worker
    """
    try:
        # Create a worker agent from the external module
        worker = create_worker_agent()
        
        task_prompt = f"""
{instruction}

Task data: {task_data}

Provide your response in a structured format.
"""
        
        result = worker(task_prompt)
        return str(result)
        
    except Exception as e:
        return f"Error in worker agent: {str(e)}"

def create_agent() -> Agent:
    """Create Orchestrator Ollie agent."""
    
    return Agent(
        name="Orchestrator Ollie",
        description="A specialized agent for coordinating and orchestrating tasks across multiple systems and workflows, including CSV processing with sub-agents",
        model=model,
        system_prompt=SYSTEM_PROMPT,
        tools=tools + [worker_agent]  # Include all basic-open-agent-tools + worker agent tool
    )

# Module-level agent
root_agent = create_agent()

if __name__ == "__main__":
    agent = create_agent()
    print(f"✓ Agent: {agent.name}")
    print(f"✓ Model: {agent.model}")
    print("✓ Orchestrator Ollie ready for task coordination and CSV processing")
    
    # Simple test
    try:
        response = agent("Hello! What can you help me orchestrate today?")
        print(f"\nAgent Response: {response}")
    except Exception as e:
        print(f"Error: {e}")