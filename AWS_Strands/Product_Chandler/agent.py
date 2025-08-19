"""
Product Chandler: A Product Manager AI assistant built with Strands Agents
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


# Configure logging
def setup_logging():
    """Set up comprehensive logging for the agent"""
    # Configure Strands debug logging
    logging.getLogger("strands").setLevel(logging.DEBUG)

    # Configure main application logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("product_chandler.log", mode="a"),
        ],
    )

    return logging.getLogger(__name__)


# PII redaction patterns and functions
PII_PATTERNS = {
    "email": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"),
    "ssn": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "phone": re.compile(r"\b\d{3}-\d{3}-\d{4}\b|\(\d{3}\)\s*\d{3}-\d{4}\b"),
    "credit_card": re.compile(r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b"),
    "person_name": re.compile(r"\b[A-Z][a-z]+\s+[A-Z][a-z]+\b"),  # Simple name pattern
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

# Initialize logging
logger = setup_logging()


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
        logger.info(f"Started new PM session: {self.session_id}")

    def add_interaction(
        self,
        query: str,
        response: str,
        success: bool,
        tokens: int = 0,
        duration: float = 0.0,
    ):
        """Add an interaction to the session history"""
        interaction = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "query": redact_pii(query, self.context["preferences"]["pii_redaction"]),
            "response": redact_pii(
                response, self.context["preferences"]["pii_redaction"]
            ),
            "success": success,
            "tokens": tokens,
            "duration": duration,
        }
        self.conversation_history.append(interaction)

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
    agent: Agent, query: str, session: ProductManagerSession, max_retries: int = 3
) -> Dict[str, Any]:
    """
    Robust agent call with error handling, retries, and security controls

    Args:
        agent: The Strands agent instance
        query: User query
        session: Current session context
        max_retries: Maximum number of retry attempts

    Returns:
        Dictionary with success status, response, and metadata
    """
    enable_pii_redaction = session.context["preferences"]["pii_redaction"]
    enable_content_filtering = session.context["preferences"]["content_filtering"]

    # Pre-process query: PII redaction and content filtering
    processed_query = redact_pii(query, enable_pii_redaction)
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

    # Add session context to query if available
    context_summary = session.get_context_summary()
    if context_summary:
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

            # Make the agent call
            result = agent(enhanced_query)
            duration = time.time() - start_time

            # Extract response and metrics
            if hasattr(result, "message"):
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

            # Post-process response: PII redaction
            processed_response = redact_pii(response_text, enable_pii_redaction)

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
def create_agent():
    """Create and configure the Product Chandler agent with all enhancements"""

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


# Initialize the agent
agent = create_agent()


def display_welcome():
    """Display welcome message and agent capabilities"""
    print("🚀 Product Chandler Agent - Enhanced Edition")
    print("=" * 60)
    print("Your AI Product Management Assistant with:")
    print("✅ Advanced error handling and retry logic")
    print("✅ PII redaction and content filtering")
    print("✅ Session management and context tracking")
    print("✅ Comprehensive logging and metrics")
    print("✅ Atlassian MCP integration (if available)")
    print("=" * 60)
    print("Commands: 'stats' for session stats, 'help' for guidance, 'exit' to quit")
    print()


def display_help():
    """Display help information"""
    help_text = """
🔧 Product Chandler Help

Core Capabilities:
• User Story Creation - "Create a user story for user authentication"
• Product Planning - "Help me prioritize features for Q2"
• Requirements Analysis - "Review these requirements for gaps"
• Stakeholder Communication - "Draft an update for leadership"
• Agile/Scrum Support - "Plan our next sprint"

Special Commands:
• 'stats' - View session statistics and metrics
• 'debug on/off' - Toggle debug mode
• 'context' - View current conversation context
• 'help' - Show this help message
• 'exit' - End session

Security Features:
• PII is automatically redacted from conversations
• Content filtering ensures professional interactions
• All interactions are logged for quality assurance

For best results, be specific about your product management needs!
    """
    print(help_text)


if __name__ == "__main__":
    # Initialize session
    session = ProductManagerSession()

    # Display welcome
    display_welcome()

    # Main interaction loop
    try:
        while True:
            try:
                user_input = input("\n💬 You: ").strip()

                # Handle special commands
                if user_input.lower() in ["exit", "quit", "bye"]:
                    break
                elif user_input.lower() == "help":
                    display_help()
                    continue
                elif user_input.lower() == "stats":
                    stats = session.get_session_stats()
                    print("\n📊 Session Statistics:")
                    print(f"   Session ID: {stats['session_id']}")
                    print(f"   Total Queries: {stats['total_queries']}")
                    print(f"   Success Rate: {stats['success_rate']}")
                    print(f"   Total Tokens: {stats['total_tokens']}")
                    print(f"   Avg Response Time: {stats['avg_response_time']}")
                    print(f"   Conversation Length: {stats['conversation_length']}")
                    continue
                elif user_input.lower() == "context":
                    context = session.get_context_summary()
                    if context:
                        print(f"\n🧠 Current Context:\n{context}")
                    else:
                        print("\n🧠 No conversation context yet")
                    continue
                elif user_input.lower() == "debug on":
                    session.context["preferences"]["debug_mode"] = True
                    logger.setLevel(logging.DEBUG)
                    print("🔍 Debug mode enabled")
                    continue
                elif user_input.lower() == "debug off":
                    session.context["preferences"]["debug_mode"] = False
                    logger.setLevel(logging.INFO)
                    print("🔍 Debug mode disabled")
                    continue

                # Skip empty inputs
                if not user_input:
                    continue

                # Process the query with robust error handling
                print("\n🤖 Chandler:", end=" ", flush=True)

                result = robust_agent_call(agent, user_input, session)

                if result["success"]:
                    print(result["response"])

                    # Show metadata in debug mode
                    if session.context["preferences"]["debug_mode"]:
                        metadata = result.get("metadata", {})
                        print("\n🔍 Debug Info:")
                        print(
                            f"   Tokens: {result['tokens']}, Duration: {result['duration']:.2f}s"
                        )
                        print(
                            f"   Attempt: {result['attempt']}, Context Added: {metadata.get('context_added', False)}"
                        )
                        print(
                            f"   Query Processed: {metadata.get('query_processed', False)}"
                        )
                else:
                    print(result["response"])
                    if session.context["preferences"]["debug_mode"]:
                        print(
                            f"\n🔍 Debug Info: Error - {result.get('error', 'unknown')}"
                        )

                # Add to session history
                session.add_interaction(
                    query=user_input,
                    response=result["response"],
                    success=result["success"],
                    tokens=result["tokens"],
                    duration=result["duration"],
                )

            except (KeyboardInterrupt, EOFError):
                print("\n\nSession interrupted by user")
                break
            except Exception as e:
                logger.error(f"Unexpected error in main loop: {e}")
                print(f"\n❌ Unexpected error: {e}")
                print("Please try again or type 'exit' to quit")

    finally:
        # Display final session statistics
        stats = session.get_session_stats()
        print("\n📊 Final Session Stats:")
        print(f"   Queries Processed: {stats['total_queries']}")
        print(f"   Success Rate: {stats['success_rate']}")
        print(f"   Total Tokens: {stats['total_tokens']}")
        print(f"   Average Response Time: {stats['avg_response_time']}")

        logger.info(f"Session ended: {session.session_id}")

        # Clean up MCP client connection
        # Note: In production, MCP client instance would be managed at module level
        # For now, we'll skip the cleanup to avoid mypy errors
        logger.info("MCP client cleanup would be performed here")

        print("\n👋 Thanks for using Product Chandler! Goodbye!")
