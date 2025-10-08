"""
Complex Coding Clara - Meta Orchestrator Agent

A sophisticated multi-agent coding system that coordinates specialist agents
for coding, testing, and code review tasks.
"""

import os
from pathlib import Path
from strands import Agent
from strands.models.bedrock import BedrockModel

# Load environment - search up to 3 parent folders for root .env
try:
    from dotenv import load_dotenv

    # Search up to 3 levels up (to find root .env)
    env_loaded = False
    for i in range(3):
        env_path = Path(__file__).parents[i] / ".env"
        if env_path.exists():
            load_dotenv(env_path, override=False)  # Don't override if already set
            env_loaded = True
            break

    if not env_loaded:
        load_dotenv(override=False)  # Try default location
except ImportError:
    pass

# Import prompts
try:
    from .prompts import ORCHESTRATOR_SYSTEM_PROMPT
except ImportError:
    from prompts import ORCHESTRATOR_SYSTEM_PROMPT

# Import specialist agents
try:
    from .agents import (
        architect,
        senior_coder,
        fast_coder,
        test_engineer,
        code_reviewer,
        debug,
        documentation,
        python_specialist,
        web_specialist,
        database_specialist,
        devops_specialist,
        data_science_specialist,
        agile_specialist,
        doc_research_specialist,
    )
except ImportError:
    from agents import (
        architect,
        senior_coder,
        fast_coder,
        test_engineer,
        code_reviewer,
        debug,
        documentation,
        python_specialist,
        web_specialist,
        database_specialist,
        devops_specialist,
        data_science_specialist,
        agile_specialist,
        doc_research_specialist,
    )


# Create the Bedrock model for Clara (orchestrator)
model = BedrockModel(
    model_id="us.anthropic.claude-sonnet-4-5-20250929-v1:0",  # Claude Sonnet 4.5 (inference profile)
    region_name=os.getenv("AWS_REGION", "us-east-1"),
    max_tokens=16384,  # Higher for orchestration
    temperature=0.3,  # Moderate for planning and coordination
)


def create_agent() -> Agent:
    """
    Create the Complex Coding Clara orchestrator agent.

    Returns:
        Agent configured with specialist agents as tools
    """
    return Agent(
        name="Complex Coding Clara",
        description="Meta-orchestrator for multi-agent coding system with 14 specialized agents for architecture, coding, testing, review, debugging, documentation, domain expertise, and SDLC processes",
        model=model,
        system_prompt=ORCHESTRATOR_SYSTEM_PROMPT,
        tools=[
            # General coding agents
            architect,
            senior_coder,
            fast_coder,
            test_engineer,
            code_reviewer,
            debug,
            documentation,
            # Domain/language specialists
            python_specialist,
            web_specialist,
            database_specialist,
            devops_specialist,
            data_science_specialist,
            # SDLC process specialists
            agile_specialist,
            doc_research_specialist,
        ],
    )


# Create the root agent
root_agent = create_agent()


# Simple test function for local execution
def main():
    """Test function to verify Clara works."""
    print("=" * 60)
    print("Complex Coding Clara - Multi-Agent Coding System")
    print("=" * 60)
    print()
    print("Available Specialist Agents (14 total):")
    print()
    print("General Coding:")
    print("  • Architect: System design & architecture")
    print("  • Senior Coder: Complex algorithms & advanced coding")
    print("  • Fast Coder: CRUD operations & boilerplate")
    print("  • Test Engineer: Test generation & coverage")
    print("  • Code Reviewer: Code quality & best practices")
    print("  • Debug: Error analysis & bug fixing")
    print("  • Documentation: Docstrings & documentation")
    print()
    print("Domain/Language Specialists:")
    print("  • Python Specialist: Python idioms, PEP standards, type hints")
    print("  • Web Specialist: React, TypeScript, modern frontend")
    print("  • Database Specialist: SQL/NoSQL, schema design, optimization")
    print("  • DevOps Specialist: Docker, Kubernetes, CI/CD, IaC")
    print("  • Data Science Specialist: ML, data preprocessing, model training")
    print()
    print("SDLC Process Specialists:")
    print("  • Agile Specialist: User stories, epics, sprint planning, Scrum")
    print("  • Doc Research Specialist: Technical documentation research")
    print()
    print("Testing Clara with a simple query...")
    print("-" * 60)

    try:
        response = root_agent(
            "Hello! Please explain what you can help me with as a coding assistant."
        )
        print(f"\nClara's Response:\n{response}")
        print("-" * 60)
        print("\n✅ Clara is operational!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
