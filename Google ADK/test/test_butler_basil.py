"""
Test script for Butler_Basil agent.

This script demonstrates that the Butler_Basil agent can be loaded
and responds to messages.
"""

import sys
import os
import pytest


from Butler_Basil.agent import root_agent

def test_butler_basil():
    """Test that Butler_Basil agent can be loaded and responds to messages."""
    # Initialize the Butler_Basil agent
    agent = root_agent

    # Example: Get help with a task
    response = agent.run_live("I need help organizing my project files")
    # Assert that the response exists and is not empty
    assert response is not None, "Response should not be None"
    assert str(response).strip() != "", "Response should not be empty"

    # Example: Ask for information
    response = agent.run_live("What are some best practices for code documentation?")
    # Assert that the response exists and is not empty
    assert response is not None, "Response should not be None"
    assert str(response).strip() != "", "Response should not be empty"
