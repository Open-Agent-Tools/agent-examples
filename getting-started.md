# Getting Started with Agent Examples

This repository contains examples from two AI agent frameworks. Choose the framework that best fits your needs and follow the corresponding setup guide.

## Framework Selection Guide

### 🔍 Which Framework Should I Choose?

**For specialized single-purpose agents:**
- **[GoogleADK](GoogleADK/)** - Best for cost-effective, focused agents with local model support and comprehensive tool integration

**For product management and Atlassian integration:**
- **[AWS Strands](AWS_Strands/)** - Perfect for product management workflows with Jira/Confluence integration

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

- **[GoogleADK Setup](GoogleADK/ADK-getting-started.md)** - Multiple specialized agents with comprehensive tooling
- **[AWS Strands Setup](AWS_Strands/)** - Product management agent with Atlassian MCP integration

## Framework Comparison

| Framework | Best For | Complexity | Local Models | Multi-Agent |
|-----------|----------|------------|--------------|-------------|
| GoogleADK | Specialized tasks | Low-Medium | ✅ Yes | Limited |
| AWS Strands | Product management | Low | ✅ Yes | Single |

## General Setup Steps

### Quick Install (Recommended)

1. **Install Dependencies**: 
   ```bash
   # Core dependencies only
   pip install -r requirements.txt
   
   # OR full development setup
   pip install -r requirements.txt requirements-dev.txt requirements-optional.txt
   
   # OR using UV (faster)
   uv sync  # Installs everything from uv.lock
   ```

2. **Configure Environment**: Set up API keys and environment variables
3. **Choose Your Model**: Local models for cost-effectiveness or cloud models for performance
4. **Run Examples**: Start with the provided examples in each framework directory

For detailed installation options, see [INSTALL.md](INSTALL.md).

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
