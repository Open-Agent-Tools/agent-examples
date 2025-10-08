# Complex Coding Clara

A sophisticated multi-agent coding system built on AWS Strands framework, featuring specialized agents for coding, testing, and code review with intelligent orchestration.

## Overview

Clara is a **meta-orchestrator** that coordinates **14 specialist agents** across three categories:

**General Coding (7 agents):**
- 🏛️ **Architect**: System design and architecture planning
- 🏗️ **Senior Coder**: Complex algorithms, refactoring, advanced coding
- ⚡ **Fast Coder**: CRUD operations and boilerplate code
- 🧪 **Test Engineer**: Comprehensive test generation and coverage
- 🔍 **Code Reviewer**: Code quality, security, and best practices
- 🐛 **Debug**: Error analysis and bug fixing
- 📝 **Documentation**: Docstrings, READMEs, and technical docs

**Domain/Language Specialists (5 agents):**
- 🐍 **Python Specialist**: Python idioms, PEP standards, type hints
- 🌐 **Web Specialist**: React, TypeScript, modern frontend development
- 🗄️ **Database Specialist**: SQL/NoSQL, schema design, query optimization
- 🚀 **DevOps Specialist**: Docker, Kubernetes, CI/CD, Infrastructure as Code
- 📊 **Data Science Specialist**: ML, data preprocessing, model training

**SDLC Process Specialists (2 agents):**
- 📋 **Agile Specialist**: User stories, epics, sprint planning, Scrum processes
- 🔎 **Doc Research Specialist**: Technical documentation research and analysis

## Quick Start

### Prerequisites

```bash
# Install dependencies
pip install -r requirements.txt

# Set up AWS credentials and environment
cp ../../../example_env .env
# Edit .env and add your AWS_REGION and other settings
```

### Running Clara

```bash
# Test the agent
python agent.py

# Use programmatically
python
>>> from AWS_Strands.Complex_Coding_Clara import root_agent
>>> result = root_agent("Add a GET /health endpoint with tests")
```

### System Validation & Health Checks

**Validate Agent Configurations:**
```bash
# Check all agent model IDs and settings
python config_validator.py

# Output shows which agents have valid/invalid configurations
```

**Test All Agents:**
```bash
# Run health check on all 14 agents
python agent_health_check.py

# Generates:
# - Real-time testing progress
# - Success/failure summary
# - Performance metrics
# - Detailed report (health_check_report.md)
```

See [FIXES.md](FIXES.md) for complete documentation on configuration fixes and monitoring tools.

## Architecture

### Agents-as-Tools Pattern

Clara uses the **agents-as-tools** pattern where each specialist agent is wrapped as a tool that the orchestrator can invoke:

```python
@tool
def senior_coder(task: str) -> str:
    """Complex coding tasks"""
    # Delegates to Senior Coder agent

@tool
def test_engineer(task: str) -> str:
    """Test generation"""
    # Delegates to Test Engineer agent

@tool
def code_reviewer(task: str) -> str:
    """Code review"""
    # Delegates to Code Reviewer agent
```

### Workflow

For most coding tasks, Clara follows this pattern:
1. **Understand**: Analyze the user's request
2. **Delegate**: Route to appropriate specialist(s)
3. **Coordinate**: Manage multi-agent interactions
4. **Synthesize**: Integrate results into coherent output

Example flow:
```
User Request → Clara Orchestrator
              ↓
              Senior Coder (implements code)
              ↓
              Test Engineer (generates tests)
              ↓
              Code Reviewer (reviews quality)
              ↓
              Clara (synthesizes final output)
```

## Models

All models run on **AWS Bedrock** with inference profile configuration:

| Agent | Model | Use Case |
|-------|-------|----------|
| Clara (Orchestrator) | Claude Sonnet 4.5 | Planning & coordination |
| Architect | Claude Sonnet 4.5 | System design |
| Senior Coder | Claude Sonnet 4.5 | Complex coding |
| Fast Coder | Nova Lite | Quick CRUD operations |
| Test Engineer | Llama 3.3 70B | Test generation |
| Code Reviewer | Nova Pro | Code quality review |
| Debug | Nova Pro | Error analysis |
| Documentation | Nova Lite | Documentation generation |
| Python Specialist | Nova Pro | Python expertise |
| Web Specialist | Nova Pro | Web development |
| Database Specialist | Nova Pro | Database design |
| DevOps Specialist | Nova Pro | DevOps practices |
| Data Science Specialist | Nova Pro | ML/data science |
| Agile Specialist | Nova Lite | Agile processes |
| Doc Research Specialist | Nova Lite | Doc research |

**Note:** All model IDs use inference profile format (e.g., `us.anthropic.claude-sonnet-4-5-20250929-v1:0`). See [FIXES.md](FIXES.md) for configuration requirements.

## Tools

Each agent has access to:

**From `strands-agents-tools`:**
- File operations: `file_read`, `file_write`, `editor`
- Code execution: `python_repl`, `shell`
- Utilities: `calculator`, `current_time`

