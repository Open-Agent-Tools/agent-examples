# Getting Started with Agent Examples

This repository contains examples from multiple AI agent frameworks. Choose the framework that best fits your needs and follow the corresponding setup guide.

## Framework Selection Guide

### 🔍 Which Framework Should I Choose?

**For specialized single-purpose agents:**
- **[GoogleADK](GoogleADK/)** - Best for cost-effective, focused agents with local model support

**For team-based collaboration:**
- **[CrewAI](CrewAI/)** - Ideal for multi-agent teams working together on complex tasks

**For complex workflow orchestration:**
- **[LangChain LangGraph](LangChain%20LangGraph/)** - Perfect for graph-based workflows and state management

**For conversational multi-agent systems:**
- **[MS AutoGen](MS%20AutoGen/)** - Great for dialogue-based agent interactions

**For lightweight deployment:**
- **[Hugging Face SmolAgents](Hugging%20Face%20SmolAgents/)** - Minimal overhead, fast execution

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer) or UV (faster Python package installer)
- Git for cloning the repository

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd agent-examples
```

### 2. Choose Your Framework

Navigate to your chosen framework directory and follow the specific setup instructions:

- **[GoogleADK Setup](GoogleADK/ADK-getting-started.md)** - FileOps agent and local model integration
- **[CrewAI Setup](CrewAI/getting-started.md)** - Multi-agent team examples *(coming soon)*
- **[LangGraph Setup](LangChain%20LangGraph/getting-started.md)** - Graph workflow examples *(coming soon)*
- **[AutoGen Setup](MS%20AutoGen/getting-started.md)** - Conversational agent examples *(coming soon)*
- **[SmolAgents Setup](Hugging%20Face%20SmolAgents/getting-started.md)** - Lightweight agent examples *(coming soon)*

## Framework Comparison

| Framework | Best For | Complexity | Local Models | Multi-Agent |
|-----------|----------|------------|--------------|-------------|
| GoogleADK | Specialized tasks | Low-Medium | ✅ Yes | Limited |
| CrewAI | Team collaboration | Medium | ✅ Yes | ✅ Yes |
| LangGraph | Complex workflows | High | ✅ Yes | ✅ Yes |
| AutoGen | Conversations | Medium | ✅ Yes | ✅ Yes |
| SmolAgents | Simple automation | Low | ✅ Yes | Limited |

## General Setup Steps

### Using pip (Standard)

1. **Install Framework Dependencies**: Each framework has its own requirements.txt
   ```bash
   pip install -r requirements.txt  # For all dependencies
   # OR
   pip install -r GoogleADK/requirements.txt  # For specific framework
   ```

### Using UV (Faster Alternative)

1. **Install UV**:
   ```bash
   pip install uv
   ```

2. **Install Dependencies with UV**:
   ```bash
   uv pip install -r requirements.txt  # For all dependencies
   # OR
   uv pip install -r GoogleADK/requirements.txt  # For specific framework
   ```

3. **Create Virtual Environment with UV** (optional):
   ```bash
   uv venv .venv
   # Activate on Windows
   .venv\Scripts\activate
   # Activate on Unix/MacOS
   source .venv/bin/activate
   ```

For both methods:

1. **Configure Environment**: Set up API keys and environment variables
2. **Choose Your Model**: Local models for cost-effectiveness or cloud models for performance
3. **Run Examples**: Start with the provided examples in each framework directory

## Common Environment Variables

Most frameworks will require similar environment setup:

```env
# Choose your preferred model provider
ANTHROPIC_API_KEY=your_key_here

OPENAI_API_KEY=your_key_here

GOOGLE_API_KEY=your_key_here
GOOGLE_MODEL="gemini-2.0-flash"
GOOGLE_GENAI_USE_VERTEXAI=0

# Optional: Local model settings
OLLAMA_BASE_URL=http://localhost:11434
```

## Next Steps

1. **Explore Framework Examples**: Each directory contains practical examples
2. **Compare Approaches**: See how different frameworks solve similar problems
3. **Build Your Own**: Use the examples as templates for your specific use cases
4. **Contribute**: Add new examples or improve existing ones

## Support

- Check framework-specific documentation in each directory
- Review individual agent README files
- Ensure environment variables are properly configured
- Verify all dependencies are installed

## Security Notes

- Never commit API keys to version control
- Use environment variables for sensitive configuration
- Keep your API keys secure and rotate them regularly
- Consider using local models for sensitive data processing
