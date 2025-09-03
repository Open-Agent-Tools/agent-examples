"""
Deep Research Dave Agent Implementation

A specialized research agent built on AWS Strands framework for comprehensive
information gathering, analysis, and synthesis across any domain.
"""

import asyncio
import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

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

class ResearchSession:
    """Manages research session state and progress tracking."""
    
    def __init__(self, topic: str, research_type: str = "comprehensive"):
        self.topic = topic
        self.research_type = research_type
        self.start_time = datetime.now()
        self.sources = []
        self.findings = {}
        self.insights = []
        self.status = "initialized"
        self.current_phase = "planning"
        self.confidence_level = "unknown"
        
    def add_source(self, source: Dict[str, Any]) -> None:
        """Add a research source with metadata."""
        self.sources.append({
            **source,
            "added_at": datetime.now().isoformat(),
            "credibility": self._assess_credibility(source)
        })
        
    def add_finding(self, category: str, finding: Dict[str, Any]) -> None:
        """Add a research finding to a specific category."""
        if category not in self.findings:
            self.findings[category] = []
        
        self.findings[category].append({
            **finding,
            "discovered_at": datetime.now().isoformat()
        })
        
    def add_insight(self, insight: str, evidence: List[str] = None) -> None:
        """Add a synthesized insight with supporting evidence."""
        self.insights.append({
            "insight": insight,
            "evidence": evidence or [],
            "generated_at": datetime.now().isoformat()
        })
        
    def update_phase(self, phase: str) -> None:
        """Update current research phase."""
        self.current_phase = phase
        logger.info(f"Research phase updated to: {phase}")
        
    def update_confidence(self, level: str) -> None:
        """Update overall confidence level in findings."""
        self.confidence_level = level
        
    def get_summary(self) -> Dict[str, Any]:
        """Get session summary for reporting."""
        duration = datetime.now() - self.start_time
        
        return {
            "topic": self.topic,
            "research_type": self.research_type,
            "duration_minutes": duration.total_seconds() / 60,
            "sources_count": len(self.sources),
            "findings_categories": len(self.findings),
            "insights_count": len(self.insights),
            "current_phase": self.current_phase,
            "confidence_level": self.confidence_level,
            "status": self.status
        }
        
    def _assess_credibility(self, source: Dict[str, Any]) -> str:
        """Assess source credibility based on metadata."""
        # Simple heuristic-based credibility assessment
        url = source.get("url", "").lower()
        title = source.get("title", "").lower()
        
        high_credibility = [
            ".edu", ".gov", ".org", "arxiv", "doi.org", "ieee", "acm",
            "official documentation", "api reference"
        ]
        
        medium_credibility = [
            "stackoverflow", "github", "medium", "towards", "papers"
        ]
        
        for indicator in high_credibility:
            if indicator in url or indicator in title:
                return "high"
                
        for indicator in medium_credibility:
            if indicator in url or indicator in title:
                return "medium"
                
        return "needs_verification"

