#!/usr/bin/env python3
"""
Generic Chat Loop for AWS Strands Agents

A unified chat interface that can run any Strands agent by importing the
root_agent from the specified agent module.

Usage:
    python AWS_Strands/chat_loop.py --agent AWS_Strands/Product_Pete/agent.py
    python AWS_Strands/chat_loop.py --agent AWS_Strands/DeepResearch_Dave/agent.py
"""

import argparse
import asyncio
import importlib.util
import logging
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, Optional

from dotenv import load_dotenv

# Setup logging directory
log_dir = Path(__file__).parent.parent / '.logs'
log_dir.mkdir(exist_ok=True)

# We'll configure logging after we know the agent name
logger = logging.getLogger(__name__)

def setup_logging(agent_name: str):
    """Setup logging with agent-specific filename."""
    log_file = log_dir / f'{agent_name.lower().replace(" ", "_")}_chat.log'
    
    # Clear any existing handlers
    logging.root.handlers = []
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file)
        ]
    )

def load_environment_variables():
    """Load environment variables from .env file."""
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

def load_agent_module(agent_path: str):
    """Dynamically load agent module and extract root_agent."""
    if not os.path.exists(agent_path):
        raise FileNotFoundError(f"Agent file not found: {agent_path}")
    
    # Add the agent directory to sys.path to fix import issues
    agent_dir = os.path.dirname(agent_path)
    if agent_dir not in sys.path:
        sys.path.insert(0, agent_dir)
    
    # Convert path to module name
    spec = importlib.util.spec_from_file_location("agent_module", agent_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load module from {agent_path}")
    
    module = importlib.util.module_from_spec(spec)
    sys.modules["agent_module"] = module
    spec.loader.exec_module(module)
    
    # Extract root_agent
    if not hasattr(module, 'root_agent'):
        raise AttributeError(f"Agent module {agent_path} must expose a 'root_agent' attribute")
    
    agent = module.root_agent
    
    # Extract agent metadata if available
    agent_name = getattr(agent, 'name', os.path.basename(os.path.dirname(agent_path)))
    agent_description = getattr(agent, 'description', "A Strands Agent")
    
    return agent, agent_name, agent_description

def format_agent_response(response: Any, duration: float) -> None:
    """Format and display agent response with consistent styling."""
    print(f"\n{'-' * 60}")
    
    # Handle different response formats
    if hasattr(response, 'message'):
        # Standard Strands agent response
        message = response.message
        if isinstance(message, dict):
            if 'content' in message:
                content = message['content']
                if isinstance(content, list) and len(content) > 0:
                    for block in content:
                        if isinstance(block, dict) and 'text' in block:
                            print(block['text'])
                        else:
                            print(str(block))
                else:
                    print(content)
            else:
                print(message)
        else:
            print(message)
    elif isinstance(response, dict):
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

class ChatLoop:
    """Generic chat loop for any Strands agent."""
    
    def __init__(self, agent, agent_name: str, agent_description: str):
        self.agent = agent
        self.agent_name = agent_name
        self.agent_description = agent_description
        
    def display_banner(self):
        """Display agent banner and help."""
        print(f"\n{self.agent_name.upper()} - Interactive Chat")
        print("=" * 60)
        print(f"Welcome to {self.agent_name}!")
        print(f"{self.agent_description}")
        print()
        print("Commands:")
        print("  help  - Show this help message")
        print("  quit  - Exit the chat")
        print("  exit  - Exit the chat")
        print("=" * 60)
    
    def display_help(self):
        """Display help information."""
        print(f"\n{self.agent_name.upper()} - Help")
        print("=" * 50)
        print(f"Agent: {self.agent_name}")
        print(f"Description: {self.agent_description}")
        print()
        print("Commands:")
        print("  help  - Show this help message")
        print("  quit  - Exit the chat")
        print("  exit  - Exit the chat")
        print("=" * 50)
    
    def run(self):
        """Run the interactive chat loop."""
        self.display_banner()
        
        try:
            while True:
                try:
                    # Get user input
                    user_input = input(f"\nYou: ").strip()
                    
                    # Handle commands
                    if user_input.lower() in ["exit", "quit", "bye"]:
                        print(f"\nGoodbye! Thanks for using {self.agent_name}!")
                        break
                    elif user_input.lower() == "help":
                        self.display_help()
                        continue
                    elif not user_input:
                        continue
                    
                    # Process query through agent
                    print(f"{self.agent_name}: Processing your query...")
                    start_time = time.time()
                    
                    try:
                        # Call the agent directly
                        logger.info(f"Processing query: {user_input[:100]}...")
                        response = self.agent(user_input)
                        duration = time.time() - start_time
                        logger.info(f"Query completed successfully in {duration:.1f}s")
                        format_agent_response(response, duration)
                        
                    except Exception as e:
                        duration = time.time() - start_time
                        print(f"{self.agent_name}: Query failed - {e}")
                        print("Try rephrasing your question or check the logs for details.")
                        logger.error(f"Agent query failed after {duration:.1f}s: {e}", exc_info=True)
                    
                except KeyboardInterrupt:
                    print(f"\n\nChat interrupted. Thanks for using {self.agent_name}!")
                    break
                except EOFError:
                    print(f"\n\nChat ended. Thanks for using {self.agent_name}!")
                    break
                    
        finally:
            # Cleanup agent if it has cleanup method
            if hasattr(self.agent, 'cleanup'):
                try:
                    self.agent.cleanup()
                except Exception as e:
                    logger.warning(f"Error during agent cleanup: {e}")
            
            print(f"{self.agent_name} session complete!")

def main():
    """Main entry point for the chat loop."""
    parser = argparse.ArgumentParser(
        description="Generic Chat Loop for AWS Strands Agents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python AWS_Strands/chat_loop.py --agent AWS_Strands/Product_Pete/agent.py
    python AWS_Strands/chat_loop.py --agent AWS_Strands/DeepResearch_Dave/agent.py
    python AWS_Strands/chat_loop.py --agent AWS_Strands/QuickResearch_Quinten/agent.py
        """
    )
    
    parser.add_argument(
        '--agent', 
        required=True,
        help='Path to the agent.py file (must expose root_agent)'
    )
    
    args = parser.parse_args()
    
    try:
        # Load environment variables
        env_path = load_environment_variables()
        if env_path:
            print(f"Loaded environment from: {env_path}")
            logger.info(f"Loaded environment from: {env_path}")
        
        # Load the agent
        print(f"Loading agent from: {args.agent}")
        agent, agent_name, agent_description = load_agent_module(args.agent)
        
        # Setup logging with agent name
        setup_logging(agent_name)
        
        print(f"Agent loaded successfully: {agent_name}")
        logger.info(f"Agent loaded successfully: {agent_name} - {agent_description}")
        
        # Start chat loop
        chat_loop = ChatLoop(agent, agent_name, agent_description)
        chat_loop.run()
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()