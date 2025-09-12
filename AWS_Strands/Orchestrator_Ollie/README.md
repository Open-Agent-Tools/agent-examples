# Orchestrator Ollie

A specialized AWS Strands agent for coordinating and orchestrating complex tasks across multiple systems, agents, and workflows.

## Overview

Orchestrator Ollie excels at:
- **Task Decomposition**: Breaking complex processes into manageable components
- **Workflow Management**: Designing and executing multi-stage workflows
- **System Integration**: Coordinating interactions between different tools and services
- **Agent Coordination**: Delegating tasks to specialized agents and aggregating results

## Quick Start

### Prerequisites
```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp ../../example_env .env  # Add your ANTHROPIC_API_KEY
```

### Running the Agent

#### Interactive Chat (via generic chat loop)
```bash
cd /path/to/agent-examples
python AWS_Strands/chat_loop.py --agent AWS_Strands/Orchestrator_Ollie/agent.py
```

#### Direct execution
```bash
cd AWS_Strands/Orchestrator_Ollie
python agent.py
```

#### Programmatic usage
```python
from AWS_Strands.Orchestrator_Ollie import root_agent

# Simple task orchestration
response = root_agent("Help me coordinate a multi-step deployment process")

# Complex workflow design
workflow_plan = root_agent("""
Design a workflow for:
1. Code review and testing
2. Staging deployment
3. Production deployment with rollback capability
""")
```

## Agent Capabilities

### Core Orchestration Features
- **Multi-step Process Management**: Coordinate complex sequences of operations
- **Dependency Resolution**: Handle task dependencies and execution ordering
- **Parallel Execution Planning**: Identify opportunities for concurrent operations
- **Error Recovery**: Implement robust failure handling and recovery strategies
- **Progress Monitoring**: Track and report on workflow execution status

### Use Cases
- **DevOps Workflows**: CI/CD pipeline coordination, deployment orchestration
- **Data Processing**: Multi-stage data pipelines with validation and error handling
- **Business Process Automation**: Coordinating tasks across different business systems
- **Multi-Agent Coordination**: Managing interactions between specialized AI agents
- **Project Management**: Task scheduling and resource coordination

## Configuration

### Environment Variables
```env
# Required
ANTHROPIC_API_KEY=your_anthropic_key_here

# Optional: For enhanced capabilities
MCP_SERVER_URL=http://localhost:9000/mcp/
```

### Model Configuration
- **Default Model**: Claude 3.5 Sonnet (claude-3-5-sonnet-20241022)
- **Max Tokens**: 8192 (suitable for complex orchestration plans)
- **Temperature**: 0.3 (balanced between reliability and creativity)

## Architecture

### Core Components
- **agent.py**: Main agent implementation with Strands framework integration
- **prompts.py**: Orchestration-specific system prompts and instructions
- **__init__.py**: Module exports and version management
- **requirements.txt**: Dependency specifications

### Available Tools
- **27 data processing tools** from basic-open-agent-tools (CSV reading, writing, cleaning, validation)
- **18 file system tools** from basic-open-agent-tools (read/write/move/copy files and directories)  
- **worker_agent** - Tool for delegating tasks to specialized worker sub-agents
- Fallback to strands_tools if basic-open-agent-tools unavailable

## Example Interactions

### Workflow Design
```
User: Design a workflow for deploying a web application with proper testing and rollback capabilities.

Ollie: I'll design a comprehensive deployment workflow for you:

## Analysis
This requires a multi-stage process with validation gates, parallel testing, and rollback mechanisms.

## Decomposition
1. Pre-deployment validation
2. Staging deployment and testing
3. Production deployment
4. Post-deployment verification
5. Rollback procedures (if needed)

## Dependencies
- Code must pass all tests before staging
- Staging must be validated before production
- Rollback plan must be prepared before production deployment

[Detailed execution plan follows...]
```

### Worker Agent Delegation
```
User: Process this CSV file of customer data - validate emails, standardize phone numbers, and flag duplicates.

Ollie: I'll orchestrate this using worker agents:

## Analysis
CSV has 1000 rows of customer data requiring validation and standardization.

## Agent Strategy  
I'll delegate individual rows to worker agents, processing up to 5 concurrent workers.

## Execution Plan
1. Read CSV structure using data processing tools
2. Delegate each row to worker_agent with specific validation instructions
3. Workers will validate emails, standardize phones, check for duplicates
4. Aggregate results and generate summary report

[Processing begins with worker delegation...]
```

## Development

### Extending Capabilities
To add new orchestration capabilities:

1. **Add Tools**: Extend the tools list in `agent.py`
2. **Update Prompts**: Modify `prompts.py` for new orchestration patterns
3. **Create Workflows**: Add reusable workflow templates

### Testing
```bash
# Basic functionality test
python agent.py

# Interactive testing
python ../chat_loop.py --agent agent.py
```

## Status
- **Framework**: AWS Strands ✅
- **Model Integration**: Anthropic Claude ✅
- **Basic Tools**: File operations, time utilities ✅
- **Multi-Agent Tools**: Swarm and graph coordination ✅
- **Core Orchestration**: Task decomposition and workflow design ✅
- **Status**: Ready for advanced multi-agent orchestration

## Next Steps
- Add specialized orchestration tools (task queues, monitoring)
- Implement workflow persistence and resumption
- Add integration with common DevOps and automation platforms
- Create reusable workflow templates library

---

*Agent Status: ✅ Functional - Basic orchestration capabilities ready*