"""ADK evaluation tests for Butler Basil agent.

This test suite validates that Butler Basil's tools work correctly
when called by AI agents in the Google ADK framework.
"""

import asyncio

import pytest
from google.adk.evaluation.agent_evaluator import AgentEvaluator


class TestButlerBasilAgentEvaluation:
    """Agent evaluation tests for Butler Basil."""

    @pytest.mark.agent_evaluation
    @pytest.mark.asyncio
    async def test_list_available_tools_agent(self, agent_evaluation_sequential):
        """Test agent listing available tools."""
        await AgentEvaluator.evaluate(
            agent_module="GoogleADK.Butler_Basil",
            eval_dataset_file_path_or_dir="GoogleADK/Butler_Basil/evals/list_available_tools.test.json",
        )
        await asyncio.sleep(2)  # Rate limiting delay