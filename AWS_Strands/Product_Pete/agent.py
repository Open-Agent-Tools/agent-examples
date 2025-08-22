"""
Product Pete: A Product Manager AI assistant built with Strands Agents
Includes Atlassian MCP server for Jira/Confluence integration
Enhanced with production features: logging, error handling, security, and session management
"""

import os
import logging
import time
import re
from pathlib import Path
from typing import Dict, Any
from strands import Agent
from strands_tools import calculator, current_time, file_read, file_write  # type: ignore
from prompts import SYSTEM_PROMPT  # type: ignore

# Terminal colors and formatting
class Colors:
    """ANSI color codes for terminal formatting"""
    # Reset
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    
    # Colors
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Bright colors
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    
    # Background colors
    BG_BLUE = '\033[44m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'

def format_agent_response(text: str, use_colors: bool = True) -> str:
    """Format the agent response with colors and styling"""
    if not use_colors or not text:
        return text
    
    # Format headers (lines starting with #)
    lines = text.split('\n')
    formatted_lines = []
    
    for line in lines:
        stripped = line.strip()
        
        # Main headers (##, ###)
        if stripped.startswith('###'):
            formatted_lines.append(f"{Colors.BRIGHT_CYAN}{Colors.BOLD}{line}{Colors.RESET}")
        elif stripped.startswith('##'):
            formatted_lines.append(f"{Colors.BRIGHT_BLUE}{Colors.BOLD}{line}{Colors.RESET}")
        elif stripped.startswith('#'):
            formatted_lines.append(f"{Colors.BLUE}{Colors.BOLD}{line}{Colors.RESET}")
        
        # Bold sections (**text**)
        elif '**' in line:
            # Replace **text** with bold formatting
            line = re.sub(r'\*\*(.*?)\*\*', f'{Colors.BOLD}\\1{Colors.RESET}', line)
            formatted_lines.append(line)
        
        # Bullet points
        elif stripped.startswith(('•', '-', '*')) and not stripped.startswith('**'):
            formatted_lines.append(f"{Colors.BRIGHT_GREEN}  {stripped}{Colors.RESET}")
        
        # Numbered lists
        elif re.match(r'^\d+\.', stripped):
            formatted_lines.append(f"{Colors.BRIGHT_YELLOW}{line}{Colors.RESET}")
        
        # Questions or prompts
        elif '?' in stripped and len(stripped) < 100:
            formatted_lines.append(f"{Colors.CYAN}{line}{Colors.RESET}")
        
        # Code blocks or examples (lines with backticks)
        elif '`' in line:
            formatted_lines.append(f"{Colors.DIM}{Colors.WHITE}{line}{Colors.RESET}")
        
        # Normal text
        else:
            formatted_lines.append(line)
    
    return '\n'.join(formatted_lines)

def print_agent_response(text: str, use_colors: bool = True):
    """Print agent response with proper formatting"""
    if use_colors:
        formatted_text = format_agent_response(text, use_colors)
        print(formatted_text)
    else:
        formatted_text = text
        print(formatted_text)
    print()  # Add line break after agent response


