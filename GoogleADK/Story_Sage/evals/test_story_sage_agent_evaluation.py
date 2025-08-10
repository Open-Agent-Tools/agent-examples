"""ADK evaluation tests for Story_Sage agent.

This test suite validates that Story_Sage's tools work correctly
when called by AI agents in the Google ADK framework.
"""

import asyncio

import pytest
from google.adk.evaluation.agent_evaluator import AgentEvaluator


class TestStorySageAgentEvaluation:
    """Agent evaluation tests for Story_Sage."""

    @pytest.mark.agent_evaluation
    @pytest.mark.asyncio
    async def test_list_available_tools_agent(self):
        """Test agent listing available tools."""
        await AgentEvaluator.evaluate(
            agent_module="GoogleADK.Story_Sage",
            eval_dataset_file_path_or_dir="GoogleADK/Story_Sage/evals/list_available_tools_test.json",
        )
        await asyncio.sleep(2)  # Rate limiting delay
