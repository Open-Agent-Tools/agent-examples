# Getting Started with Agent Examples

This repository contains specialized AI agent examples, including the **FileOps_Freddy** agent - a file and directory operations specialist designed for efficient local processing, and the **Butler_Basil** agent - a generic task and facilitation agent.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer) or UV (faster Python package installer)
- Optional: Ollama (for local models like Gemma)

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd agent-examples
```

### 2. Create Virtual Environment (Recommended)

#### Using standard venv:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### Using UV (faster alternative):
```bash
# Install UV if you haven't already
pip install uv

# Create virtual environment with UV
uv venv .venv
# Activate on Windows
.venv\Scripts\activate
# Activate on Unix/MacOS
source .venv/bin/activate
```

### 3. Install Dependencies

#### Using pip:
```bash
pip install -r GoogleADK/requirements.txt
```

#### Using UV (faster alternative):
```bash
# If you haven't installed UV yet
pip install uv

# Install dependencies with UV
uv pip install -r GoogleADK/requirements.txt
```

## Environment Configuration

### 1. Create Environment File

Create a `.env` file in the root directory:

```bash
touch .env
```

### 2. Configure API Keys and Settings

Add the following environment variables to your `.env` file:

```env
# Required: Choose your preferred model provider
# Option 1: Anthropic Claude
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Option 2: OpenAI
OPENAI_API_KEY=your_openai_api_key_here

# Option 3: Google AI
GOOGLE_API_KEY=your_google_api_key_here

# Optional: Local model settings (if using Ollama)
OLLAMA_BASE_URL=http://localhost:11434

# Optional: LiteLLM configuration
LITELLM_LOG=DEBUG
```

### 3. Install Local Models (Optional)

For cost-effective local processing, install Ollama and download models:

```bash
# Install Ollama (visit https://ollama.ai for installation instructions)
# Then download the Gemma models
ollama pull gemma:2b
ollama pull gemma:7b
```

## Quick Start

### Web Interface (Recommended)

CD into the  GoogleADK directory and start the web interface for an interactive experience. 
(** running this command at the root folders will cause errors because of the other agent framework folders)

```bash
cd GoogleADK
adk web
```

This launches a web interface at `http://localhost:8000` where you can interact with your agents through a user-friendly interface.

For more information about the ADK web interface, visit:
- [ADK Web documentation](https://github.com/google/adk-web)
- [ADK Quickstart Guide](https://google.github.io/adk-docs/get-started/quickstart/#run-your-agent)



## Troubleshooting

### Common Issues

**Missing API Keys**: Ensure your `.env` file exists and contains the required API keys for your chosen model provider.


**Package Installation Errors**: 

With pip:
```bash
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
```

With UV:
```bash
pip install --upgrade uv
uv pip install -r requirements.txt --no-deps-check
```

### Getting Help

- Check the individual agent README files for specific documentation
- Review the model configurations in each agent's `agent.py` file
- Ensure all environment variables are properly set in your `.env` file

## Security Notes

- Never commit your `.env` file to version control
- Keep your API keys secure and rotate them regularly
- Use local models when processing sensitive data
