# -*- coding: utf-8 -*-
"""
AI MCN Studio - 热点速报生成器
研究中心（瞭望·趋势分析师 + 疾风·热点追踪员）联合输出：
将原始热点信号结构化为主题/风险/借势角度/建议动作，供创意中心快速立项。
"""

from __future__ import annotations

import random
from datetime import datetime
from typing import Any


# 热点信号 → 借势角度映射（行业通用启发式规则）
_ANGLE_RULES: dict[str, list[str]] = {
    "产品翻车": ["第三方客观测评", "消费者权益科普", "行业乱象盘点", "理性吃瓜指南"],
    "科技发布": ["第一时间拆解", "对普通人意味着什么", "国产替代对比", "应用落地预测"],
    "社会议题": ["理性观点输出", "情绪共鸣+实用建议", "多方视角拆解", "冷知识切入"],
    "娱乐榜单": ["幕后故事揭秘", "行业现象解读", "经典回顾", "数据榜单可视化"],
    "政策新规": ["新规影响清单", "合规操作指南", "时间轴解读", "案例对照"],
    "突发事件": ["已证实信息整理", "安全/实用提示", "权威来源汇总", "后续跟踪预告"],
}

_PLATFORM_FOCUS: dict[str, str] = {
    "douyin": "短视频快闪拆解，前3秒强钩子，强调时效性",
    "bilibili": "中长视频深度解读，强调逻辑完整与数据支撑",
    "xiaohongshu": "图文攻略/情绪种草，标题口语化，搜索长尾词布局",
    "kuaishou": "真实接地气，强调人与产品的强连接",
    "video_account": "社交链传播友好，便于转发，观点清晰",
}


def build_hot_topic_report(
    raw_topics: list[dict[str, Any]],
    platform: str = "douyin",
    top_n: int = 5,
) -> dict[str, Any]:
    """
    输入原始热点信号 [{title, category, heat, ...}]，
    输出结构化速报：排序 + 借势角度 + 风险提示 + 建议动作 + SLA。
    """
    scored = []
    for t in raw_topics:
        heat = float(t.get("heat", 50))
        # 时效性加权：越高越热越优先
        scored.append({
            **t,
            "score": round(heat * 0.6 + random.uniform(0, 20), 1),
            "angles": _ANGLE_RULES.get(t.get("category", "社会议题"), _ANGLE_RULES["社会议题"]),
        })
    scored.sort(key=lambda x: x["score"], reverse=True)
    top = scored[:top_n]

    report_lines = [
        f"【热点速报】{datetime.now().strftime('%Y-%m-%d %H:%M')}  |  平台焦点：{_PLATFORM_FOCUS.get(platform, '通用')}",
        "-" * 52,
    ]
    for i, t in enumerate(top, 1):
        report_lines += [
            f"{i}. {t.get('title', '未命名热点')}（{t.get('category', '综合')}）  热度:{t['score']}",
            f"   借势角度：{t['angles'][0]}  备选：{t['angles'][1]}",
            f"   风险：涉{t.get('category', '热点')}需前置合规审查；突发事件仅采用已证实信息",
            f"   建议动作：3h内由疾风评估立项 → 墨言定稿 → 笔灵快脚本 → 守法快审 → 星轨加急发布",
        ]
    report_lines += ["-" * 52, f"SLA：热点响应<4h；合规快审<1h；加急发布窗口按平台高峰对齐。"]

    return {
        "platform": platform,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "top_topics": top,
        "report_text": "\n".join(report_lines),
        "action_owner_chain": ["hottracker", "creative_director", "copy_chief",
                                "compliance_reviewer", "publication_planner"],
    }


def next_suggestion(report: dict[str, Any]) -> dict[str, Any]:
    """基于速报给出下一步可执行建议（供总调度直接分派）"""
    if not report.get("top_topics"):
        return {"suggestion": "无热点信号，转入常规内容排期"}
    top1 = report["top_topics"][0]
    return {
        "suggestion": f"立即立项「{top1.get('title')}」，角度：{top1['angles'][0]}",
        "owner": report["action_owner_chain"][0],
        "sla_hours": 4,
        "follow_up_roles": report["action_owner_chain"][1:],
    }
