# Quick Research Quinten

Fast AI research agent optimized for rapid insights in 30-90 seconds.

## Key Capabilities
- **Rapid Web Search** - Tavily MCP integration for targeted research
- **Quick Comparisons** - Side-by-side analysis under 2 minutes  
- **Fact Checking** - Source validation with credibility assessment
- **Trend Analysis** - Current developments and patterns
- **Technical Lookups** - API docs, syntax, best practices

## Quick Start

```bash
# Install
pip install strands-agents strands-agents-tools

# Configure .env
ANTHROPIC_API_KEY=your_key
TAVILY_API_KEY=your_key

# Run
python agent.py
```

## Usage

**Interactive Chat:**
```bash
python agent.py
```

**Programmatic:**
```python
from agent import QuickResearchQuinten
quinten = QuickResearchQuinten()
result = await quinten.quick_research("Python 3.13 features")
```

**Commands:**
- `compare X vs Y` - Quick comparisons
- `fact check: [claim]` - Verify claims  
- `trends: [topic]` - Current trends
- `status` - Session info

## Output Format

Delivers concise, scannable results in 30-120 seconds:

```
Key Points: • Finding 1 • Finding 2 • Finding 3
Sources: [Source] (credibility) - date  
Insights: → Takeaway 1 → Takeaway 2
```

## Features
- Response times: 30-120 seconds
- Source credibility assessment
- Multiple fallback options
- Lightweight session tracking

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