"""
Common utilities for AWS Strands agents.
Provides shared functionality for environment setup, logging, and agent creation.
Note: Chat loop functionality has been moved to chat_loop.py
"""

import logging
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, Optional
from dotenv import load_dotenv


def load_environment_variables():
    """Load environment variables from .env file in project root."""
    try:
        # Look for .env file up to 4 levels up from current file
        for i in range(4):
            env_path = Path(__file__).parents[i] / ".env"
            if env_path.exists():
                load_dotenv(env_path)
                return env_path
    except ImportError:
        pass
    return None


def setup_file_logging(agent_name: str, log_level: int = logging.INFO) -> Path:
    """
    Configure logging to file only for clean terminal output.
    
    Args:
        agent_name: Name of the agent for log file naming
        log_level: Logging level (default: INFO)
        
    Returns:
        Path to the log file
    """
    # Create logs directory in project root (3 levels up from this file)
    logs_dir = Path(__file__).parents[2] / ".logs"
    logs_dir.mkdir(exist_ok=True)
    
    log_file = logs_dir / f"{agent_name.lower().replace(' ', '_')}_chat.log"
    
    # Clear any existing handlers
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    
    # Configure root logger to file only
    file_handler = logging.FileHandler(log_file, mode='a')
    file_handler.setFormatter(
        logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    )
    root_logger.addHandler(file_handler)
    root_logger.setLevel(log_level)
    
    # Suppress noisy loggers
    noisy_loggers = [
        "httpx", "strands.telemetry", "mcp.client", 
        "strands.tools", "agent", "urllib3"
    ]
    for logger_name in noisy_loggers:
        logging.getLogger(logger_name).setLevel(logging.ERROR)
    
    return log_file


def suppress_output_during_execution(func):
    """
    Context manager/decorator to suppress stdout/stderr during function execution.
    Useful for hiding initialization logs while keeping agent responses clean.
    """
    def wrapper(*args, **kwargs):
        original_stdout = sys.stdout
        original_stderr = sys.stderr
        
        with open(os.devnull, 'w') as devnull:
            sys.stdout = devnull
            sys.stderr = devnull
            try:
                return func(*args, **kwargs)
            finally:
                sys.stdout = original_stdout
                sys.stderr = original_stderr
    
    return wrapper


# Async utilities moved to chat_loop.py


# Display functions moved to chat_loop.py


def format_agent_response(response: Any, duration: float) -> None:
    """
    Format and display agent response with consistent styling.
    
    Args:
        response: Agent response (can be dict or string)
        duration: Time taken for the response in seconds
    """
    print(f"\n{'-' * 60}")
    
    # Handle different response formats
    if isinstance(response, dict):
        if 'content' in response:
            content = response['content']
            if isinstance(content, list) and len(content) > 0:
                print(content[0].get('text', str(response)))
            else:
                print(content)
        elif 'response' in response:
            print(response['response'])
        else:
            print(response)
    else:
        print(response)
    
    print(f"{'-' * 60}")
    print(f"Completed in {duration:.1f}s")


def check_environment_requirements(required_keys: Dict[str, str]) -> list:
    """
    Check if required environment variables are present.
    
    Args:
        required_keys: Dict mapping env var names to descriptions
        
    Returns:
        List of missing keys with descriptions
    """
    missing_keys = []
    for key, description in required_keys.items():
        if not os.getenv(key):
            missing_keys.append(f"{key} ({description})")
    return missing_keys


# Chat interface functionality has been moved to chat_loop.py
# This module now focuses on core utilities only


# Terminal color constants
RESET = '\033[0m'
BOLD = '\033[1m'
DIM = '\033[2m'
CYAN = '\033[36m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
MAGENTA = '\033[35m'
BRIGHT_CYAN = '\033[96m'
BRIGHT_GREEN = '\033[92m'
BRIGHT_YELLOW = '\033[93m'
BRIGHT_BLUE = '\033[94m'
BRIGHT_MAGENTA = '\033[95m'


