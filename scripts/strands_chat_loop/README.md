# Strands Chat Loop

A feature-rich, interactive CLI for AWS Strands agents with token tracking, prompt templates, and extensive configuration options.

## Features

✅ **Command History** - Navigate previous queries with ↑↓ arrows (saved to `~/.chat_history`)
✅ **Multi-line Input** - Type `\\` to enter multi-line mode for code blocks
✅ **Token Tracking** - Track tokens and costs per query and session
✅ **Prompt Templates** - Reusable prompts from `~/.prompts/`
✅ **Configuration** - YAML-based config with per-agent overrides
✅ **Status Bar** - Real-time metrics (queries, tokens, duration)
✅ **Session Summary** - Full stats on exit (always shown)
✅ **Rich Formatting** - Enhanced markdown rendering with syntax highlighting
✅ **Error Recovery** - Automatic retry logic with exponential backoff
✅ **Agent Metadata** - Display model, tools, and capabilities

## Installation

```bash
# Install dependencies
pip install -r scripts/strands_chat_loop/requirements.txt

# Or with uv (faster)
uv pip install -r scripts/strands_chat_loop/requirements.txt
```

## Quick Start

```bash
# Run with any Strands agent
python scripts/strands_chat_loop/chat_loop.py --agent AWS_Strands/Product_Pete/agent.py

# With custom config
python scripts/strands_chat_loop/chat_loop.py --agent <agent> --config ~/.chatrc-custom
```

## Configuration

### Setup Config File

```bash
# Copy example config
cp scripts/strands_chat_loop/.chatrc.example ~/.chatrc

# Edit your preferences
nano ~/.chatrc
```

### Config Hierarchy

Configs are loaded in order (later overrides earlier):
1. Built-in defaults
2. Global `~/.chatrc`
3. Project `.chatrc` (current dir or up to 3 parents)
4. Explicit `--config` flag

### Example Config

```yaml
features:
  show_tokens: true           # Display token counts
  auto_save: false            # Save conversations on exit
  rich_enabled: true          # Enhanced formatting

ui:
  show_status_bar: true       # Top status bar
  show_duration: true         # Query duration

behavior:
  max_retries: 3              # Retry attempts on failure
  timeout: 120.0              # Request timeout (seconds)

agents:
  'Product Pete':
    features:
      show_tokens: false      # Override for Pete
```

See [CONFIG.md](CONFIG.md) for full documentation.

## Prompt Templates

### Create Templates

Save markdown files to `~/.prompts/`:

```bash
# Create template directory
mkdir -p ~/.prompts

# Create a code review template
cat > ~/.prompts/review.md <<'EOF'
# Code review
Please review the following code for:
- Best practices and design patterns
- Potential bugs or edge cases
{input}
EOF
```

### Use Templates

```
You: templates
Available Prompt Templates (1):
  /review - Code review

You: /review def foo(): return bar
✓ Loaded template: review
[Agent receives full template with your code]
```

### Template Variables

- `{input}` - Replaced with your context
- If no `{input}`, context is appended to template

## Commands

| Command | Description |
|---------|-------------|
| `help` | Show help message |
| `info` | Show agent details (model, tools) |
| `templates` | List available prompt templates |
| `/name` | Use prompt template from `~/.prompts/name.md` |
| `clear` | Clear screen and reset agent session |
| `exit` / `quit` | Exit chat (shows session summary) |

## Multi-line Input

```
You: \\
... def factorial(n):
...     if n <= 1:
...         return 1
...     return n * factorial(n - 1)
...
[Press Enter on empty line to submit]
```

## Token Tracking

### During Chat (with `show_tokens: true`)
```
------------------------------------------------------------
Time: 6.3s │ 1 cycle │ Tokens: 4.6K (in: 4.4K, out: 237) │ Cost: $0.017
```

### Session Summary (always shown on exit)
```
============================================================
Session Summary
------------------------------------------------------------
  Duration: 12m 34s
  Queries: 15
  Tokens: 67.8K (in: 45.2K, out: 22.6K)
  Total Cost: $0.475
============================================================
```

## Status Bar

Enable in config with `ui.show_status_bar: true`:

```
┌────────────────────────────────────────────────────────┐
│ Clara │ Sonnet 4.5 │ 5 queries │ 23.4K tokens │ 8m 42s │
└────────────────────────────────────────────────────────┘
```

## Programmatic Usage

```python
from scripts.strands_chat_loop import ChatLoop

# Create chat interface
chat = ChatLoop(
    agent=your_agent,
    name="My Agent",
    description="Agent description",
    config_path=Path("~/.chatrc")  # Optional
)

# Run interactive loop
chat.run()
```

## Dependencies

### Required
- `anthropic-bedrock>=0.10.0` - AWS Bedrock integration
- `pyyaml>=6.0.1` - Config file parsing

### Optional but Recommended
- `rich>=13.7.0` - Enhanced markdown rendering
- Built-in `readline` (Unix) or `pyreadline3` (Windows) - Command history

## Progress

**Completed:** 11/27 features (41%)

See [Chat_TODO.md](Chat_TODO.md) for full roadmap.

## Files

- `chat_loop.py` - Main chat loop implementation (1300+ lines)
- `chat_config.py` - Configuration management (300+ lines)
- `.chatrc.example` - Example configuration with docs
- `CONFIG.md` - Configuration guide
- `Chat_TODO.md` - Feature roadmap and progress

## License

Part of the [agent-examples](../..) repository.

## See Also

- [CONFIG.md](CONFIG.md) - Full configuration documentation
- [Chat_TODO.md](Chat_TODO.md) - Feature roadmap
- [AWS Strands Documentation](../../AWS_Strands/)
