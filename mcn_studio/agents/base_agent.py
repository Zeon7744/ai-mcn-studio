# -*- coding: utf-8 -*-
"""
AI MCN Studio - Agent基类与注册系统
所有Agent继承自BaseAgent，拥有独立的思维模式和决策能力
"""

from __future__ import annotations

import json
import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field

from core.models import Agent as AgentModel, AgentRole, Priority, TaskStatus

logger = logging.getLogger(__name__)


# ─── Agent上下文 ─────────────────────────────────────────────────────────────

class AgentContext(BaseModel):
    """Agent运行时的上下文环境"""
    agent_id: str
    agent_name: str
    current_task: dict[str, Any] | None = None
    memory: list[dict[str, Any]] = Field(default_factory=list)  # 短期记忆
    preferences: dict[str, Any] = Field(default_factory=dict)
    environment_state: dict[str, Any] = Field(default_factory=dict)


# ─── Agent输出 ───────────────────────────────────────────────────────────────

class AgentOutput(BaseModel):
    """Agent执行任务的输出"""
    success: bool
    agent_id: str
    agent_name: str
    task_id: str
    output_type: str          # analysis / content / decision / suggestion / review
    content: str
    confidence: float = 1.0
    metadata: dict[str, Any] = Field(default_factory=dict)
    suggestions: list[str] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.now)


# ─── BaseAgent ───────────────────────────────────────────────────────────────

class BaseAgent(ABC):
    """
    所有AI员工的基础类。
    每个Agent拥有独立的人格、专业能力和协作模式。
    """

    def __init__(self, config: AgentModel):
        self.config = config
        self.context = AgentContext(
            agent_id=config.id,
            agent_name=config.name,
        )
        self._personality_traits = self._extract_personality_traits()

    def _extract_personality_traits(self) -> dict[str, Any]:
        """从配置中提取性格特征"""
        return {
            "communication_style": self.config.communication_style,
            "core_values": self.config.core_values,
            "pet_peeves": self.config.pet_peeves,
            "collaboration_mode": self.config.collaboration_mode,
        }

    def get_identity(self) -> dict[str, Any]:
        """返回Agent的身份信息"""
        return {
            "id": self.config.id,
            "name": self.config.name,
            "title": self.config.title,
            "department": self.config.department,
            "role": self.config.role.value,
            "personality": self.config.personality[:100] + "..." if len(self.config.personality) > 100 else self.config.personality,
            "expertise": self.config.expertise,
            "scores": {
                "productivity": self.config.productivity_score,
                "creativity": self.config.creativity_score,
                "reliability": self.config.reliability_score,
            },
        }

    def record_memory(self, entry: dict[str, Any]) -> None:
        """记录到短期记忆（保留最近20条）"""
        self.context.memory.append({
            "time": datetime.now().isoformat(),
            **entry,
        })
        if len(self.context.memory) > 20:
            self.context.memory = self.context.memory[-20:]

    def get_memory_summary(self) -> str:
        """生成记忆摘要"""
        if not self.context.memory:
            return "无近期记忆"
        recent = self.context.memory[-5:]
        return "\n".join(f"[{m.get('time', '')[:16]}] {m.get('content', '')}" for m in recent)

    @abstractmethod
    def think(self, input_data: dict[str, Any]) -> AgentOutput:
        """
        核心思考方法 - 每个Agent根据自己的专业领域和人格特质处理输入。
        这是Agent"有思想"的关键。
        """
        pass

    def __repr__(self) -> str:
        return f"<Agent: {self.config.name} ({self.config.role.value})>"


# ─── Agent注册表 ─────────────────────────────────────────────────────────────

_agent_registry: dict[str, type[BaseAgent]] = {}


def register_agent(role: AgentRole):
    """Agent类注册装饰器"""
    def decorator(cls: type[BaseAgent]) -> type[BaseAgent]:
        _agent_registry[role.value] = cls
        return cls
    return decorator


def get_agent_class(role: AgentRole) -> Optional[type[BaseAgent]]:
    return _agent_registry.get(role.value)


def list_available_agents() -> list[str]:
    return list(_agent_registry.keys())
