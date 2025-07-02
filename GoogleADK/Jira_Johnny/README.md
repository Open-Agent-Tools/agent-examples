# Jira Agent

A specialized Jira operations agent designed to handle Atlassian Jira interactions through Docker-containerized MCP server integration.

## Prerequisites

Requires first setting up the MCP server in Docker:

https://github.com/sooperset/mcp-atlassian/

## Usage

See the main [getting-started.md](../ADK-getting-started.md) for installation and setup instructions.

## Environment Variables

The following environment variables need to be configured:

- `CONFLUENCE_URL`: Your Confluence instance URL
- `ATTLASSIAN_USERNAME`: Your Atlassian username  
- `JIRA_URL`: Your Jira instance URL
- `ATTLASSIAN_KEY`: Your Atlassian API token
- `GOOGLE_MODEL`: Optional Google model override (defaults to "gemini-pro")

## Agent Capabilities

The Jira_Johnny agent specializes in:

**Jira Operations:**
- Create, read, update, and delete Jira issues
- Manage Jira projects and workflows
- Handle issue transitions and status updates
- Search and filter Jira issues
- Manage issue comments and attachments

**Confluence Integration:**
- Read and write Confluence pages
- Manage Confluence spaces
- Handle page hierarchies and links
- Search Confluence content

**File System Support:**
- Generate directory trees for context
- Read files to string for processing
- Basic file system navigation


## Example Interactions

1. **Issue Creation:**
   - **User:** "Create a new task issue for the login issue"
   - **Johnny:** *Creates Jira issue with appropriate fields and returns issue key*

2. **Issue Search:**
   - **User:** "Find all open issues assigned to <user>"
   - **Johnny:** *Searches Jira and returns filtered results*

3. **Status Updates:**
   - **User:** "Move issue ABC-123 to In Progress"
   - **Johnny:** *Transitions issue status and confirms update*