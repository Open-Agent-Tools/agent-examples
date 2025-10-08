# Tools Analysis for Complex Coding Clara

Analysis of available tools from `strands-agents-tools` and `basic-open-agent-tools` for the MVP implementation.

---

## Available from `strands-agents-tools` (Confirmed)

### File Operations ✅
- **file_read** - Read file contents with multiple modes
- **file_write** - Write content to files
- **editor** - Advanced file editing with syntax highlighting, pattern replacement

### Code Execution ✅
- **python_repl** - Execute Python code with state persistence (⚠️ not Windows)
- **shell** - Execute shell commands (⚠️ not Windows)
- **code_interpreter** - Sandboxed multi-language execution (Python, JS, TS) via AgentCore

### Basic Tools ✅
- **calculator** - Mathematical operations with symbolic math
- **current_time** - Get current time in various timezones

### AWS Integration ✅
- **use_aws** - Interact with AWS services (S3, EC2, etc.)

### Web & Research 🔍
- **http_request** - Make HTTP API calls
- **tavily_search** - Web search (requires TAVILY_API_KEY)
- **tavily_extract** - Extract content from URLs
- **tavily_crawl** - Advanced web crawling
- **tavily_map** - Website mapping

### Advanced Features ⚡
- **batch** - Execute multiple tools in parallel
- **workflow** - Multi-step workflow management
- **mcp_client** - Connect to MCP servers
- **think** - Multi-step reasoning
- **memory** - Store/retrieve from Bedrock Knowledge Bases
- **image_reader** - Process images for AI analysis
- **generate_image** - Create AI-generated images
- **use_computer** - Computer automation (mouse, keyboard, screen analysis)

---

## Available from `basic-open-agent-tools` (From documentation)

### Filesystem Tools (18 functions) ✅
From Orchestrator_Ollie example:
- `boat.load_all_filesystem_tools()` - Returns all file/directory tools
- File ops: read, write, append, delete, copy, move
- Directory ops: create, list, delete, tree visualization
- File info and existence checking

### Data Processing Tools (23 functions) ✅
From Orchestrator_Ollie example:
- `boat.data.read_csv_simple`
- `boat.data.write_csv_simple`
- `boat.data.csv_to_dict_list`
- JSON processing
- Configuration files (YAML, TOML, INI)
- Data validation

### Other Categories (166 total functions)
- **Network Tools** (4): HTTP client, DNS, port checking
- **System Tools** (19): Cross-platform shell, processes, env vars
- **Datetime Tools** (40): Date/time operations
- **Crypto Tools** (14): Cryptographic functions
- **PDF Tools** (8): PDF operations
- **Archive Tools** (9): Zip/tar operations
- **Logging Tools** (5): Logging utilities
- **Monitoring Tools** (8): System monitoring

---

## Gap Analysis for Coding Agent MVP

### ✅ COVERED - Available in existing tools

**File Operations**
- ✅ Read files (`file_read`, `boat.load_all_filesystem_tools()`)
- ✅ Write files (`file_write`, `boat.load_all_filesystem_tools()`)
- ✅ List directories (strands `file_read` or `boat` filesystem)
- ✅ Search files (strands `file_read` with glob patterns)

**Code Execution**
- ✅ Python execution (`python_repl` or `code_interpreter`)
- ✅ Shell commands (`shell` tool)
- ✅ Sandboxed execution (`code_interpreter` via AgentCore)

**Testing**
- ✅ Execute tests via `shell` tool
- ✅ Parse output via Python/shell

**Git Operations (Read-only)**
- ✅ `git status` via `shell` tool
- ✅ `git diff` via `shell` tool
- ✅ `git log` via `shell` tool

---

### ❌ GAPS - Need custom tools or workarounds

#### 1. **Code Analysis Tools** ❌
**Missing:**
- `parse_ast(code: str, language: str) -> dict`
- `analyze_complexity(code: str) -> dict`
- `find_references(symbol: str, workspace: str) -> list`
- `get_type_info(symbol: str, file: str) -> dict` (LSP integration)

**Options:**
- **Custom tool**: Use Python `ast` module for Python code
- **Shell + external tools**: Use `tree-sitter`, `ctags`, `ast-grep`
- **LSP client**: Integrate `pygls` or `python-lsp-server`
- **Defer to Phase 3**: Start without AST analysis

**Recommendation**: Create lightweight custom tools using Python `ast` module for MVP.

---

#### 2. **Git Operations (Write)** ⚠️
**Partially covered via shell:**
- ✅ `git status` (read)
- ✅ `git diff` (read)
- ⚠️ `git commit` (write - available via shell but needs wrapping)
- ⚠️ `create_branch` (write - available via shell but needs wrapping)

**Options:**
- **Use shell tool directly**: `agent.tool.shell(command="git commit -m 'message'")`
- **Custom git wrapper**: Create `@tool` wrappers for safety/validation
- **GitPython library**: Create tools using `gitpython` package
- **Defer write operations**: MVP with read-only git access

**Recommendation**: Use `shell` tool directly for MVP. Add git wrapper tools in Phase 3 for better error handling.

---

#### 3. **Linting & Formatting** ⚠️
**Available via shell:**
- ✅ `ruff check` via shell
- ✅ `ruff format` via shell
- ✅ `mypy` via shell
- ✅ `black`, `prettier`, etc. via shell

