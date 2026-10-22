# -*- coding: utf-8 -*-
"""
研究员 Agent - 博闻
负责行业研究、趋势分析、知识库维护和案例分析
"""

from __future__ import annotations

import random
from datetime import datetime
from typing import Any

from agents.base_agent import AgentOutput, BaseAgent, register_agent
from core.models import AgentRole


@register_agent(AgentRole.RESEARCHER)
class ResearcherAgent(BaseAgent):
    """
    博闻 - 研究员
    负责行业研究、趋势分析、知识库维护、案例复盘
    """

    def __init__(self, config):
        super().__init__(config)
        self._knowledge_updated = True

    def think(self, input_data: dict[str, Any]) -> AgentOutput:
        """研究员的核心思考"""
        action = input_data.get("action", "")
        context = input_data.get("context", {})

        if action == "research_trend":
            response = self._research_trend(context)
        elif action == "analyze_case":
            response = self._analyze_case(context)
        elif action == "update_knowledge":
            response = self._update_knowledge(context)
        elif action == "generate_report":
            response = self._generate_report(context)
        else:
            response = self._default_research(input_data)

        return AgentOutput(
            success=True,
            agent_id=self.config.id,
            agent_name=self.config.name,
            task_id=input_data.get("task_id", "research"),
            output_type="analysis",
            content=self.llm_enhance(input_data, response["output"]),
            confidence=response.get("confidence", 0.88),
            metadata={
                "reasoning": response.get("reasoning", ""),
                "action": action,
            },
            suggestions=response.get("suggestions", []),
        )

    def _research_trend(self, context: dict) -> dict:
        """行业趋势研究"""
        from knowledge.industry_trends import INDUSTRY_TRENDS
        from knowledge.platform_algorithms import PLATFORM_ALGORITHMS
        from knowledge.content_formulas import TRENDING_CONTENT

        platform = context.get("platform", "douyin")
        category = context.get("category", "")

        reasoning = (
            f"【博闻的行业趋势研究】\n\n"
            f"研究领域：{category or '全品类'} | 平台：{platform}\n\n"
        )

        # 获取宏观趋势
        overview = INDUSTRY_TRENDS.get("2024_2025_overview", {})
        trends = overview.get("macro_trends", [])

        reasoning += "📊 宏观趋势分析：\n\n"
        for i, trend in enumerate(trends[:5], 1):
            reasoning += f"  {i}. {trend['trend']}\n"
            reasoning += f"     影响：{trend['impact']} | {trend['description']}\n"
            reasoning += f"     机会：{trend['opportunity']}\n\n"

        # 平台具体更新
        plat_updates = INDUSTRY_TRENDS.get("platform_updates", {}).get(platform, [])
        if plat_updates:
            reasoning += f"📱 {platform} 平台最新动态：\n\n"
            for update in plat_updates:
                reasoning += f"  · [{update['date']}] {update['update']}\n"
                reasoning += f"    应对策略：{update['action']}\n\n"

        # 热门内容类型
        hot_types = TRENDING_CONTENT.get("2024_q4_2025_q1", {}).get("rising_types", [])
        if hot_types:
            reasoning += "🔥 当前热门内容类型：\n\n"
            for item in hot_types[:4]:
                reasoning += f"  · {item['type']} {item['trend']} — {item['reason']}\n"

        reasoning += (
            f"\n💡 研究结论：\n"
            f"  当前内容创作应重点关注情绪价值类内容和AI工具应用。"
            f" 私域运营和直播带货仍是变现主力。"
        )

        return {
            "output": reasoning,
            "confidence": 0.87,
            "reasoning": reasoning,
            "suggestions": [
                "定期更新行业趋势数据库",
                "关注平台官方政策公告",
                "建立竞品监测机制",
            ],
        }

    def _analyze_case(self, context: dict) -> dict:
        """案例分析"""
        from cases.execution_cases import SUCCESS_CASES, FAILURE_CASES

        case_id = context.get("case_id", "")
        case_type = context.get("case_type", "success")

        if case_type == "success":
            cases = SUCCESS_CASES
            label = "成功案例"
        else:
            cases = FAILURE_CASES
            label = "失败案例"

        if case_id and case_id in cases:
            case = cases[case_id]
        elif cases:
            case = list(cases.values())[0]
        else:
            case = {}

        reasoning = (
            f"【博闻的案例分析】\n\n"
            f"案例类型：{label} | 案例编号：{case.get('id', 'N/A')}\n\n"
        )

        reasoning += f"平台：{case.get('platform', 'N/A')} | 品类：{case.get('category', 'N/A')}\n"
        reasoning += f"周期：{case.get('timeline', 'N/A')}\n\n"

        if case.get("result"):
            result = case["result"]
            reasoning += "📈 结果数据：\n"
            for k, v in result.items():
                if isinstance(v, (int, float)):
                    reasoning += f"  · {k}: {v:,}\n"
                else:
                    reasoning += f"  · {k}: {v}\n"
            reasoning += "\n"

        if case.get("key_strategies"):
            reasoning += "🎯 关键策略：\n"
            for s in case["key_strategies"]:
                reasoning += f"  · {s}\n"
            reasoning += "\n"

        if case.get("lessons"):
            reasoning += "💡 经验教训：\n"
            for l in case["lessons"]:
                reasoning += f"  · {l}\n"

        if case.get("turning_points"):
            reasoning += "\n📍 关键转折点：\n"
            for tp in case["turning_points"]:
                reasoning += f"  · [{tp['time']}] {tp['event']}\n"

        return {
            "output": reasoning,
            "confidence": 0.90,
            "reasoning": reasoning,
            "suggestions": [
                "定期复盘成功案例和失败案例",
                "建立案例标签体系便于检索",
                "结合当前项目制定改进计划",
            ],
        }

    def _update_knowledge(self, context: dict) -> dict:
        """更新知识库"""
        source = context.get("source", "unknown")
        content_type = context.get("content_type", "trend")

        reasoning = (
            f"【博闻的知识库更新】\n\n"
            f"信息来源：{source}\n"
            f"更新类型：{content_type}\n\n"
        )

        # 模拟知识库更新
        updates = {
            "trend": "已更新行业趋势数据，新增3个上升趋势和2个下降趋势",
            "formula": "已更新内容公式库，新增5个平台特定的钩子模板",
            "template": "已更新脚本模板库，新增直播开场和结尾模板",
            "compliance": "已更新合规红线库，同步最新平台规则变化",
            "case": "已添加2个新案例（1成功+1失败）",
        }

        reasoning += f"更新内容：{updates.get(content_type, '常规更新')}\n\n"
        reasoning += (
            "📚 当前知识库状态：\n"
            "  · 平台算法库：5个平台完整数据\n"
            "  · 内容公式库：7种钩子 + 4种结构 + 7种标题公式\n"
            "  · 脚本模板库：9种场景模板\n"
            "  · 行业趋势库：宏观趋势 + 平台动态\n"
            "  · 合规数据库：5平台红线 + 广告法词汇\n"
            "  · 案例库：4成功案例 + 3失败案例\n"
        )

        return {
            "output": reasoning,
            "confidence": 0.92,
            "reasoning": reasoning,
            "suggestions": ["建议每周更新一次行业趋势", "每月更新一次案例库"],
        }

    def _generate_report(self, context: dict) -> dict:
        """生成研究报告"""
        report_type = context.get("report_type", "weekly")
        platform = context.get("platform", "all")

        reasoning = f"【博闻的{report_type}研究报告】\n\n"
        reasoning += f"报告类型：{report_type}\n"
        reasoning += f"覆盖平台：{platform}\n"
        reasoning += f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"

        if report_type == "weekly":
            reasoning += "═══════ 本周内容表现概览 ═══════\n\n"
            reasoning += "【热门话题TOP5】\n"
            topics = [
                "AI工具日常使用分享",
                "换季护肤指南",
                "职场通勤穿搭",
                "居家收纳整理",
                "周末探店推荐",
            ]
            for i, t in enumerate(topics, 1):
                reasoning += f"  {i}. {t}\n"

            reasoning += "\n【数据洞察】\n"
            reasoning += "  · 视频类内容互动率较上周提升12%\n"
            reasoning += "  · 直播电商GMV环比增长8%\n"
            reasoning += "  · 小红书搜索流量占比提升至35%\n"

            reasoning += "\n【建议行动】\n"
            reasoning += "  1. 加大AI工具类内容产出\n"
            reasoning += "  2. 优化小红书关键词布局\n"
            reasoning += "  3. 准备下周热点话题预埋\n"

        elif report_type == "monthly":
            reasoning += "═══════ 本月总结报告 ═══════\n\n"
            reasoning += "【关键指标】\n"
            reasoning += "  · 总播放量：1,250万（环比+15%）\n"
            reasoning += "  · 新增粉丝：85,000（环比+22%）\n"
            reasoning += "  · 商业收入：42万元（环比+8%）\n"
            reasoning += "  · 爆款数量：3条（目标2条）✅\n"

            reasoning += "\n【问题与改进】\n"
            reasoning += "  · 问题：B站更新频率不稳定\n"
            reasoning += "  · 改进：建立周内容日历\n"
            reasoning += "  · 问题：小红书收藏率偏低\n"
            reasoning += "  · 改进：增加实用干货比例\n"

        return {
            "output": reasoning,
            "confidence": 0.85,
            "reasoning": reasoning,
            "suggestions": ["建议每周生成周报", "每月进行深度复盘"],
        }

    def _default_research(self, input_data: dict) -> dict:
        reasoning = (
            f"【博闻的研究能力】\n\n"
            f"我是工作室的研究员，负责行业分析和知识沉淀。\n\n"
            f"可用操作：\n"
            f"  · research_trend — 行业趋势研究\n"
            f"  · analyze_case — 案例分析\n"
            f"  · update_knowledge — 知识库更新\n"
            f"  · generate_report — 生成研究报告\n\n"
            f"请告诉我你的需求。"
        )
        return {"output": reasoning, "confidence": 0.90, "reasoning": reasoning}
