# -*- coding: utf-8 -*-
"""
AI MCN Studio - LLM 适配层
让任意数字员工在内置模板思维之上，可选对接真实 LLM（OpenAI 兼容接口）。
设计原则：
  1. 零外部依赖——只用标准库 urllib，无需安装 SDK。
  2. 优雅降级——未配置 KEY 或调用失败时，自动回退到内置思维，业务不中断。
  3. 人格注入——把 Agent 的 personality/expertise/core_values 写进 system prompt，
     让 LLM 输出符合该数字员工的人设。
"""

from __future__ import annotations

import json
import logging
import os
import urllib.request
from typing import Any, Optional

logger = logging.getLogger(__name__)

# 默认采用 OpenAI 兼容的 Base URL，可用环境变量覆盖（指向任意兼容网关）
_DEFAULT_BASE_URL = "https://api.openai.com/v1"
_DEFAULT_MODEL = "gpt-4o-mini"


class LLMClient:
    """极简 OpenAI 兼容 Chat 客户端（标准库实现，可选用）"""

    def __init__(self, api_key: Optional[str] = None,
                 base_url: Optional[str] = None,
                 model: Optional[str] = None,
                 timeout: int = 60):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY") or os.getenv("MCN_LLM_API_KEY")
        self.base_url = (base_url or os.getenv("MCN_LLM_BASE_URL") or _DEFAULT_BASE_URL).rstrip("/")
        self.model = model or os.getenv("MCN_LLM_MODEL") or _DEFAULT_MODEL
        self.timeout = timeout

    @property
    def available(self) -> bool:
        return bool(self.api_key)

    def chat(self, system: str, user: str, temperature: float = 0.4) -> Optional[str]:
        """调用 LLM；不可用或失败时返回 None（由调用方决定回退策略）"""
        if not self.available:
            logger.debug("LLM 未配置 KEY，跳过真实调用")
            return None
        payload = {
            "model": self.model,
            "temperature": temperature,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        }
        req = urllib.request.Request(
            f"{self.base_url}/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            return data["choices"][0]["message"]["content"]
        except Exception as exc:  # noqa: BLE001 — 网络/解析异常统一降级
            logger.warning("LLM 调用失败，回退到内置思维：%s", exc)
            return None


# 全局单例，惰性初始化
_client: Optional[LLMClient] = None


def get_llm_client() -> LLMClient:
    global _client
    if _client is None:
        _client = LLMClient()
    return _client


def build_system_prompt(agent_config: Any, task_type: str) -> str:
    """把数字员工的人设注入 system prompt"""
    return (
        f"你是 AI MCN 工作室的数字员工「{agent_config.name}」，"
        f"职位：{agent_config.title}，部门：{agent_config.department}。\n"
        f"性格：{agent_config.personality}\n"
        f"专长：{', '.join(agent_config.expertise)}\n"
        f"核心价值观：{', '.join(agent_config.core_values)}\n"
        f"沟通风格：{agent_config.communication_style}\n"
        f"当前任务类型：{task_type}。请以该身份输出专业、可落地的结果，"
        f"控制在 300 字内，使用中文。"
    )


def think_with_llm(agent_config: Any, task_input: dict[str, Any],
                   fallback_text: str, temperature: float = 0.4) -> str:
    """
    混合思维：优先真实 LLM；不可用/失败时返回 fallback_text（内置模板结果）。
    这样 24 名员工在离线环境也能全程运行，联网时自动升级为真实 LLM 输出。
    """
    client = get_llm_client()
    if not client.available:
        return fallback_text
    system = build_system_prompt(agent_config, task_input.get("task_type", "通用"))
    user = (
        f"任务：{task_input.get('title', '未命名')}\n"
        f"平台：{task_input.get('platform', 'douyin')}\n"
        f"上下文：{json.dumps(task_input.get('context', {}), ensure_ascii=False)}\n"
        f"（参考内置产出：{fallback_text[:400]}）"
    )
    result = client.chat(system, user, temperature)
    return result if result is not None else fallback_text
