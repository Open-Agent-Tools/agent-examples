# Complex Coding Clara - Implementation TODO

**Current Status:** ✅ **Phases 1-6 Complete** - All 14 agents operational with 3-tier cost optimization

This TODO tracks remaining enhancements and optimizations for the Clara multi-agent coding system.

## Current State (January 2025)

**✅ Completed:**
- 14 specialist agents implemented and operational (100% success rate)
- 3-tier cost-optimized model distribution (54% cost savings)
- Agents-as-tools pattern across all agents
- Basic tool integration (strands-tools + basic-open-agent-tools)
- MCP integrations: Atlassian (Agile Specialist), Context7 (Doc Research)
- Configuration validation and health monitoring systems
- http_request tool added to Web Specialist and Doc Research Specialist

**See [STATUS.md](STATUS.md) for complete implementation details.**

---

## Remaining Work

### Priority 0 (Critical - High Impact, Low Effort)

#### Custom Tools - Structured Test Output
**Impact:** Test Engineer can't parse test results → manual analysis required
- [ ] Create `run_pytest()` wrapper that:
  - Executes pytest with `--json-report` flag
  - Parses JSON output into structured format
  - Returns: passed/failed counts, coverage %, specific failures
  - Error handling for missing pytest-json-report plugin
- [ ] Add to Test Engineer agent tools
- [ ] Update Test Engineer prompt to use structured output

**Files:** `tools/testing_tools.py`, `agents/test_engineer/agent.py`

---

#### Custom Tools - Git Write Operations
**Impact:** Can't create commits, branches, PRs → manual git operations required
- [ ] Create `git_commit()` wrapper:
  - Stage files with validation
  - Create commit with message
  - Return commit hash and summary
  - Error handling for conflicts
- [ ] Create `git_branch()` wrapper:
  - Create/switch branches
  - Check branch existence
  - Handle conflicts
- [ ] Create `git_push()` wrapper with safety checks
- [ ] Add to relevant agents (Senior Coder, Fast Coder, Debug)
- [ ] Update prompts to document git write capabilities

**Files:** `tools/git_tools.py`, multiple agent files

---

#### Intelligence - Cost Tracking
**Impact:** No visibility into actual costs → can't validate savings claims
- [ ] Implement token usage logging per agent call
- [ ] Calculate cost using model pricing:
  - Sonnet 4.5: $3/$15 per million
  - Haiku 3.5: $0.80/$4 per million
  - Nova Pro: $0.80/$3.20 per million
  - Llama 3.3: $0.99/$0.99 per million
  - Nova Lite: $0.075/$0.30 per million
- [ ] Log to file or database per request
- [ ] Create summary report function
- [ ] Add to Clara orchestrator

**Files:** `agent.py`, `tools/cost_tracking.py`

---

### Priority 1 (Important - High Impact, Medium Effort)

#### Custom Tools - Static Analysis JSON Parsers
**Impact:** Linting/type checking via shell only → no structured feedback
- [ ] Create `run_ruff_check()` wrapper:
  - Execute `ruff check --output-format=json`
  - Parse JSON output
  - Return structured errors by file/line
- [ ] Create `run_mypy()` wrapper:
  - Execute `mypy --output=json`
  - Parse JSON output
  - Return type errors by file/line
- [ ] Add to Code Reviewer agent
- [ ] Update Code Reviewer prompt

**Files:** `tools/static_analysis_tools.py`, `agents/code_reviewer/agent.py`

---

#### Custom Tools - Secret Detection
**Impact:** Security risk - can't scan for leaked secrets
- [ ] Create `scan_secrets()` tool:
  - Regex patterns for common secrets (API keys, tokens, passwords)
  - Integration with truffleHog or detect-secrets (optional)
  - Return: file, line, secret type, severity
- [ ] Add to Code Reviewer agent
- [ ] Update Code Reviewer prompt for security scanning

**Files:** `tools/security_tools.py`, `agents/code_reviewer/agent.py`

---

#### Custom Tools - AST Parsing
**Impact:** Can't analyze code structure programmatically
- [ ] Create `parse_ast()` tool:
  - Use Python `ast` module for Python code
  - Support for function/class extraction
  - Return: functions, classes, imports, complexity hints
- [ ] Create `analyze_complexity()` tool:
  - McCabe complexity calculation
  - Lines of code metrics
  - Return: complexity score, refactoring candidates
- [ ] Add to Senior Coder and Code Reviewer agents
- [ ] Update prompts

**Files:** `tools/ast_tools.py`, multiple agent files

---

#### Intelligence - Router Agent (Nova Micro)
**Impact:** Clara manually decides routing → no automatic task classification
- [ ] Create Router agent with Nova Micro:
  - Task complexity classifier (SIMPLE → MEDIUM → COMPLEX → CRITICAL)
  - Return: recommended agent(s), confidence score, reasoning
  - Use Nova Micro for cost optimization
- [ ] Integrate into Clara orchestrator:
  - Query router before delegating
  - Allow override for low confidence
  - Log routing decisions for analysis
- [ ] Track routing accuracy over time

**Files:** `agents/router/agent.py`, `agent.py`

