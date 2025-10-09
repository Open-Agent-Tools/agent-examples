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
- ✅ **Complex_Coding_Clara** - 14-agent coding system with specialists (Architect, Senior Coder, Python, Web, Database, DevOps, Data Science, Agile, etc.)
- ✅ **DeepResearch_Dave** - Comprehensive research agent
- ✅ **QuickResearch_Quinten** - Rapid research (30-90s responses)

## Quick Start


**Manual Installation:**
```bash
# Install dependencies
pip install -r requirements.txt

# Setup environment
cp example_env .env  # Add your API keys
```

**Run Agents:**
```bash
# GoogleADK web interface
cd GoogleADK && adk web

# AWS Strands agents - Recommended: Use Basic-Agent-Chat-Loop
# https://github.com/Open-Agent-Tools/Basic-Agent-Chat-Loop
git clone https://github.com/Open-Agent-Tools/Basic-Agent-Chat-Loop.git
cd Basic-Agent-Chat-Loop
pip install -e .  # Install the chat loop tool
chat_loop /path/to/agent-examples/AWS_Strands/Complex_Coding_Clara/agent.py

# Optional: Save aliases for quick access
chat_loop --save-alias clara /path/to/Complex_Coding_Clara/agent.py
chat_loop clara  # Use the alias

# AWS Strands agents - Direct execution (basic)
cd AWS_Strands/Complex_Coding_Clara && python agent.py
```



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
- Individual agent READMEs in framework directories
