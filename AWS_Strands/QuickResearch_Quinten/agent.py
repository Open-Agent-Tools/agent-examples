"""
Quick Research Quinten Agent Implementation

A specialized quick research agent built on AWS Strands framework for rapid
information gathering and immediate insights across any domain.
"""

import asyncio
import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from strands import Agent, tool
import logging

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

try:
    from .prompts import SYSTEM_PROMPT
except ImportError:
    from prompts import SYSTEM_PROMPT

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QuickResearchSession:
    """Manages quick research session state and tracking."""
    
    def __init__(self, query: str):
        self.query = query
        self.start_time = datetime.now()
        self.sources = []
        self.key_findings = []
        self.insights = []
        self.status = "initialized"
        
    def add_source(self, source: Dict[str, Any]) -> None:
        """Add a research source with metadata."""
        self.sources.append({
            **source,
            "added_at": datetime.now().isoformat(),
            "credibility": self._assess_credibility(source)
        })
        
    def add_finding(self, finding: str, source: str = None) -> None:
        """Add a key finding from research."""
        self.key_findings.append({
            "finding": finding,
            "source": source,
            "discovered_at": datetime.now().isoformat()
        })
        
    def add_insight(self, insight: str) -> None:
        """Add an actionable insight."""
        self.insights.append({
            "insight": insight,
            "generated_at": datetime.now().isoformat()
        })
        
    def get_summary(self) -> Dict[str, Any]:
        """Get session summary for reporting."""
        duration = datetime.now() - self.start_time
        
        return {
            "query": self.query,
            "duration_seconds": duration.total_seconds(),
            "sources_count": len(self.sources),
            "findings_count": len(self.key_findings),
            "insights_count": len(self.insights),
            "status": self.status
        }
        
    def _assess_credibility(self, source: Dict[str, Any]) -> str:
        """Assess source credibility based on metadata."""
        url = source.get("url", "").lower()
        title = source.get("title", "").lower()
        
        high_credibility = [
            ".edu", ".gov", ".org", "arxiv", "doi.org", "ieee", "acm",
            "official documentation", "api reference", "wikipedia"
        ]
        
        medium_credibility = [
            "stackoverflow", "github", "medium", "towards", "papers", "reddit"
        ]
        
        for indicator in high_credibility:
            if indicator in url or indicator in title:
                return "high"
                
        for indicator in medium_credibility:
            if indicator in url or indicator in title:
                return "medium"
                
        return "needs_verification"

