# -*- coding: utf-8 -*-
"""
AI MCN Studio - AI 内容标注合规模块
行业标准：深度合成/AI 生成内容须显著标注（对应《互联网信息服务深度合成管理规定》
及抖音/B站/小红书/YouTube 等平台 AI 标注要求）。供守法（合规审查员）发布前核验。
"""

from __future__ import annotations

from typing import Any


# 各平台 AI 内容标注要求
AI_LABELING_RULES: dict[str, dict[str, Any]] = {
    "douyin": {
        "name": "抖音",
        "mandatory": True,
        "method": "发布时勾选『内容由AI生成』或使用平台AI标识工具",
        "scope": "AI换脸、AI生成画面/语音、深度合成内容必须标注",
        "risk_if_missing": "未标注的AI内容可能被限流、下架并计入违规",
    },
    "bilibili": {
        "name": "B站",
        "mandatory": True,
        "method": "在视频简介或描述区注明AI参与程度；AI虚拟UP主需实名认证+标注",
        "scope": "AI配音、AI绘画画面、数字人需披露",
        "risk_if_missing": "AI虚拟UP主未标注将被停止商业化",
    },
    "xiaohongshu": {
        "name": "小红书",
        "mandatory": True,
        "method": "AI生成图文/视频需使用平台AI标识功能",
        "scope": "AI修图、AI文案、数字人出镜",
        "risk_if_missing": "虚假种草+AI未标注双重违规，处罚更重",
    },
    "kuaishou": {
        "name": "快手",
        "mandatory": True,
        "method": "AI内容发布时选择AI标识",
        "scope": "AI换脸、合成视频",
        "risk_if_missing": "限流+账号扣分",
    },
    "youtube": {
        "name": "YouTube",
        "mandatory": True,
        "method": "对『realistic content』勾选 I altered or synthesized this content",
        "scope": "AI生成或编辑的真实感画面/语音",
        "risk_if_missing": "违反 YP 政策，影响变现与推荐",
    },
    "tiktok": {
        "name": "TikTok",
        "mandatory": True,
        "method": "AI-generated content effect label（发布时勾选）",
        "scope": "AI效果、换脸、合成语音",
        "risk_if_missing": "内容被限流或下架",
    },
}


def check_ai_labeling(platform: str, is_ai_generated: bool,
                      ai_disclosed: bool) -> dict[str, Any]:
    """
    发布前核验 AI 内容是否满足标注要求。
    返回：是否合规、缺口说明、补救动作。
    """
    rule = AI_LABELING_RULES.get(platform, {
        "name": platform, "mandatory": True,
        "method": "按平台AI标注要求披露", "risk_if_missing": "可能被限流/下架",
    })

    if not is_ai_generated:
        return {"platform": platform, "ai_labeling_required": False,
                "compliant": True, "gap": "", "action": "无需AI标注"}

    required = rule.get("mandatory", True)
    if required and not ai_disclosed:
        return {"platform": platform, "ai_labeling_required": True,
                "compliant": False,
                "gap": "AI生成内容未完成标注",
                "action": f"发布前务必{rule.get('method', '标注AI生成')}，否则{rule.get('risk_if_missing', '')}",
                "owner": "compliance_reviewer"}
    return {"platform": platform, "ai_labeling_required": True,
            "compliant": True, "gap": "", "action": "AI标注已满足"}
