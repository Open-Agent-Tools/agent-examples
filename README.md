# Agent Examples

Practical AI agent implementations across multiple frameworks with specialized agents for file operations, research, Jira integration, and more.

## Frameworks & Agents

### GoogleADK (5/7 working)
- ✅ **Butler_Basil** - Generic task coordination
- ✅ **FileOps_Freddy** - File operations (98.9% success)
- ✅ **Jira_Johnny** - Jira integration (100% success)
- ✅ **Scrum_Sam** - Multi-agent Scrum Master
- ✅ **Story_Sage** - User story specialist
- ❌ **Data_Daniel** - Tool schema errors
- ❌ **Stocks_Sarah** - MCP timeout issues

### AWS Strands
- ✅ **DeepResearch_Dave** - Comprehensive research agent
- ✅ **QuickResearch_Quinten** - Rapid research (30-90s responses)

## Quick Start

**Install & Configure:**
```bash
# Core dependencies
pip install -r requirements.txt

# Environment setup
cp example_env .env  # Add your API keys
```

**Run Agents:**
```bash
# GoogleADK web interface
cd GoogleADK && adk web

# AWS Strands agents
cd AWS_Strands/DeepResearch_Dave && uv run python agent.py
```

## Key Features

- **Production-Ready** - 71.4% success rate across all agents
- **Multi-Model Support** - Anthropic, OpenAI, Google, local models
- **Cost Optimization** - Local model integration via Ollama
- **MCP Integration** - Web search, Atlassian, Context7 tools
- **Specialized Tasks** - File ops, research, project management

## Environment Setup

Add to `.env` file:
```env
# Choose your model provider
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
GOOGLE_API_KEY=your_key_here

# Optional: Web search
TAVILY_API_KEY=your_key_here

# Optional: Local models
OLLAMA_BASE_URL=http://localhost:11434
```

## Documentation

- **[CLAUDE.md](CLAUDE.md)** - Comprehensive development guide
- **[INSTALL.md](INSTALL.md)** - Detailed installation options
- Individual agent READMEs in framework directories
