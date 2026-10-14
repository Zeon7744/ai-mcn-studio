# -*- coding: utf-8 -*-
"""
总调度 Agent - 令仪（CEO）
负责全局任务编排、协调各Agent协作、分级分部门管理
v3.0: 支持全部24个Agent的集中+分布双模管理
"""

from __future__ import annotations

import json
import logging
from datetime import datetime
from typing import Any, Optional

from agents.base_agent import AgentOutput, BaseAgent, register_agent, get_agent_class
from core.models import (
    Agent, AgentRole, Priority, Project, ProjectStatus, Task, TaskStatus,
    DEPARTMENTS,
)

# 各总监Agent类（8个核心角色）
from agents.creative_director import CreativeDirectorAgent
from agents.copy_chief import CopyChiefAgent
from agents.visual_designer import VisualDesignerAgent
from agents.operations_strategy import OperationsStrategyAgent
from agents.talent_manager import TalentManagerAgent
from agents.monetization import MonetizationAgent
from agents.risk_control import RiskControlAgent
from agents.researcher import ResearcherAgent

logger = logging.getLogger(__name__)

# 已知8个核心角色的Agent类映射（其余16个角色由 agents.specialists 批量注册）
_AGENT_FACTORIES = {
    AgentRole.CREATIVE_DIRECTOR: CreativeDirectorAgent,
    AgentRole.COPY_CHIEF: CopyChiefAgent,
    AgentRole.VISUAL_DESIGNER: VisualDesignerAgent,
    AgentRole.OPERATIONS_STRATEGY: OperationsStrategyAgent,
    AgentRole.TALENT_MANAGER: TalentManagerAgent,
    AgentRole.MONETIZATION: MonetizationAgent,
    AgentRole.RISK_CONTROL: RiskControlAgent,
    AgentRole.RESEARCHER: ResearcherAgent,
}

# 需要强制触发的模块（批量注册16个专员角色）
_FORCE_IMPORT_MODULES = [
    "agents.specialists",
]