class DeepResearchDave:
    """Deep Research Dave agent for comprehensive research tasks."""
    
    def __init__(self, model_provider: str = "anthropic/claude-3-5-sonnet-20241022"):
        self.model_provider = model_provider
        self.agent = None
        self.current_session = None
        self._tavily_client = None  # Will hold MCP client reference if connected
        
    def create_agent(self) -> Agent:
        """Create and configure the research agent."""
        try:
            # Model configuration with fallback based on available API keys
            model = self._get_model_config()
            
            # Configure MCP tools for research
            tools = self._setup_research_tools()
            
            # Create agent with research tools
            agent = Agent(
                name="Deep Research Dave",
                description="A specialized research agent for comprehensive information gathering and analysis",
                model=model,
                system_prompt=SYSTEM_PROMPT,
                tools=tools
            )
            
            logger.info(f"Deep Research Dave agent created successfully with {len(tools)} tools")
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
                # API key must be provided as URL query parameter
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
                    temperature=0.1,  # Lower temperature for research consistency
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
                    temperature=0.1,
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
                    temperature=0.1,
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
                    temperature=0.1,
                )
                logger.info("Using OpenAI Direct API (fallback)")
                return model
                
            except ImportError:
                logger.warning("OpenAI library not available")
                return "openai/gpt-4"
                
        else:
            logger.warning("No API keys found, using Bedrock fallback")
            return "anthropic.claude-3-7-sonnet-20250219-v1:0"
            
            
    async def start_research_session(self, topic: str, research_type: str = "comprehensive") -> str:
        """Start a new research session."""
        try:
            self.current_session = ResearchSession(topic, research_type)
            self.current_session.status = "active"
            
            if not self.agent:
                self.agent = self.create_agent()
                
            # Initial research planning
            planning_prompt = f"""
            I need to conduct {research_type} research on: {topic}
            
            Please help me:
            1. Define the research scope and key questions
            2. Identify the best information sources and search strategies
            3. Create a structured research plan with phases
            4. Set success criteria for the research
            
            Focus on creating a systematic approach that ensures comprehensive coverage.
            """
            
            self.current_session.update_phase("planning")
            response = await self.robust_agent_call(planning_prompt)
            
            logger.info(f"Research session started for topic: {topic}")
            return response
            
        except Exception as e:
            logger.error(f"Error starting research session: {str(e)}")
            if self.current_session:
                self.current_session.status = "error"
            raise
            
    async def conduct_research_phase(self, phase_instructions: str) -> str:
        """Execute a specific research phase."""
        if not self.current_session:
            raise ValueError("No active research session")
            
        try:
            self.current_session.update_phase("information_gathering")
            
            prompt = f"""
            Research Session: {self.current_session.topic}
            Current Phase: Information Gathering
            
            Instructions: {phase_instructions}
            
            Please conduct thorough research following these guidelines:
            1. Use multiple search strategies and sources
            2. Evaluate source credibility and recency
            3. Extract key information and insights
            4. Identify any gaps that need further research
            5. Organize findings in a structured format
            
            Provide detailed findings with proper source attribution.
            """
            
            response = await self.robust_agent_call(prompt)
            return response
            
        except Exception as e:
            logger.error(f"Error in research phase: {str(e)}")
            raise
            
    async def synthesize_findings(self, focus_areas: List[str] = None) -> str:
        """Analyze and synthesize research findings."""
        if not self.current_session:
            raise ValueError("No active research session")
            
        try:
            self.current_session.update_phase("analysis_synthesis")
            
            session_summary = self.current_session.get_summary()
            
            prompt = f"""
            Research Session Summary:
            - Topic: {session_summary['topic']}
            - Sources Gathered: {session_summary['sources_count']}
            - Research Duration: {session_summary['duration_minutes']:.1f} minutes
            
            Focus Areas: {focus_areas or ['comprehensive analysis']}
            
            Please synthesize the research findings by:
            1. Identifying key patterns and themes across sources
            2. Comparing different perspectives and approaches
            3. Evaluating strengths, weaknesses, and trade-offs
            4. Generating unique insights and recommendations
            5. Assessing confidence level in findings
            6. Highlighting areas needing further research
            
            Provide a comprehensive analysis with actionable insights.
            """
            
            response = await self.robust_agent_call(prompt)
            
            # Update confidence level based on synthesis
            self.current_session.update_confidence("medium")  # Default, can be refined
            
            return response
            
        except Exception as e:
            logger.error(f"Error synthesizing findings: {str(e)}")
            raise
            
    async def generate_research_report(self, report_type: str = "comprehensive") -> str:
        """Generate a structured research report."""
        if not self.current_session:
            raise ValueError("No active research session")
            
        try:
            self.current_session.update_phase("documentation")
            
            session_summary = self.current_session.get_summary()
            
            prompt = f"""
            Generate a {report_type} research report for the topic: {self.current_session.topic}
            
            Session Details:
            - Research Type: {self.current_session.research_type}
            - Duration: {session_summary['duration_minutes']:.1f} minutes
            - Sources: {session_summary['sources_count']}
            - Confidence Level: {self.current_session.confidence_level}
            
            Please create a professional research report including:
            
            1. **Executive Summary**: Key findings and recommendations (2-3 paragraphs)
            
            2. **Methodology**: Research approach and sources used
            
            3. **Key Findings**: Organized by themes with source attribution
            
            4. **Analysis & Insights**: Critical evaluation and unique perspectives
            
            5. **Recommendations**: Actionable next steps based on research
            
            6. **Limitations & Further Research**: Areas of uncertainty and additional needs
            
            7. **Sources**: Bibliography with credibility assessment
            
            Format the report professionally with clear structure and evidence-based conclusions.
            """
            
            response = await self.robust_agent_call(prompt)
            self.current_session.status = "completed"
            
            logger.info(f"Research report generated for: {self.current_session.topic}")
            return response
            
        except Exception as e:
            logger.error(f"Error generating research report: {str(e)}")
            self.current_session.status = "error"
            raise
            
    async def deep_research(self, topic: str) -> str:
        """Initiate a comprehensive deep research session."""
        try:
            # Start comprehensive research session
            await self.start_research_session(topic, "comprehensive")
            
            # Phase 1: Gather information
            gather_phase = await self.conduct_research_phase(
                "Gather comprehensive information from multiple sources, "
                "focusing on authoritative and recent content"
            )
            
            # Phase 2: Analysis and synthesis
            synthesis = await self.synthesize_findings()
            
            # Phase 3: Generate comprehensive report
            report = await self.generate_research_report("comprehensive")
            
            return report
            
        except Exception as e:
            logger.error(f"Error in deep research: {str(e)}")
            if self.current_session:
                self.current_session.status = "error"
            raise
            
    async def comparative_deep_research(self, options: List[str], criteria: List[str] = None) -> str:
        """Conduct deep comparative research analysis with multiple phases."""
        try:
            if not criteria:
                criteria = ["features", "performance", "scalability", "cost", "ecosystem", 
                          "learning curve", "maintenance", "future outlook"]
            
            # Start research session
            topic = f"Comparative analysis of {', '.join(options)}"
            await self.start_research_session(topic, "comparative")
            
            # Phase 1: Research each option thoroughly
            research_prompt = f"""
            Phase 1: Comprehensive Information Gathering
            
            Options to Research: {', '.join(options)}
            
            For each option, gather detailed information on:
            - Core features and capabilities
            - Technical architecture and design
            - Performance characteristics
            - Ecosystem and community
            - Documentation and support
            - Real-world use cases
            - Recent developments and roadmap
            """
            await self.conduct_research_phase(research_prompt)
            
            # Phase 2: Comparative analysis
            analysis_prompt = f"""
            Phase 2: Deep Comparative Analysis
            
            Evaluation Criteria: {', '.join(criteria)}
            
            Conduct thorough comparison:
            1. **Detailed Feature Matrix**: Comprehensive capability comparison
            2. **Performance Analysis**: Benchmarks, scalability, efficiency
            3. **Ecosystem Evaluation**: Tools, libraries, community strength
            4. **Total Cost Analysis**: Licensing, development, maintenance costs
            5. **Risk Assessment**: Technical debt, vendor lock-in, obsolescence
            6. **Future Viability**: Roadmap, industry adoption, trends
            """
            await self.conduct_research_phase(analysis_prompt)
            
            # Phase 3: Synthesis and recommendations
            synthesis = await self.synthesize_findings(criteria)
            
            # Generate comprehensive comparison report
            report = await self.generate_research_report("comparative")
            
            return report
            
        except Exception as e:
            logger.error(f"Error in comparative deep research: {str(e)}")
            if self.current_session:
                self.current_session.status = "error"
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
    """Create Deep Research Dave agent instance."""
    research_dave = DeepResearchDave()
    return research_dave.create_agent()

# Root agent instance for module-level access
root_agent = create_agent()

# Simple test function for local execution
def main():
    """Simple test function to verify DeepResearch_Dave works."""
    print("Testing Deep Research Dave...")
    
    try:
        response = root_agent("Quick research on Python 3.13 new features")
        print(f"Agent Response: {response}")
    except Exception as e:
        logger.error(f"Test failed: {e}")
        print(f"Error: {e}")

if __name__ == "__main__":
    main()