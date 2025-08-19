# Claude Instructions

## Quick Cleanup Command

When user says **"cleanup"**: 
1. **Run Quality Tools**: Execute all quality checks and fix issues
   ```bash
   python3 -m ruff check GoogleADK/ evals/ --fix
   python3 -m ruff format GoogleADK/ evals/
   python3 -m mypy GoogleADK/
   python3 -m pytest
   ```
2. **Review TODO Files**: Check all TODO.md files for outdated information
   - Update version numbers to match current project version
   - Mark completed items as checked off
   - Remove obsolete information (e.g., outdated test coverage stats)
   - Consolidate any duplicate items
   - Verify future module TODOs remain accurate
3. **Commit Changes**: Create commit with standard message
   ```bash
   git commit -m "Run quality checks and cleanup"
   ```
4. **Provide Summary**: Report on quality status and TODO updates made

## Running ADK Evaluations

When running ADK agent evaluations, **ALWAYS** use the `adk eval` command from the project root directory:

### Single Agent Evaluation
```bash
# Must be run from project root with PYTHONPATH set
PYTHONPATH=.:$PYTHONPATH adk eval \
  --config_file_path GoogleADK/{Agent_Name}/evals/test_config.json \
  --print_detailed_results \
  GoogleADK/{Agent_Name} \
  GoogleADK/{Agent_Name}/evals/{test_name}.json
```

### Example: Running Jira_Johnny Evaluation
```bash
# From project root directory
PYTHONPATH=.:$PYTHONPATH adk eval \
  --config_file_path GoogleADK/Jira_Johnny/evals/test_config.json \
  --print_detailed_results \
  GoogleADK/Jira_Johnny \
  GoogleADK/Jira_Johnny/evals/00_list_available_tools_test.json
```

### Important Notes:
- **MUST run from project root**: The evaluation will fail if not run from the root directory
- **PYTHONPATH required**: Always prefix with `PYTHONPATH=.:$PYTHONPATH`
- **Environment variables**: The .env file is automatically loaded by ADK
- **Do NOT use pytest**: The pytest test files are for CI/CD automation only