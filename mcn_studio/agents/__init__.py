# -*- coding: utf-8 -*-
"""
AI MCN Studio - Agents包初始化
"""

from agents.base_agent import BaseAgent, AgentContext, AgentOutput, register_agent, get_agent_class, list_available_agents
from agents.orchestrator import OrchestratorAgent
# 批量注册16个专员角色（导入即完成注册）
import agents.specialists  # noqa: F401

__all__ = [
    "BaseAgent", "AgentContext", "AgentOutput", "register_agent",
    "get_agent_class", "list_available_agents", "OrchestratorAgent",
]
