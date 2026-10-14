# -*- coding: utf-8 -*-
"""
AI MCN Studio - 包初始化文件
"""

from core.models import (
    Agent,
    AgentLevel,
    AgentRole,
    ContentPlatform,
    DEPARTMENTS,
    Project,
    ProjectStatus,
    Priority,
    Task,
    TaskStatus,
    create_all_agents,
    PROJECT_TEMPLATES,
)

from core.regulations import (
    COMPANY_REGULATIONS,
    PROJECT_TEMPLATES as _REG_PROJECT_TEMPLATES,
    WORKFLOW_DEFINITIONS,
)

# 统一对外：工作流与模板均以 regulations 中定义为准
PROJECT_TEMPLATES = _REG_PROJECT_TEMPLATES

__all__ = [
    "Agent", "AgentLevel", "AgentRole", "ContentPlatform", "DEPARTMENTS",
    "Priority", "Task", "TaskStatus", "create_all_agents",
    "PROJECT_TEMPLATES", "COMPANY_REGULATIONS", "WORKFLOW_DEFINITIONS",
]
