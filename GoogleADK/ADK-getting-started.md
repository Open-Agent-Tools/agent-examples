# GoogleADK Getting Started

Quick setup guide for Google Agent Development Kit examples.

## Setup

```bash
# Install dependencies
pip install -r GoogleADK/requirements.txt

# Configure .env
ANTHROPIC_API_KEY=your_key_here
GOOGLE_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here

# Optional: Local models
OLLAMA_BASE_URL=http://localhost:11434
```

## Run Agents

**Web Interface (Recommended):**
```bash
cd GoogleADK && adk web
# Opens http://localhost:8000
```

**Individual Evaluation:**
```bash
PYTHONPATH=.:$PYTHONPATH adk eval \
  --config_file_path GoogleADK/Butler_Basil/evals/test_config.json \
  GoogleADK/Butler_Basil \
  GoogleADK/Butler_Basil/evals/list_available_tools.test.json
```

## Agents Available

- **Butler_Basil** - Task coordination
- **FileOps_Freddy** - File operations  
- **Jira_Johnny** - Jira integration
- **Scrum_Sam** - Multi-agent Scrum Master
- **Story_Sage** - User story specialist

## Troubleshooting

- Ensure API keys in `.env` file
- Run `adk web` from GoogleADK directory only
- Use `PYTHONPATH=.:$PYTHONPATH` for evaluations
