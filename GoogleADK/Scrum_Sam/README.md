# Scrum Master Agent

A specialized Scrum Master agent designed to coach teams and handle Atlassian Jira interactions for agile project management through Docker-containerized MCP server integration.

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

The Scrum_Sam agent specializes in:

**Scrum Master Responsibilities:**
- Sprint planning and management
- Daily standup facilitation
- Sprint retrospectives and reviews
- Team coaching and process improvement
- Impediment identification and removal
- Agile metrics tracking and reporting

**Jira Scrum Operations:**
- Create and manage sprints
- Handle user stories and epics
- Manage backlog prioritization
- Track sprint progress and burndown
- Generate sprint reports
- Manage story points and estimation

**Confluence Integration:**
- Create and maintain sprint documentation
- Document retrospective outcomes
- Maintain team processes and guidelines
- Create and update project wikis
- Handle meeting notes and action items

**File System Support:**
- Generate directory trees for project context
- Read files to string for analysis
- Basic file system navigation


## Example Interactions

1. **Sprint Planning:**
   - **User:** "Help plan our next 2-week sprint"
   - **Sam:** *Reviews backlog, estimates capacity, and creates sprint with appropriate stories*

2. **Daily Standup:**
   - **User:** "Generate our daily standup report"
   - **Sam:** *Pulls current sprint progress, identifies blockers, and formats standup summary*

3. **Retrospective:**
   - **User:** "Facilitate our sprint retrospective"
   - **Sam:** *Analyzes sprint metrics, identifies improvement areas, and documents action items*

4. **Process Coaching:**
   - **User:** "Our team is struggling with story estimation"
   - **Sam:** *Provides guidance on estimation techniques and helps establish team standards*

