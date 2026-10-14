# -*- coding: utf-8 -*-
"""
AI MCN Studio - 矩阵数据看板生成器
运营中心（慧眼·数据分析师 + 鉴往·案例复盘员）输出：
多账号效率对比、账号间资源调优建议、矩阵健康度评分。
"""

from __future__ import annotations

from typing import Any


def build_matrix_dashboard(accounts: list[dict[str, Any]]) -> dict[str, Any]:
    """
    输入账号指标列表 [{name, followers, avg_views, engagement_rate, conversion_rate, gmv}]
    输出：排序榜、资源调优建议（从低效→高效导流）、矩阵健康度。
    """
    rows = []
    for a in accounts:
        views = float(a.get("avg_views", 0))
        eng = float(a.get("engagement_rate", 0))
        conv = float(a.get("conversion_rate", 0))
        gmv = float(a.get("gmv", 0))
        # 效率分：互动率与转化为核心，播放量做量级修正
        efficiency = round(eng * 50 + conv * 50 + min(views / 100000, 1) * 10 + min(gmv / 100000, 1) * 5, 1)
        rows.append({
            **a,
            "efficiency_score": efficiency,
        })
    rows.sort(key=lambda x: x["efficiency_score"], reverse=True)

    best = rows[0] if rows else None
    worst = rows[-1] if rows else None
    suggestions = []
    if best and worst and best["name"] != worst["name"]:
        suggestions.append(
            f"将 {worst['name']} 的粉丝向 {best['name']} 内容导流（效率分 {best['efficiency_score']} vs {worst['efficiency_score']}）"
        )
    low_eng = [r for r in rows if r["engagement_rate"] < 2]
    if low_eng:
        suggestions.append(f"以下账号互动率偏低需优化内容钩子：{', '.join(r['name'] for r in low_eng)}")

    health = "healthy" if not low_eng else "needs_work"
    if best:
        health = "healthy" if best["efficiency_score"] >= 40 else "needs_work"

    lines = ["【矩阵数据看板】账号效率对比（降序）", "-" * 44]
    for i, r in enumerate(rows, 1):
        lines.append(
            f"{i}. {r.get('name','?')}  效率分:{r['efficiency_score']}  "
            f"粉丝:{int(r.get('followers',0)):,}  互动:{r.get('engagement_rate',0):.1f}%  "
            f"转化:{r.get('conversion_rate',0):.1f}%"
        )
    lines.append("-" * 44)
    for sug in suggestions:
        lines.append(f"· {sug}")
    lines.append(f"矩阵健康度：{health}")

    return {
        "ranked_accounts": rows,
        "best": best,
        "worst": worst,
        "suggestions": suggestions,
        "health": health,
        "dashboard_text": "\n".join(lines),
    }


def next_optimization(dashboard: dict[str, Any]) -> dict[str, Any]:
    """看板下一步动作（供总调度分派给运营中心）"""
    if not dashboard.get("ranked_accounts"):
        return {"suggestion": "无账号数据，先由慧眼采集基线", "owner": "data_analyst"}
    return {
        "suggestion": dashboard.get("suggestions", ["维持当前矩阵结构"])[0],
        "owner": "data_analyst",
        "follow_up_roles": ["operations_strategy", "case_reviewer"],
    }