---

#### Intelligence - Prompt Caching
**Impact:** Missing 40%+ potential cost savings on repeated prompts
- [ ] Implement prompt caching for:
  - Agent system prompts (cached per agent)
  - Project context (file structures, common imports)
  - Tool definitions (cached per agent)
- [ ] Use AWS Bedrock caching features (if available)
- [ ] Track cache hit rates
- [ ] Implement cache invalidation strategy:
  - Time-based (e.g., 5 minutes)
  - Content-based (hash of prompt)

**Files:** `agent.py`, all agent files in `agents/*/agent.py`

---

#### Orchestration - Graph Pattern
**Impact:** Sequential execution only → can't optimize workflows
- [ ] Implement `patterns/graph_pattern.py`:
  - Use Strands `GraphBuilder` (if available)
  - Define standard workflow: Code → Test → Review → Doc
  - Add conditional branching:
    - If review fails → return to coder with feedback
    - If tests fail → return to coder with error details
  - Support parallel execution where possible
- [ ] Integrate into Clara orchestrator
- [ ] Add workflow selection logic

**Example Flow:**
```
User Request → Clara
              ↓
         [Coder Agent] → Test Engineer → Code Reviewer → Documentation
                            ↓ fail          ↓ fail
                         Back to Coder   Back to Coder
```

**Files:** `patterns/graph_pattern.py`, `agent.py`

---

#### Orchestration - Conditional Branching
**Impact:** No retry logic on failures → manual intervention required
- [ ] Implement retry logic for:
  - Test failures → send errors back to coder
  - Review issues → send feedback back to coder
  - Build failures → send logs to debug agent
- [ ] Add max retry limit (e.g., 3 attempts)
- [ ] Track retry success rates

**Files:** `agent.py`, `patterns/graph_pattern.py`

---

### Priority 2 (Enhancement - Medium Impact, Medium-High Effort)

#### Custom Tools - Profiling & Performance
**Impact:** Can't identify performance bottlenecks
- [ ] Create `profile_code()` tool:
  - Integrate cProfile
  - Run code with profiling
  - Return: top functions by time, call counts
- [ ] Create `detect_memory_leaks()` tool:
  - Integration with memory_profiler or tracemalloc
  - Return: memory usage over time, leak candidates
- [ ] Add to Debug agent
- [ ] Update Debug prompt

**Files:** `tools/profiling_tools.py`, `agents/debug/agent.py`

---

#### Custom Tools - LSP Integration
**Impact:** Missing type hints, autocomplete context, go-to-definition
- [ ] Research LSP libraries (pylsp, pyright, jedi)
- [ ] Create `get_type_info()` tool:
  - Query LSP server for type at position
  - Return: type, documentation, signature
- [ ] Create `find_references()` tool:
  - Find all references to symbol
  - Return: file, line, context
- [ ] Add to Senior Coder and Python Specialist
- [ ] Requires LSP server running (separate process)

**Files:** `tools/lsp_tools.py`, multiple agent files

---

#### Domain Tools - Database Specialist
**Impact:** No query optimization guidance
- [ ] Create `analyze_query_plan()` tool:
  - Execute EXPLAIN/EXPLAIN ANALYZE
  - Parse output for slow operations
  - Return: scan types, index usage, recommendations
- [ ] Create `suggest_indexes()` tool:
  - Analyze query patterns
  - Suggest missing indexes
  - Estimate impact
- [ ] Add to Database Specialist
- [ ] Update Database Specialist prompt

**Files:** `tools/database_tools.py`, `agents/database_specialist/agent.py`

---

#### Domain Tools - DevOps Specialist
**Impact:** No validation for K8s/Terraform configs
- [ ] Create `validate_k8s_manifest()` tool:
  - Use kubeval or kubectl --dry-run
  - Return: validation errors, warnings
- [ ] Create `terraform_plan()` wrapper:
  - Execute terraform plan
  - Parse output for changes
  - Return: resources to add/change/destroy
- [ ] Add to DevOps Specialist
- [ ] Update DevOps Specialist prompt

**Files:** `tools/devops_tools.py`, `agents/devops_specialist/agent.py`

---

#### Intelligence - Metrics Dashboard
**Impact:** Can't measure agent performance over time
- [ ] Create metrics collection:
  - Success/failure rates per agent
  - Average response time per agent
  - Cost per task type
  - Routing accuracy (if router implemented)
- [ ] Create dashboard (web-based or CLI):
  - Summary statistics
  - Agent performance comparison
  - Cost trends over time
  - Routing decision analysis
- [ ] Export to CSV for analysis

**Files:** `tools/metrics.py`, `dashboard/app.py` (optional)

---

### Priority 3 (Future - Low Impact or High Effort)

#### Orchestration - Swarm Pattern
**Impact:** Can't parallelize exploration tasks (low priority for coding)
- [ ] Implement `patterns/swarm_pattern.py`:
  - Use Strands `Swarm` class (if available)
  - Allow multiple agents to work in parallel
  - Synthesize results in Clara
  - Good for: research, multiple approaches, brainstorming
- [ ] Integrate into Clara orchestrator
- [ ] Define use cases where Swarm is beneficial

