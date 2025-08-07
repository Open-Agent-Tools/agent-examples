# Story_Sage Agent - User Story Specialist

A specialized User Story agent designed to craft high-quality user stories following INVEST principles and integrate seamlessly with Agile development workflows.

## Features

**Story Creation Excellence:**
- INVEST principle compliance (Independent, Negotiable, Valuable, Estimable, Small, Testable)
- Structured "As a... I want... So that..." format
- Comprehensive acceptance criteria with Given-When-Then scenarios
- Epic breakdown and story splitting capabilities

**Agile Integration:**
- Sprint planning and capacity estimation support
- Backlog refinement and prioritization
- Definition of Done establishment
- Story dependency management
- Acceptance testing criteria

**Dual Operation Modes:**
- **Standalone Root Agent**: Full functionality with Jira integration
- **Sub-Agent Mode**: Integrates with Scrum_Sam and other composite agents

**Jira Integration:**
- Create and manage user stories in Jira
- Epic and story hierarchy management  
- Sprint assignment and progress tracking
- Story linking and relationship mapping

## Usage

See the main [getting-started.md](../ADK-getting-started.md) for installation and setup instructions.

### As Standalone Agent
```python
from GoogleADK.Story_Sage import create_agent

# Full functionality with Jira integration
agent = create_agent(include_jira=True)
```

### As Sub-Agent
```python
from GoogleADK.Story_Sage import create_agent

# Lightweight mode for sub-agent usage
story_agent = create_agent(include_jira=False)

# Then include in parent agent's sub_agents list
parent_agent = Agent(
    # ... other config
    sub_agents=[story_agent]
)
```

## Environment Variables

The following environment variables can be configured:

- `GOOGLE_MODEL`: Optional Google model override (defaults to "gemini-2.0-flash")

When using Jira integration, also configure:
- `CONFLUENCE_URL`: Your Confluence instance URL
- `ATTLASSIAN_USERNAME`: Your Atlassian username  
- `JIRA_URL`: Your Jira instance URL
- `ATTLASSIAN_KEY`: Your Atlassian API token

## Agent Capabilities

### Story Crafting
- **Requirements Analysis**: Transform business needs into user stories
- **INVEST Validation**: Ensure stories meet all INVEST criteria
- **Story Templates**: Apply consistent "As a... I want... So that..." formatting
- **Acceptance Criteria**: Create comprehensive Given-When-Then scenarios
- **Story Splitting**: Break large epics into sprint-sized stories

### Agile Process Support
- **Sprint Planning**: Assist with story estimation and sprint capacity
- **Backlog Management**: Help prioritize and refine product backlogs
- **User Persona Development**: Create context for story creation
- **Value Analysis**: Articulate business impact and user benefits
- **Risk Assessment**: Identify story risks and dependencies

### Jira Operations (when integrated)
- **Story Creation**: Create properly formatted user stories
- **Epic Management**: Organize stories under appropriate epics
- **Workflow Tracking**: Monitor story progress through states
- **Sprint Assignment**: Assign stories to appropriate sprints
- **Story Linking**: Establish relationships between related stories

### File System Support
- **Documentation**: Generate and maintain story documentation
- **Templates**: Create reusable story templates
- **Reports**: Generate story metrics and analysis

## Example Interactions

### Story Creation
**User:** "We need users to be able to reset their passwords"
**Sage:** *Creates properly formatted user story with comprehensive acceptance criteria covering happy path, edge cases, and security considerations*

### Story Refinement  
**User:** "This epic is too big for our sprint"
**Sage:** *Analyzes the epic and suggests logical story splits using workflow steps, user roles, or CRUD operations*

### Sprint Planning
**User:** "Help estimate these stories for our 2-week sprint"
**Sage:** *Reviews stories for estimability, identifies dependencies, and provides capacity recommendations*

### Backlog Management
**User:** "Which stories should we prioritize for the next release?"
**Sage:** *Analyzes story value, dependencies, and risk to provide prioritization recommendations*

## Architecture

Story_Sage uses a flexible dual-mode architecture:

**Standalone Mode:**
- Full agent with filesystem, text, and Jira tools
- Independent operation for story-focused workflows
- Complete Jira integration through Jira_Johnny sub-agent

**Sub-Agent Mode:**
- Lightweight configuration without Jira sub-agent
- Prevents circular dependencies when used within Scrum_Sam
- Focuses on core story crafting capabilities

## Integration with Scrum_Sam

When integrated with Scrum_Sam, Story_Sage provides:
- Enhanced story creation during sprint planning
- Story quality validation and INVEST compliance
- Acceptance criteria development for team guidance
- Story splitting recommendations for capacity planning
- Value analysis to support prioritization decisions

This creates a comprehensive Agile workflow combining Scrum process facilitation with specialized story crafting expertise.