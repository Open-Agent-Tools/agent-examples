"""ADK evaluation tests for Stocks Sarah agent.

This test suite validates that Stocks Sarah's tools work correctly
when called by AI agents in the Google ADK framework.
"""

import asyncio

import pytest
from google.adk.evaluation.agent_evaluator import AgentEvaluator


class TestStocksSarahAgentEvaluation:
    """Agent evaluation tests for Stocks Sarah."""

    @pytest.mark.agent_evaluation
    @pytest.mark.asyncio
    async def test_list_available_tools_agent(self):
        """Test agent listing available tools."""
        await AgentEvaluator.evaluate(
            agent_module="GoogleADK.Stocks_Sarah",
            eval_dataset_file_path_or_dir="GoogleADK/Stocks_Sarah/evals/list_available_tools_test.json",
        )
        await asyncio.sleep(2)  # Rate limiting delay