class SessionTracker:
    """Simple session tracking for agent interactions."""
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.session_id = str(int(time.time()))
        self.history = []
        self.metrics = {"queries": 0, "tokens": 0, "duration": 0.0}
        
    def add_interaction(self, query: str, response: str, tokens: int = 0, duration: float = 0.0):
        """Add interaction to session history (keep last 5 only)."""
        self.history.append({
            "timestamp": time.strftime("%H:%M:%S"),
            "query": query[:100] + "..." if len(query) > 100 else query,
            "response_length": len(response)
        })
        if len(self.history) > 5:
            self.history.pop(0)
            
        self.metrics["queries"] += 1
        self.metrics["tokens"] += tokens
        self.metrics["duration"] += duration
    
    def get_stats(self) -> Dict[str, Any]:
        """Get session statistics."""
        return {
            "session_id": self.session_id,
            "queries": self.metrics["queries"],
            "tokens": self.metrics["tokens"],
            "avg_duration": f"{self.metrics['duration'] / max(self.metrics['queries'], 1):.2f}s"
        }
    
    def get_context(self) -> str:
        """Get recent context summary."""
        if not self.history:
            return ""
        
        context = "Recent context:\n"
        for i, item in enumerate(self.history[-3:], 1):
            context += f"{i}. {item['timestamp']}: {item['query']}\n"
        return context


def setup_agent_logging(agent_name: str):
    """Setup file-only logging for an agent."""
    logs_dir = Path(__file__).parents[1] / ".logs"
    logs_dir.mkdir(exist_ok=True)
    log_file = logs_dir / f"{agent_name.lower().replace(' ', '_')}_chat.log"
    
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    
    handler = logging.FileHandler(log_file, mode="a")
    handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s"))
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.DEBUG)
    
    # Suppress noisy loggers
    for name in ["httpx", "mcp", "strands.telemetry", "urllib3"]:
        logging.getLogger(name).setLevel(logging.ERROR)
    
    return logging.getLogger(__name__)


def create_strands_agent(model_config: dict, tools: list, system_prompt: str, logger=None, name="Agent", description="A Strands Agent"):
    """Create a Strands agent with error handling."""
    from strands import Agent
    
    # Model selection
    if os.getenv("ANTHROPIC_API_KEY"):
        try:
            from strands.models.anthropic import AnthropicModel
            model = AnthropicModel(**model_config)
            if logger:
                logger.info("Using Anthropic Direct API")
        except ImportError:
            model = "anthropic.claude-3-7-sonnet-20250219-v1:0"
            if logger:
                logger.info("Using Bedrock (Anthropic import failed)")
    else:
        model = "anthropic.claude-3-7-sonnet-20250219-v1:0"
        if logger:
            logger.info("Using Bedrock")

    return Agent(name=name, description=description, model=model, tools=tools, system_prompt=system_prompt)


def add_mcp_tools(base_tools: list, mcp_url: str, logger=None):
    """Add MCP tools to base tools list."""
    try:
        from mcp.client.streamable_http import streamablehttp_client
        from strands.tools.mcp.mcp_client import MCPClient
        
        mcp_client = MCPClient(lambda: streamablehttp_client(mcp_url))
        mcp_client.start()
        mcp_tools = list(mcp_client.list_tools_sync())
        base_tools.extend(mcp_tools)
        
        if logger:
            logger.info(f"Added {len(mcp_tools)} MCP tools")
    except Exception as e:
        if logger:
            logger.warning(f"MCP tools unavailable: {e}")
    
    return base_tools


def call_agent_with_context(agent, query: str, session_tracker, logger=None):
    """Call agent with context and error handling."""
    start_time = time.time()
    
    try:
        # Add context if available
        context = session_tracker.get_context()
        if context and "Recent context:" not in query:
            enhanced_query = f"{context}\nCurrent request: {query}"
        else:
            enhanced_query = query
        
        # Call agent
        result = agent(enhanced_query)
        duration = time.time() - start_time
        
        # Extract response and tokens
        if hasattr(result, "message"):
            if isinstance(result.message, dict) and "content" in result.message:
                content = result.message["content"]
                if isinstance(content, list):
                    response_text = "\n".join(block.get("text", "") for block in content if isinstance(block, dict))
                else:
                    response_text = str(content)
            else:
                response_text = str(result.message)
            
            try:
                tokens = result.metrics.get_summary()["accumulated_usage"]["totalTokens"]
            except (AttributeError, KeyError):
                tokens = 0
        else:
            response_text = str(result)
            tokens = 0
        
        session_tracker.add_interaction(query, response_text, tokens, duration)
        return {"success": True, "response": response_text, "tokens": tokens, "duration": duration}
        
    except Exception as e:
        duration = time.time() - start_time
        if logger:
            logger.error(f"Agent call failed: {e}")
        return {"success": False, "response": f"Error: {e}", "tokens": 0, "duration": duration}