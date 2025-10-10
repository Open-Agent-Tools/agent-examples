# Simple Sam - LangChain Agent

A minimal LangChain agent demonstrating the ReAct pattern with basic tools. Designed as a 2025 starter example following modern LangChain best practices.

## Features

- **ReAct Pattern**: Uses reasoning and acting cycle with tools
- **Basic Tools**: Weather, Calculator, and Time utilities
- **Error Handling**: Graceful error handling and parsing
- **Modern LangChain**: Uses latest patterns and hub integration

## Tools Available

1. **Weather**: Get weather for any city
2. **Calculator**: Perform basic mathematical calculations
3. **Time**: Get current date and time

## Architecture

```
Simple Sam (LangChain Agent)
├── Language Model: GPT-4o-mini
├── Pattern: ReAct (Reasoning + Acting)
├── Prompt: hwchase17/react from LangChain Hub
└── Tools: [Weather, Calculator, Time]
```

## Usage

```python
from agent import create_agent

# Create agent
agent = create_agent()

# Run a query
response = agent.invoke({"input": "What's 25 * 4 and what's the weather in Boston?"})
print(response["output"])
```

## Example Interactions

```
User: "What's the weather in San Francisco?"
Agent: Uses Weather tool → "The weather in San Francisco is sunny and 72°F."

User: "Calculate 15 * 8 + 7"
Agent: Uses Calculator tool → "The result of 15 * 8 + 7 is 127"

User: "What time is it?"
Agent: Uses Time tool → "Current time: 2025-01-15 14:30:22"
```

## Requirements

- OpenAI API key in environment or `.env` file
- `langchain`, `langchain-openai`, `python-dotenv`

## Configuration

Set your OpenAI API key:
```bash
export OPENAI_API_KEY="your-key-here"
```

Or create a `.env` file:
```
OPENAI_API_KEY=your-key-here
```