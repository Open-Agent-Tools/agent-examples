# ADK Testing and Evaluations Guide

This guide documents the agent evaluation testing approach for Google ADK agents in this repository. The evaluation tests validate that agents work correctly when called by AI models in the Google ADK framework.

## Overview

Each agent has its own `evals/` directory containing evaluation tests that focus on verifying basic agent functionality, particularly the ability to list available tools. This approach follows the simplified pattern proven to work reliably with Google ADK evaluation framework.

## Directory Structure

```
GoogleADK/
   {Agent_Name}/
      agent.py              # Main agent implementation
      prompts.py            # Agent prompts
      __init__.py           # Package initialization
      evals/                # Agent-specific evaluations
          test_config.json                          # ADK evaluation criteria
          list_available_tools.test.json            # Tool listing test case
          test_{agent_name}_agent_evaluation.py     # Test runner
```

## Implementation Steps

### 1. Create the evals Directory

Create an `evals/` folder inside each agent directory:

```bash
mkdir -p GoogleADK/{Agent_Name}/evals
```

### 2. Create test_config.json

This file defines the evaluation criteria with scoring thresholds:

```json
{
  "criteria": {
    "tool_trajectory_avg_score": 0.5,
    "response_match_score": 0.5
  }
}
```

- `tool_trajectory_avg_score`: Measures correct tool usage (0.5 = 50% threshold)
- `response_match_score`: Measures response similarity to expected output (0.5 = 50% threshold)

### 3. Create list_available_tools.test.json

This file contains the test case for listing available tools. Update the expected response to match your agent's actual tools:

```json
{
  "eval_set_id": "list_available_tools_test_set",
  "name": "List Available Tools Test",
  "description": "Test case for listing available tools through agent interaction",
  "eval_cases": [
    {
      "eval_id": "list_available_tools_test",
      "conversation": [
        {
          "invocation_id": "list-tools-001",
          "user_content": {
            "parts": [
              {
                "text": "List all available tools alphabetically. Do not try to run them though. Just list the names."
              }
            ],
            "role": "user"
          },
          "final_response": {
            "parts": [
              {
                "text": "YOUR_EXPECTED_RESPONSE_HERE"
              }
            ],
            "role": "model"
          },
          "intermediate_data": {
            "tool_uses": [],
            "intermediate_responses": []
          }
        }
      ],
      "session_input": {
        "app_name": "{agent_name}_agent",
        "user_id": "test_user",
        "state": {}
      }
    }
  ]
}
```

### 4. Create test_{agent_name}_agent_evaluation.py

This is the pytest runner for agent evaluations:

```python
"""ADK evaluation tests for {Agent Name} agent.

This test suite validates that {Agent Name}'s tools work correctly
when called by AI agents in the Google ADK framework.
"""

import asyncio

import pytest
from google.adk.evaluation.agent_evaluator import AgentEvaluator


class Test{AgentName}AgentEvaluation:
    """Agent evaluation tests for {Agent Name}."""

    @pytest.mark.agent_evaluation
    @pytest.mark.asyncio
    async def test_list_available_tools_agent(self):
        """Test agent listing available tools."""
        await AgentEvaluator.evaluate(
            agent_module="GoogleADK.{Agent_Name}",
            eval_dataset_file_path_or_dir="GoogleADK/{Agent_Name}/evals/list_available_tools_test.json",
        )
        await asyncio.sleep(2)  # Rate limiting delay
```

### 5. Update Agent's __init__.py

Ensure your agent module exports correctly for ADK evaluation. The __init__.py should include:

```python
# Expose the root agent and create_agent function at the package level
from .agent import root_agent, create_agent
from . import agent

__all__ = ["root_agent", "create_agent", "agent"]
```

The `from . import agent` line is crucial - ADK looks for an `agent` attribute in the module.

## Running Evaluations

### Manual Evaluation (Single Agent)

Run evaluation for a specific agent using the ADK CLI:

```bash
PYTHONPATH=.:$PYTHONPATH adk eval \
  --config_file_path GoogleADK/{Agent_Name}/evals/test_config.json \
  --print_detailed_results \
  GoogleADK/{Agent_Name} \
  GoogleADK/{Agent_Name}/evals/list_available_tools.test.json
```

### Automated Testing with pytest

Run all agent evaluation tests:

```bash
# All tests including agent evaluations (requires GOOGLE_API_KEY)
python3 -m pytest GoogleADK/ -v -m "agent_evaluation"

# Skip agent evaluations (no API key needed)
python3 -m pytest GoogleADK/ -v -m "not agent_evaluation"
```

## Example: Butler_Basil Implementation

Here's the complete implementation for Butler_Basil agent:

1. **Agent Setup** - The agent uses basic_open_agent_tools for filesystem operations:
   ```python
   agent_tools = boat.load_all_filesystem_tools()
   ```

2. **Expected Response** - The test expects the agent to list all filesystem tools alphabetically:
   ```
   create_directory
   copy_file
   delete_directory
   ...
   ```

3. **Running the Test**:
   ```bash
   PYTHONPATH=.:$PYTHONPATH adk eval \
     --config_file_path GoogleADK/Butler_Basil/evals/test_config.json \
     --print_detailed_results \
     GoogleADK/Butler_Basil \
     GoogleADK/Butler_Basil/evals/list_available_tools.test.json
   ```

## Troubleshooting

### Common Issues

1. **AttributeError: module 'agent' has no attribute 'agent'**
   - Ensure your agent's `__init__.py` includes `from . import agent`

2. **API Quota Exceeded**
   - Tests include 2-second delays between evaluations
   - Run tests sequentially, not in parallel
   - Free tier allows 15 requests/minute

3. **Response Match Score Too Low**
   - Update the expected response in `list_available_tools.test.json`
   - Agent responses can include greetings/formatting - adjust expectations accordingly
   - The threshold is 0.5 (50%) so exact matches aren't required

4. **Import Errors**
   - Ensure `PYTHONPATH=.:$PYTHONPATH` is set when running evaluations
   - Check that all dependencies are installed

## Best Practices

1. **Focus on Tool Listing** - The most reliable evaluation pattern tests the agent's ability to list its available tools

2. **Update Expected Responses** - When agent tools change, update the expected response in test files

3. **Agent Instructions** - Be aware that agent prompts/instructions may affect responses (e.g., greetings, formatting)

4. **Sequential Execution** - Always run evaluations sequentially with delays to avoid API rate limits

5. **Environment Setup** - Ensure `GOOGLE_API_KEY` is set in your environment or `.env` file


