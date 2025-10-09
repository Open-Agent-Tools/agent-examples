# Installation Guide

Choose your installation method: automated scripts (recommended) or manual installation.

## Automated Installation (Recommended)

### Using install.sh (Linux/macOS/Git Bash)
```bash
# Clone repository
git clone <repository-url>
cd agent-examples

# Run installation script
./install.sh
```

### Using install.py (Cross-platform)
```bash
# Clone repository
git clone <repository-url>
cd agent-examples

# Run Python installation script
python install.py
# or
python3 install.py
```

**Installation scripts will:**
- ✅ Check Python version (3.8+ required)
- ✅ Create virtual environment (optional, recommended)
- ✅ Install all dependencies from requirements.txt
- ✅ Setup .env file from example_env template
- ✅ Verify installation

## Manual Installation

### Core Dependencies
```bash
# Install essential packages for running agents
pip install -r requirements.txt
```

## What Gets Installed

### Core Dependencies (`requirements.txt`)
All essential packages needed to run agents:
- **Agent frameworks**: GoogleADK, Strands
- **AI/LLM providers**: Anthropic, OpenAI, LiteLLM, Ollama
- **MCP tools**: Model Context Protocol tools and basic utilities
- **Data processing**: pandas, numpy, openpyxl, pyyaml
- **Testing**: pytest, pytest-asyncio
- **Utilities**: pydantic, python-dotenv, requests, httpx, rich, click

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

UV is a fast Python package installer written in Rust. The install scripts will automatically use it if available.

```bash
# Install UV first
pip install uv

# Then install dependencies (much faster than pip)
uv pip install -r requirements.txt
```

The installation scripts automatically detect and use UV if installed.

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

## Installation Scripts Features

Both `install.sh` and `install.py` provide:
- ✅ **Cross-platform**: Works on Linux, macOS, Windows (Git Bash/WSL)
- ✅ **Interactive**: Prompts for virtual environment creation
- ✅ **Smart detection**: Automatically uses UV if installed for faster installs
- ✅ **Verification**: Checks Python version and verifies package installation
- ✅ **Environment setup**: Creates .env from template
- ✅ **Color output**: Clear, readable installation progress

### Virtual Environment Support

Both scripts offer to create a virtual environment:
- **install.sh**: Automatically activates venv after creation
- **install.py**: Guides you to activate venv and re-run script

Recommended for clean dependency isolation.