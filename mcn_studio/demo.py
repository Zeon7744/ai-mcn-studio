# -*- coding: utf-8 -*-
"""
AI MCN Studio - 完整功能演示 v3.0
展示24个数字员工的分级组织架构、12套工作流、知识库与案例库
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.models import create_all_agents, AgentRole, AgentLevel
from agents.orchestrator import OrchestratorAgent
from knowledge import (
    search_platform_info, check_compliance, get_best_posting_time,
    get_title_suggestions, get_compliance_guide,
    CONTENT_FORMULAS, SCRIPT_TEMPLATES, PLATFORM_COMPARISON,
    quick_compliance_scan, get_platform_checklist,
)
from cases import SUCCESS_CASES, FAILURE_CASES, EXTRA_SUCCESS_CASES, EXTRA_FAILURE_CASES, CASE_REVIEW_FRAMEWORK
from core.regulations import WORKFLOW_DEFINITIONS, COMPANY_REGULATIONS


def _section(title: str) -> None:
    print("\n" + "═" * 60)
    print(f"【{title}】")
    print("═" * 60)


def demo():
    print("\n╔" + "═" * 58 + "╗")
    print("║       AI MCN Studio v3.0 — 人工智能自媒体工作室      ║")
    print("║       24名数字员工 · 7部门 · 12套工作流            ║")
    print("╚" + "═" * 58 + "╝\n")

    # ── 初始化 ──────────────────────────────────────────────────────
    all_agents = create_all_agents()
    orchestrator = OrchestratorAgent(
        config=all_agents[0],
        all_agents=all_agents,
    )
    print(f"✅ 已初始化 {len(orchestrator.agent_instances) + 1} 名数字员工"
          f"（含总调度CEO令仪）\n")

    # ── 第一部分：分级组织架构 ─────────────────────────────────────
    _section("第一部分：分级组织架构（CEO → 总监 → 专员）")
    print(orchestrator.print_org_chart())

    # 职级分布
    print("\n  职级分布：")
    level_counts = {}
    for a in all_agents:
        level_counts[a.level.value] = level_counts.get(a.level.value, 0) + 1
    for lvl, cnt in level_counts.items():
        label = {"ceo": "CEO", "director": "总监", "senior": "高级专员",
                 "staff": "专员", "assistant": "助理"}.get(lvl, lvl)
        print(f"    · {label}（{lvl}）：{cnt}人")

    # ── 第二部分：全员名册 ─────────────────────────────────────────
    _section("第二部分：24名数字员工名册（按部门）")
    by_dept = {}
    for agent in all_agents:
        by_dept.setdefault(agent.department, []).append(agent)
    for dept, members in by_dept.items():
        print(f"\n  {dept}：")
        for m in members:
            level_mark = {"ceo": "👑", "director": "◆", "senior": "◇",
                          "staff": "·"}.get(m.level.value, "·")
            print(f"    {level_mark} {m.name}（{m.title}，职级:{m.level.value}，"
                  f"汇报:{m.reports_to or '令仪'}）")

    # ── 第三部分：平台算法知识库 ──────────────────────────────────
    _section("第三部分：平台算法知识库（6大平台）")
    print(PLATFORM_COMPARISON)

    print("  抖音算法详情：")
    dy_info = search_platform_info("douyin")
    print(f"     核心机制：{dy_info.get('algorithm_core', 'N/A')}")
    for p in dy_info.get("traffic_pools", [])[:3]:
        print(f"     · {p['pool']}: {p['range']}播放 | 关键指标：{p['key_metric']}")
    print(f"     最佳发布时间：{get_best_posting_time('douyin', True)}")

    print("\n  B站算法详情：")
    bilibili_info = search_platform_info("bilibili")
    print(f"     核心机制：{bilibili_info.get('algorithm_core', 'N/A')}")
    for k, v in list(bilibili_info.get("key_metrics", {}).items())[:3]:
        print(f"     · {k}: 权重{v.get('weight', 0)}, 优秀线{v.get('target_excellent', 'N/A')}")

    print("\n  小红书算法详情：")
    xhs_info = search_platform_info("xiaohongshu")
    print(f"     核心机制：{xhs_info.get('algorithm_core', 'N/A')}")
    print("     核心特色：收藏率权重最高（30%），搜索长尾效应强")

    # ── 第四部分：内容公式库演示 ──────────────────────────────────
    _section("第四部分：内容公式库")
    hooks = CONTENT_FORMULAS.get("hooks", {})
    print("  爆款钩子公式：")
    for name, hook in list(hooks.items())[:4]:
        print(f"     · {name}")
        print(f"       公式：{hook.get('formula', 'N/A')}")
        print(f"       示例：{hook.get('example', 'N/A')}")
        print()

    structures = CONTENT_FORMULAS.get("structures", {})
    print("  内容结构模型：")
    for name, struct in list(structures.items())[:3]:
        print(f"     · {name}：{' -> '.join(s[0] for s in struct.get('steps', []))}")
    print()

    # ── 第五部分：合规审查演示 ────────────────────────────────────
    _section("第五部分：合规审查演示（守法·合规审查员）")
    test_contents = [
        ("正常内容", "大家好，今天给大家介绍一款好用的护肤品，使用感受很不错"),
        ("违规内容", "这款护肤品根治湿疹，100%有效，绝对第一品牌！"),
    ]
    for label, content in test_contents:
        result = check_compliance("douyin", content)
        status = "✅ 合规" if result["safe"] else f"⚠️ 发现 {len(result['violations'])} 处问题"
        print(f"  [{label}] {status}")
        if not result["safe"]:
            for v in result["violations"][:2]:
                print(f"     · 问题词：{v.get('word', v.get('issue', '未知'))}")
                print(f"       建议：{v.get('suggestion', '修改表述')}")
        print()

    guide = get_compliance_guide("douyin")
    print(f"  抖音合规指南：违禁词 {len(guide['forbidden_words'])} 个，"
          f"违规行为 {len(guide['forbidden_behaviors'])} 类")

    print("  平台红线清单库（新）：")
    for p in ["douyin", "kuaishou", "tiktok"]:
        cl = get_platform_checklist(p)
        print(f"     · {cl['name']}：红线 {len(cl.get('redlines', []))} 条",
              f" 高危词 {len(cl.get('high_risk_words', []))} 个")
    bad_text = "这款面霜全网第一，100%有效，绝对无副作用！"
    scan = quick_compliance_scan("douyin", bad_text)
    print(f"  文本快扫演示：'{bad_text[:14]}...'")
    print(f"     命中 {len(scan['hits'])} 处：",
          f"{', '.join(h['word'] for h in scan['hits'][:4])}")

    # ── 第六部分：脚本模板演示 ────────────────────────────────────
    _section("第六部分：脚本模板库（11种场景）")
    print("  可用模板类型：")
    for name, template in SCRIPT_TEMPLATES.items():
        print(f"     · {template.get('name', name)} ({template.get('duration', 'N/A')})")
    print()

    kb_template = SCRIPT_TEMPLATES.get("short_video_knowledge", {})
    if kb_template:
        print("  知识类短视频模板结构：")
        for time_marker, info in kb_template.get("structure", {}).items():
            print(f"     {time_marker}: {info.get('content', 'N/A')}")

    # ── 第七部分：行业趋势与执行案例 ─────────────────────────────
    _section("第七部分：行业趋势与执行案例（博闻·研究总监团队）")
    from knowledge.industry_trends import INDUSTRY_TRENDS
    overview = INDUSTRY_TRENDS.get("2024_2025_overview", {})
    trends = overview.get("macro_trends", [])
    print("  宏观趋势（前3条）：")
    for i, t in enumerate(trends[:3], 1):
        print(f"     {i}. {t['trend']} (影响: {t['impact']})")
        print(f"        机会：{t['opportunity']}")
    print()

    print("  成功案例库（8个）：")
    all_success = {**SUCCESS_CASES, **EXTRA_SUCCESS_CASES}
    for case_id, case in list(all_success.items())[:4]:
        result = case.get("result", {})
        print(f"     · [{case['platform']}] {case['category']} — "
              f"{case.get('account_type', 'N/A')}")
        print(f"       粉丝：{result.get('followers_start', 0):,} → "
              f"{result.get('followers_end', 0):,}")
        print(f"       变现：{result.get('monetization', 'N/A')}")
    print()

    print("  失败案例库（8个，教训）：")
    all_failure = {**FAILURE_CASES, **EXTRA_FAILURE_CASES}
    for case_id, case in list(all_failure.items())[:4]:
        print(f"     · [{case['platform']}] {case.get('category', 'N/A')}")
        print(f"       原因：{case.get('root_cause', 'N/A')}")
        print(f"       结果：{case.get('result', {}).get('outcome', 'N/A')}")

    # ── 第八部分：完整工作流执行演示 ─────────────────────────────
    _section("第八部分：完整工作流执行演示（12套工作流）")
    print(f"  当前工作流总数：{len(WORKFLOW_DEFINITIONS)}\n")

    # 短视频生产流程
    print("  ▶ 演示：短视频生产流程（6步）")
    result = orchestrator.think({
        "action": "execute_workflow",
        "workflow": "short_video_production",
        "project_id": "Demo短视频项目v3",
        "platform": "douyin",
        "context": {"topic": "AI工具使用教程"},
        "task_id": "demo-wf1",
    })
    print(result.content)

    # 危机公关流程
    print("  ▶ 演示：危机公关流程（7步，CEO集中管理）")
    result = orchestrator.think({
        "action": "execute_workflow",
        "workflow": "crisis_management",
        "project_id": "Demo危机公关项目",
        "platform": "douyin",
        "context": {"crisis": "账号被投诉虚假宣传"},
        "task_id": "demo-wf2",
    })
    print(result.content)

    # 热点借势流程
    print("  ▶ 演示：热点借势响应流程（6步，SLA<4h）")
    result = orchestrator.think({
        "action": "execute_workflow",
        "workflow": "hot_topic_response",
        "project_id": "Demo热点响应",
        "platform": "douyin",
        "context": {"hot_topic": "某产品翻车事件"},
        "task_id": "demo-wf3",
    })
    print(result.content)

    # 账号矩阵运营流程
    print("  ▶ 演示：账号矩阵运营流程（6步）")
    result = orchestrator.think({
        "action": "execute_workflow",
        "workflow": "account_matrix",
        "project_id": "Demo矩阵运营",
        "platform": "douyin",
        "context": {"matrix_size": 4},
        "task_id": "demo-wf4",
    })
    print(result.content)

    # ── 第九部分：总调度状态检查 ─────────────────────────────────
    _section("第十部分：总调度（令仪·CEO）状态检查")
    result = orchestrator.think({
        "action": "status_check",
        "context": {},
        "task_id": "demo-status",
    })
    print(result.content)

    # ── 热点速报演示（研究中心·瞭望+疾风） ──────────────────────
    _section("第十一部分：热点速报（研究中心·瞭望+疾风 联合输出）")
    from knowledge import make_hot_report, hot_report_next_step
    sample=[
        {"title": "某头部品牌虚假宣传被曝光", "category": "产品翻车", "heat": 92},
        {"title": "AI 生成视频新规生效", "category": "政策新规", "heat": 78},
        {"title": "城市夜经济出圈", "category": "社会议题", "heat": 65},
    ]
    report = make_hot_report(sample, "douyin", top_n=3)
    print(report["report_text"])
    nxt = hot_report_next_step(report)
    print()
    print("  下一步：" + nxt["suggestion"])
    print("  负责人：" + nxt["owner"] + "  SLA：" + str(nxt["sla_hours"]) + "h")
    print("  后续链路：" + " → ".join(nxt["follow_up_roles"]))
    # ── 新模块演示：AI标注 + 矩阵看板 + LLM适配层 ─────────────
    _section("第十二部分：本轮新增模块演示（AI标注/矩阵看板/LLM适配层）")
    from knowledge import check_ai_content_labeling, build_matrix_board, matrix_next_step
    from agents.llm_adapter import get_llm_client

    ai_res = check_ai_content_labeling("douyin", is_ai_generated=True, ai_disclosed=False)
    print("  AI内容标注核验（抖音，AI生成未标注）：")
    print("     合规：" + str(ai_res["compliant"]) + "  缺口：" + ai_res["gap"])
    print("     补救：" + ai_res["action"])
    print()

    board = build_matrix_board([
        {"name": "主账号", "followers": 520000, "avg_views": 95000,
         "engagement_rate": 5.1, "conversion_rate": 2.8, "gmv": 150000},
        {"name": "新账号", "followers": 60000, "avg_views": 8000,
         "engagement_rate": 1.5, "conversion_rate": 0.6, "gmv": 5000},
    ])
    print("  矩阵数据看板：")
    print(board["dashboard_text"])
    print("  下一步：" + matrix_next_step(board)["suggestion"])
    print()

    llm = get_llm_client()
    if llm.available:
        print("  LLM 适配层：已配置KEY（可接真实大模型）")
    else:
        print("  LLM 适配层：未配置KEY（自动使用内置模板思维，联网后可无缝升级）")
    print("     目标模型：" + llm.model)

    # ── 总结 ───────────────────────────────────────────────────────
    print("\n" + "═" * 60)
    print("  ✅ 演示完成！AI MCN Studio v3.0 已就绪。")
    print("  团队规模：24名数字员工（1CEO + 7总监 + 16专员）")
    print("  部门覆盖：创意/视觉/运营/主播/商业/风控/研究 7中心")
    print("  工作流：12套全业务线流程（短视频/直播/商单/IP/热点/矩阵/私域/危机/版权/审核/异常/出海）")
    print("  制度库：平台红线清单（7平台）+ 广告法高危词 + 部门岗位与职级手册")
    print("  测试：python tests/test_full_coverage.py 一键全量验证")
    print("  知识库：6平台算法 + 7种钩子公式 + 11种脚本模板 + 合规数据库")
    print("  案例库：4成功 + 4失败执行案例")
    print("  运行 'python main.py' 进入交互模式")
    print("═" * 60 + "\n")


if __name__ == "__main__":
    demo()
