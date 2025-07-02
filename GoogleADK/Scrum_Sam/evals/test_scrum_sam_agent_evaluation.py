"""ADK evaluation tests for Scrum Sam agent.

This test suite validates that Scrum Sam's tools work correctly
when called by AI agents in the Google ADK framework.
"""

import asyncio

import pytest
from google.adk.evaluation.agent_evaluator import AgentEvaluator


class TestScrumSamAgentEvaluation:
    """Agent evaluation tests for Scrum Sam."""

    @pytest.mark.agent_evaluation
    @pytest.mark.asyncio
    async def test_list_available_tools_agent(self):
        """Test agent listing available tools."""
        await AgentEvaluator.evaluate(
            agent_module="GoogleADK.Scrum_Sam",
            eval_dataset_file_path_or_dir="GoogleADK/Scrum_Sam/evals/list_available_tools_test.json",
        )
        await asyncio.sleep(2)  # Rate limiting delay
