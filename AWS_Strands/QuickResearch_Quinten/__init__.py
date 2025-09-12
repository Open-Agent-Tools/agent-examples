"""
Quick Research Quinten Agent

A specialized quick research agent for rapid information gathering.
"""

from .agent import create_agent, root_agent
from .prompts import SYSTEM_PROMPT
from .tools import generate_search_url, process_web_content, extract_urls_from_content, extract_contact_info

__all__ = [
    "create_agent",
    "SYSTEM_PROMPT",
    "root_agent",
    "generate_search_url",
    "process_web_content", 
    "extract_urls_from_content",
    "extract_contact_info",
]

__version__ = "1.0.0"