# Configure logging
def setup_logging(console_output=False):
    """Set up comprehensive logging for the agent"""
    # Configure logging for all relevant modules to go to file only
    modules_to_configure = [
        "strands", "mcp", "httpx", "anthropic", "botocore", "boto3", 
        "__main__", "agent", "opentelemetry"
    ]
    
    for module_name in modules_to_configure:
        logging.getLogger(module_name).setLevel(logging.DEBUG)
    
    # Remove any existing handlers to avoid duplication
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Set up file logging for all output
    file_handler = logging.FileHandler("product_pete.log", mode="a")
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
    file_handler.setFormatter(file_formatter)
    
    # Configure root logger
    logging.basicConfig(
        level=logging.DEBUG,
        handlers=[file_handler],
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
    
    # If console output is requested (for debugging), add console handler
    if console_output:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter("%(levelname)s: %(message)s")
        console_handler.setFormatter(console_formatter)
        logging.getLogger().addHandler(console_handler)
    
    return logging.getLogger(__name__)


# PII redaction patterns and functions
PII_PATTERNS = {
    "email": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"),
    "ssn": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "phone": re.compile(r"\b\d{3}-\d{3}-\d{4}\b|\(\d{3}\)\s*\d{3}-\d{4}\b"),
    "credit_card": re.compile(r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b"),
    "person_name": re.compile(r"\b(?!\b)[A-Z][a-z]{2,}\s+[A-Z][a-z]{2,}\b"),
}


def redact_pii(text: str, enable_redaction: bool = True) -> str:
    """
    Redact personally identifiable information from text

    Args:
        text: Input text that may contain PII
        enable_redaction: Whether to actually perform redaction

    Returns:
        Text with PII redacted or original text if disabled
    """
    if not enable_redaction:
        return text

    redacted_text = text
    for pii_type, pattern in PII_PATTERNS.items():
        replacement = f"[{pii_type.upper()}]"
        redacted_text = pattern.sub(replacement, redacted_text)

    return redacted_text


def filter_content(text: str, enable_filtering: bool = True) -> tuple[str, bool]:
    """
    Basic content filtering for inappropriate content

    Args:
        text: Input text to filter
        enable_filtering: Whether to perform filtering

    Returns:
        Tuple of (filtered_text, is_safe)
    """
    if not enable_filtering:
        return text, True

    # Simple content filtering - can be expanded with more sophisticated filtering
    inappropriate_patterns = [
        r"\b(?:hate|violence|threat)\b",
        r"\b(?:attack|harm|hurt)\s+(?:someone|people|person)\b",
    ]

    for pattern in inappropriate_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return "[CONTENT FILTERED]", False

    return text, True


# Load .env file
try:
    from dotenv import load_dotenv

    for i in range(4):
        env_path = Path(__file__).parents[i] / ".env"
        if env_path.exists():
            load_dotenv(env_path)
            break
except ImportError:
    pass

# Logger will be initialized in main function based on command line args


# Session management
class ProductManagerSession:
    """
    Manages conversation context and state for Product Manager sessions
    """

    def __init__(self):
        self.session_id = str(int(time.time()))
        self.conversation_history = []
        self.context = {
            "user_role": "product_manager",
            "active_projects": [],
            "preferences": {
                "pii_redaction": True,
                "content_filtering": True,
                "debug_mode": os.getenv("DEBUG", "false").lower() == "true",
            },
        }
        self.metrics = {
            "total_queries": 0,
            "successful_responses": 0,
            "failed_responses": 0,
            "total_tokens": 0,
            "total_duration": 0.0,
        }
        logging.getLogger(__name__).info(f"Started new PM session: {self.session_id}")

    def add_interaction(
        self,
        query: str,
        response: str,
        success: bool,
        tokens: int = 0,
        duration: float = 0.0,
    ):
        """Add an interaction to the session history"""
        # Store only the original user query without context enhancement to prevent loops
        original_query = self._extract_original_query(query)
        
        interaction = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "query": original_query,  # Store clean original query only
            "response": response,  # PII redaction disabled
            "success": success,
            "tokens": tokens,
            "duration": duration,
        }
        self.conversation_history.append(interaction)
        
        # Keep conversation history manageable to prevent memory issues and context bloat
        if len(self.conversation_history) > 10:
            self.conversation_history = self.conversation_history[-10:]

        # Update metrics
        self.metrics["total_queries"] += 1
        if success:
            self.metrics["successful_responses"] += 1
        else:
            self.metrics["failed_responses"] += 1
        self.metrics["total_tokens"] += tokens
        self.metrics["total_duration"] += duration

    def get_context_summary(self) -> str:
        """Generate a context summary for the agent"""
        recent_interactions = (
            self.conversation_history[-3:] if self.conversation_history else []
        )
        context_items = []

        if recent_interactions:
            context_items.append("Recent conversation context:")
            for i, interaction in enumerate(recent_interactions, 1):
                context_items.append(f"{i}. User: {interaction['query'][:100]}...")

        if self.context.get("active_projects"):
            context_items.append(
                f"Active projects: {', '.join(self.context['active_projects'])}"
            )

        return "\n".join(context_items) if context_items else ""
    
    def _extract_original_query(self, query: str) -> str:
        """Extract the original user query from a potentially context-enhanced query"""
        # Check if this query contains context enhancement
        if "Recent conversation context:" in query and "Current request:" in query:
            # Extract just the current request part
            parts = query.split("Current request:")
            if len(parts) > 1:
                return parts[-1].strip()
        
        # Return the query as-is if no context enhancement detected
        return query

    def get_session_stats(self) -> Dict[str, Any]:
        """Get session statistics"""
        success_rate = (
            self.metrics["successful_responses"]
            / max(self.metrics["total_queries"], 1)
            * 100
        )
        avg_duration = self.metrics["total_duration"] / max(
            self.metrics["total_queries"], 1
        )

        return {
            "session_id": self.session_id,
            "total_queries": self.metrics["total_queries"],
            "success_rate": f"{success_rate:.1f}%",
            "total_tokens": self.metrics["total_tokens"],
            "avg_response_time": f"{avg_duration:.2f}s",
            "conversation_length": len(self.conversation_history),
        }


def robust_agent_call(
    agent: Agent, query: str, session: ProductManagerSession, max_retries: int = 3, logger=None
) -> Dict[str, Any]:
    """
    Robust agent call with error handling, retries, and security controls

    Args:
        agent: The Strands agent instance
        query: User query
        session: Current session context
        max_retries: Maximum number of retry attempts
        logger: Logger instance to use

    Returns:
        Dictionary with success status, response, and metadata
    """
    if logger is None:
        logger = logging.getLogger(__name__)
    enable_pii_redaction = False  # Disabled as it interferes with PM terminology
    enable_content_filtering = session.context["preferences"]["content_filtering"]

    # Pre-process query: PII redaction disabled, content filtering only
    processed_query = query  # redact_pii(query, enable_pii_redaction)
    filtered_query, is_safe = filter_content(processed_query, enable_content_filtering)

    if not is_safe:
        logger.warning(f"Content filtered for session {session.session_id}")
        return {
            "success": False,
            "response": "I can't process that request due to content policy restrictions. Please rephrase your question in a professional manner.",
            "error": "content_filtered",
            "attempt": 1,
            "tokens": 0,
            "duration": 0.0,
        }

    # Add session context to query if available (but prevent double enhancement)
    context_summary = session.get_context_summary()
    if context_summary and "Recent conversation context:" not in filtered_query:
        enhanced_query = f"{context_summary}\n\nCurrent request: {filtered_query}"
    else:
        enhanced_query = filtered_query

    # Retry loop with exponential backoff
    for attempt in range(max_retries):
        start_time = time.time()
        try:
            logger.info(
                f"Agent call attempt {attempt + 1} for session {session.session_id}"
            )

            # Make the agent call (streams directly to stdout)
            result = agent(enhanced_query)
            duration = time.time() - start_time

            # Extract response and metrics
            if hasattr(result, "message"):
                # Handle structured message response (dictionary format)
                if isinstance(result.message, dict) and "content" in result.message:
                    content = result.message["content"]
                    if isinstance(content, list):
                        # Extract text from content blocks
                        text_parts = []
                        for content_block in content:
                            if isinstance(content_block, dict) and "text" in content_block:
                                text_parts.append(content_block["text"])
                        response_text = "\n".join(text_parts) if text_parts else str(result.message)
                    else:
                        response_text = str(result.message)
                else:
                    response_text = str(result.message)
                
                # Get token usage if available
                try:
                    token_usage = result.metrics.get_summary()["accumulated_usage"][
                        "totalTokens"
                    ]
                except (AttributeError, KeyError):
                    token_usage = 0
            else:
                response_text = str(result)
                token_usage = 0

            # PII redaction disabled as it interferes with product management terminology
            processed_response = response_text

            # Validate response quality
            if len(processed_response.strip()) < 10:
                raise ValueError("Response too short, likely incomplete")

            if (
                "error" in processed_response.lower()
                and "sorry" in processed_response.lower()
            ):
                raise ValueError("Agent returned an error response")

            logger.info(
                f"Successful agent call (attempt {attempt + 1}, {duration:.2f}s, {token_usage} tokens)"
            )

            return {
                "success": True,
                "response": processed_response,
                "attempt": attempt + 1,
                "tokens": token_usage,
                "duration": duration,
                "metadata": {
                    "query_processed": processed_query != query,
                    "response_processed": processed_response != response_text,
                    "context_added": bool(context_summary),
                },
            }

        except Exception as e:
            duration = time.time() - start_time
            error_msg = str(e)
            logger.warning(f"Agent call failed (attempt {attempt + 1}): {error_msg}")

            if attempt == max_retries - 1:
                # Final attempt failed
                return {
                    "success": False,
                    "response": "I encountered an error processing your request. Please try rephrasing your question or try again later.",
                    "error": error_msg,
                    "attempt": attempt + 1,
                    "tokens": 0,
                    "duration": duration,
                }
            else:
                # Wait before retry (exponential backoff)
                wait_time = 2**attempt
                logger.info(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)

    # This shouldn't be reached, but just in case
    return {
        "success": False,
        "response": "Maximum retries exceeded",
        "error": "max_retries_exceeded",
        "attempt": max_retries,
        "tokens": 0,
        "duration": 0.0,
    }


# Create agent with enhanced configuration
def create_agent(logger=None):
    if logger is None:
        logger = logging.getLogger(__name__)

    # Model configuration with fallback
    if os.getenv("ANTHROPIC_API_KEY"):
        try:
            from strands.models.anthropic import AnthropicModel

            model = AnthropicModel(
                model_id="claude-3-5-sonnet-20241022",
                max_tokens=4096,
                temperature=0.3,  # More deterministic for product management tasks
            )
            logger.info("Using Anthropic Direct API")
        except ImportError:
            logger.warning("Anthropic library not available, falling back to Bedrock")
            model = "anthropic.claude-3-7-sonnet-20250219-v1:0"
            logger.info("Using Bedrock (Anthropic import failed)")
    else:
        logger.warning("No ANTHROPIC_API_KEY found, using Bedrock")
        model = "anthropic.claude-3-7-sonnet-20250219-v1:0"
        logger.info("Using Bedrock (no Anthropic API key)")

    # Setup basic tools
    tools = [calculator, current_time, file_read, file_write]
    logger.info(f"Loaded basic tools: {len(tools)} tools")

    # Add Atlassian MCP tools with enhanced error handling
    mcp_tools_count = 0
    mcp_client_instance = None

    try:
        from mcp.client.streamable_http import streamablehttp_client
        from strands.tools.mcp.mcp_client import MCPClient

        def create_streamable_http_transport():
            return streamablehttp_client("http://localhost:9000/mcp/")

        logger.info("Attempting to connect to Atlassian MCP server...")

        # Keep the MCP client instance alive - don't use context manager here
        mcp_client_instance = MCPClient(create_streamable_http_transport)

        # Start the MCP client and get tools
        try:
            # Start the client to make the session active
            mcp_client_instance.start()

            # Now list the tools using the sync method
            mcp_tools_paginated = mcp_client_instance.list_tools_sync()
            mcp_tools = list(
                mcp_tools_paginated
            )  # Convert PaginatedList to regular list
            tools.extend(mcp_tools)
            mcp_tools_count = len(mcp_tools)
            logger.info(
                f"✅ Connected to Atlassian MCP server ({mcp_tools_count} tools added)"
            )
            logger.info("MCP client session started and ready for tool execution")
        except Exception as mcp_error:
            logger.warning(f"MCP server connection failed: {mcp_error}")
            logger.info(
                "Continuing without MCP integration - agent will work with basic tools"
            )
            mcp_client_instance = None

    except ImportError as import_error:
        logger.warning(f"MCP libraries not available: {import_error}")
        logger.info(
            "Continuing without MCP integration - install MCP client libraries for Atlassian integration"
        )
    except Exception as e:
        logger.error(f"Failed to initialize MCP client: {e}")
        logger.info("Continuing without MCP integration")

    # Create the agent with security configurations
    try:
        # Enhanced system prompt with security context
        enhanced_system_prompt = f"""{SYSTEM_PROMPT}

## Security & Privacy Notice
- PII (personally identifiable information) will be automatically redacted in conversations
- Content filtering is enabled to ensure professional interactions
- All interactions are logged for quality and security purposes
- Session context is maintained to provide better assistance

## Available Tools Summary
- Basic tools: {len(tools) - mcp_tools_count} (calculator, file operations, time)
- MCP tools: {mcp_tools_count} (Atlassian integration {"enabled" if mcp_tools_count > 0 else "disabled"})
- Total tools available: {len(tools)}
"""

        agent = Agent(model=model, tools=tools, system_prompt=enhanced_system_prompt)

        logger.info(f"✅ Agent created successfully with {len(tools)} tools")
        return agent

    except Exception as e:
        logger.error(f"Failed to create agent: {e}")
        raise


# Agent will be initialized in main function with proper logging


def display_welcome(use_colors: bool = True):
    """Display welcome message and agent capabilities"""
    if use_colors:
        print(f"\n{Colors.BRIGHT_MAGENTA}{Colors.BOLD}🚀 Product Pete{Colors.RESET} - Your AI Product Management Assistant")
        display_help(use_colors)
        print(f"\n{Colors.DIM}Type 'help' for commands, 'exit' to quit{Colors.RESET}\n")
    else:
        print("\n🚀 Product Pete - Your AI Product Management Assistant")
        display_help(use_colors)
        print("\nType 'help' for commands, 'exit' to quit\n")


def display_help(use_colors: bool = True):
    """Display help information"""
    if use_colors:
        print(f"""
{Colors.BRIGHT_CYAN}{Colors.BOLD}🔧 Product Pete Help{Colors.RESET}

{Colors.BRIGHT_GREEN}Core Capabilities:{Colors.RESET}
{Colors.GREEN}• User Story Creation{Colors.RESET} - "Create a user story for user authentication"
{Colors.GREEN}• Product Planning{Colors.RESET} - "Help me prioritize features for Q2"
{Colors.GREEN}• Requirements Analysis{Colors.RESET} - "Review these requirements for gaps"
{Colors.GREEN}• Stakeholder Communication{Colors.RESET} - "Draft an update for leadership"
{Colors.GREEN}• Agile/Scrum Support{Colors.RESET} - "Plan our next sprint"

{Colors.BRIGHT_YELLOW}Special Commands:{Colors.RESET}
{Colors.YELLOW}• 'stats'{Colors.RESET} - View session statistics and metrics
{Colors.YELLOW}• 'context'{Colors.RESET} - View current conversation context
{Colors.YELLOW}• 'logs'{Colors.RESET} - Show log file location
{Colors.YELLOW}• 'help'{Colors.RESET} - Show this help message
{Colors.YELLOW}• 'exit'{Colors.RESET} - End session

{Colors.CYAN}For best results, be specific about your product management needs!{Colors.RESET}
        """)
    else:
        help_text = """
🔧 Product Pete Help

Core Capabilities:
• User Story Creation - "Create a user story for user authentication"
• Product Planning - "Help me prioritize features for Q2"
• Requirements Analysis - "Review these requirements for gaps"
• Stakeholder Communication - "Draft an update for leadership"
• Agile/Scrum Support - "Plan our next sprint"

Special Commands:
• 'stats' - View session statistics and metrics
• 'context' - View current conversation context
• 'logs' - Show log file location
• 'help' - Show this help message
• 'exit' - End session

For best results, be specific about your product management needs!
        """
        print(help_text)


if __name__ == "__main__":
    import sys
    
    # Check command line arguments
    console_logging = "--verbose" in sys.argv or "-v" in sys.argv
    use_colors = "--no-color" not in sys.argv
    
    # Set up logging (quiet by default)
    logger = setup_logging(console_output=console_logging)
    
    # Initialize agent with logger
    logger.info("Initializing Product Pete agent...")
    try:
        agent = create_agent(logger)
        logger.info("Agent initialization complete")
    except Exception as e:
        print(f"Error initializing agent: {e}")
        print("Please check product_pete.log for details")
        sys.exit(1)
    
    # Initialize session
    session = ProductManagerSession()
    
    # Log startup but don't print to console
    logger.info("Product Pete agent ready for interaction")
    
    # Display clean welcome
    display_welcome(use_colors)
    
    # Main interaction loop
    try:
        while True:
            try:
                # Ensure clean terminal state and single prompt with color
                sys.stdout.flush()
                prompt = f"{Colors.BRIGHT_WHITE}{Colors.BOLD}You:{Colors.RESET} " if use_colors else "You: "
                user_input = input(prompt).strip()
                sys.stdout.flush()

                # Handle special commands
                if user_input.lower() in ["exit", "quit", "bye"]:
                    break
                elif user_input.lower() == "help":
                    display_help(use_colors)
                    continue
                elif user_input.lower() == "stats":
                    stats = session.get_session_stats()
                    if use_colors:
                        print(f"\n{Colors.BRIGHT_BLUE}📊 Session Statistics:{Colors.RESET}")
                        print(f"   {Colors.CYAN}Total Queries:{Colors.RESET} {stats['total_queries']}")
                        print(f"   {Colors.CYAN}Success Rate:{Colors.RESET} {stats['success_rate']}")
                        print(f"   {Colors.CYAN}Total Tokens:{Colors.RESET} {stats['total_tokens']}")
                        print(f"   {Colors.CYAN}Avg Response Time:{Colors.RESET} {stats['avg_response_time']}")
                    else:
                        print("\n📊 Session Statistics:")
                        print(f"   Total Queries: {stats['total_queries']}")
                        print(f"   Success Rate: {stats['success_rate']}")
                        print(f"   Total Tokens: {stats['total_tokens']}")
                        print(f"   Avg Response Time: {stats['avg_response_time']}")
                    continue
                elif user_input.lower() == "context":
                    context = session.get_context_summary()
                    if context:
                        if use_colors:
                            print(f"\n{Colors.BRIGHT_GREEN}🧠 Current Context:{Colors.RESET}")
                            print(f"{Colors.DIM}{context}{Colors.RESET}")
                        else:
                            print(f"\n🧠 Current Context:\n{context}")
                    else:
                        if use_colors:
                            print(f"\n{Colors.DIM}🧠 No conversation context yet{Colors.RESET}")
                        else:
                            print("\n🧠 No conversation context yet")
                    continue
                elif user_input.lower() == "logs":
                    if use_colors:
                        print(f"\n{Colors.BRIGHT_YELLOW}📝 All diagnostic information is being logged to:{Colors.RESET} {Colors.BOLD}product_pete.log{Colors.RESET}")
                        print(f"   {Colors.DIM}Use 'tail -f product_pete.log' to monitor in real-time{Colors.RESET}")
                    else:
                        print("\n📝 All diagnostic information is being logged to: product_pete.log")
                        print("   Use 'tail -f product_pete.log' to monitor in real-time")
                    continue

                # Skip empty inputs
                if not user_input:
                    continue

                # Log the user query
                logger.info(f"User query: {user_input}")
                
                result = robust_agent_call(agent, user_input, session, max_retries=3, logger=logger)

                # Agent already streamed response, just add spacing and log
                if result["success"]:
                    print()  # Add line break after streamed response
                    logger.info(f"Response delivered successfully (tokens: {result['tokens']}, duration: {result['duration']:.2f}s)")
                else:
                    # Error responses (not streamed)
                    print(f"\n\n{result['response']}")
                    print()  # Add line break after error response
                    logger.warning(f"Response failed: {result.get('error', 'unknown')}")

                # Add to session history
                session.add_interaction(
                    query=user_input,
                    response=result["response"],
                    success=result["success"],
                    tokens=result["tokens"],
                    duration=result["duration"],
                )

                # Ensure proper terminal state
                sys.stdout.flush()
                sys.stderr.flush()

            except (KeyboardInterrupt, EOFError):
                print("\n\nGoodbye!")
                break
            except Exception as e:
                logger.error(f"Unexpected error in main loop: {e}")
                print(f"Sorry, I encountered an error. Please try again or type 'exit' to quit.")

    finally:
        # Log final stats but keep console output minimal
        stats = session.get_session_stats()
        logger.info(f"Session ended - Queries: {stats['total_queries']}, Success Rate: {stats['success_rate']}, Tokens: {stats['total_tokens']}")
        
        if stats['total_queries'] > 0:
            print(f"\nSession complete: {stats['total_queries']} queries, {stats['success_rate']} success rate")
            print(f"Full session details logged to: product_pete.log")
        
        print("\n👋 Thanks for using Product Pete!")
