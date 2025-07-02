"""ADK evaluation tests for FileOps Freddy agent.

This test suite validates that FileOps Freddy's tools work correctly
when called by AI agents in the Google ADK framework.
"""

import asyncio

import pytest
from google.adk.evaluation.agent_evaluator import AgentEvaluator


class TestFileOpsFrEddyAgentEvaluation:
    """Agent evaluation tests for FileOps Freddy."""

    @pytest.mark.agent_evaluation
    @pytest.mark.asyncio
    async def test_list_available_tools_agent(self):
        """Test agent listing available tools."""
        await AgentEvaluator.evaluate(
            agent_module="GoogleADK.FileOps_Freddy",
            eval_dataset_file_path_or_dir="GoogleADK/FileOps_Freddy/evals/list_available_tools_test.json",
        )
        await asyncio.sleep(2)  # Rate limiting delay
