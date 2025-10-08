"""
Complex Coding Clara - Multi-Agent Coding System

A sophisticated multi-agent coding system built on AWS Strands framework,
featuring specialized agents for coding, testing, and code review.
"""

__version__ = "0.1.0"

# Root agent will be imported from agent.py
from .agent import root_agent, create_agent

__all__ = ["root_agent", "create_agent", "__version__"]