**From `basic-open-agent-tools`:**
- CSV operations: `read_csv_simple`, `write_csv_simple`
- Filesystem tools: Complete file/directory operations

**Via shell:**
- Testing: `pytest`, coverage tools
- Linting: `ruff`, `mypy`
- Git: `status`, `diff`, `log` (read-only in MVP)

## Example Usage

### Simple Task
```python
result = root_agent("Add a function to calculate fibonacci numbers")
# Clara delegates to Senior Coder → Test Engineer → Code Reviewer
```

### Complex Task
```python
result = root_agent("""
Refactor the authentication module to use JWT tokens:
1. Update the login endpoint
2. Add token validation middleware
3. Include comprehensive tests
4. Ensure security best practices
""")
# Clara orchestrates all three agents with multiple iterations
```

## Project Structure

```
Complex_Coding_Clara/
├── agent.py                          # Main orchestrator (Clara)
├── prompts.py                        # System prompts for all agents
├── agents/                           # Specialist agent modules
│   ├── __init__.py
│   ├── architect/                    # System architecture agent
│   ├── senior_coder/                 # Complex coding agent
│   ├── fast_coder/                   # Quick CRUD agent
│   ├── test_engineer/                # Test generation agent
│   ├── code_reviewer/                # Code review agent
│   ├── debug/                        # Debugging agent
│   ├── documentation/                # Documentation agent
│   ├── python_specialist/            # Python expert agent
│   ├── web_specialist/               # Web development agent
│   ├── database_specialist/          # Database expert agent
│   ├── devops_specialist/            # DevOps expert agent
│   ├── data_science_specialist/      # Data science agent
│   ├── agile_specialist/             # Agile process agent
│   └── doc_research_specialist/      # Doc research agent
├── config_validator.py               # Configuration validation system
├── agent_health_check.py             # Agent health monitoring
├── requirements.txt
├── README.md
├── FIXES.md                          # Configuration fixes documentation
├── TODO.md                           # Implementation roadmap
├── STATUS.md                         # Current development status
├── TOOLS_ANALYSIS.md                 # Tool capability analysis
└── coding-agent-architecture.md      # Architecture specification
```

## Configuration

### Environment Variables

```env
# Required
AWS_REGION=us-west-2              # AWS Bedrock region

# Optional
AWS_PROFILE=default               # AWS credentials profile
LOG_LEVEL=INFO                    # Logging level
```

## Development Status

**Current Status**: ✅ **Fully Operational** - All 14 agents working (100% success rate)

**Implemented:**
- ✅ Orchestrator with 14 specialist agents
- ✅ Agents-as-tools pattern across all agents
- ✅ Full tool integration (strands-tools + basic-open-agent-tools)
- ✅ AWS Bedrock model integration with inference profiles
- ✅ Retry logic with exponential backoff
- ✅ Configuration validation system
- ✅ Agent health monitoring system
- ✅ File, shell, and Python REPL access
- ✅ General coding agents (7): Architect, Senior Coder, Fast Coder, Test Engineer, Code Reviewer, Debug, Documentation
- ✅ Domain specialists (5): Python, Web, Database, DevOps, Data Science
- ✅ SDLC specialists (2): Agile, Doc Research

**Recent Fixes (2025-10-08):**
- ✅ Fixed test_engineer model configuration (inference profile format)
- ✅ Fixed documentation agent timeout handling
- ✅ Added comprehensive error handling and retry logic
- ✅ Created configuration validation system
- ✅ Created agent health monitoring system

**Planned Enhancements:**
- [ ] Custom AST analysis tools
- [ ] Structured test runner wrapper
- [ ] Enhanced git operation wrappers
- [ ] Router for automatic task classification
- [ ] Graph/Swarm coordination patterns
- [ ] Cost tracking and optimization dashboard

See [TODO.md](TODO.md) for complete roadmap and [FIXES.md](FIXES.md) for recent improvements.

## Cost Estimates

Based on architecture specifications:

| Task Type | Estimated Cost |
|-----------|---------------|
| Simple (endpoint, bug fix) | ~$0.04 |
| Medium (feature) | ~$0.20 |
| Complex (algorithm, refactor) | ~$0.57 |
| Daily (mixed tasks) | ~$2.54 |

## Known Limitations

- No custom code analysis (AST parsing) yet
- Git operations read-only (via shell)
- Test results require manual parsing
- No automatic task routing (orchestrator decides directly)
- Local execution not sandboxed (use with caution)
- Model timeout handling relies on retry logic (see [FIXES.md](FIXES.md))

## References

- [Strands Agents Documentation](https://strandsagents.com)
- [AWS Bedrock Models](https://docs.aws.amazon.com/bedrock/latest/userguide/models-supported.html)
- [Configuration Fixes & Monitoring](FIXES.md)
- [Architecture Design](coding-agent-architecture.md)
- [Implementation Roadmap](TODO.md)
- [Development Status](STATUS.md)
- [Tools Analysis](TOOLS_ANALYSIS.md)

---

**Status**: 🟢 Fully Operational (14/14 agents working)
**Version**: 1.0.0
**Last Updated**: October 2025
