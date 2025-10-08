"""
Script to extract individual agent prompts from root prompts.py
into separate prompt.py files in each agent folder.
"""

import re
from pathlib import Path

# Read the root prompts.py
prompts_file = Path(__file__).parent / "prompts.py"
with open(prompts_file, "r") as f:
    content = f.read()

# Define the mapping of prompt names to folder names
prompt_mappings = {
    "ARCHITECT_SYSTEM_PROMPT": "architect",
    "SENIOR_CODER_SYSTEM_PROMPT": "senior_coder",
    "FAST_CODER_SYSTEM_PROMPT": "fast_coder",
    "TEST_ENGINEER_SYSTEM_PROMPT": "test_engineer",
    "CODE_REVIEWER_SYSTEM_PROMPT": "code_reviewer",
    "DEBUG_SYSTEM_PROMPT": "debug",
    "DOCUMENTATION_SYSTEM_PROMPT": "documentation",
    "PYTHON_SPECIALIST_SYSTEM_PROMPT": "python_specialist",
    "WEB_SPECIALIST_SYSTEM_PROMPT": "web_specialist",
    "DATABASE_SPECIALIST_SYSTEM_PROMPT": "database_specialist",
    "DEVOPS_SPECIALIST_SYSTEM_PROMPT": "devops_specialist",
    "DATA_SCIENCE_SPECIALIST_SYSTEM_PROMPT": "data_science_specialist",
}

# Extract each prompt
for prompt_name, folder_name in prompt_mappings.items():
    # Pattern to match the prompt definition
    pattern = rf'^{prompt_name} = """(.*?)"""$'
    match = re.search(pattern, content, re.MULTILINE | re.DOTALL)

    if match:
        prompt_content = match.group(1)

        # Write to agent folder
        agent_folder = Path(__file__).parent / "agents" / folder_name
        prompt_file = agent_folder / "prompt.py"

        with open(prompt_file, "w") as f:
            f.write(
                f'"""\nSystem prompt for {folder_name.replace("_", " ").title()}\n"""\n\n'
            )
            f.write(f'{prompt_name} = """{prompt_content}"""\n')

        print(f"✓ Extracted {prompt_name} to {folder_name}/prompt.py")
    else:
        print(f"✗ Could not find {prompt_name}")

# Now create a new root prompts.py with only ORCHESTRATOR_SYSTEM_PROMPT
pattern = r'^ORCHESTRATOR_SYSTEM_PROMPT = """(.*?)"""$'
match = re.search(pattern, content, re.MULTILINE | re.DOTALL)

if match:
    orchestrator_prompt = match.group(1)

    # Write new root prompts.py
    with open(prompts_file, "w") as f:
        f.write('"""\nSystem Prompts for Complex Coding Clara\n\n')
        f.write("This file contains only the orchestrator (Clara) system prompt.\n")
        f.write(
            "Individual agent prompts are in their respective folders under agents/.\n"
        )
        f.write('"""\n\n')
        f.write(f'ORCHESTRATOR_SYSTEM_PROMPT = """{orchestrator_prompt}"""\n')

    print("\n✓ Updated root prompts.py with only ORCHESTRATOR_SYSTEM_PROMPT")
else:
    print("\n✗ Could not find ORCHESTRATOR_SYSTEM_PROMPT")

print("\n✅ Prompt extraction complete!")
