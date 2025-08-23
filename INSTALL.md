# Installation Guide

This repository now uses a modular dependency structure to reduce bloat and installation time.

## Quick Install (Recommended)

### Core Dependencies Only
```bash
# Install essential packages for running agents
pip install -r requirements.txt
```

### Full Development Setup
```bash
# Install core + development tools + optional features
pip install -r requirements.txt
pip install -r requirements-dev.txt
pip install -r requirements-optional.txt
```

## Modular Installation

### Core Dependencies (`requirements.txt`)
Essential packages needed to run the agents:
- Agent frameworks (GoogleADK, Strands)
- AI/LLM providers (Anthropic, OpenAI, LiteLLM, Ollama)
- MCP tools and basic utilities
- Core data processing (pandas, numpy)
- Testing framework

### Development Tools (`requirements-dev.txt`)
Code quality and development tools:
- Linting/formatting (black, ruff, mypy, flake8)
- Build tools (hatchling, hatch)
- Version control (pre-commit, commitizen)
- Jupyter notebooks
- FastAPI/Uvicorn for web interfaces

### Optional Features (`requirements-optional.txt`)
Advanced features for specialized use cases:
- Web scraping (beautifulsoup4, selenium)
- Machine learning (torch, transformers, scikit-learn)
- Vector databases (faiss-cpu)
- Advanced code analysis

## Framework-Specific Installation

### GoogleADK Only
```bash
pip install -r GoogleADK/requirements.txt
```

### AWS Strands Only
```bash
pip install strands-agents strands-agents-tools
```

## Using UV (Faster Alternative)

```bash
# Install UV first
pip install uv

# Then install dependencies
uv pip install -r requirements.txt
uv pip install -r requirements-dev.txt    # Optional
uv pip install -r requirements-optional.txt  # Optional
```

## Environment Setup

1. Create `.env` file:
```bash
cp example_env .env
```

2. Add your API keys:
```env
GOOGLE_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
```

## Dependency Reduction Summary

The previous requirements.txt had **60+ packages**. The new structure:
- **Core**: 25 essential packages
- **Dev**: 15 development tools  
- **Optional**: 10 specialized packages

This reduces initial installation size by ~60% while maintaining all functionality.