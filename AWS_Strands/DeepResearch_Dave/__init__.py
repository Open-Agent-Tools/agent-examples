"""
Deep Research Dave Agent

A specialized research agent built on AWS Strands framework for comprehensive
information gathering, analysis, and synthesis across any domain.
"""

from .agent import DeepResearchDave, create_agent, ResearchSession
from .prompts import SYSTEM_PROMPT

__version__ = "1.0.0"
__author__ = "Deep Research Dave"

__all__ = [
    "DeepResearchDave",
    "create_agent", 
    "ResearchSession",
    "SYSTEM_PROMPT"
]