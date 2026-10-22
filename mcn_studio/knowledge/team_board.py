# -*- coding: utf-8 -*-
"""
AI MCN Studio - 团队效能与项目看板
总调度（令仪·CEO）视角：跨部门项目进度汇总、数字员工效能评分、组织健康度。
"""

from __future__ import annotations

from typing import Any


def team_efficiency_report(agents: list[Any]) -> dict[str, Any]:
    """
    基于 24 名数字员工的 productivity/creativity/reliability 三项分，
    计算团队效能画像与组织健康度。
    """
    total = len(agents)
    if total == 0:
        return {"total": 0, "health": "unknown"}

    prod = sum(a.productivity_score for a in agents) / total
    crea = sum(a.creativity_score for a in agents) / total
    reli = sum(a.reliability_score for a in agents) / total

    # 效能分 = 效率50% + 可靠30% + 创意20%
    efficiency = round(prod * 0.5 + reli * 0.3 + crea * 0.2, 1)

    dept_stats: dict[str, dict] = {}
    for a in agents:
        d = dept_stats.setdefault(a.department, {
            "count": 0, "prod": 0.0, "crea": 0.0, "reli": 0.0,
        })
        d["count"] += 1
        d["prod"] += a.productivity_score
        d["crea"] += a.creativity_score
        d["reli"] += a.reliability_score

    dept_lines = []
    weak_depts = []
    for dept, d in dept_stats.items():
        n = d["count"]
        d_eff = round(d["prod"] / n * 0.5 + d["reli"] / n * 0.3 + d["crea"] / n * 0.2, 1)
        dept_lines.append(f"  · {dept}（{n}人）效能 {d_eff}")
        if d_eff < 85:
            weak_depts.append(f"{dept}({d_eff})")

    health = "healthy" if efficiency >= 90 else "watch" if efficiency >= 85 else "at_risk"
    text = "\n".join([
        f"【团队效能看板】{total}名数字员工",
        f"  均值：效率 {prod:.1f} | 创意 {crea:.1f} | 可靠 {reli:.1f}",
        f"  综合效能分：{efficiency}",
        f"  组织健康度：{health}",
        "  分部门效能：",
        *dept_lines,
    ])
    return {
        "total": total,
        "efficiency": efficiency,
        "health": health,
        "dept_stats": dept_stats,
        "weak_departments": weak_depts,
        "report_text": text,
    }


def project_board(projects: list[Any]) -> dict[str, Any]:
    """
    跨项目进度看板：按状态分组、暴露阻塞项、给出 CEO 决策建议。
    projects: Project 对象列表（含 tasks）
    """
    by_status: dict[str, list] = {}
    blocked_tasks = []
    for p in projects:
        by_status.setdefault(p.status.value, []).append(p.name)
        for t in p.tasks:
            if t.status.value == "blocked":
                blocked_tasks.append(f"{p.name} / {t.title}")

    total_tasks = sum(len(p.tasks) for p in projects)
    done = sum(1 for p in projects for t in p.tasks if t.status.value in ("done", "revised"))
    progress = round(done / total_tasks * 100) if total_tasks else 0

    lines = [f"【项目看板】{len(projects)}个活跃项目 / {total_tasks}个任务 / 进度 {progress}%",
             "  按状态："]
    for st, names in by_status.items():
        lines.append(f"    {st}: {', '.join(names) if names else '无'}")
    if blocked_tasks:
        lines.append(f"  ⚠ 阻塞项 {len(blocked_tasks)} 个需CEO协调：" + "；".join(blocked_tasks))
    else:
        lines.append("  ✅ 无阻塞项")

    suggestion = "维持当前节奏"
    if blocked_tasks:
        suggestion = f"优先协调 {len(blocked_tasks)} 个阻塞项，必要时调拨跨部门资源"
    return {
        "project_count": len(projects),
        "task_count": total_tasks,
        "progress_pct": progress,
        "blocked_tasks": blocked_tasks,
        "suggestion": suggestion,
        "board_text": "\n".join(lines),
    }
