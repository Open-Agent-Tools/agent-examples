"""
Simple Sam - LangChain Agent

A minimal LangChain agent demonstrating ReAct pattern with basic tools.
Uses modern LangChain patterns for 2025.
"""

import os
from pathlib import Path
from typing import Any, Dict

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

# Core LangChain imports
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import Tool
from langchain import hub

# Simple tools
def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"The weather in {city} is sunny and 72°F."

def calculate(expression: str) -> str:
    """Safely evaluate mathematical expressions."""
    try:
        # Only allow basic math operations for safety
        allowed_chars = "0123456789+-*/.() "
        if all(c in allowed_chars for c in expression):
            result = eval(expression)
            return f"The result of {expression} is {result}"
        else:
            return "Error: Only basic math operations are allowed."
    except Exception as e:
        return f"Error calculating {expression}: {str(e)}"

def get_time() -> str:
    """Get the current time."""
    from datetime import datetime
    return f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

# Define tools list
tools = [
    Tool(
        name="Weather",
        func=get_weather,
        description="Get weather information for a city. Input should be a city name."
    ),
    Tool(
        name="Calculator",
        func=calculate,
        description="Perform mathematical calculations. Input should be a mathematical expression."
    ),
    Tool(
        name="Time",
        func=get_time,
        description="Get the current date and time. No input required."
    )
]

def create_agent() -> AgentExecutor:
    """Create Simple Sam agent with basic tools."""

    # Initialize the language model
    llm = ChatOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-4.1-mini",
        temperature=0.3
    )

    # Get the ReAct prompt from hub
    prompt = hub.pull("hwchase17/react")

    # Create the agent
    agent = create_react_agent(llm, tools, prompt)

    # Create agent executor
    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=3
    )

# Module-level agent
root_agent = create_agent()

def run_agent(query: str) -> Dict[str, Any]:
    """Run the agent with a query."""
    try:
        return root_agent.invoke({"input": query})
    except Exception as e:
        return {"error": str(e), "input": query}

if __name__ == "__main__":
    agent = create_agent()
    print("✓ Simple Sam (LangChain) ready!")
    print("✓ Tools: Weather, Calculator, Time")
    print("✓ Model: GPT-4.1-mini")

    # Test interaction
    try:
        test_query = "What's the weather in San Francisco?"
        print(f"\nTest Query: {test_query}")
        response = agent.invoke({"input": test_query})
        print(f"Response: {response['output']}")
    except Exception as e:
        print(f"Error: {e}")