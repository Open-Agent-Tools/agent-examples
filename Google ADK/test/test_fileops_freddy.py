"""
Test script for FileOps_Freddy agent.

This script demonstrates that the FileOps_Freddy agent can be loaded
and responds to messages.
"""

import sys
import os
import pytest

from FileOps_Freddy.agent import root_agent

def test_fileops_freddy():
    """Test that FileOps_Freddy agent can be loaded and responds to messages."""
    # Initialize the FileOps_Freddy agent
    agent = root_agent

    # Example: List directory contents
    # Using run_live method based on available methods
    response = agent.run_live("List all files in the current directory")
    # Assert that the response exists and is not empty
    assert response is not None, "Response should not be None"
    assert str(response).strip() != "", "Response should not be empty"

    # Example: Create a new file
    response = agent.run_live("Create a new file called 'test.txt' with the content 'Hello World'")
    # Assert that the response exists and is not empty
    assert response is not None, "Response should not be None"
    assert str(response).strip() != "", "Response should not be empty"

    # Example: Remove the created file
    response = agent.run_live("Delete the file 'test.txt'")
    # Assert that the response exists and is not empty
    assert response is not None, "Response should not be None"
    assert str(response).strip() != "", "Response should not be empty"
