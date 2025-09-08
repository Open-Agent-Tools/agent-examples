# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a multi-framework AI agent examples repository showcasing specialized agents across Google ADK and AWS Strands frameworks. The project focuses on practical agent implementations for file operations, Jira integration, user story creation, and more.

## Architecture

### Framework Structure
- **GoogleADK/**: Google's Agent Development Kit agents
  - Each agent follows pattern: `agent.py`, `prompts.py`, `__init__.py`, `evals/`
  - Agents use `google.adk.agents.Agent` base class
  - Tools loaded via `basic_open_agent_tools` or MCP servers
- **AWS_Strands/**: Strands framework agents  
  - Uses `strands.Agent` and `strands_tools`
  - Product_Pete agent demonstrates Atlassian MCP integration

### Agent Pattern
All agents follow consistent structure:
1. **agent.py**: Main agent configuration with `create_agent()` and `root_agent`
2. **prompts.py**: Agent-specific system prompts and instructions
3. **evals/**: Evaluation tests (JSON test cases + test runners)

## Development Commands

### Installation
```bash
# Core dependencies only (recommended for most users)
pip install -r requirements.txt

# Full development setup
pip install -r requirements.txt
pip install -r requirements-dev.txt
pip install -r requirements-optional.txt

# Using UV (faster alternative)
uv pip install -r requirements.txt
uv pip install -r requirements-dev.txt      # Optional
uv pip install -r requirements-optional.txt # Optional

# GoogleADK only
pip install -r GoogleADK/requirements.txt
```

### Quality Checks
```bash
# Linting and formatting
python3 -m ruff check GoogleADK/ AWS_Strands/ --fix
python3 -m ruff format GoogleADK/ AWS_Strands/

# Type checking
python3 -m mypy GoogleADK/

# Run tests (limited - mainly Story_Sage has actual Python tests)
uv run pytest
```

### Running ADK Agents

#### Web Interface (from GoogleADK directory)
```bash
cd GoogleADK
adk web  # Launches at http://localhost:8000
```

#### ADK Evaluations (MUST run from project root)
```bash
# Single agent evaluation
PYTHONPATH=.:$PYTHONPATH adk eval \
  --config_file_path GoogleADK/{Agent_Name}/evals/test_config.json \
  --print_detailed_results \
  GoogleADK/{Agent_Name} \
  GoogleADK/{Agent_Name}/evals/{test_name}.json

# Example: Jira_Johnny
PYTHONPATH=.:$PYTHONPATH adk eval \
  --config_file_path GoogleADK/Jira_Johnny/evals/test_config.json \
  --print_detailed_results \
  GoogleADK/Jira_Johnny \
  GoogleADK/Jira_Johnny/evals/00_list_available_tools_test.json
```

### Running Strands Agents
```bash
# Run Product Pete agent
python AWS_Strands/Product_Pete/agent.py
```

## Quick Cleanup Command

When user says **"cleanup"**: 
1. **Run Quality Tools**: Execute all quality checks and fix issues
   ```bash
   python3 -m ruff check GoogleADK/ AWS_Strands/ --fix
   python3 -m ruff format GoogleADK/ AWS_Strands/
   python3 -m mypy GoogleADK/
   uv run pytest
   ```
2. **Review TODO Files**: Update TODO.md files for outdated information
3. **Commit Changes**: Create commit with standard message
   ```bash
   git commit -m "Run quality checks and cleanup"
   ```

## Agent Status (August 2025)

### ✅ Working Agents (5/7 GoogleADK)
- **Butler_Basil**: Basic filesystem operations
- **FileOps_Freddy**: Advanced file operations (98.9% success)
- **Jira_Johnny**: Jira integration via HTTP MCP (100% success)
- **Scrum_Sam**: Multi-agent Scrum Master with sub-agents
- **Story_Sage**: User story specialist with INVEST principles

### ❌ Broken Agents (2/7 GoogleADK)
- **Data_Daniel**: Tool schema validation errors
- **Stocks_Sarah**: MCP server timeout issues

### AWS Strands Agents
- **Product_Pete**: Product Manager assistant with Atlassian MCP integration
- **QuickResearch_Quinten**: Generic web research agent for targeted information gathering

## Important Notes

- **Environment Setup**: Create `.env` file with API keys (GOOGLE_API_KEY, ANTHROPIC_API_KEY, etc.)
- **ADK Evaluations**: Always run from project root with PYTHONPATH set
- **pytest Files**: For CI/CD automation only - use `adk eval` for manual testing
- **Local Models**: Support for Ollama with Gemma models (gemma:2b, gemma:7b)