"""
Strands Chat Loop - Interactive CLI for AWS Strands Agents

A feature-rich, configurable chat interface for interacting with AWS Strands agents.

Features:
- Command history with readline (↑↓ to navigate)
- Multi-line input support (type \\ to start)
- Token tracking and cost estimation
- Prompt templates (~/.prompts/)
- Configuration file support (~/.chatrc)
- Status bar with metrics
- Session summaries on exit

Usage:
    from scripts.strands_chat_loop import ChatLoop

    chat = ChatLoop(agent, name, description)
    chat.run()

Or run directly:
    python scripts/strands_chat_loop/chat_loop.py --agent <agent_path>
"""

__version__ = "1.0.0"
__author__ = "Agent Examples"

from .chat_loop import ChatLoop, main

__all__ = ['ChatLoop', 'main']
