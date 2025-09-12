# QA Issues and Improvements

This file tracks issues found during QA testing and development.

## QA Testing Report - 2025-09-11

### Test Execution Summary
- Agent: Orchestrator_Ollie
- Code Quality: 2 MyPy errors, 2 runtime errors found
- Linting: All ruff checks passed ✅
- Functionality: Critical runtime errors prevent agent from starting

### Issues Found

#### Critical - Runtime Error - Incorrect function name in basic-open-agent-tools
**File/Location**: 
- `/Users/wes/Development/agent-examples/AWS_Strands/Orchestrator_Ollie/agent.py:41`
- `/Users/wes/Development/agent-examples/AWS_Strands/Orchestrator_Ollie/subagent.py:34`

**Description**: Both agent files call `boat.helpers.merge_tools_list()` but the correct function name is `merge_tool_lists()` (note the 's' at the end).

**Reproduction Steps**: 
1. Run `python agent.py` 
2. AttributeError occurs: `module 'basic_open_agent_tools.helpers' has no attribute 'merge_tools_list'`

**Expected Behavior**: Agent should start without errors
**Actual Behavior**: Runtime AttributeError prevents agent initialization
**Impact**: Agent completely non-functional - cannot start at all
**Testing Approach**: Fix function name and verify agent starts successfully

#### Critical - Runtime Error - Incorrect function name for data processing tools
**File/Location**: 
- `/Users/wes/Development/agent-examples/AWS_Strands/Orchestrator_Ollie/agent.py:42`
- `/Users/wes/Development/agent-examples/AWS_Strands/Orchestrator_Ollie/subagent.py:35`

**Description**: Both agent files call `boat.load_all_data_processing_tools()` but the correct function name is `load_all_data_tools()`.

**Reproduction Steps**: 
1. Fix the `merge_tools_list` issue first
2. Run `python agent.py`
3. AttributeError occurs for the data processing function

**Expected Behavior**: Agent should load 27 data processing tools as mentioned in documentation
**Actual Behavior**: Runtime AttributeError prevents proper tool loading
**Impact**: Agent lacks advertised CSV/data processing capabilities
**Testing Approach**: Fix function name and verify tools are loaded correctly

#### Medium - Type Safety - MyPy redefinition warnings
**File/Location**: `/Users/wes/Development/agent-examples/AWS_Strands/Orchestrator_Ollie/agent.py:35,71`

**Description**: MyPy reports "Name already defined (possibly by an import)" for SYSTEM_PROMPT and create_worker_agent due to try/except import blocks.

**Reproduction Steps**: 
1. Run `mypy AWS_Strands/Orchestrator_Ollie/ --ignore-missing-imports`
2. Two no-redef errors appear

**Expected Behavior**: Clean type checking with no redefinition warnings
**Actual Behavior**: MyPy warnings about name redefinition
**Impact**: Type safety concerns, potential confusion in IDE
**Testing Approach**: Use different variable names in except blocks or suppress warnings appropriately

#### Low - Documentation - Inconsistent tool count claims
**File/Location**: 
- `/Users/wes/Development/agent-examples/AWS_Strands/Orchestrator_Ollie/prompts.py:76`
- `/Users/wes/Development/agent-examples/AWS_Strands/Orchestrator_Ollie/README.md:95`

**Description**: Documentation claims "27 CSV/data tools" but uses incorrect function name that would cause runtime error.

**Reproduction Steps**: 
1. Read documentation claims about tool counts
2. Check actual function calls in code
3. Verify available functions in basic-open-agent-tools

**Expected Behavior**: Documentation should match working code
**Actual Behavior**: Documentation promises capabilities that don't work due to code errors
**Impact**: Misleading documentation, user confusion
**Testing Approach**: Verify actual tool counts after fixing runtime errors and update documentation accordingly

#### Low - Code Quality - Weak worker system prompt
**File/Location**: `/Users/wes/Development/agent-examples/AWS_Strands/Orchestrator_Ollie/subagent.py:61`

**Description**: Worker agent has minimal system prompt "You are a worker agent." which provides no guidance for task processing.

**Reproduction Steps**: 
1. Review WORKER_SYSTEM_PROMPT in subagent.py
2. Compare with main agent's comprehensive SYSTEM_PROMPT

**Expected Behavior**: Worker agents should have clear instructions for processing delegated tasks
**Actual Behavior**: Minimal prompt provides no task-specific guidance
**Impact**: Poor worker agent performance, unclear task processing
**Testing Approach**: Create comprehensive worker prompt and test delegation scenarios

#### Low - Architecture - Model inconsistency between orchestrator and worker
**File/Location**: 
- `/Users/wes/Development/agent-examples/AWS_Strands/Orchestrator_Ollie/agent.py:60` (Claude 3.5 Sonnet)
- `/Users/wes/Development/agent-examples/AWS_Strands/Orchestrator_Ollie/subagent.py:53` (Claude 3.5 Haiku)

**Description**: Orchestrator uses Sonnet (premium model) while worker uses Haiku (fast model). This is intentional for cost optimization but not documented.

**Reproduction Steps**: 
1. Compare model_id in both files
2. Check documentation for model choice rationale

**Expected Behavior**: Model choice should be documented and justified
**Actual Behavior**: No explanation for different model choices
**Impact**: Unclear architecture decisions, potential performance mismatches
**Testing Approach**: Document model selection rationale and test performance impact

### Standards Validation Results
- ❌ Runtime functionality: Agent fails to start due to function name errors
- ✅ Linting compliance: 100% ruff compliance achieved
- ❌ Type safety: MyPy warnings about name redefinitions
- ❌ Documentation accuracy: Claims don't match working code
- ❌ Error handling: No graceful degradation when tools fail to load
- ✅ AWS Strands compliance: Follows framework patterns correctly
- ❌ Integration testing: Cannot test due to runtime errors

### Recommended Next Steps
1. **URGENT**: Fix function name errors (`merge_tools_list` → `merge_tool_lists`, `load_all_data_processing_tools` → `load_all_data_tools`)
2. **HIGH**: Improve worker agent system prompt with specific task guidance
3. **MEDIUM**: Resolve MyPy type checking warnings with proper import handling
4. **LOW**: Update documentation to match actual working functionality
5. **LOW**: Document model selection rationale for orchestrator vs worker agents

### Testing Commands for Verification
```bash
# After fixes, verify agent starts
python AWS_Strands/Orchestrator_Ollie/agent.py

# Verify worker agent starts
python AWS_Strands/Orchestrator_Ollie/subagent.py

# Check tool loading
python3 -c "from AWS_Strands.Orchestrator_Ollie import root_agent; print(len(root_agent.tools))"

# Run quality checks
python3 -m ruff check AWS_Strands/Orchestrator_Ollie/ --fix
python3 -m mypy AWS_Strands/Orchestrator_Ollie/ --ignore-missing-imports
```