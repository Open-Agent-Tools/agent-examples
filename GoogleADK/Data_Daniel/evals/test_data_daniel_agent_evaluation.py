"""ADK evaluation tests for Data Daniel agent.

This test suite validates that Data Daniel's tools work correctly
when called by AI agents in the Google ADK framework.
"""

import asyncio

import pytest
from google.adk.evaluation.agent_evaluator import AgentEvaluator


class TestDataDanielAgentEvaluation:
    """Agent evaluation tests for Data Daniel."""

    @pytest.mark.agent_evaluation
    @pytest.mark.asyncio
    async def test_list_available_tools_agent(self):
        """Test agent listing available tools."""
        await AgentEvaluator.evaluate(
            agent_module="GoogleADK.Data_Daniel",
            eval_dataset_file_path_or_dir="GoogleADK/Data_Daniel/evals/list_available_tools_test.json",
        )
        await asyncio.sleep(2)  # Rate limiting delay
