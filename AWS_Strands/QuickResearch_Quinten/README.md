# Quick Research Quinten 🔍⚡

A specialized AI research agent built on the AWS Strands framework, optimized for rapid information gathering and immediate insights. Quinten focuses on delivering fast, accurate, and actionable research results with exceptional speed and clarity.

## Overview

Quick Research Quinten is designed for scenarios where you need immediate answers and quick insights. Unlike comprehensive research agents that may take several minutes, Quinten optimizes for speed while maintaining quality, typically delivering results in 30-90 seconds.

## Key Features

### 🚀 Core Capabilities
- **Rapid Web Search**: Leverages Tavily MCP for fast, targeted internet research
- **Quick Comparisons**: Side-by-side analysis of options in under 2 minutes
- **Fast Fact Checking**: Verify claims with source validation
- **Trend Analysis**: Current developments and emerging patterns
- **Immediate Insights**: Actionable takeaways from research

### ⚡ Speed Optimization
- Targeted search strategies for maximum efficiency
- Limited to 1-3 strategic searches per query
- Focuses on most relevant and recent information
- Concise, scannable output format
- Response times: 30-120 seconds typically

## Installation

### Prerequisites
- Python 3.10+
- At least one AI model API key (Anthropic, OpenAI, or Google)
- Tavily API key (optional but recommended for web search)

### Setup

1. Install dependencies:
```bash
pip install strands-agents strands-agents-tools python-dotenv
```

2. Configure environment variables in `.env`:
```env
# AI Model Access (at least one required)
ANTHROPIC_API_KEY=your_anthropic_key    # Primary recommendation
OPENAI_API_KEY=your_openai_key         # Alternative
GOOGLE_API_KEY=your_google_key         # Alternative

# Web Search (recommended)
TAVILY_API_KEY=your_tavily_key
```

## Usage

### Quick Start

```python
from agent import QuickResearchQuinten

# Initialize the agent
quinten = QuickResearchQuinten()

# Quick research
result = await quinten.quick_research("What are the key features of Python 3.13?")

# Comparison
result = await quinten.compare_options(["React", "Vue", "Angular"])

# Fact checking
result = await quinten.fact_check("Python is faster than C++")

# Trend analysis
result = await quinten.trend_analysis("AI agent frameworks")
```

### Command Line Interface

Run the interactive mode:
```bash
python agent.py
```

Or run example usage:
```bash
python example_usage.py
python example_usage.py interactive  # For interactive mode
```

### Interactive Commands

- **General query**: Type any research question
- **Comparison**: `compare X vs Y` or `compare X versus Y`
- **Fact check**: `fact check: [claim]` or `verify: [claim]`
- **Trends**: `trends: [topic]` or include "trend" in your query
- **Status**: `status` - Show current session information
- **Exit**: `quit` or `exit`

## Output Formats

### Quick Research Brief
```
Key Points:
• Essential finding 1
• Essential finding 2
• Essential finding 3-5

Primary Sources:
1. [Source Name] (High credibility) - Date
2. [Source Name] (Medium credibility) - Date

Immediate Insights:
→ Actionable takeaway 1
→ Actionable takeaway 2

Follow-up Areas:
- Topic needing deeper research
```

### Comparison Matrix
```
Quick Overview:
- Option A: Brief description
- Option B: Brief description

Key Differentiators:
| Criteria    | Option A | Option B |
|------------|----------|----------|
| Performance | Fast     | Faster   |
| Complexity  | Low      | Medium   |

Recommendation: Option A for X scenarios, Option B for Y scenarios
```

### Fact Check Result
```
Verdict: TRUE / FALSE / PARTIALLY TRUE

Evidence:
✓ Supporting evidence point
✗ Refuting evidence point

Sources: [Authoritative source with date]
Confidence: High/Medium/Low
```

## Architecture

### Session Management
- Lightweight session tracking for research context
- Automatic source credibility assessment
- Duration and performance metrics

### Tool Integration
- **Tavily MCP**: Primary web search interface
- **HTTP Request Tool**: Direct API access when faster
- **Fallback Support**: Works without web search using LLM knowledge

### Speed Optimizations
- Targeted query formulation
- Parallel search execution when beneficial
- Rapid source evaluation
- Concise information extraction

## Testing

Run the test suite:
```bash
python evals/test_quick_research.py
```

Tests cover:
- Quick research functionality
- Comparison capabilities
- Fact checking accuracy
- Trend analysis
- Session tracking

## Comparison with Deep Research Dave

| Aspect | Quick Research Quinten | Deep Research Dave |
|--------|------------------------|-------------------|
| **Focus** | Speed and immediacy | Depth and comprehensiveness |
| **Response Time** | 30-120 seconds | 2-10 minutes |
| **Search Depth** | 1-3 targeted searches | Multiple phases, extensive searches |
| **Output Length** | Concise bullets & summaries | Detailed reports with sections |
| **Use Cases** | Quick lookups, fact checks | Academic research, detailed analysis |
| **Source Count** | 3-5 most relevant | 10+ diverse sources |
| **Confidence Assessment** | Quick evaluation | Detailed credibility analysis |

## Best Practices

### When to Use Quinten
- Need immediate answers (< 2 minutes)
- Quick fact verification
- Rapid technology comparisons
- Current trend snapshots
- API documentation lookups
- Syntax verification

### When to Use Deep Research Instead
- Academic or professional research
- Comprehensive market analysis
- Multi-faceted complex topics
- Need for extensive source documentation
- Detailed credibility assessment required
- Long-form report generation

## Development

### Project Structure
```
QuickResearch_Quinten/
├── agent.py           # Main agent implementation
├── prompts.py         # System prompt for quick research
├── example_usage.py   # Usage examples and interactive mode
├── __init__.py        # Package initialization
├── README.md          # This file
├── AGENT_SUMMARY.md   # Agent summary for showcases
└── evals/
    └── test_quick_research.py  # Test suite
```

### Extending Quinten

Add new quick research methods to the `QuickResearchQuinten` class:

```python
async def quick_api_lookup(self, api_name: str, endpoint: str) -> str:
    """Quick API documentation lookup."""
    # Implementation for rapid API reference
    pass
```

## Troubleshooting

### No Web Search Results
- Verify `TAVILY_API_KEY` is set correctly
- Check internet connectivity
- Agent will fall back to LLM knowledge if search unavailable

### Slow Response Times
- Check model API latency
- Consider using faster model (e.g., Claude Haiku)
- Reduce `max_sources` parameter

### Session Not Tracking
- Sessions are created per research query
- Use `get_session_status()` to check current session

## Contributing

Contributions are welcome! Areas for improvement:
- Additional quick research patterns
- Speed optimization techniques
- Enhanced source evaluation
- More output format options

## License

This project is part of the Open Agent Tools initiative. See the main repository for license information.

## Support

For issues or questions:
- Check the [example usage](example_usage.py) for implementation patterns
- Run tests to verify setup: `python evals/test_quick_research.py`
- Review the [main repository](https://github.com/Open-Agent-Tools/agent-examples) for additional context