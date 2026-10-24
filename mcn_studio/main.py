# -*- coding: utf-8 -*-
"""
AI MCN Studio - 主程序入口 v3.0
支持24名数字员工、11套工作流、分级管理
"""

import sys
import json
import logging
from pathlib import Path
from datetime import datetime

# 添加项目根目录到路径
PROJECT_ROOT = Path(__file__).parent.resolve()
sys.path.insert(0, str(PROJECT_ROOT))

# 有偿授权门控：免费版 3 条/天，超限触发 Pro CTA（接 paywall.check_free_quota）
from paywall import check_free_quota, build_upgrade_cta


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("mcn_studio")

from core.models import (
    AgentRole, AgentLevel, Project, Task, TaskStatus, Priority,
    create_all_agents, ContentPlatform,
)
from core.regulations import (
    COMPANY_REGULATIONS, WORKFLOW_DEFINITIONS, PROJECT_TEMPLATES,
)
from agents.orchestrator import OrchestratorAgent


class MCNStudio:
    """AI MCN工作室主类（v3.0，24名数字员工）"""

    def __init__(self):
        self.agents = create_all_agents()
        # orchestrator 是第一个（CEO令仪），其余23人为员工
        self.orchestrator = OrchestratorAgent(
            config=self.agents[0],
            all_agents=self.agents,
        )
        self.projects: dict[str, Project] = {}
        logger.info(
            "AI MCN Studio v3.0 启动成功，已加载 %d 名数字员工",
            len(self.agents),
        )

    # ── 团队状态 ───────────────────────────────────────────────────

    def get_team_status(self) -> dict:
        """获取团队状态（含职级与汇报关系）"""
        return {
            "studio_name": "AI MCN Studio v3.0",
            "team_size": len(self.agents),
            "active_workflows": len(WORKFLOW_DEFINITIONS),
            "level_distribution": {
                lvl.value: sum(1 for a in self.agents if a.level == lvl)
                for lvl in AgentLevel
            },
            "agents": [
                {
                    "id": a.id,
                    "name": a.name,
                    "title": a.title,
                    "department": a.department,
                    "role": a.role.value,
                    "level": a.level.value,
                    "reports_to": a.reports_to or "令仪",
                    "productivity": a.productivity_score,
                    "creativity": a.creativity_score,
                    "reliability": a.reliability_score,
                }
                for a in self.agents
            ],
        }

    # ── 项目管理 ───────────────────────────────────────────────────

    def create_project(self, name: str, goal: str, platforms: list[str],
                       template: str = "") -> Project:
        """创建新项目（支持6种任务模板）"""
        project = Project(
            name=name,
            description=goal,
            goal=goal,
            platform=[
                ContentPlatform(p) for p in platforms
                if p in [x.value for x in ContentPlatform]
            ],
        )

        if template and template in PROJECT_TEMPLATES:
            for t_def in PROJECT_TEMPLATES[template].get("default_tasks", []):
                task = Task(
                    title=t_def["title"],
                    description=f"{t_def['title']} - {name}",
                    task_type=t_def["type"],
                    priority=Priority.MEDIUM,
                    platform=project.platform[0] if project.platform else None,
                )
                project.add_task(task)

        self.projects[project.id] = project
        self.orchestrator.active_projects[project.id] = project
        logger.info("项目已创建: %s (ID: %s)", name, project.id)
        return project

    # ── 工作流执行（全24角色，0缺失） ──────────────────────────────

    def execute_workflow(self, workflow_name: str, project_name: str,
                        platform: str = "douyin",
                        context: dict | None = None) -> str:
        """通过总调度执行完整工作流（新角色owner自动路由）"""
        if workflow_name not in WORKFLOW_DEFINITIONS:
            available = ", ".join(WORKFLOW_DEFINITIONS.keys())
            return f"未找到工作流：{workflow_name}\n可用：{available}"

        result = self.orchestrator.think({
            "action": "execute_workflow",
            "workflow": workflow_name,
            "project_id": project_name,
            "platform": platform,
            "context": context or {"project_name": project_name},
            "task_id": f"wf-{workflow_name}",
        })
        return result.content

    # ── 交互模式 ───────────────────────────────────────────────────

    def interactive_mode(self):
        """交互模式（扩展命令）"""
        print("\n" + "=" * 60)
        print("  AI MCN Studio v3.0 - 交互式控制台")
        print("=" * 60)
        print("\n可用命令：")
        print("  team            - 查看团队状态（含职级/汇报关系）")
        print("  org             - 查看分级组织架构图")
        print("  regulations    - 查看公司规章制度")
        print("  workflows      - 查看11套可用工作流")
        print("  create <name> <goal> <platform> [template] - 创建项目")
        print("  run <workflow> <project> [platform] - 执行工作流")
        print("  agent <name> <task_type> <task_desc> - 与单个Agent对话")
        print("  crisis <event> - 触发危机响应（CEO集中管理）")
        print("  status          - 查看总调度状态")
        print("  exit            - 退出\n")

        while True:
            try:
                cmd = input("mcn> ").strip()
                if not cmd:
                    continue
                if cmd == "exit":
                    print("再见！")
                    break
                elif cmd == "team":
                    self._cmd_team()
                elif cmd == "org":
                    print(self.orchestrator.print_org_chart())
                elif cmd == "regulations":
                    print("\n" + COMPANY_REGULATIONS)
                elif cmd == "workflows":
                    self._cmd_workflows()
                elif cmd.startswith("create "):
                    self._cmd_create(cmd[7:])
                elif cmd.startswith("run "):
                    self._cmd_run(cmd[4:])
                elif cmd.startswith("agent "):
                    self._cmd_agent(cmd[6:])
                elif cmd.startswith("crisis "):
                    self._cmd_crisis(cmd[7:])
                elif cmd == "status":
                    self._cmd_status()
                else:
                    print(f"未知命令：{cmd}")
            except (EOFError, KeyboardInterrupt):
                print("\n再见！")
                break

    def _cmd_team(self):
        status = self.get_team_status()
        print(f"\n团队规模：{status['team_size']} 人")
        print(f"   职级分布：{status['level_distribution']}")
        print("-" * 50)
        for agent in status["agents"]:
            mark = {"ceo": "[CEO]", "director": "[总监]",
                    "senior": "[高级]", "staff": "[专员]"}.get(
                agent["level"], "[?]")
            print(f"  {mark} {agent['name']} | {agent['title']}")
            print(f"     部门：{agent['department']} | 汇报：{agent['reports_to']}")
            print(f"     效率:{agent['productivity']} 创意:{agent['creativity']} "
                  f"可靠:{agent['reliability']}")
            print()

    def _cmd_workflows(self):
        print(f"\n可用工作流（共{len(WORKFLOW_DEFINITIONS)}套）：")
        for key, wf in WORKFLOW_DEFINITIONS.items():
            print(f"  · {wf['name']} ({key})")
            print(f"    步骤数：{len(wf['steps'])} | "
                  f"{wf.get('description', '')}\n")

    def _cmd_create(self, args: str):
        parts = args.strip().split(None, 3)
        if len(parts) < 2:
            print("用法：create <项目名称> <目标> <平台> [模板]")
            print(f"   可用模板：{', '.join(PROJECT_TEMPLATES.keys())}")
            return
        name, goal = parts[0], parts[1]
        platform = parts[2] if len(parts) > 2 else "douyin"
        template = parts[3] if len(parts) > 3 else ""
        project = self.create_project(name, goal, [platform], template)
        print(f"项目已创建：{name} (ID: {project.id})")
        print(f"   任务数：{len(project.tasks)}")

    def _cmd_run(self, args: str):
        parts = args.strip().split(None, 2)
        if len(parts) < 2:
            print("用法：run <工作流key> <项目名> [平台]")
            print(f"   可用工作流：{', '.join(WORKFLOW_DEFINITIONS.keys())}")
            return
        workflow, project_name = parts[0], parts[1]
        platform = parts[2] if len(parts) > 2 else "douyin"
        print(self.execute_workflow(workflow, project_name, platform))

    def _cmd_agent(self, args: str):
        """agent <姓名或角色> <任务类型> <任务描述>"""
        parts = args.strip().split(None, 2)
        if len(parts) < 2:
            print("用法：agent <姓名> <任务类型> <任务描述>")
            print("   示例：agent 慧眼 数据 分析本周数据")
            return
        agent_name, task_type = parts[0], parts[1]
        task_desc = parts[2] if len(parts) > 2 else agent_name

        agent = self.orchestrator.get_agent_by_name(agent_name)
        if not agent:
            # 尝试按角色查找
            try:
                agent = self.orchestrator.get_agent_by_role(AgentRole(agent_name))
            except ValueError:
                agent = None
        if not agent:
            available = " ".join(a.name for a in self.agents)
            print(f"未找到Agent：{agent_name}\n可用：{available}")
            return

        result = agent.think({
            "title": task_desc,
            "task_type": task_type,
            "platform": "douyin",
            "context": {},
            "task_id": "interactive",
        })
        print(f"\n{agent.config.name}（{agent.config.title}，"
              f"{agent.config.department}）回应：\n")
        print(result.content)
        print(f"\n置信度：{result.confidence:.0%}")

    def _cmd_crisis(self, event: str):
        result = self.orchestrator.think({
            "action": "crisis_response",
            "context": {},
            "task_id": "crisis",
            "crisis": event,
            "severity": "high",
        })
        print("\n" + result.content)

    def _cmd_status(self):
        result = self.orchestrator.think({
            "action": "status_check",
            "context": {},
            "task_id": "status",
        })
        print("\n" + result.content)


