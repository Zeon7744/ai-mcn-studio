# -*- coding: utf-8 -*-
"""
AI MCN Studio - 全量自动化验证
覆盖：24名Agent实例化与think()、12套工作流0缺失、模板覆盖、知识库/案例库、合规快扫
运行：python tests/test_full_coverage.py （无需pytest，直接运行即可）
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.models import create_all_agents, AgentRole, AgentLevel
from agents.orchestrator import OrchestratorAgent
from core.regulations import WORKFLOW_DEFINITIONS, PROJECT_TEMPLATES
from knowledge import make_hot_report, hot_report_next_step
from knowledge import (
    search_platform_info, get_best_posting_time, get_title_suggestions,
    check_compliance, get_compliance_guide, quick_compliance_scan,
    get_platform_checklist,
)
from knowledge.content_formulas import CONTENT_FORMULAS
from knowledge.script_templates import SCRIPT_TEMPLATES
from knowledge.industry_trends import INDUSTRY_TRENDS
from cases import SUCCESS_CASES, FAILURE_CASES, EXTRA_SUCCESS_CASES, EXTRA_FAILURE_CASES


def _check(label, ok, detail=""):
    mark = "PASS" if ok else "FAIL"
    print(f"  [{mark}] {label}" + (f" — {detail}" if detail and not ok else ""))
    return ok


def main():
    print("=" * 60)
    print("AI MCN Studio 全量覆盖验证")
    print("=" * 60)
    all_ok = True

    # 1. 员工名册
    agents = create_all_agents()
    ok = _check("员工名册 = 24人", len(agents) == 24, f"实际 {len(agents)}")
    all_ok &= ok
    roles = [a.role for a in agents]
    ok = _check("24个角色唯一", len(set(roles)) == 24, "存在重复角色")
    all_ok &= ok
    level_dist = {lvl.value: 0 for lvl in AgentLevel}
    for a in agents:
        level_dist[a.level.value] += 1
    ok = _check("职级分布合理", level_dist["ceo"] == 1 and level_dist["director"] == 7,
                str(level_dist))
    all_ok &= ok

    # 2. 总调度与全部Agent实例化
    orch = OrchestratorAgent(config=agents[0], all_agents=agents)
    ok = _check("Agent实例化 = 23（除CEO）", len(orch.agent_instances) == 23,
                f"实际 {len(orch.agent_instances)}")
    all_ok &= ok

    # 3. 全角色think()可达
    think_fail = []
    for role in AgentRole:
        if role == AgentRole.ORCHESTRATOR:
            continue
        a = orch.get_agent_by_role(role)
        if not a:
            think_fail.append(f"{role.value}(未实例化)")
        else:
            r = a.think({"title": "验证任务", "task_type": "数据",
                         "platform": "douyin", "context": {}, "task_id": "t"})
            if not r.success:
                think_fail.append(f"{role.value}(think失败)")
    ok = _check("23个非CEO角色全部think()成功", not think_fail, "; ".join(think_fail))
    all_ok &= ok

    # 4. 工作流0缺失
    total = 0
    bad_wf = []
    for key, wf in WORKFLOW_DEFINITIONS.items():
        result = orch.think({
            "action": "execute_workflow", "workflow": key,
            "project_id": "coverage-test", "platform": "douyin",
        "context": {}, "task_id": "cov",
        })
        # 通过输出文本核对：步骤标记 ✅/❌
        done = result.content.count("✅")
        failed_marks = result.content.count("❌")
        total += done + failed_marks
        if failed_marks > 0:
            bad_wf.append(f"{key}:{failed_marks}步失败")
    ok = _check(f"工作流{len(WORKFLOW_DEFINITIONS)}套全步骤0缺失（共{total}步）",
                not bad_wf, "; ".join(bad_wf))
    all_ok &= ok

    # 5. 项目模板覆盖
    tpl_roles = {t["type"] for tpl in PROJECT_TEMPLATES.values() for t in tpl["default_tasks"]}
    ok = _check(f"项目模板{len(PROJECT_TEMPLATES)}套（任务类型{len(tpl_roles)}种）",
                len(PROJECT_TEMPLATES) >= 7, f"实际 {len(PROJECT_TEMPLATES)}")
    all_ok &= ok

    # 6. 知识库
    ok = _check("平台算法库检索", bool(search_platform_info("douyin")))
    all_ok &= ok
    ok = _check("最佳发布时间检索", bool(get_best_posting_time("douyin", True)))
    all_ok &= ok
    ok = _check("标题建议生成", len(get_title_suggestions("AI工具", "douyin")) > 0)
    all_ok &= ok
    ok = _check("合规检查API", isinstance(check_compliance("douyin", "测试内容"), dict))
    all_ok &= ok
    ok = _check("合规指南API", bool(get_compliance_guide("douyin")))
    all_ok &= ok

    # 7. 合规快扫（新模块）
    scan = quick_compliance_scan("douyin", "这款产品100%有效，全网第一！")
    ok = _check("合规快扫命中高危词", (not scan["safe"]) and len(scan["hits"]) >= 2,
                f"hits={len(scan.get('hits', []))}")
    all_ok &= ok
    clean = quick_compliance_scan("douyin", "今天分享三款好用的效率工具")
    ok = _check("合规快扫干净文本通过", clean["safe"])
    all_ok &= ok
    cl = get_platform_checklist("kuaishou")
    ok = _check("快手红线清单加载", len(cl.get("redlines", [])) >= 4,
                f"实际 {len(cl.get('redlines', []))}")
    all_ok &= ok
    cl_unknown = get_platform_checklist("unknown_platform")
    ok = _check("未知平台兜底清单", "redlines" in cl_unknown)
    all_ok &= ok

    # 8. 公式与模板库
    ok = _check("钩子公式库", len(CONTENT_FORMULAS.get("hooks", {})) >= 7)
    all_ok &= ok
    ok = _check("脚本模板库", len(SCRIPT_TEMPLATES) >= 11, f"实际 {len(SCRIPT_TEMPLATES)}")
    all_ok &= ok
    ok = _check("行业趋势库", len(INDUSTRY_TRENDS) >= 2, f"实际 {len(INDUSTRY_TRENDS)}")
    all_ok &= ok

    # 9. 案例库
    ok = _check("案例库（成功+失败）",
                len({**SUCCESS_CASES, **EXTRA_SUCCESS_CASES}) >= 8
                and len({**FAILURE_CASES, **EXTRA_FAILURE_CASES}) >= 8)
    all_ok &= ok

    # 10. 热点速报
    hr = make_hot_report([{"title": "测试热点", "category": "产品翻车", "heat": 80}],
                        "douyin", top_n=2)
    ok = _check("热点速报生成", bool(hr.get("report_text")) and len(hr.get("top_topics", [])) >= 1)
    all_ok &= ok
    hs = hot_report_next_step(hr)
    ok = _check("热点下一步建议", hs.get("owner") == "hottracker", str(hs))
    all_ok &= ok
    print("=" * 60)
    print(f"结果：{'全部通过 ✔' if all_ok else '存在失败项 ✘'}")
    print("=" * 60)
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
