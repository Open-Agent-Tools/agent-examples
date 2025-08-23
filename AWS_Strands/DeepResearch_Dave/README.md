# Deep Research Dave Agent

A specialized AI research agent built on the AWS Strands framework for conducting comprehensive, systematic research across any domain.

## Overview

Deep Research Dave is designed to handle complex research tasks that require:
- Multi-source information gathering
- Critical evaluation and synthesis
- Structured analysis and reporting  
- Evidence-based insights and recommendations

## Key Features

### Research Capabilities
- **Live Web Search**: Real-time information gathering via Tavily MCP integration
- **Comprehensive Research**: Multi-phase research sessions with systematic approach
- **Quick Research**: Rapid insights for immediate needs
- **Comparative Analysis**: Side-by-side evaluation of options
- **Source Evaluation**: Automatic credibility assessment and fact-checking

### Research Types
- Technical research (frameworks, APIs, documentation)
- Market research (trends, competition, analysis)
- Academic research (papers, methodologies, literature reviews)
- Business research (companies, strategies, regulatory landscape)

### Output Formats
- **Research Reports**: Comprehensive analysis with methodology and sources
- **Quick Briefs**: Essential findings in bullet-point format
- **Comparison Matrices**: Side-by-side option evaluation
- **Executive Summaries**: Key insights for decision-makers

## Usage Examples

### Interactive Chat (Recommended)
Run Deep Research Dave in an interactive terminal chat:

```bash
cd AWS_Strands/DeepResearch_Dave
uv run python agent.py
```

This provides a user-friendly chat interface where you can:
- Ask research questions directly
- Access specialized research functions via commands
- Get formatted, real-time responses
- Use commands like `help`, `quit`
- See research timing and status

#### Specialized Commands:
- `session: <topic>` - Start a comprehensive research session
- `phase: <instructions>` - Execute a specific research phase
- `synthesize` - Analyze and synthesize current findings
- `report: <type>` - Generate structured reports (comprehensive/executive)
- `status` - Show current session status
- `Compare X vs Y` - Comparative analysis between options

### Quick Research (Programmatic)
```python
from AWS_Strands.DeepResearch_Dave import DeepResearchDave
import asyncio

async def main():
    dave = DeepResearchDave()
    
    # Get quick insights on a topic
    result = await dave.quick_research(
        "Latest trends in AI agent frameworks 2025"
    )
    print(result)

asyncio.run(main())
```

**Important:** Run with `uv run python your_script.py` to ensure proper environment loading and package access.

## Configuration

### Required Environment Variables

Add these to your `.env` file:

```env
# Required for AI model access
ANTHROPIC_API_KEY=your_anthropic_key_here

# Required for live web search (get from tavily.com)
TAVILY_API_KEY=your_tavily_key_here

# Optional: Alternative AI models
OPENAI_API_KEY=your_openai_key_here
GOOGLE_API_KEY=your_google_key_here
```

### Web Search Integration

Deep Research Dave uses Tavily's hosted MCP server for live web search:
- **Service**: Tavily MCP at `https://mcp.tavily.com/mcp/`
- **Authentication**: Bearer token via TAVILY_API_KEY
- **Capabilities**: Real-time web search, content extraction, source verification
- **No installation required**: Connects to hosted service automatically

### Comprehensive Research Session
```python
async def comprehensive_research():
    dave = DeepResearchDave()
    
    # Start research session
    planning = await dave.start_research_session(
        topic="AWS Strands vs Google ADK comparison",
        research_type="comparative"
    )
    
    # Conduct information gathering
    findings = await dave.conduct_research_phase(
        "Focus on architecture, capabilities, and use cases"
    )
    
    # Synthesize insights
    analysis = await dave.synthesize_findings([
        "architecture", "performance", "ease of use"
    ])
    
    # Generate final report
    report = await dave.generate_research_report("comprehensive")
    
    return report
```

### Comparative Analysis
```python
async def compare_frameworks():
    dave = DeepResearchDave()
    
    result = await dave.compare_options(
        options=["AWS Strands", "Google ADK", "LangChain"],
        criteria=["ease of use", "documentation", "community", "features"]
    )
    
    return result
```

## Research Process

### Phase 1: Research Planning
- Scope definition and objective setting
- Source identification and mapping
- Question framework development
- Timeline and milestone planning

### Phase 2: Information Gathering
- Systematic multi-source searching
- Source credibility evaluation
- Data extraction and organization
- Gap analysis and additional research

### Phase 3: Analysis & Synthesis  
- Pattern and trend identification
- Comparative analysis across sources
- Critical evaluation of findings
- Insight generation and hypothesis development

### Phase 4: Documentation & Presentation
- Structured report generation
- Evidence-based conclusions
- Actionable recommendations
- Knowledge transfer optimization

## Research Quality Standards

### Source Verification
- Multiple independent sources for critical claims
- Primary source preference over secondary
- Recency validation (prefer <2 years unless historical)
- Authority verification (expert credentials, institutional backing)

### Bias Mitigation
- Diverse perspective inclusion
- Assumption challenging
- Conflict of interest identification
- Balanced representation of viewpoints

### Accuracy Validation
- Cross-referencing across sources
- Fact-checking against authoritative databases
- Version/date verification for technical information
- Expert consensus validation

## Configuration

### Model Selection
```python
# Use different model providers
dave = DeepResearchDave(model_provider="openai/gpt-4")
dave = DeepResearchDave(model_provider="google/gemini-pro")
dave = DeepResearchDave(model_provider="anthropic/claude-3-5-sonnet-20241022")  # default
```

### Research Session Tracking
```python
# Get session status
status = dave.get_session_status()
print(f"Research progress: {status['current_phase']}")
print(f"Sources gathered: {status['sources_count']}")
print(f"Confidence level: {status['confidence_level']}")
```

## Integration with MCP Tools

Deep Research Dave integrates with several MCP (Model Context Protocol) tools:

- **Web Search**: Comprehensive internet research
- **Context7**: Library documentation and code examples
- **Atlassian**: Jira and Confluence for enterprise research

## Best Practices

### Research Planning
- Start with clear, specific research objectives
- Define success criteria upfront
- Consider multiple perspectives and potential biases
- Plan for iterative refinement of research questions

### Source Management
- Prioritize authoritative and recent sources
- Maintain source diversity to avoid echo chambers
- Document methodology for reproducibility
- Keep detailed citations for transparency

### Analysis Quality
- Support all conclusions with evidence
- Acknowledge limitations and uncertainties
- Consider alternative explanations
- Validate findings through multiple sources

## Limitations

- Research quality depends on available sources
- Real-time information may have slight delays
- Complex technical topics may require domain expert validation
- Proprietary/confidential information is not accessible

## Contributing

To extend Deep Research Dave's capabilities:

1. Add new research methodologies to the system prompt
2. Integrate additional MCP tools for specialized domains
3. Enhance source credibility assessment algorithms
4. Develop domain-specific research templates

## Version History

- **v1.0.0**: Initial release with core research capabilities
  - Multi-phase research sessions
  - Quick research functionality
  - Comparative analysis tools
  - Automated source credibility assessment