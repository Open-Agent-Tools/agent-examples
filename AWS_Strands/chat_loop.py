#!/usr/bin/env python3
"""
Generic Chat Loop for AWS Strands Agents

A unified chat interface that can run any Strands agent by importing the
root_agent from the specified agent module.

Features:
- Async streaming support with real-time response display
- Command history with readline (↑↓ to navigate, saved to ~/.chat_history)
- Multi-line input support (type \\\\ to enter multi-line mode)
- Automatic error recovery with retry logic (timeouts, connection errors, rate limits)
- Color-coded output for better readability
- Configuration file support (~/.chatrc or .chatrc in project root)
- Graceful error handling

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
from typing import Any, Dict, Optional, List

try:
    import readline
    READLINE_AVAILABLE = True
except ImportError:
    READLINE_AVAILABLE = False

from dotenv import load_dotenv

# Configuration management
try:
    from .chat_config import get_config, ChatConfig
except ImportError:
    try:
        from chat_config import get_config, ChatConfig
    except ImportError:
        # Fallback if config module not available
        get_config = None
        ChatConfig = None

# Rich library for better formatting
try:
    from rich.console import Console
    from rich.markdown import Markdown
    from rich.spinner import Spinner
    from rich.live import Live
    from rich.table import Table
    from rich.panel import Panel
    from rich.layout import Layout
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    Console = None
    Markdown = None

# Setup logging directory
log_dir = Path(__file__).parent.parent / '.logs'
log_dir.mkdir(exist_ok=True)

# We'll configure logging after we know the agent name
logger = logging.getLogger(__name__)

# Terminal colors using ANSI escape codes
class Colors:
    """ANSI color codes for terminal output."""
    # Default colors (can be overridden by config)
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'

    # Text colors - these will be updated from config
    USER = '\033[97m'      # Bright white for user input (maximum contrast)
    AGENT = '\033[94m'     # Bright blue for agent
    SYSTEM = '\033[33m'    # Yellow for system messages
    ERROR = '\033[91m'     # Bright red for errors
    SUCCESS = '\033[92m'   # Bright green for success

    @classmethod
    def configure(cls, config: Dict[str, str]):
        """
        Configure colors from config dictionary.

        Args:
            config: Dictionary of color codes
        """
        cls.USER = config.get('user', cls.USER)
        cls.AGENT = config.get('agent', cls.AGENT)
        cls.SYSTEM = config.get('system', cls.SYSTEM)
        cls.ERROR = config.get('error', cls.ERROR)
        cls.SUCCESS = config.get('success', cls.SUCCESS)
        cls.DIM = config.get('dim', cls.DIM)
        cls.RESET = config.get('reset', cls.RESET)

    @staticmethod
    def user(text: str) -> str:
        """Format text as user input."""
        return f"{Colors.USER}{text}{Colors.RESET}"

    @staticmethod
    def agent(text: str) -> str:
        """Format text as agent response."""
        return f"{Colors.AGENT}{text}{Colors.RESET}"

    @staticmethod
    def system(text: str) -> str:
        """Format text as system message."""
        return f"{Colors.SYSTEM}{text}{Colors.RESET}"

    @staticmethod
    def error(text: str) -> str:
        """Format text as error."""
        return f"{Colors.ERROR}{text}{Colors.RESET}"

    @staticmethod
    def success(text: str) -> str:
        """Format text as success."""
        return f"{Colors.SUCCESS}{text}{Colors.RESET}"

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

def setup_readline_history():
    """Setup readline command history with persistence."""
    if not READLINE_AVAILABLE:
        return None

    # History file in user's home directory
    history_file = Path.home() / '.chat_history'

    # Set history length
    readline.set_history_length(1000)

    # Enable tab completion and better editing
    try:
        # Parse readline init file if it exists
        readline.parse_and_bind("tab: complete")

        # Enable vi or emacs mode (emacs is default)
        readline.parse_and_bind("set editing-mode emacs")

        # Enable better line editing
        readline.parse_and_bind("set show-all-if-ambiguous on")
        readline.parse_and_bind("set completion-ignore-case on")
    except Exception as e:
        logger.debug(f"Could not configure readline: {e}")

    # Load existing history
    if history_file.exists():
        try:
            readline.read_history_file(str(history_file))
        except Exception as e:
            logger.debug(f"Could not load history: {e}")

    return history_file

def save_readline_history(history_file: Optional[Path]):
    """Save readline command history."""
    if history_file and READLINE_AVAILABLE:
        try:
            readline.write_history_file(str(history_file))
        except Exception as e:
            logger.debug(f"Could not save history: {e}")

class TokenTracker:
    """Track token usage and cost estimation."""

    # Model pricing (per 1M tokens)
    PRICING = {
        'Claude Sonnet 4.5': {'input': 3.00, 'output': 15.00},
        'Sonnet 4.5': {'input': 3.00, 'output': 15.00},
        'Claude Sonnet 4': {'input': 3.00, 'output': 15.00},
        'Sonnet 4': {'input': 3.00, 'output': 15.00},
        'Claude Sonnet 3.5': {'input': 3.00, 'output': 15.00},
        'Sonnet 3.5': {'input': 3.00, 'output': 15.00},
        'Claude Opus': {'input': 15.00, 'output': 75.00},
        'Opus': {'input': 15.00, 'output': 75.00},
        'Claude Haiku': {'input': 0.25, 'output': 1.25},
        'Haiku': {'input': 0.25, 'output': 1.25},
        'GPT-4': {'input': 30.00, 'output': 60.00},
        'GPT-4 Turbo': {'input': 10.00, 'output': 30.00},
        'GPT-3.5': {'input': 0.50, 'output': 1.50},
    }

    def __init__(self, model_name: str = 'Unknown'):
        """
        Initialize token tracker.

        Args:
            model_name: Name of the model for pricing
        """
        self.model_name = model_name
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.query_history = []  # List of (input, output) tuples

    def add_usage(self, input_tokens: int, output_tokens: int):
        """
        Add token usage for a query.

        Args:
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
        """
        self.total_input_tokens += input_tokens
        self.total_output_tokens += output_tokens
        self.query_history.append((input_tokens, output_tokens))

    def get_total_tokens(self) -> int:
        """Get total tokens (input + output)."""
        return self.total_input_tokens + self.total_output_tokens

    def get_cost(self) -> float:
        """
        Calculate estimated cost in USD.

        Returns:
            Estimated cost in dollars
        """
        # Try to find pricing for this model
        pricing = None
        for model_key in self.PRICING:
            if model_key.lower() in self.model_name.lower():
                pricing = self.PRICING[model_key]
                break

        if not pricing:
            return 0.0  # Unknown model

        # Calculate cost (pricing is per 1M tokens)
        input_cost = (self.total_input_tokens / 1_000_000) * pricing['input']
        output_cost = (self.total_output_tokens / 1_000_000) * pricing['output']
        return input_cost + output_cost

    def format_cost(self) -> str:
        """Format cost as currency string."""
        cost = self.get_cost()
        if cost < 0.01:
            return f"${cost:.4f}"
        elif cost < 1.0:
            return f"${cost:.3f}"
        else:
            return f"${cost:.2f}"

    def format_tokens(self, tokens: int) -> str:
        """Format token count with K/M suffix."""
        if tokens >= 1_000_000:
            return f"{tokens / 1_000_000:.1f}M"
        elif tokens >= 1_000:
            return f"{tokens / 1_000:.1f}K"
        else:
            return str(tokens)


class StatusBar:
    """Simple status bar for chat loop."""

    def __init__(self, agent_name: str, model_info: str, show_tokens: bool = False):
        """
        Initialize status bar.

        Args:
            agent_name: Name of the agent
            model_info: Model identifier string
            show_tokens: Whether to show token count
        """
        self.agent_name = agent_name
        self.model_info = model_info
        self.query_count = 0
        self.start_time = time.time()
        self.show_tokens = show_tokens
        self.total_tokens = 0

    def get_session_time(self) -> str:
        """Get formatted session time."""
        elapsed = int(time.time() - self.start_time)
        minutes = elapsed // 60
        seconds = elapsed % 60
        if minutes > 0:
            return f"{minutes}m {seconds}s"
        return f"{seconds}s"

    def increment_query(self):
        """Increment query counter."""
        self.query_count += 1

    def update_tokens(self, total_tokens: int):
        """Update total token count."""
        self.total_tokens = total_tokens

    def render(self) -> str:
        """
        Render status bar as string.

        Returns:
            Formatted status bar string
        """
        session_time = self.get_session_time()
        queries_text = "query" if self.query_count == 1 else "queries"

        # Build status line
        parts = [
            self.agent_name,
            self.model_info,
        ]

        # Add tokens if enabled and available
        if self.show_tokens and self.total_tokens > 0:
            if self.total_tokens >= 1_000_000:
                token_str = f"{self.total_tokens / 1_000_000:.1f}M tokens"
            elif self.total_tokens >= 1_000:
                token_str = f"{self.total_tokens / 1_000:.1f}K tokens"
            else:
                token_str = f"{self.total_tokens} tokens"
            parts.append(token_str)

        parts.extend([
            f"{self.query_count} {queries_text}",
            session_time
        ])

        status_line = " │ ".join(parts)
        width = len(status_line) + 4  # Padding

        # Create bordered status bar
        top = "┌" + "─" * (width - 2) + "┐"
        middle = f"│ {status_line} │"
        bottom = "└" + "─" * (width - 2) + "┘"

        return f"{top}\n{middle}\n{bottom}"


def load_environment_variables():
    """Load environment variables from .env file up to 3 levels up."""
    try:
        # Look for .env file up to 3 levels up from current file
        for i in range(3):
            env_path = Path(__file__).parents[i] / ".env"
            if env_path.exists():
                load_dotenv(env_path, override=False)  # Don't override existing vars
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


class ChatLoop:
    """Generic chat loop for any Strands agent with async streaming support."""

    def __init__(self, agent, agent_name: str, agent_description: str, agent_factory=None, config: Optional['ChatConfig'] = None):
        self.agent = agent
        self.agent_name = agent_name
        self.agent_description = agent_description
        self.agent_factory = agent_factory  # Function to create fresh agent instance
        self.history_file = None
        self.last_response = ""  # Track last response for copy command

        # Load or use provided config
        self.config = config if config else (get_config() if get_config else None)

        # Apply configuration values (with agent-specific overrides)
        if self.config:
            self.max_retries = int(self.config.get('behavior.max_retries', 3, agent_name=agent_name))
            self.retry_delay = float(self.config.get('behavior.retry_delay', 2.0, agent_name=agent_name))
            self.timeout = float(self.config.get('behavior.timeout', 120.0, agent_name=agent_name))
            self.spinner_style = self.config.get('behavior.spinner_style', 'dots', agent_name=agent_name)

            # Feature flags
            self.auto_save = self.config.get('features.auto_save', False, agent_name=agent_name)
            self.show_metadata = self.config.get('features.show_metadata', True, agent_name=agent_name)
            self.show_thinking = self.config.get('ui.show_thinking_indicator', True, agent_name=agent_name)
            self.show_duration = self.config.get('ui.show_duration', True, agent_name=agent_name)
            self.show_banner = self.config.get('ui.show_banner', True, agent_name=agent_name)

            # Rich override
            rich_enabled = self.config.get('features.rich_enabled', True, agent_name=agent_name)
            self.use_rich = RICH_AVAILABLE and rich_enabled
        else:
            # Defaults when no config
            self.max_retries = 3
            self.retry_delay = 2.0
            self.timeout = 120.0
            self.spinner_style = 'dots'
            self.auto_save = False
            self.show_metadata = True
            self.show_thinking = True
            self.show_duration = True
            self.show_banner = True
            self.use_rich = RICH_AVAILABLE

        # Setup rich console if available and enabled
        self.console = Console() if self.use_rich else None

        # Setup prompt templates directory
        self.prompts_dir = Path.home() / '.prompts'

        # Extract agent metadata
        self.agent_metadata = self._extract_agent_metadata()

        # Setup token tracking (always enabled for session summary)
        self.show_tokens = self.config.get('features.show_tokens', False, agent_name=agent_name) if self.config else False
        model_for_pricing = self.agent_metadata.get('model_id', 'Unknown')

        # Check for config override
        if self.config:
            model_override = self.config.get('agents.' + agent_name + '.model_display_name', None)
            if model_override:
                model_for_pricing = model_override

        # Always create token tracker for session summary (not just when show_tokens is true)
        self.token_tracker = TokenTracker(model_for_pricing)

        # Track session start time for summary
        self.session_start_time = time.time()
        self.query_count = 0

        # Setup status bar if enabled
        self.show_status_bar_enabled = self.config.get('ui.show_status_bar', False, agent_name=agent_name) if self.config else False
        self.status_bar = None
        if self.show_status_bar_enabled:
            model_info = self.agent_metadata.get('model_id', 'Unknown Model')

            # Check for config override
            if self.config:
                model_override = self.config.get('agents.' + agent_name + '.model_display_name', None)
                if model_override:
                    model_info = model_override

            # Shorten long model IDs
            if len(model_info) > 30:
                model_info = model_info[:27] + "..."

            self.status_bar = StatusBar(agent_name, model_info, show_tokens=self.show_tokens)

            # Log for debugging
            logger.debug(f"Status bar initialized: agent={agent_name}, model={model_info}, show_tokens={self.show_tokens}")

    def _extract_agent_metadata(self) -> Dict[str, Any]:
        """Extract metadata from agent for display."""
        metadata = {}

        # Try to extract model information
        if hasattr(self.agent, 'model'):
            model = self.agent.model

            # Try multiple attribute names for model ID
            model_id = None
            for attr in ['model_id', 'model', 'model_name', '_model_id', 'name']:
                if hasattr(model, attr):
                    model_id = getattr(model, attr)
                    if model_id and model_id != 'Unknown':
                        break

            # Clean up model_id if it's a long AWS model string
            if model_id and isinstance(model_id, str):
                # Extract meaningful part from AWS model IDs
                # e.g., "us.anthropic.claude-sonnet-4-5-20250929-v1:0" -> "Claude Sonnet 4.5"
                if 'claude-sonnet' in model_id.lower():
                    if '4-5' in model_id or '4.5' in model_id:
                        model_id = "Claude Sonnet 4.5"
                    elif '3-5' in model_id or '3.5' in model_id:
                        model_id = "Claude Sonnet 3.5"
                    else:
                        model_id = "Claude Sonnet"
                elif 'claude-opus' in model_id.lower():
                    model_id = "Claude Opus"
                elif 'claude-haiku' in model_id.lower():
                    model_id = "Claude Haiku"

            metadata['model_id'] = model_id or 'Unknown Model'
            metadata['max_tokens'] = getattr(model, 'max_tokens', 'Unknown')
            metadata['temperature'] = getattr(model, 'temperature', 'Unknown')

        # Try to extract tools - check multiple attributes
        tools = None
        for attr in ['tools', '_tools', 'tool_list']:
            if hasattr(self.agent, attr):
                tools = getattr(self.agent, attr)
                if tools:
                    break

        if tools and isinstance(tools, (list, tuple)):
            metadata['tool_count'] = len(tools)
            # Extract tool names safely
            tool_names = []
            for t in tools[:10]:  # First 10
                if hasattr(t, 'name'):
                    tool_names.append(t.name)
                elif hasattr(t, '__name__'):
                    tool_names.append(t.__name__)
                elif hasattr(t, 'func') and hasattr(t.func, '__name__'):
                    tool_names.append(t.func.__name__)
                else:
                    tool_names.append(str(t)[:30])
            metadata['tools'] = tool_names
        else:
            metadata['tool_count'] = 0
            metadata['tools'] = []

        return metadata

    def display_banner(self):
        """Display agent banner and help."""
        if not self.show_banner:
            return

        # Show status bar if enabled
        if self.status_bar:
            print(f"\n{self.status_bar.render()}")

        print(f"\n{self.agent_name.upper()} - Interactive Chat")
        print("=" * 60)
        print(f"Welcome to {self.agent_name}!")
        print(f"{self.agent_description}")

        # Display agent metadata if enabled and available
        if self.show_metadata and self.agent_metadata:
            print()
            print(Colors.DIM + "Agent Configuration:" + Colors.RESET)

            # Use status bar model if available (it has overrides applied)
            if self.status_bar and self.status_bar.model_info:
                print(f"  Model: {self.status_bar.model_info}")
            elif 'model_id' in self.agent_metadata:
                print(f"  Model: {self.agent_metadata['model_id']}")

            if 'max_tokens' in self.agent_metadata and self.agent_metadata['max_tokens'] != 'Unknown':
                print(f"  Max Tokens: {self.agent_metadata['max_tokens']}")

            if 'tool_count' in self.agent_metadata and self.agent_metadata['tool_count'] > 0:
                tool_count = self.agent_metadata['tool_count']
                print(f"  Tools: {tool_count} available")

        print()
        print("Commands:")
        print("  help      - Show this help message")
        print("  info      - Show detailed agent information")
        print("  templates - List available prompt templates")
        print("  /name     - Use prompt template from ~/.prompts/name.md")
        print("  clear     - Clear screen and reset agent session")
        print("  quit      - Exit the chat")
        print("  exit      - Exit the chat")
        print()
        print("Features:")
        if READLINE_AVAILABLE:
            print("  ↑↓     - Navigate command history")
        print("  Enter  - Submit single line")
        print("  \\\\     - Start multi-line input (end with empty line)")
        if self.use_rich:
            print("  Rich   - Enhanced markdown rendering with syntax highlighting")

        # Show config info if config loaded
        if self.config:
            print()
            print(Colors.DIM + "Configuration loaded" + Colors.RESET)
            if self.auto_save:
                save_loc = self.config.get('paths.save_location', '~/agent-conversations', agent_name=self.agent_name)
                print(f"  Auto-save: enabled → {save_loc}")

        print("=" * 60)

    def display_help(self):
        """Display help information."""
        print(f"\n{self.agent_name.upper()} - Help")
        print("=" * 50)
        print(f"Agent: {self.agent_name}")
        print(f"Description: {self.agent_description}")
        print()
        print("Commands:")
        print("  help      - Show this help message")
        print("  info      - Show detailed agent information")
        print("  templates - List available prompt templates")
        print("  /name     - Use prompt template from ~/.prompts/name.md")
        print("  clear     - Clear screen and reset agent session")
        print("  quit      - Exit the chat")
        print("  exit      - Exit the chat")
        print()
        print("Prompt Templates:")
        print("  Create: Save markdown files to ~/.prompts/name.md")
        print("  Use: Type /name <optional context>")
        print("  Variables: Use {input} in template for substitution")
        print("  Example: /review {input} → replaces {input} with context")
        print()
        print("Multi-line Input:")
        print("  Type \\\\ to start multi-line mode")
        print("  Press Enter on empty line to submit")
        print("  Great for code blocks and long prompts")
        if READLINE_AVAILABLE:
            print()
            print("History:")
            print("  Use ↑↓ arrows to navigate previous queries")
            print("  History saved to ~/.chat_history")
        print("=" * 50)

    def display_info(self):
        """Display detailed agent information."""
        print(f"\n{self.agent_name.upper()} - Information")
        print("=" * 60)
        print(f"Name: {self.agent_name}")
        print(f"Description: {self.agent_description}")
        print()

        if self.agent_metadata:
            print("Configuration:")
            if 'model_id' in self.agent_metadata:
                print(f"  Model ID: {self.agent_metadata['model_id']}")
            if 'max_tokens' in self.agent_metadata:
                print(f"  Max Tokens: {self.agent_metadata['max_tokens']}")
            if 'temperature' in self.agent_metadata:
                print(f"  Temperature: {self.agent_metadata['temperature']}")
            print()

            if 'tools' in self.agent_metadata and self.agent_metadata['tools']:
                print(f"Available Tools ({self.agent_metadata['tool_count']}):")
                for i, tool in enumerate(self.agent_metadata['tools'], 1):
                    print(f"  {i}. {tool}")
                if self.agent_metadata['tool_count'] > len(self.agent_metadata['tools']):
                    remaining = self.agent_metadata['tool_count'] - len(self.agent_metadata['tools'])
                    print(f"  ... and {remaining} more")
            elif self.agent_metadata['tool_count'] > 0:
                print(f"Tools: {self.agent_metadata['tool_count']} available")
            else:
                print("Tools: None")

        print()
        print("Features:")
        if self.use_rich:
            print("  ✓ Rich markdown rendering with syntax highlighting")
        if READLINE_AVAILABLE:
            print("  ✓ Command history with full readline editing")
        print("  ✓ Multi-line input support")
        print("  ✓ Automatic error recovery and retry logic")
        print("  ✓ Session reset with 'clear' command")
        if self.config:
            print("  ✓ Configuration file support (~/.chatrc or .chatrc)")
        if self.auto_save:
            print("  ✓ Auto-save conversations on exit")
        print("=" * 60)

    def _extract_token_usage(self, response_obj) -> Optional[Dict[str, int]]:
        """
        Extract token usage from response object.

        Args:
            response_obj: Response object from agent

        Returns:
            Dict with 'input_tokens' and 'output_tokens', or None if not available
        """
        if not response_obj:
            return None

        # Try common attribute patterns
        usage = None

        # Pattern 1: response['result'].metrics.accumulated_usage (Strands/AWS style)
        if isinstance(response_obj, dict) and 'result' in response_obj:
            result = response_obj['result']
            if hasattr(result, 'metrics') and hasattr(result.metrics, 'accumulated_usage'):
                usage = result.metrics.accumulated_usage

        # Pattern 2: response.usage (Anthropic/Claude style)
        elif hasattr(response_obj, 'usage'):
            usage = response_obj.usage

        # Pattern 3: response['usage'] (dict style)
        elif isinstance(response_obj, dict) and 'usage' in response_obj:
            usage = response_obj['usage']

        # Pattern 4: response.metadata.usage
        elif hasattr(response_obj, 'metadata') and hasattr(response_obj.metadata, 'usage'):
            usage = response_obj.metadata.usage

        # Pattern 5: response.data.usage (streaming event)
        elif hasattr(response_obj, 'data') and hasattr(response_obj.data, 'usage'):
            usage = response_obj.data.usage

        # Pattern 6: response.data['usage'] (streaming event dict)
        elif hasattr(response_obj, 'data') and isinstance(response_obj.data, dict) and 'usage' in response_obj.data:
            usage = response_obj.data['usage']

        if not usage:
            return None

        # Extract input and output tokens
        input_tokens = 0
        output_tokens = 0

        # Try different attribute names (check dict keys first, then attributes)
        if isinstance(usage, dict):
            # Strands/AWS camelCase
            if 'inputTokens' in usage:
                input_tokens = usage['inputTokens']
            elif 'input_tokens' in usage:
                input_tokens = usage['input_tokens']
            elif 'prompt_tokens' in usage:
                input_tokens = usage['prompt_tokens']

            if 'outputTokens' in usage:
                output_tokens = usage['outputTokens']
            elif 'output_tokens' in usage:
                output_tokens = usage['output_tokens']
            elif 'completion_tokens' in usage:
                output_tokens = usage['completion_tokens']
        else:
            # Object attributes
            if hasattr(usage, 'input_tokens'):
                input_tokens = usage.input_tokens
            elif hasattr(usage, 'prompt_tokens'):
                input_tokens = usage.prompt_tokens

            if hasattr(usage, 'output_tokens'):
                output_tokens = usage.output_tokens
            elif hasattr(usage, 'completion_tokens'):
                output_tokens = usage.completion_tokens

        if input_tokens > 0 or output_tokens > 0:
            return {
                'input_tokens': input_tokens,
                'output_tokens': output_tokens
            }

        return None

    async def get_multiline_input(self) -> str:
        """Get multi-line input from user. Empty line submits."""
        lines = []
        print(Colors.system("Multi-line mode (empty line to submit):"))

        while True:
            # Don't use executor - it breaks readline editing
            line = input(Colors.user("... "))

            if not line.strip():  # Empty line submits
                break

            lines.append(line)

        return "\n".join(lines)

    async def _show_thinking_indicator(self, stop_event: asyncio.Event):
        """Show thinking indicator while waiting for response."""
        if not self.show_thinking:
            # Just wait silently
            while not stop_event.is_set():
                await asyncio.sleep(0.1)
            return

        if not self.use_rich:
            # Fallback to simple dots animation
            print(Colors.system("Thinking"), end='', flush=True)
            dot_count = 0
            while not stop_event.is_set():
                print(".", end='', flush=True)
                dot_count += 1
                if dot_count >= 3:
                    print("\b\b\b   \b\b\b", end='', flush=True)  # Clear dots
                    dot_count = 0
                await asyncio.sleep(0.5)
            print("\r" + " " * 15 + "\r", end='', flush=True)  # Clear line
        else:
            # Use rich spinner with configured style
            spinner_style = self.spinner_style if hasattr(self, 'spinner_style') else 'dots'
            with Live(Spinner(spinner_style, text=Colors.system("Thinking...")), console=self.console, refresh_per_second=10) as live:
                while not stop_event.is_set():
                    await asyncio.sleep(0.1)

    async def _stream_agent_response(self, query: str) -> Dict[str, Any]:
        """
        Stream agent response asynchronously.

        Returns:
            Dict with 'duration' and optional 'usage' (input_tokens, output_tokens)
        """
        start_time = time.time()
        response_text = []  # Collect response for rich rendering
        response_obj = None  # Store the response object for token extraction

        # Agent name in blue
        print(f"\n{Colors.agent(self.agent_name)}: ", end='', flush=True)

        # Setup thinking indicator
        stop_thinking = asyncio.Event()
        thinking_task = None

        try:
            # Start thinking indicator if enabled
            if self.show_thinking:
                thinking_task = asyncio.create_task(self._show_thinking_indicator(stop_thinking))

            first_token_received = False

            # Check if agent supports streaming
            if hasattr(self.agent, 'stream_async'):
                async for event in self.agent.stream_async(query):
                    # Store last event for token extraction
                    response_obj = event

                    # Stop thinking indicator on first token
                    if not first_token_received:
                        stop_thinking.set()
                        if thinking_task:
                            await thinking_task
                        first_token_received = True

                    # Handle different event types
                    if hasattr(event, 'data'):
                        data = event.data
                        if isinstance(data, str):
                            response_text.append(data)
                            if self.use_rich:
                                # Don't print during streaming, render at end
                                pass
                            else:
                                print(data, end='', flush=True)
                        elif isinstance(data, dict):
                            # Handle structured data
                            if 'text' in data:
                                text = data['text']
                                response_text.append(text)
                                if not self.use_rich:
                                    print(text, end='', flush=True)
                            elif 'content' in data:
                                content = data['content']
                                if isinstance(content, list):
                                    for block in content:
                                        if isinstance(block, dict) and 'text' in block:
                                            text = block['text']
                                            response_text.append(text)
                                            if not self.use_rich:
                                                print(text, end='', flush=True)
                                else:
                                    text = str(content)
                                    response_text.append(text)
                                    if not self.use_rich:
                                        print(text, end='', flush=True)
            else:
                # Fallback to synchronous call if streaming not supported
                response = await asyncio.get_event_loop().run_in_executor(
                    None, self.agent, query
                )
                response_obj = response  # Store for token extraction

                # Stop thinking indicator
                stop_thinking.set()
                if thinking_task:
                    await thinking_task

                # Format and display response
                if hasattr(response, 'message'):
                    message = response.message
                    if isinstance(message, dict) and 'content' in message:
                        content = message['content']
                        if isinstance(content, list):
                            for block in content:
                                if isinstance(block, dict) and 'text' in block:
                                    response_text.append(block['text'])
                        else:
                            response_text.append(str(content))
                    else:
                        response_text.append(str(message))
                else:
                    response_text.append(str(response))

            # Render collected response
            full_response = "".join(response_text)
            self.last_response = full_response

            if self.use_rich and full_response.strip():
                # Use rich markdown rendering
                print()  # New line after agent name
                md = Markdown(full_response)
                self.console.print(md)
            elif not self.use_rich and response_text:
                # Already printed during streaming, just add newline
                if not first_token_received:
                    # Non-streaming case where nothing was printed yet
                    print(full_response)

            duration = time.time() - start_time

            # Extract token usage if available
            usage_info = self._extract_token_usage(response_obj)

            # Extract additional metrics (Strands-specific)
            cycle_count = None
            tool_count = None
            if isinstance(response_obj, dict) and 'result' in response_obj:
                result = response_obj['result']
                if hasattr(result, 'metrics'):
                    metrics = result.metrics
                    if hasattr(metrics, 'cycle_count'):
                        cycle_count = metrics.cycle_count
                    if hasattr(metrics, 'tool_metrics') and metrics.tool_metrics:
                        # Count total tool calls across all tools
                        tool_count = sum(len(calls) for calls in metrics.tool_metrics.values()) if isinstance(metrics.tool_metrics, dict) else len(metrics.tool_metrics)

            # Track tokens (always, for session summary)
            if usage_info:
                self.token_tracker.add_usage(usage_info['input_tokens'], usage_info['output_tokens'])

                # Update status bar
                if self.status_bar:
                    self.status_bar.update_tokens(self.token_tracker.get_total_tokens())

            # Increment query count for session summary
            self.query_count += 1

            # Display duration and token info
            # Determine what to show
            show_info_line = (
                self.show_duration or
                (self.show_tokens and usage_info) or
                cycle_count or
                tool_count
            )

            if show_info_line:
                print(f"\n{Colors.DIM}{'-' * 60}{Colors.RESET}")

                info_parts = []
                if self.show_duration:
                    info_parts.append(f"Time: {duration:.1f}s")

                # Show agent metrics (cycles, tools) - always show if available
                if cycle_count is not None and cycle_count > 0:
                    cycle_word = "cycle" if cycle_count == 1 else "cycles"
                    info_parts.append(f"{cycle_count} {cycle_word}")

                if tool_count is not None and tool_count > 0:
                    tool_word = "tool" if tool_count == 1 else "tools"
                    info_parts.append(f"{tool_count} {tool_word}")

                # Only show tokens if show_tokens is enabled
                if self.show_tokens and usage_info:
                    input_tok = usage_info['input_tokens']
                    output_tok = usage_info['output_tokens']
                    total_tok = input_tok + output_tok

                    # Format tokens
                    token_str = f"Tokens: {self.token_tracker.format_tokens(total_tok)} "
                    token_str += f"(in: {self.token_tracker.format_tokens(input_tok)}, "
                    token_str += f"out: {self.token_tracker.format_tokens(output_tok)})"
                    info_parts.append(token_str)

                    # Show cost
                    cost = self.token_tracker.get_cost()
                    if cost > 0:
                        info_parts.append(f"Cost: {self.token_tracker.format_cost()}")
                        info_parts.append(f"Session: {self.token_tracker.format_cost()}")

                if info_parts:  # Only print if we have something to show
                    print(Colors.system(" │ ".join(info_parts)))

            logger.info(f"Query completed successfully in {duration:.1f}s")

            return {'duration': duration, 'usage': usage_info}

        except Exception as e:
            # Cleanup thinking indicator on error
            stop_thinking.set()
            if thinking_task and not thinking_task.done():
                await thinking_task

            duration = time.time() - start_time
            print(f"\n{Colors.DIM}{'-' * 60}{Colors.RESET}")
            print(Colors.error(f"{self.agent_name}: Query failed - {e}"))
            print(Colors.system("Try rephrasing your question or check the logs for details."))
            logger.error(f"Agent query failed after {duration:.1f}s: {e}", exc_info=True)

            return {'duration': duration, 'usage': None}

    async def process_query(self, query: str):
        """Process query through agent with streaming and error recovery."""
        for attempt in range(1, self.max_retries + 1):
            try:
                await self._stream_agent_response(query)
                return  # Success, exit retry loop

            except asyncio.TimeoutError:
                print(Colors.error(f"\n⚠️  Timeout (attempt {attempt}/{self.max_retries})"))
                if attempt < self.max_retries:
                    print(Colors.system(f"Retrying in {self.retry_delay}s..."))
                    await asyncio.sleep(self.retry_delay)
                    logger.warning(f"Timeout on attempt {attempt}, retrying...")
                else:
                    print(Colors.error("Max retries reached. Please try again later."))
                    logger.error("Max retries reached after timeout")

            except ConnectionError as e:
                print(Colors.error(f"\n⚠️  Connection error: {e}"))
                if attempt < self.max_retries:
                    print(Colors.system(f"Retrying in {self.retry_delay}s..."))
                    await asyncio.sleep(self.retry_delay)
                    logger.warning(f"Connection error on attempt {attempt}, retrying...")
                else:
                    print(Colors.error("Max retries reached. Check your network connection."))
                    logger.error(f"Max retries reached after connection error: {e}")

            except Exception as e:
                # For other exceptions, don't retry - they're likely not transient
                error_msg = str(e)

                # Check for rate limit errors
                if "rate" in error_msg.lower() or "429" in error_msg:
                    print(Colors.error(f"\n⚠️  Rate limit reached"))
                    if attempt < self.max_retries:
                        wait_time = self.retry_delay * (2 ** (attempt - 1))  # Exponential backoff
                        print(Colors.system(f"Waiting {wait_time:.0f}s before retry..."))
                        await asyncio.sleep(wait_time)
                        logger.warning(f"Rate limit on attempt {attempt}, backing off...")
                    else:
                        print(Colors.error("Rate limit persists. Please wait and try again."))
                        logger.error("Max retries reached due to rate limiting")
                else:
                    # Non-retryable error, log and exit
                    logger.error(f"Non-retryable error: {e}", exc_info=True)
                    raise

    def load_template(self, template_name: str, input_text: str = "") -> Optional[str]:
        """
        Load a prompt template from ~/.prompts/{template_name}.md

        Args:
            template_name: Name of the template (without .md extension)
            input_text: Text to substitute for {input} placeholder

        Returns:
            Processed template text, or None if template not found
        """
        template_path = self.prompts_dir / f"{template_name}.md"

        if not template_path.exists():
            return None

        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                template = f.read()

            # Replace {input} placeholder with provided text
            if '{input}' in template:
                template = template.replace('{input}', input_text)
            elif input_text:
                # If no {input} placeholder but input provided, append it
                template = f"{template}\n\n{input_text}"

            return template

        except Exception as e:
            logger.error(f"Error loading template {template_name}: {e}")
            return None

    def list_templates(self) -> List[str]:
        """
        List available prompt templates from ~/.prompts/

        Returns:
            List of template names (without .md extension)
        """
        if not self.prompts_dir.exists():
            return []

        templates = []
        for file in self.prompts_dir.glob('*.md'):
            templates.append(file.stem)

        return sorted(templates)

    def display_session_summary(self):
        """Display session summary on exit."""
        session_duration = time.time() - self.session_start_time

        # Format duration
        if session_duration < 60:
            duration_str = f"{session_duration:.0f}s"
        elif session_duration < 3600:
            minutes = int(session_duration / 60)
            seconds = int(session_duration % 60)
            duration_str = f"{minutes}m {seconds}s"
        else:
            hours = int(session_duration / 3600)
            minutes = int((session_duration % 3600) / 60)
            duration_str = f"{hours}h {minutes}m"

        print(f"\n{Colors.DIM}{'=' * 60}{Colors.RESET}")
        print(Colors.system("Session Summary"))
        print(f"{Colors.DIM}{'-' * 60}{Colors.RESET}")

        summary_parts = []
        summary_parts.append(f"Duration: {duration_str}")
        summary_parts.append(f"Queries: {self.query_count}")

        # Token and cost info
        total_tokens = self.token_tracker.get_total_tokens()
        if total_tokens > 0:
            input_tok = self.token_tracker.total_input_tokens
            output_tok = self.token_tracker.total_output_tokens

            token_str = f"Tokens: {self.token_tracker.format_tokens(total_tokens)}"
            token_str += f" (in: {self.token_tracker.format_tokens(input_tok)}, "
            token_str += f"out: {self.token_tracker.format_tokens(output_tok)})"
            summary_parts.append(token_str)

            cost = self.token_tracker.get_cost()
            if cost > 0:
                summary_parts.append(f"Total Cost: {self.token_tracker.format_cost()}")

        for part in summary_parts:
            print(Colors.system(f"  {part}"))

        print(f"{Colors.DIM}{'=' * 60}{Colors.RESET}")

    async def _async_run(self):
        """Async implementation of the chat loop."""
        # Setup readline history
        self.history_file = setup_readline_history()

        self.display_banner()

        try:
            while True:
                try:
                    # Get user input directly (blocking is fine for user input)
                    # Don't use executor as it breaks readline editing
                    user_input = input(f"\n{Colors.user('You')}: ").strip()

                    # Handle commands
                    if user_input.lower() in ["exit", "quit", "bye"]:
                        print(Colors.system(f"\nGoodbye! Thanks for using {self.agent_name}!"))
                        break
                    elif user_input.lower() == "help":
                        self.display_help()
                        continue
                    elif user_input.lower() == "info":
                        self.display_info()
                        continue
                    elif user_input.lower() == "templates":
                        # List available prompt templates
                        templates = self.list_templates()
                        if templates:
                            print(f"\n{Colors.system('Available Prompt Templates')} ({len(templates)}):")
                            print(f"{Colors.DIM}{'-' * 60}{Colors.RESET}")
                            for template in templates:
                                template_path = self.prompts_dir / f"{template}.md"
                                # Read first line for description if available
                                try:
                                    with open(template_path, 'r', encoding='utf-8') as f:
                                        first_line = f.readline().strip()
                                        # If first line is a comment, use it as description
                                        if first_line.startswith('#'):
                                            desc = first_line.lstrip('#').strip()
                                            print(f"  /{Colors.SUCCESS}{template}{Colors.RESET} - {Colors.DIM}{desc}{Colors.RESET}")
                                        else:
                                            print(f"  /{Colors.SUCCESS}{template}{Colors.RESET}")
                                except:
                                    print(f"  /{Colors.SUCCESS}{template}{Colors.RESET}")
                            print(f"{Colors.DIM}{'-' * 60}{Colors.RESET}")
                            print(Colors.system(f"Usage: /template_name <optional context>"))
                            print(Colors.system(f"Location: {self.prompts_dir}"))
                        else:
                            print(f"\n{Colors.system('No prompt templates found')}")
                            print(f"Create templates in: {self.prompts_dir}")
                            print(f"Example: {self.prompts_dir}/review.md")
                        continue
                    elif user_input.startswith('/') and len(user_input) > 1:
                        # Template command: /template_name <optional input>
                        parts = user_input[1:].split(maxsplit=1)
                        template_name = parts[0]
                        input_text = parts[1] if len(parts) > 1 else ""

                        # Try to load template
                        template = self.load_template(template_name, input_text)
                        if template:
                            print(Colors.system(f"✓ Loaded template: {template_name}"))
                            # Use the template as the user input
                            user_input = template
                        else:
                            print(Colors.error(f"Template not found: {template_name}"))
                            print(f"Available templates: {', '.join(self.list_templates()) or 'none'}")
                            print(f"Create at: {self.prompts_dir}/{template_name}.md")
                            continue
                    elif user_input.lower() == "clear":
                        # Clear screen (cross-platform)
                        os.system('clear' if os.name != 'nt' else 'cls')

                        # Reset agent session if factory available
                        if self.agent_factory:
                            try:
                                # Cleanup old agent if possible
                                if hasattr(self.agent, 'cleanup'):
                                    try:
                                        if asyncio.iscoroutinefunction(self.agent.cleanup):
                                            await self.agent.cleanup()
                                        else:
                                            self.agent.cleanup()
                                    except Exception as e:
                                        logger.debug(f"Error during agent cleanup: {e}")

                                # Create fresh agent instance
                                self.agent = self.agent_factory()
                                print(Colors.success("✓ Screen cleared and agent session reset"))
                                logger.info("Agent session reset via clear command")
                            except Exception as e:
                                print(Colors.error(f"⚠️  Could not reset agent session: {e}"))
                                logger.error(f"Failed to reset agent session: {e}")
                                print(Colors.system("Screen cleared but agent session maintained"))
                        else:
                            print(Colors.success("✓ Screen cleared"))

                        self.display_banner()
                        continue
                    elif user_input == "\\\\":  # Multi-line input trigger
                        user_input = await self.get_multiline_input()
                        if not user_input.strip():
                            continue
                    elif not user_input:
                        continue

                    # Process query through agent
                    logger.info(f"Processing query: {user_input[:100]}...")

                    # Update status bar before query
                    if self.status_bar:
                        self.status_bar.increment_query()
                        # Clear screen and redraw status bar
                        print("\033[2J\033[H", end='')  # Clear screen, move to top
                        print(self.status_bar.render())
                        print()  # Blank line after status bar

                    await self.process_query(user_input)

                except KeyboardInterrupt:
                    print(Colors.system(f"\n\nChat interrupted. Thanks for using {self.agent_name}!"))
                    break
                except EOFError:
                    print(Colors.system(f"\n\nChat ended. Thanks for using {self.agent_name}!"))
                    break

        finally:
            # Save command history
            save_readline_history(self.history_file)

            # Cleanup agent if it has cleanup method
            if hasattr(self.agent, 'cleanup'):
                try:
                    if asyncio.iscoroutinefunction(self.agent.cleanup):
                        await self.agent.cleanup()
                    else:
                        self.agent.cleanup()
                except Exception as e:
                    logger.warning(f"Error during agent cleanup: {e}")

            # Display session summary
            self.display_session_summary()

            print(Colors.success(f"\n{self.agent_name} session complete!"))

    def run(self):
        """Run the interactive chat loop."""
        try:
            asyncio.run(self._async_run())
        except KeyboardInterrupt:
            print(f"\n\nChat interrupted. Thanks for using {self.agent_name}!")
        except Exception as e:
            logger.error(f"Fatal error in chat loop: {e}", exc_info=True)
            print(f"\nFatal error: {e}")


def main():
    """Main entry point for the chat loop."""
    # Load environment variables FIRST, before any imports or parsing
    # This ensures credentials are available when agent modules are loaded
    env_path = load_environment_variables()

    parser = argparse.ArgumentParser(
        description="Generic Chat Loop for AWS Strands Agents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python AWS_Strands/chat_loop.py --agent AWS_Strands/Product_Pete/agent.py
    python AWS_Strands/chat_loop.py --agent AWS_Strands/DeepResearch_Quinten/agent.py
        """
    )

    parser.add_argument(
        '--agent',
        required=True,
        help='Path to the agent.py file (must expose root_agent)'
    )

    parser.add_argument(
        '--config',
        help='Path to configuration file (default: ~/.chatrc or .chatrc)'
    )

    args = parser.parse_args()

    try:
        # Load configuration FIRST (before any print statements)
        config = None
        if get_config:
            config_path = Path(args.config) if args.config else None
            config = get_config(config_path)

            # Apply color configuration immediately
            if config:
                color_config = config.get_section('colors')
                Colors.configure(color_config)

        # Now print messages with colors configured
        if env_path:
            print(Colors.system(f"Loaded environment from: {env_path}"))

        # Show config info
        if config:
            if args.config:
                print(Colors.system(f"Loaded configuration from: {args.config}"))
            else:
                # Check which config file was loaded
                global_config = Path.home() / '.chatrc'
                project_config = Path.cwd() / '.chatrc'
                if project_config.exists():
                    print(Colors.system(f"Loaded configuration from: {project_config}"))
                elif global_config.exists():
                    print(Colors.system(f"Loaded configuration from: {global_config}"))

        # Load the agent
        print(Colors.system(f"Loading agent from: {args.agent}"))
        agent, agent_name, agent_description = load_agent_module(args.agent)

        # Setup logging with agent name
        setup_logging(agent_name)

        if env_path:
            logger.info(f"Loaded environment from: {env_path}")

        print(Colors.success(f"Agent loaded successfully: {agent_name}"))
        logger.info(f"Agent loaded successfully: {agent_name} - {agent_description}")

        # Create agent factory for session reset
        def create_fresh_agent():
            """Factory function to create a fresh agent instance."""
            new_agent, _, _ = load_agent_module(args.agent)
            return new_agent

        # Start chat loop with config
        chat_loop = ChatLoop(agent, agent_name, agent_description, agent_factory=create_fresh_agent, config=config)
        chat_loop.run()

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