def main():
    """主函数"""
    print("\n" + "═" * 60)
    print("  AI MCN Studio v3.0 - 人工智能自媒体工作室")
    print("  24名数字员工 · 7部门 · 11套工作流")
    print("═" * 60 + "\n")

    studio = MCNStudio()

    # 检查命令行参数
    if len(sys.argv) > 1:
        if sys.argv[1] == "--demo":
            import demo as demo_module
            demo_module.demo()
        elif sys.argv[1] == "--status":
            status = studio.get_team_status()
            print(json.dumps(status, ensure_ascii=False, indent=2))
        elif sys.argv[1] == "--org":
            print(studio.orchestrator.print_org_chart())
        elif sys.argv[1] == "--workflows":
            studio._cmd_workflows()
        else:
            print(f"未知命令：{sys.argv[1]}")
            print("可用命令：--demo, --status, --org, --workflows, "
                  "(无参数进入交互模式)")
    else:
        studio.interactive_mode()


if __name__ == "__main__":
    main()


def gate_access(used_today=0, is_pro=False):
    """有偿授权门控：免费 3 条/天，Pro 不限（原 paywall 路径，行为不变）"""
    return check_free_quota(used_today, is_pro)


def gate_access_unified(plan="free", action="use", tenant_id=""):
    """统一门控入口：走 billing.check_access 代理（与其他 7 仓 billing 签名一致，
    返回 {"allowed","remaining","reason","upgrade_url"}）。
    两个入口并存：gate_access 保持原 paywall 行为（超限抛 QuotaExceededError），
    gate_access_unified 为结构化返回，供 API/前端消费。"""
    import billing
    return billing.check_access(plan=plan, action=action, tenant_id=tenant_id)