**Files:** `patterns/swarm_pattern.py`, `agent.py`

---

#### Security - Code Execution Sandboxing
**Impact:** Security risk for arbitrary code execution
- [ ] Research sandboxing options:
  - Docker containers (isolated execution)
  - pyodide (WASM-based Python)
  - Firecracker microVMs
  - AWS Lambda (serverless execution)
- [ ] Implement sandbox wrapper for python_repl
- [ ] Add resource limits (CPU, memory, time)
- [ ] Add filesystem restrictions
- [ ] Update all agents using python_repl

**Files:** `tools/sandbox.py`, all agent files

---

#### Production - Session State Persistence
**Impact:** Can't save/resume conversations
- [ ] Implement session storage:
  - Local filesystem (MVP)
  - S3 (production)
  - Include: conversation history, agent state, context
- [ ] Add session management:
  - Create/load/save/delete sessions
  - Session expiration
  - Session summary generation
- [ ] Integrate into Clara orchestrator

**Files:** `session/manager.py`, `agent.py`

---

#### Production - AgentCore Deployment
**Impact:** Not production-ready for scale
- [ ] Research Amazon Bedrock AgentCore Runtime
- [ ] Create containerization strategy (Docker)
- [ ] Implement auto-scaling configuration
- [ ] Set up CloudWatch integration:
  - Custom metrics (cost, latency, quality)
  - Distributed tracing
  - Error tracking and alerting
- [ ] Security hardening:
  - API key management (Secrets Manager)
  - Input validation and sanitization
  - Audit logging
  - Rate limiting

**Files:** `Dockerfile`, `deployment/`, `observability/`

---

## Individual Agent TODO Lists

For agent-specific tool needs, see:
- `agents/test_engineer/TODO.md` - Coverage tools, fixture generation
- `agents/code_reviewer/TODO.md` - Static analysis, secret detection
- `agents/python_specialist/TODO.md` - PEP compliance, type hints
- `agents/database_specialist/TODO.md` - Query analysis, migrations
- `agents/devops_specialist/TODO.md` - K8s validation, Terraform
- `agents/debug/TODO.md` - Profiling, memory leak detection
- `agents/web_specialist/TODO.md` - Bundle analysis, accessibility
- `agents/agile_specialist/TODO.md` - MCP enhancements
- `agents/doc_research_specialist/TODO.md` - MCP enhancements
- (Others have minimal tool gaps)

---

## Success Metrics

### Phase 7 (Custom Tools - P0/P1)
- [ ] Structured test output reduces manual analysis by 80%
- [ ] Git write operations enable full workflow automation
- [ ] Cost tracking shows actual spend vs estimates
- [ ] Static analysis JSON parsing improves code quality feedback
- [ ] Secret detection prevents credential leaks
- [ ] AST parsing enables intelligent refactoring suggestions

### Phase 8 (Intelligence - P1)
- [ ] Router agent correctly classifies 90%+ of tasks
- [ ] Prompt caching reduces costs by 40%+
- [ ] Graph pattern reduces workflow steps by 30%
- [ ] Conditional branching enables automatic error recovery

### Phase 9 (Production - P2/P3)
- [ ] Metrics dashboard provides visibility into all operations
- [ ] Domain tools (DB, DevOps) reduce manual validation time
- [ ] LSP integration improves code intelligence
- [ ] Sandboxing enables safe arbitrary code execution
- [ ] AgentCore deployment supports production scale

---

## Cost Targets

**Current (with Phase 7 tools):**
- Simple Task: ~$0.04 (endpoint, bug fix)
- Medium Task: ~$0.20 (feature implementation)
- Complex Task: ~$0.57 (algorithm, architecture)

**After Prompt Caching (Phase 8):**
- Simple Task: ~$0.02 (50% reduction)
- Medium Task: ~$0.12 (40% reduction)
- Complex Task: ~$0.34 (40% reduction)

---

## Technical Decisions Needed

1. **LSP Integration**: Which library? pylsp, pyright, jedi? Separate process or embedded?
2. **Sandboxing**: Docker, pyodide, Lambda, or accept risk for MVP?
3. **Router Model**: Nova Micro (when available) or use Nova Pro/Haiku?
4. **Metrics Storage**: Local files, SQLite, or cloud database?
5. **Session Storage**: Local filesystem for MVP or S3 from start?
6. **Graph Pattern**: Use Strands GraphBuilder if available, or custom implementation?

---

## References

- **Architecture:** [coding-agent-architecture.md](coding-agent-architecture.md)
- **Current Status:** [STATUS.md](STATUS.md)
- **Recent Work:** [OPTIMIZATION_SUMMARY.md](OPTIMIZATION_SUMMARY.md)
- **Configuration:** [FIXES.md](FIXES.md)
- **Strands Docs:** https://strandsagents.com
- **AWS Bedrock:** https://aws.amazon.com/bedrock/models

---

**Last Updated:** January 2025
**Status:** 🟢 System Operational - Planning Phase 7+ Enhancements
**Next Priority:** P0 Custom Tools (Structured Testing, Git Operations, Cost Tracking)