@register_agent(AgentRole.ORCHESTRATOR)
class OrchestratorAgent(BaseAgent):
    """
    令仪 - 总调度/CEO
    负责全局任务编排、跨部门协调、分级管理（CEO→总监→专员）
    集中管理：危机公关/合规/重大决策等必须总部拍板的场景
    分布管理：日常业务由各总监在授权范围内自主决策
    """

    def __init__(self, config, all_agents: list[Agent]):
        super().__init__(config)
        self.all_agents = all_agents
        self.agent_instances: dict[str, BaseAgent] = {}
        self._ensure_specialists_registered()
        self._init_agents()
        self.project_history: list[dict] = []
        self.active_projects: dict[str, Project] = {}

    def _ensure_specialists_registered(self) -> None:
        """确保专员角色（16个）已注册到AgentRegistry"""
        for mod_name in _FORCE_IMPORT_MODULES:
            try:
                __import__(mod_name)
            except ImportError:
                logger.warning(f"无法导入模块 {mod_name}，相关专员角色可能不可用")

    def _init_agents(self):
        """初始化所有Agent实例（24人全员）"""
        self.agent_instances = {}
        for agent_config in self.all_agents:
            if agent_config.role == AgentRole.ORCHESTRATOR:
                continue
            factory = _AGENT_FACTORIES.get(agent_config.role) or get_agent_class(agent_config.role)
            if factory:
                self.agent_instances[agent_config.id] = factory(agent_config)
                logger.debug("初始化Agent: %s (%s)", agent_config.name, agent_config.role.value)
            else:
                logger.warning("角色 %s 无可用Agent类，跳过", agent_config.role.value)

    # ── 查询接口 ─────────────────────────────────────────────────────

    def get_agent_by_role(self, role: AgentRole) -> Optional[BaseAgent]:
        """根据角色获取Agent实例"""
        for agent in self.all_agents:
            if agent.role == role and agent.id in self.agent_instances:
                return self.agent_instances[agent.id]
        return None

    def get_agent_by_name(self, name: str) -> Optional[BaseAgent]:
        """根据姓名获取Agent实例"""
        for agent in self.all_agents:
            if agent.name == name and agent.id in self.agent_instances:
                return self.agent_instances[agent.id]
        return None

    def list_team(self) -> list[dict]:
        """列出全部团队成员信息（含职级与汇报关系）"""
        return [
            {
                "name": a.name,
                "title": a.title,
                "department": a.department,
                "level": a.level.value,
                "reports_to": a.reports_to or "令仪",
                "role": a.role.value,
            }
            for a in self.all_agents
        ]

    # ── 核心思考 ─────────────────────────────────────────────────────

    def think(self, input_data: dict[str, Any]) -> AgentOutput:
        """总调度的核心思考——全局任务编排与分级管理"""
        action = input_data.get("action", "")
        context = input_data.get("context", {})

        if action == "create_project":
            response = self._create_project(input_data)
        elif action == "assign_task":
            response = self._assign_task(input_data)
        elif action == "execute_workflow":
            response = self._execute_workflow(input_data)
        elif action == "coordinate_team":
            response = self._coordinate_team(input_data)
        elif action == "status_check":
            response = self._status_check(input_data)
        elif action == "crisis_response":
            response = self._crisis_response(input_data)
        else:
            response = self._default_orchestration(input_data)

        output = AgentOutput(
            success=response["success"],
            agent_id=self.config.id,
            agent_name=self.config.name,
            task_id=input_data.get("task_id", "orch"),
            output_type="decision",
            content=response["output"],
            confidence=response.get("confidence", 0.95),
            metadata={
                "action": action,
                "reasoning": response.get("reasoning", ""),
                "project_id": response.get("project_id"),
                "task_id": response.get("task_id"),
            },
            suggestions=response.get("suggestions", []),
        )

        self.record_memory({
            "type": "orchestration",
            "content": f"执行操作: {action}",
            "result": response.get("reasoning", "")[:80],
        })

        return output

    # ── 项目创建 ─────────────────────────────────────────────────────

    def _create_project(self, input_data):
        """创建新项目"""
        name = input_data.get("project_name", "未命名项目")
        goal = input_data.get("goal", "")
        platform = input_data.get("platform", [])
        template = input_data.get("template", "")

        # 平台值归一化（兼容 "rednote"/"wechat_video" 等旧键）
        from core.models import ContentPlatform
        _platform_alias = {
            "rednote": "rednote",
            "wechat_video": "video_account",
            "xiaohongshu": "xiaohongshu",
        }
        valid_values = [p.value for p in ContentPlatform]
        platforms = []
        for p in platform:
            p = _platform_alias.get(p, p)
            if p in valid_values:
                platforms.append(p)
        project = Project(
            name=name,
            description=goal,
            goal=goal,
            platform=[ContentPlatform(p) for p in platforms] if platforms else [],
        )

        # 根据模板生成初始任务
        if template:
            tasks = self._generate_tasks_from_template(template, project)
            for task in tasks:
                project.add_task(task)

        self.active_projects[project.id] = project
        self.project_history.append({
            "action": "create",
            "project_id": project.id,
            "name": name,
            "timestamp": datetime.now().isoformat(),
        })

        reasoning = (
            f"【总调度的项目创建】\n\n"
            f"项目已创建：{name}\n"
            f"目标：{goal}\n"
            f"平台：{', '.join(platforms) if platforms else '未指定'}\n"
            f"任务数：{len(project.tasks)}\n\n"
            f"项目已加入待执行队列。\n"
            f"下一步：分配任务给对应Agent，开始执行。"
        )

        return {"success": True, "output": reasoning, "confidence": 0.95,
                "reasoning": reasoning, "project_id": project.id}

    # ── 任务分配 ─────────────────────────────────────────────────────

    def _assign_task(self, input_data):
        """分配任务给指定角色/姓名Agent"""
        task_id = input_data.get("task_id", "")
        agent_role = input_data.get("assign_to", "")
        task_info = input_data.get("task", {})
        task_info["task_id"] = task_id

        agent = None
        if agent_role in ("", None):
            # 按姓名
            pass
        else:
            try:
                agent = self.get_agent_by_role(AgentRole(agent_role))
            except ValueError:
                agent = None
        if agent is None:
            agent = self.get_agent_by_name(agent_role)
        if not agent:
            return {"success": False, "output": f"未找到角色为 {agent_role} 的Agent", "reasoning": ""}

        result = agent.think(task_info)

        reasoning = (
            f"【总调度的任务分配】\n\n"
            f"任务：{task_info.get('title', '未命名')}\n"
            f"分配给：{agent.config.name}（{agent.config.title}）\n"
            f"状态：执行中...\n\n"
            f"结果摘要：{result.content[:200]}..."
        )

        return {"success": True, "output": reasoning, "confidence": 0.92,
                "reasoning": reasoning, "agent_id": agent.config.id}

    # ── 工作流执行（全24角色支持） ────────────────────────────────────

    def _execute_workflow(self, input_data):
        """执行完整工作流（支持新角色owner）"""
        workflow_name = input_data.get("workflow", "")
        project_id = input_data.get("project_id", "")

        from core.regulations import WORKFLOW_DEFINITIONS
        workflow = WORKFLOW_DEFINITIONS.get(workflow_name)

        if not workflow:
            return {"success": False, "output": f"未找到工作流：{workflow_name}", "reasoning": ""}

        reasoning = (
            f"【总调度的工作流执行】\n\n"
            f"工作流：{workflow['name']}\n"
            f"项目：{project_id}\n\n"
            f"开始执行 {len(workflow['steps'])} 个步骤：\n\n"
        )

        executed_steps = []
        missing_roles = []
        for step in workflow["steps"]:
            owner_role = step["owner"]

            # orchestrator角色由总调度（CEO）自己直接执行（集中管理场景）
            if owner_role == AgentRole.ORCHESTRATOR.value:
                executed_steps.append({
                    "step": step["step"], "name": step["name"],
                    "owner": self.config.name, "status": "completed",
                })
                reasoning += (
                    f"  ✅ 步骤 {step['step']}: {step['name']} — "
                    f"{self.config.name}（CEO直接执行）\n"
                )
                continue

            try:
                role_enum = AgentRole(owner_role)
            except ValueError:
                role_enum = None
                executed_steps.append({
                    "step": step["step"], "name": step["name"],
                    "owner": owner_role, "status": "failed", "reason": "未知角色",
                })
                reasoning += f"  ❌ 步骤 {step['step']}: {step['name']} — 未知角色 {owner_role}\n"
                continue

            agent = self.get_agent_by_role(role_enum)
            if agent:
                task_input = {
                    "title": step["name"],
                    "task_type": step.get("task_type", step["name"]),
                    "platform": input_data.get("platform", "douyin"),
                    "context": input_data.get("context", {}),
                    "task_id": f"{project_id}-{step['step']}",
                }
                result = agent.think(task_input)
                executed_steps.append({
                    "step": step["step"],
                    "name": step["name"],
                    "owner": agent.config.name,
                    "status": "completed",
                })
                reasoning += f"  ✅ 步骤 {step['step']}: {step['name']} — {agent.config.name} 完成\n"
            else:
                missing_roles.append(owner_role)
                executed_steps.append({
                    "step": step["step"], "name": step["name"],
                    "owner": owner_role, "status": "failed", "reason": "Agent未实例化",
                })
                reasoning += f"  ❌ 步骤 {step['step']}: {step['name']} — Agent未实例化（{owner_role}）\n"

        ok = sum(1 for s in executed_steps if s.get("status") == "completed")
        total = len(workflow["steps"])
        reasoning += f"\n执行完成：{ok}/{total} 步成功"
        if missing_roles:
            reasoning += f"（缺失角色：{', '.join(missing_roles)}）"

        return {"success": ok == total, "output": reasoning, "confidence": 0.90,
                "reasoning": reasoning, "executed_steps": executed_steps}

    # ── 团队协作 ─────────────────────────────────────────────────────

    def _coordinate_team(self, input_data):
        """协调跨部门团队协作（支持新角色）"""
        challenge = input_data.get("challenge", "")
        required_roles = input_data.get("required_roles", [])

        reasoning = (
            f"【总调度的团队协作】\n\n"
            f"挑战：{challenge}\n\n"
            f"需要以下角色协同完成：\n\n"
        )

        for role in required_roles:
            try:
                role_enum = AgentRole(role)
            except ValueError:
                reasoning += f"  ❌ {role} — 未知角色\n"
                continue
            agent = self.get_agent_by_role(role_enum)
            if agent:
                reasoning += f"  👤 {agent.config.name}（{agent.config.title}，"
                reasoning += f"{agent.config.department}）"
                reasoning += f" — {agent.config.expertise[0] if agent.config.expertise else '待分配'}\n"
            else:
                reasoning += f"  ⚠️ {role} — Agent未实例化\n"

        reasoning += (
            f"\n协作流程图：\n"
            f"  创意中心 → 视觉中心 → 运营中心 → 风控中心（全链路审查）\n"
            f"        ↓           ↓           ↓           ↓\n"
            f"  墨言/笔灵  ←→  绘影/丹青  ←→  数策/星轨  ←→  镜鉴/守法\n"
            f"  研究中心（博闻/瞭望）全程提供数据与趋势支持"
        )

        return {"success": True, "output": reasoning, "confidence": 0.88,
                "reasoning": reasoning, "team": required_roles}

    # ── 危机响应（集中管理场景） ─────────────────────────────────────

    def _crisis_response(self, input_data):
        """重大危机响应——CEO直接介入，调风控中心+主播中心+商业中心三线联动"""
        crisis = input_data.get("crisis", "未指明事件")
        severity = input_data.get("severity", "high")

        agents_involved = []
        for role in (AgentRole.RISK_CONTROL, AgentRole.TALENT_MANAGER, AgentRole.MONETIZATION,
                     AgentRole.COPYRIGHT_MANAGER, AgentRole.COMPLIANCE_REVIEWER):
            a = self.get_agent_by_role(role)
            if a:
                agents_involved.append(a.config.name)

        reasoning = (
            f"【总调度·危机响应（集中管理）】\n\n"
            f"事件：{crisis}\n"
            f"等级：{severity}\n\n"
            f"重大危机必须由CEO直接指挥，触发集中管理模式：\n"
            f"  · 立即暂停所有相关内容的发布\n"
            f"  · 调风控中心（镜鉴）72小时舆情全监控\n"
            f"  · 调版权管理员确认素材合法性\n"
            f"  · 涉及商单的，调商业中心评估违约风险\n\n"
            f"介入团队：{', '.join(agents_involved) if agents_involved else '待初始化'}\n"
            f"决策原则：止损优先，合规优先，最小化长期声誉损失。"
        )

        return {"success": True, "output": reasoning, "confidence": 0.94,
                "reasoning": reasoning}

    # ── 状态检查 ─────────────────────────────────────────────────────

    def _status_check(self, input_data):
        """团队与项目状态检查（全员视图，含团队效能看板）"""
        from knowledge import team_efficiency
        efficiency_board = team_efficiency(self.all_agents)
        reasoning = "【总调度状态检查】\n\n" + efficiency_board["report_text"] + "\n\n"

        # Agent状态（按部门分组）
        reasoning += "👥 团队成员状态（按部门）：\n"
        by_dept: dict[str, list] = {}
        for agent in self.all_agents:
            by_dept.setdefault(agent.department, []).append(agent)
        for dept, members in by_dept.items():
            reasoning += f"\n  {dept}：\n"
            for m in members:
                level_mark = {"ceo": "👑", "director": "◆", "senior": "◇", "staff": "·"}.get(
                    m.level.value, "·")
                reasoning += (f"    {level_mark} {m.name}（{m.title}，职级:{m.level.value}，"
                              f"汇报:{m.reports_to or '令仪'}）\n")

        # 项目状态
        reasoning += f"\n📁 活跃项目：{len(self.active_projects)} 个\n"
        for pid, proj in self.active_projects.items():
            reasoning += f"  · {proj.name} — 进度 {proj.get_progress()}%\n"

        # 项目历史
        reasoning += f"\n📜 历史记录：{len(self.project_history)} 条\n"
        for record in self.project_history[-5:]:
            reasoning += (f"  · [{record['timestamp'][:16]}] {record['action']}: "
                          f"{record.get('name', record.get('project_id', ''))}\n")

        return {"success": True, "output": reasoning, "confidence": 0.95,
                "reasoning": reasoning}

    # ── 默认调度 ─────────────────────────────────────────────────────

    def _default_orchestration(self, input_data):
        reasoning = (
            f"【总调度·令仪】\n\n"
            f"我是工作室的总调度（CEO），负责全局任务编排和跨部门协调。\n\n"
            f"可用操作：\n"
            f"  · create_project — 创建新项目\n"
            f"  · assign_task — 分配单个任务（支持角色名/姓名）\n"
            f"  · execute_workflow — 执行完整工作流\n"
            f"  · coordinate_team — 协调跨部门协作\n"
            f"  · crisis_response — 重大危机响应（集中管理）\n"
            f"  · status_check — 查看团队与项目状态\n\n"
            f"当前团队：{len(self.agent_instances)} 名专员 + 我 = "
            f"{len(self.agent_instances) + 1} 人\n"
            f"请告诉我你需要什么帮助。"
        )
        reasoning = self.llm_enhance(input_data, reasoning, temperature=0.3)
        return {"success": True, "output": reasoning, "confidence": 0.95, "reasoning": reasoning}

    # ── 任务模板生成 ─────────────────────────────────────────────────

    def _generate_tasks_from_template(self, template_name, project):
        """根据模板生成任务"""
        from core.regulations import PROJECT_TEMPLATES
        template = PROJECT_TEMPLATES.get(template_name, {})
        tasks = []

        for t in template.get("default_tasks", []):
            task = Task(
                title=t["title"],
                description=f"{t['title']} - {project.name}",
                task_type=t.get("type", t["title"]),
                assigned_to=None,  # 由调度器分配
                priority=Priority.MEDIUM,
                platform=project.platform[0] if project.platform else None,
            )
            tasks.append(task)

        return tasks

    # ── 组织架构打印 ─────────────────────────────────────────────────

    def print_org_chart(self) -> str:
        """打印分级组织架构图（CEO→总监→专员）"""
        lines = ["╔══════════════════════════════════════════╗",
                 "║     AI MCN Studio — 分级组织架构          ║",
                 "╚══════════════════════════════════════════╝",
                 "",
                 "  👑 令仪（总调度/CEO）",
                 "  ├── ◆ 墨言（创意总监）"]
        creative_staff = [a.name for a in self.all_agents if a.department == "创意中心"
                         and a.role != AgentRole.CREATIVE_DIRECTOR]
        for n in creative_staff:
            lines.append(f"  │     · {n}")
        lines.append("  ├── ◆ 绘影（视觉总监）")
        for n in [a.name for a in self.all_agents if a.department == "视觉中心"
                  and a.role != AgentRole.VISUAL_DESIGNER]:
            lines.append(f"  │     · {n}")
        lines.append("  ├── ◆ 数策（运营总监）")
        for n in [a.name for a in self.all_agents if a.department == "运营中心"
                  and a.role != AgentRole.OPERATIONS_STRATEGY]:
            lines.append(f"  │     · {n}")
        lines.append("  ├── ◆ 声优（主播总监）")
        for n in [a.name for a in self.all_agents if a.department == "主播中心"
                  and a.role != AgentRole.TALENT_MANAGER]:
            lines.append(f"  │     · {n}")
        lines.append("  ├── ◆ 利达（商务总监）")
        for n in [a.name for a in self.all_agents if a.department == "商业中心"
                  and a.role != AgentRole.MONETIZATION]:
            lines.append(f"  │     · {n}")
        lines.append("  ├── ◆ 镜鉴（风控总监）")
        for n in [a.name for a in self.all_agents if a.department == "风控中心"
                  and a.role != AgentRole.RISK_CONTROL]:
            lines.append(f"  │     · {n}")
        lines.append("  └── ◆ 博闻（研究总监）")
        for n in [a.name for a in self.all_agents if a.department == "研究中心"
                  and a.role != AgentRole.RESEARCHER]:
            lines.append(f"        · {n}")
        return "\n".join(lines)