class QuickResearchQuinten:
    """Quick Research Quinten agent for rapid research tasks."""
    
    def __init__(self, model_provider: str = "anthropic/claude-3-5-sonnet-20241022"):
        self.model_provider = model_provider
        self.agent = None
        self.current_session = None
        self._tavily_client = None  # Will hold MCP client reference if connected
        
    def create_agent(self) -> Agent:
        """Create and configure the quick research agent."""
        try:
            # Model configuration with fallback based on available API keys
            model = self._get_model_config()
            
            # Configure MCP tools for research
            tools = self._setup_research_tools()
            
            # Create agent with research tools
            agent = Agent(
                name="Quick Research Quinten", 
                description="A specialized quick research agent for rapid information gathering and insights",
                model=model,
                system_prompt=SYSTEM_PROMPT,
                tools=tools
            )
            
            logger.info(f"Quick Research Quinten agent created successfully with {len(tools)} tools")
            return agent
            
        except Exception as e:
            logger.error(f"Error creating agent: {str(e)}")
            raise
    
    def _setup_research_tools(self) -> List:
        """Setup research tools including Tavily MCP for web search."""
        tools = []
        
        # Connect to Tavily HTTP MCP server for web search
        tavily_key = os.getenv("TAVILY_API_KEY")
        if tavily_key:
            try:
                from mcp.client.streamable_http import streamablehttp_client
                from strands.tools.mcp import MCPClient
                
                # Create MCP client for Tavily's hosted HTTP server
                tavily_mcp_client = MCPClient(
                    lambda: streamablehttp_client(
                        url=f"https://mcp.tavily.com/mcp/?tavilyApiKey={tavily_key}"
                    )
                )
                
                # Start the MCP client and get available tools
                tavily_mcp_client.__enter__()
                tavily_tools = tavily_mcp_client.list_tools_sync()
                
                # Add all Tavily tools to the agent's toolkit
                for tool in tavily_tools:
                    tools.append(tool)
                    
                logger.info(f"✓ Connected to Tavily MCP - {len(tavily_tools)} search tools added")
                for tool in tavily_tools[:3]:  # Log first 3 tools
                    logger.info(f"  - {tool.tool_name}: {tool.mcp_tool.description[:50]}...")
                
                # Store client reference for cleanup
                self._tavily_client = tavily_mcp_client
                
            except ImportError as e:
                logger.warning(f"MCP dependencies missing: {e}")
                logger.info("Falling back to generic MCP client tool")
                try:
                    from strands_tools.mcp_client import mcp_client
                    tools.append(mcp_client)
                    logger.info("✓ Added generic MCP client (manual connection required)")
                except ImportError:
                    logger.warning("No MCP client available")
                    
            except Exception as e:
                logger.error(f"Failed to connect to Tavily MCP: {e}")
                # Fallback to generic MCP client
                try:
                    from strands_tools.mcp_client import mcp_client
                    tools.append(mcp_client)
                    logger.info("✓ Added generic MCP client as fallback")
                except ImportError:
                    pass
        else:
            logger.warning("No TAVILY_API_KEY found, web search disabled")
        
        # Add HTTP request tool for additional research capabilities  
        try:
            from strands_tools.http_request import http_request
            tools.append(http_request)
            logger.info("✓ Added HTTP request tool")
        except ImportError:
            logger.debug("HTTP request tool not available")
        
        if not tools:
            logger.warning("No research tools available - agent will use only LLM knowledge")
        else:
            logger.info(f"Research tools configured: {len(tools)} tools available")
            
        return tools
    
    def _get_model_config(self):
        """Get model configuration based on provider and available API keys."""
        # If user specified a specific model, try to honor it
        if self.model_provider.startswith("anthropic/") and os.getenv("ANTHROPIC_API_KEY"):
            try:
                from strands.models.anthropic import AnthropicModel
                
                # Extract model ID from provider string
                model_id = self.model_provider.split("/", 1)[1]
                
                model = AnthropicModel(
                    model_id=model_id,
                    max_tokens=4096,
                    temperature=0.3,  # Slightly higher for quick research creativity
                )
                logger.info(f"Using Anthropic Direct API: {model_id}")
                return model
                
            except ImportError:
                logger.warning("Anthropic library not available, falling back to Bedrock")
                return "anthropic.claude-3-7-sonnet-20250219-v1:0"
                
        elif self.model_provider.startswith("openai/") and os.getenv("OPENAI_API_KEY"):
            try:
                from strands.models.openai import OpenAIModel
                
                # Extract model ID from provider string
                model_id = self.model_provider.split("/", 1)[1]
                
                model = OpenAIModel(
                    model_id=model_id,
                    max_tokens=4096,
                    temperature=0.3,
                )
                logger.info(f"Using OpenAI Direct API: {model_id}")
                return model
                
            except ImportError:
                logger.warning("OpenAI library not available")
                return self.model_provider
                
        elif self.model_provider.startswith("google/") and os.getenv("GOOGLE_API_KEY"):
            logger.info(f"Using Google model: {self.model_provider}")
            return self.model_provider
        
        # Fallback logic based on available API keys
        if os.getenv("ANTHROPIC_API_KEY"):
            try:
                from strands.models.anthropic import AnthropicModel
                
                model = AnthropicModel(
                    model_id="claude-3-5-sonnet-20241022",
                    max_tokens=4096,
                    temperature=0.3,
                )
                logger.info("Using Anthropic Direct API (fallback)")
                return model
                
            except ImportError:
                logger.warning("Anthropic library not available, using Bedrock")
                return "anthropic.claude-3-7-sonnet-20250219-v1:0"
                
        elif os.getenv("OPENAI_API_KEY"):
            try:
                from strands.models.openai import OpenAIModel
                
                model = OpenAIModel(
                    model_id="gpt-4",
                    max_tokens=4096,
                    temperature=0.3,
                )
                logger.info("Using OpenAI Direct API (fallback)")
                return model
                
            except ImportError:
                logger.warning("OpenAI library not available")
                return "openai/gpt-4"
                
        else:
            logger.warning("No API keys found, using Bedrock fallback")
            return "anthropic.claude-3-7-sonnet-20250219-v1:0"
            
    async def quick_research(self, query: str, max_sources: int = 5) -> str:
        """Conduct quick research for immediate insights."""
        try:
            if not self.agent:
                self.agent = self.create_agent()
            
            # Create session for tracking
            self.current_session = QuickResearchSession(query)
            self.current_session.status = "active"
            
            prompt = f"""
            Quick Research Query: {query}
            
            Please provide a rapid but thorough research response including:
            
            1. **Key Points**: 5-7 essential findings (bullet points)
            2. **Primary Sources**: {max_sources} most relevant sources with credibility notes
            3. **Quick Analysis**: Brief assessment of findings reliability
            4. **Immediate Insights**: 2-3 actionable takeaways
            5. **Follow-up Questions**: Areas that might need deeper research
            
            Focus on speed while maintaining research quality standards.
            """
            
            response = await self.robust_agent_call(prompt)
            
            self.current_session.status = "completed"
            logger.info(f"Quick research completed for: {query}")
            
            return response
            
        except Exception as e:
            logger.error(f"Error in quick research: {str(e)}")
            if self.current_session:
                self.current_session.status = "error"
            raise
            
    async def compare_options(self, options: List[str], criteria: List[str] = None) -> str:
        """Conduct quick comparative research analysis."""
        try:
            if not self.agent:
                self.agent = self.create_agent()
            
            # Default criteria if none provided
            if not criteria:
                criteria = ["features", "pros", "cons", "use cases", "cost"]
            
            prompt = f"""
            Quick Comparative Analysis
            
            Options to Compare: {', '.join(options)}
            Evaluation Criteria: {', '.join(criteria)}
            
            Please conduct rapid comparative research:
            
            1. **Quick Overview**: Brief description of each option (2-3 sentences)
            2. **Comparison Matrix**: Side-by-side comparison on criteria
            3. **Key Differentiators**: Main distinguishing factors
            4. **Quick Recommendation**: Best choice with brief rationale
            5. **Decision Framework**: When to choose each option (bullet points)
            
            Keep analysis concise and actionable.
            """
            
            response = await self.robust_agent_call(prompt)
            logger.info(f"Quick comparative analysis completed for: {', '.join(options)}")
            return response
            
        except Exception as e:
            logger.error(f"Error in comparative analysis: {str(e)}")
            raise
            
    async def fact_check(self, claim: str) -> str:
        """Quick fact-checking with sources."""
        try:
            if not self.agent:
                self.agent = self.create_agent()
                
            prompt = f"""
            Fact Check Request: {claim}
            
            Please provide rapid fact-checking:
            
            1. **Verdict**: TRUE / FALSE / PARTIALLY TRUE / UNVERIFIABLE
            2. **Evidence**: 2-3 key pieces of supporting/refuting evidence
            3. **Sources**: Most authoritative sources (with dates)
            4. **Context**: Important context or nuance (if applicable)
            5. **Confidence**: High / Medium / Low confidence in verdict
            
            Be concise but thorough in verification.
            """
            
            response = await self.robust_agent_call(prompt)
            logger.info(f"Fact check completed for: {claim[:50]}...")
            return response
            
        except Exception as e:
            logger.error(f"Error in fact checking: {str(e)}")
            raise
            
    async def trend_analysis(self, topic: str) -> str:
        """Quick analysis of current trends."""
        try:
            if not self.agent:
                self.agent = self.create_agent()
                
            prompt = f"""
            Trend Analysis: {topic}
            
            Please provide rapid trend analysis:
            
            1. **Current State**: What's happening now (3-4 points)
            2. **Recent Developments**: Key changes in last 3-6 months
            3. **Emerging Patterns**: Notable trends gaining momentum
            4. **Key Players**: Main organizations/people driving trends
            5. **Short-term Outlook**: Expected developments (next 3-6 months)
            
            Focus on actionable trend insights.
            """
            
            response = await self.robust_agent_call(prompt)
            logger.info(f"Trend analysis completed for: {topic}")
            return response
            
        except Exception as e:
            logger.error(f"Error in trend analysis: {str(e)}")
            raise
            
    async def robust_agent_call(self, prompt: str, max_retries: int = 3) -> str:
        """Make robust agent calls with retry logic."""
        for attempt in range(max_retries):
            try:
                if not self.agent:
                    self.agent = self.create_agent()
                    
                # Strands agents work synchronously, so wrap in async
                response = await asyncio.get_event_loop().run_in_executor(
                    None, self.agent, prompt
                )
                return response.message
                
            except Exception as e:
                logger.warning(f"Agent call attempt {attempt + 1} failed: {str(e)}")
                if attempt == max_retries - 1:
                    logger.error(f"All agent call attempts failed: {str(e)}")
                    raise
                    
                # Wait before retry
                await asyncio.sleep(2 ** attempt)
                
    def get_session_status(self) -> Optional[Dict[str, Any]]:
        """Get current session status."""
        if not self.current_session:
            return None
            
        return self.current_session.get_summary()
    
    def cleanup(self):
        """Clean up resources including MCP client connection."""
        if self._tavily_client:
            try:
                self._tavily_client.__exit__(None, None, None)
                logger.info("Tavily MCP client connection closed")
            except Exception as e:
                logger.warning(f"Error closing Tavily MCP client: {e}")
            finally:
                self._tavily_client = None

# Convenience function for direct usage
def create_agent() -> Agent:
    """Create Quick Research Quinten agent instance."""
    research_quinten = QuickResearchQuinten()
    return research_quinten.create_agent()

# Root agent instance for module-level access
root_agent = create_agent()

# Simple test function for local execution
def main():
    """Simple test function to verify QuickResearch_Quinten works."""
    print("Testing Quick Research Quinten...")
    
    try:
        response = root_agent("What are the key features of Python 3.13?")
        print(f"Agent Response: {response}")
    except Exception as e:
        logger.error(f"Test failed: {e}")
        print(f"Error: {e}")

if __name__ == "__main__":
    main()