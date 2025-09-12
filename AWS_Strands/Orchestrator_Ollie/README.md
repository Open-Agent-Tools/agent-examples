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
- **Parallel Task Execution**: Use up to 5 worker agents simultaneously for CSV processing and other tasks
- **Error Recovery**: Implement robust failure handling and recovery strategies
- **Progress Monitoring**: Track and report on workflow execution status

### CSV Processing with Worker Delegation
- **Parallel CSV Processing**: Process CSV files using multiple worker agents concurrently
- **Row-by-row Delegation**: Assign individual CSV rows to specific worker agents
- **Task Aggregation**: Collect and combine results from all worker agents
- **Data Validation**: Coordinate data validation across multiple workers

### Use Cases
- **CSV Data Processing**: Large-scale data processing with parallel worker delegation
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
- **Orchestrator Model**: Claude 3.5 Sonnet (claude-3-5-sonnet-20241022) for complex orchestration
- **Worker Model**: Claude 3.5 Haiku (claude-3-5-haiku-20241022) for fast task processing
- **Max Tokens**: 8192 (orchestrator) / 4096 (workers)
- **Temperature**: 0.3 (balanced between reliability and creativity)

## Architecture

### Core Components
- **agent.py**: Main orchestrator with 5 individual worker tools (worker1-worker5)
- **subagent.py**: Worker sub-agent for delegated task processing
- **prompts.py**: Orchestration-specific system prompts and CSV processing workflows
- **test_data.csv**: Test CSV file with 20 fictional universes/music styles
- **__init__.py**: Module exports and version management
- **requirements.txt**: Dependencies including basic-open-agent-tools

### Available Tools
- **CSV tools** from basic-open-agent-tools (read_csv_simple, write_csv_simple, csv_to_dict_list)
- **File system tools** from basic-open-agent-tools (read/write/move/copy files and directories)
- **5 Worker Agents**: worker1, worker2, worker3, worker4, worker5 - Individual tools for parallel task delegation
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

### CSV Processing with 5 Worker Agents
```
User: Process this CSV file with 20 writing styles - add descriptions for each one.

Ollie: I'll orchestrate this using 5 worker agents for parallel processing:

## Analysis
CSV has 20 rows requiring description generation for fictional universes and music styles.

## Agent Strategy  
I'll assign 4 rows each to worker1-worker5 for simultaneous processing.

## Execution Plan
1. Read CSV data using csv_to_dict_list
2. Assign rows 1-4 to worker1, 5-8 to worker2, 9-12 to worker3, 13-16 to worker4, 17-20 to worker5
3. Each worker processes their assigned rows independently
4. Aggregate all results and save to new CSV file

Example workflow:
- worker1: Process "Star Wars", "Harry Potter", "Bruno Mars", "Hobbits"
- worker2: Process "Marvel Universe", "Game of Thrones", "Taylor Swift", "Lord of the Rings"
- worker3: Process "The Beatles", "Disney Princess", "Sherlock Holmes", "Ed Sheeran"
- worker4: Process "Cyberpunk", "Adele", "Pirates of the Caribbean", "Anime"
- worker5: Process "Beyoncé", "Steampunk", "Johnny Cash", "Western"

[Processing begins with parallel worker delegation...]
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
- **Model Integration**: Anthropic Claude (Sonnet + Haiku) ✅
- **BOAT Tools**: CSV and file system operations ✅
- **5 Worker Agents**: Individual parallel task delegation ✅
- **Core Orchestration**: Task decomposition and workflow design ✅
- **Status**: Ready for parallel CSV processing and task orchestration

## Next Steps
- Add specialized orchestration tools (task queues, monitoring)
- Implement workflow persistence and resumption
- Add integration with common DevOps and automation platforms
- Create reusable workflow templates library

---

*Agent Status: ✅ Functional - Basic orchestration capabilities ready*