**Missing:**
- ❌ Structured linter output parsing
- ❌ Auto-fix capabilities wrapped nicely

**Options:**
- **Use shell tool**: Direct invocation (e.g., `shell(command="ruff check --fix")`)
- **Custom wrappers**: Parse JSON output from linters
- **Defer**: MVP without auto-formatting

**Recommendation**: Use `shell` tool for MVP. Create structured wrappers in Phase 3.

---

#### 4. **Test Framework Integration** ❌
**Missing:**
- `run_tests(test_path: str, framework: str) -> dict`
- `coverage_report(test_path: str) -> dict`
- `benchmark(code: str) -> dict`

**Available via shell:**
- ✅ `pytest` via shell
- ✅ `coverage` via shell
- ✅ Parse output manually

**Options:**
- **Custom tool**: Wrap pytest with structured output
- **Shell + parsing**: Run via shell, parse results
- **Defer**: MVP with simple shell invocation

**Recommendation**: Create custom `run_tests` tool that wraps pytest and returns structured results (pass/fail, coverage %).

---

#### 5. **Code Execution Sandboxing** ⚠️
**Available:**
- ✅ `code_interpreter` (AgentCore sandbox - requires AWS setup)
- ⚠️ `python_repl` (local, not sandboxed)
- ⚠️ `shell` (local, not sandboxed)

**Gap:** Local sandboxing for non-AgentCore deployments

**Options:**
- **Use AgentCore**: `code_interpreter` provides true sandboxing
- **Docker wrapper**: Create custom tool using Docker
- **Restricted subprocess**: Use Python `subprocess` with resource limits
- **Defer**: MVP without sandboxing, use AgentCore later

**Recommendation**: Use `python_repl` and `shell` for MVP local dev. Document need for `code_interpreter` in production.

---

## Tool Stack Recommendation for MVP

### Phase 1 MVP Toolset

**From `strands-agents-tools`:**
```python
from strands_tools import (
    file_read,           # File operations
    file_write,
    editor,              # Advanced file editing
    python_repl,         # Python execution
    shell,               # Shell commands (git, pytest, etc.)
    calculator,          # Math operations
    current_time,        # Timestamps
)
```

**From `basic-open-agent-tools`:**
```python
import basic_open_agent_tools as boat

# CSV and data processing
csv_tools = [
    boat.data.read_csv_simple,
    boat.data.write_csv_simple,
    boat.data.csv_to_dict_list,
]

# All filesystem tools
file_tools = boat.load_all_filesystem_tools()
```

**Custom Tools to Build:**
```python
# Custom tool 1: Simple AST analysis (Phase 1 or 2)
@tool
def analyze_python_code(code: str) -> dict:
    """Analyze Python code structure using ast module."""
    # Parse with Python ast, return functions, classes, imports
    pass

# Custom tool 2: Structured test runner (Phase 2)
@tool
def run_tests(test_path: str, framework: str = "pytest") -> dict:
    """Run tests and return structured results."""
    # Run pytest, parse output, return pass/fail/coverage
    pass

# Custom tool 3: Git operations wrapper (Phase 3)
@tool
def git_commit(message: str, files: list[str]) -> bool:
    """Safely commit files with validation."""
    pass
```

---

## Implementation Strategy

### Phase 1: Use Existing Tools
- ✅ File ops: `file_read`, `file_write`, `editor`, `boat.load_all_filesystem_tools()`
- ✅ Code execution: `python_repl`, `shell`
- ✅ Git (read): `shell(command="git status")`, `shell(command="git diff")`
- ✅ Tests: `shell(command="pytest")`
- ✅ Linting: `shell(command="ruff check")`

**Gaps handled:**
- Manual output parsing by agents
- No AST analysis (agents read code as text)
- No structured test results

### Phase 2: Add Custom Wrappers
- 🔧 `analyze_python_code()` - Simple AST analysis
- 🔧 `run_tests()` - Structured test execution
- 🔧 Git wrappers for better error handling

### Phase 3: Advanced Features
- 🔧 LSP integration for type info
- 🔧 Code complexity analysis
- 🔧 Symbol search/references
- 🔧 Proper sandboxing (Docker or AgentCore)

---

## Feedback for Upstream Packages

### For `strands-agents-tools`
**Feature requests:**
1. ✅ Already has: `file_read`, `file_write`, `editor`, `shell`, `python_repl`
2. 📋 Would be nice: `git` tool wrapper (status, diff, commit with validation)
3. 📋 Would be nice: `run_tests` tool with structured output
4. 📋 Would be nice: `lint` tool wrapper (ruff, mypy, black)

### For `basic-open-agent-tools`
**Feature requests:**
1. ✅ Already has: Filesystem tools, CSV tools, data processing
2. 📋 Would be nice: Git operation wrappers
3. 📋 Would be nice: Test framework integration
4. 📋 Would be nice: Code analysis tools (AST, complexity)

---

## Decision Required

**Question 7 answer based on this analysis:**

For the MVP, we should use:
- **Standard tools from both packages** (file, shell, python_repl, CSV, etc.)
- **Defer custom tools to Phase 2** (AST analysis, structured test runner)
- **Use shell for git/linting** (simple but works)

This gives us a fully functional MVP immediately, with clear path to add custom tools later.

**Does this approach work for you?**
