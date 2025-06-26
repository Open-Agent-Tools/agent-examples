"""File Operations Sub-Agent Configuration.

This module configures FileOps, a specialized sub-agent for handling
file and directory operations delegated from the main Python developer agent.

It uses a local CLAUDE_HAIKU or GEMMA_4B model for file and directory operations to reduce
the latency of the agent's response time and token cost for online models like  Claude.
"""

import logging
import warnings

from google.adk.agents import Agent

from .prompts import agent_instruction
import basic_open_agent_tools as boat  # type: ignore

from dotenv import load_dotenv

# Initialize environment and logging
load_dotenv() # or load_dotenv(dotenv_path="/env_path")
logging.basicConfig(level=logging.ERROR)
warnings.filterwarnings("ignore")

fs_tools = boat.load_all_filesystem_tools()
text_tools = boat.load_all_text_tools()
agent_tools = boat.merge_tool_lists(fs_tools, text_tools)


# Configure specialized file operations agent
root_agent = Agent(
    model="gemini-2.0-flash",
    name="FileOps",
    instruction=agent_instruction,
    description="Specialized file and directory operations agent that can enumerate directories and files, write to files, and perform basic text processing.",
    tools=agent_tools,
)

"""
The above would load:
File and Directory Operations:

read_file_to_string
write_file_from_string
append_to_file
list_directory_contents
create_directory
delete_file
delete_directory
move_file
copy_file
get_file_info
file_exists
directory_exists
get_file_size
is_empty_directory
list_all_directory_contents
generate_directory_tree
validate_path
validate_file_content
Text Processing Tools:

clean_whitespace
normalize_line_endings
strip_html_tags
normalize_unicode
to_snake_case
to_camel_case
to_title_case
smart_split_lines
extract_sentences
join_with_oxford_comma

"""
