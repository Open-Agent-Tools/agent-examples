"""
Specialist Agents for Complex Coding Clara

This module contains the specialist coding agents:

General Coding:
- Architect: System design and architecture
- Senior Coder: Complex algorithms and advanced coding
- Fast Coder: CRUD operations and boilerplate
- Test Engineer: Test generation and coverage
- Code Reviewer: Code review and best practices
- Debug: Error analysis and bug fixing
- Documentation: Docstrings and documentation

Domain/Language Specialists:
- Python Specialist: Python idioms, PEP standards, type hints
- Web Specialist: React, TypeScript, modern frontend
- Database Specialist: SQL/NoSQL, schema design, optimization
- DevOps Specialist: Docker, Kubernetes, CI/CD, IaC
- Data Science Specialist: ML, data preprocessing, model training

SDLC Process Specialists:
- Agile Specialist: User stories, epics, sprint planning, Scrum
- Doc Research Specialist: Technical documentation research
"""

from .architect.agent import architect
from .senior_coder.agent import senior_coder
from .fast_coder.agent import fast_coder
from .test_engineer.agent import test_engineer
from .code_reviewer.agent import code_reviewer
from .debug.agent import debug
from .documentation.agent import documentation
from .python_specialist.agent import python_specialist
from .web_specialist.agent import web_specialist
from .database_specialist.agent import database_specialist
from .devops_specialist.agent import devops_specialist
from .data_science_specialist.agent import data_science_specialist
from .agile_specialist.agent import agile_specialist
from .doc_research_specialist.agent import doc_research_specialist

__all__ = [
    # General coding agents
    "architect",
    "senior_coder",
    "fast_coder",
    "test_engineer",
    "code_reviewer",
    "debug",
    "documentation",
    # Domain/language specialists
    "python_specialist",
    "web_specialist",
    "database_specialist",
    "devops_specialist",
    "data_science_specialist",
    # SDLC process specialists
    "agile_specialist",
    "doc_research_specialist",
]
