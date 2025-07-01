# Claude Instructions

## Quick Cleanup Command

When user says **"cleanup"**: 
1. **Run Quality Tools**: Execute all quality checks and fix issues
   ```bash
   python3 -m ruff check ./ --fix
   python3 -m ruff format ./
   python3 -m mypy ./
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