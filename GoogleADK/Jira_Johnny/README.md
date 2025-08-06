# ✅ WORKING # 
Successfully migrated to HTTP MCP transport - fully functional!



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

## Recent Updates & Fixes

### ✅ Major Infrastructure Improvements (August 2025)

**Fixed Critical Issues:**
1. **MCP Transport Migration**: Successfully migrated from unstable Docker stdio to reliable HTTP/SSE transport
2. **Authentication Fixed**: Resolved credential passing issues with persistent Docker container
3. **Model Optimization**: Switched to `gemini-2.0-flash` for consistent API responses
4. **Real Data Integration**: All evaluations now work with actual Jira instance data

**Working Evaluations (6/12 Passing):**
- ✅ `01_jira_get_agile_boards_test`: Retrieves real Agile boards (ED board, WOB board)
- ✅ `02_jira_search_test`: JQL search with real issue data (finds WOB-2)
- ✅ `03_jira_create_issue_test`: Creates actual Jira issues (WOB-5, WOB-6)
- ✅ `04_jira_get_issue_test`: Fetches detailed issue information with full metadata
- ✅ `05_jira_update_issue_test`: Successfully updates issue descriptions and fields
- ✅ `06_jira_add_comment_test`: Adds comments to issues (score: 0.98/1.0)

**Technical Solution:**
- **HTTP MCP Server**: `docker run -p 9000:9000 ghcr.io/sooperset/mcp-atlassian:latest --transport streamable-http --port 9000`
- **Agent Config**: Uses `StreamableHTTPConnectionParams(url="http://localhost:9000/mcp")`
- **Environment Setup**: Proper credential passing via Docker environment variables

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