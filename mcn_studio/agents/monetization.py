# -*- coding: utf-8 -*-
"""
商业变现 Agent - 利达
负责商务对接、带货选品、变现方案设计
"""

from __future__ import annotations

import random
from datetime import datetime
from typing import Any

from agents.base_agent import AgentOutput, BaseAgent, register_agent
from core.models import AgentRole


@register_agent(AgentRole.MONETIZATION)
class MonetizationAgent(BaseAgent):
    """
    利达 - 商业变现总监
    性格：精明但不市侩，追求双赢，理解商业的本质是价值交换
    """

    def think(self, input_data: dict[str, Any]) -> AgentOutput:
        task_title = input_data.get("title", "")
        task_type = input_data.get("task_type", "")
        platform = input_data.get("platform", "")
        context = input_data.get("context", {})

        if task_type == "商务对接":
            response = self._handle_business_deal(task_title, platform, context)
        elif task_type == "选品策略":
            response = self._plan_product_selection(task_title, platform, context)
        elif task_type == "变现方案":
            response = self._design_monetization_plan(task_title, platform, context)
        elif task_type == "报价方案":
            response = self._create_pricing_plan(task_title, platform, context)
        else:
            response = self._default_monetization_thinking(task_title, platform, context)

        output = AgentOutput(
            success=True,
            agent_id=self.config.id,
            agent_name=self.config.name,
            task_id=input_data.get("task_id", ""),
            output_type="decision",
            content=self.llm_enhance(input_data, response["output"]),
            confidence=response["confidence"],
            metadata={
                "reasoning": response["reasoning"],
                "revenue_estimate": response.get("revenue_estimate", 0),
                "platform": platform,
            },
            suggestions=response.get("suggestions", []),
        )

        self.record_memory({
            "type": "monetization_task",
            "content": f"完成商业化: {task_title}",
            "result": response["reasoning"][:80],
        })

        return output

    def _handle_business_deal(self, title, platform, context):
        """商务对接"""
        brand = context.get("brand", "")
        budget = context.get("budget", 0)
        requirements = context.get("requirements", [])
        match_score = context.get("match_score", 70)

        reasoning = (
            f"【利达的商务对接】\n\n"
            f"合作方：{brand}\n"
            f"预算：{budget:,}元\n"
            f"匹配度：{match_score}%\n\n"
            f"好的商业合作让大家都舒服，不好的才会撕破脸。\n\n"
        )

        if match_score >= 80:
            reasoning += "  ✅ 高度匹配！品牌调性与我们账号人设契合度高，建议积极推进。\n\n"
        elif match_score >= 60:
            reasoning += "  ⚠️ 中等匹配。存在一些不确定性，建议进一步沟通确认。\n\n"
        else:
            reasoning += "  ❌ 匹配度较低。建议谨慎评估，避免伤害账号人设。\n\n"

        reasoning += "  需求拆解：\n"
        for i, req in enumerate(requirements, 1):
            reasoning += f"    {i}. {req}\n"

        reasoning += (
            f"\n商务谈判要点：\n"
            f"  1. 明确交付标准和时间节点\n"
            f"  2. 确认修改次数上限（建议不超过2次）\n"
            f"  3. 明确数据考核指标\n"
            f"  4. 约定付款周期和方式\n"
            f"  5. 确认知识产权归属"
        )

        return {
            "output": reasoning,
            "confidence": 0.88,
            "reasoning": reasoning[:200],
            "revenue_estimate": budget,
            "suggestions": [
                "签约前务必让镜鉴审核合同条款",
                "保留所有沟通记录，避免后续争议",
                "建立品牌方档案，长期维护关系",
            ],
        }

    def _plan_product_selection(self, title, platform, context):
        """选品策略"""
        category = context.get("category", "")
        target_price = context.get("price_range", "")
        audience = context.get("audience", "")

        reasoning = (
            f"【利达的选品策略】\n\n"
            f"类目：{category}\n"
            f"价格带：{target_price}\n"
            f"目标受众：{audience}\n\n"
            f"选品不是选最贵的，是选最合适的。\n"
            f"好的选品 = 好产品 + 好价格 + 好故事。\n\n"
            f"选品评估维度：\n\n"
            f"  📦 产品力（40%）\n"
            f"     · 产品质量是否有保障\n"
            f"     · 是否有独特卖点\n"
            f"     · 供应链是否稳定\n\n"
            f"  💰 价格力（30%）\n"
            f"     · 价格是否有竞争力\n"
            f"     · 佣金比例是否合理\n"
            f"     · 是否有独家优惠\n\n"
            f"  📖 故事力（30%）\n"
            f"     · 是否有讲述空间\n"
            f"     · 是否符合人设调性\n"
            f"     · 用户是否有购买冲动\n"
        )

        return {
            "output": reasoning,
            "confidence": 0.86,
            "reasoning": reasoning[:200],
            "revenue_estimate": 0,
            "suggestions": [
                "先买样品亲自体验再推荐",
                "建立选品数据库，追踪转化率",
                "与供应商建立长期稳定合作",
            ],
        }

    def _design_monetization_plan(self, title, platform, context):
        """变现方案设计"""
        current_revenue = context.get("current_revenue", 0)
        target_revenue = context.get("target_revenue", 0)
        follower_count = context.get("follower_count", 0)

        reasoning = (
            f"【利达的变现方案】\n\n"
            f"项目：{title}\n"
            f"当前月收入：{current_revenue:,}元 → 目标：{target_revenue:,}元\n"
            f"粉丝量：{follower_count:,}\n\n"
            f"变现是价值交换的结果，不是目的本身。\n"
            f"先把内容做好，变现自然水到渠成。\n\n"
            f"多元化变现路径：\n\n"
        )

        revenue_streams = [
            ("广告合作", self._calc_ad_revenue(follower_count, platform), "稳定收入来源，品牌合作为主"),
            ("直播带货", self._calc_live_revenue(follower_count, platform), "爆发力强，但波动较大"),
            ("知识付费", self._calc_knowledge_revenue(follower_count), "长期价值高，边际成本低"),
            ("电商带货", self._calc_ecommerce_revenue(follower_count, platform), "与内容深度结合"),
            ("私域变现", self._calc_private_revenue(follower_count), "高粘性用户的深度运营"),
        ]

        total_projected = 0
        for name, estimate, description in revenue_streams:
            total_projected += estimate
            bar = "█" * min(10, estimate // 1000 + 1) if estimate > 0 else "░" * 10
            reasoning += f"  {bar} {name}: 预估 {estimate:,}元/月\n"
            reasoning += f"      {description}\n\n"

        reasoning += (
            f"💰 预估总月收入：{total_projected:,}元\n"
            f"📊 收入健康度：{'多元化 ✅' if len([r for r in revenue_streams if r[1] > 0]) >= 3 else '集中风险 ⚠️'}\n\n"
            f"建议优先发展2-3个变现渠道，避免单一依赖。"
        )

        return {
            "output": reasoning,
            "confidence": 0.84,
            "reasoning": reasoning[:200],
            "revenue_estimate": total_projected,
            "suggestions": [
                "广告收入作为基础盘，保持稳定增长",
                "直播带货作为爆发点，定期举办",
                "知识付费作为长期资产，持续积累",
            ],
        }

    def _create_pricing_plan(self, title, platform, context):
        """报价方案"""
        metrics = context.get("metrics", {})
        avg_views = metrics.get("avg_views", 0)
        engagement_rate = metrics.get("engagement_rate", 0)
        follower_count = metrics.get("followers", 0)

        # 报价计算逻辑
        base_price = avg_views * 0.5  # 按均播计算
        engagement_bonus = engagement_rate * 100  # 互动率加成
        follower_bonus = follower_count * 0.1  # 粉丝基数加成
        platform_premium = {"douyin": 1.2, "bilibili": 1.3, "rednote": 1.1}.get(platform, 1.0)

        package_price = int((base_price + engagement_bonus + follower_bonus) * platform_premium)
        package_price = max(package_price, 5000)  # 最低报价底线

        reasoning = (
            f"【利达的报价方案】\n\n"
            f"项目：{title}\n"
            f"平台：{platform}\n\n"
            f"报价的依据是数据，不是感觉。\n\n"
            f"账号数据参考：\n"
            f"  · 粉丝数：{follower_count:,}\n"
            f"  · 均播：{avg_views:,}\n"
            f"  · 互动率：{engagement_rate:.2f}%\n\n"
            f"报价方案：\n\n"
            f"  📦 基础包（{package_price:,}元）\n"
            f"     · 单条内容定制\n"
            f"     · 包含脚本+拍摄指导+发布\n"
            f"     · 数据报告\n\n"
            f"  📦 进阶包（{int(package_price * 2.5):,}元）\n"
            f"     · 3条内容定制\n"
            f"     · 专属创意方案\n"
            f"     · 发布后数据追踪\n\n"
            f"  📦 年度合作（{int(package_price * 8):,}元）\n"
            f"     · 全年内容合作\n"
            f"     · 优先档期保障\n"
            f"     · 年度数据复盘\n\n"
            f"💡 报价原则：有底线但不虚高，让品牌方觉得值，让我们觉得赚。"
        )

        return {
            "output": reasoning,
            "confidence": 0.87,
            "reasoning": reasoning[:200],
            "revenue_estimate": package_price,
            "suggestions": [
                "报价时要预留议价空间",
                "首单可以适当优惠，建立长期合作",
                "报价单要专业规范，体现品牌价值",
            ],
        }

    def _default_monetization_thinking(self, title, platform, context):
        reasoning = (
            f"【利达的回应】\n\n"
            f"项目：{title}\n\n"
            f"商业的本质是价值交换。\n"
            f"我们提供内容和影响力，品牌提供预算和资源。\n"
            f"好的合作让双方都觉得值，这是长期主义的根基。\n\n"
            f"请告诉我具体需求（商务对接/选品策略/变现方案/报价方案），\n"
            f"我会给出更精准的方案。"
        )
        return {"output": reasoning, "confidence": 0.80, "reasoning": reasoning[:200],
                "revenue_estimate": 0, "suggestions": ["补充具体需求"]}

    # ── 辅助方法 ──────────────────────────────────────────────────────

    def _calc_ad_revenue(self, followers, platform):
        rates = {"douyin": 0.5, "bilibili": 0.8, "rednote": 0.6}
        return int(followers * rates.get(platform, 0.5) * 0.1)

    def _calc_live_revenue(self, followers, platform):
        rates = {"douyin": 2.0, "bilibili": 1.5, "rednote": 1.0}
        return int(followers * rates.get(platform, 1.5) * 0.05)

    def _calc_knowledge_revenue(self, followers):
        return int(followers * 0.02)

    def _calc_ecommerce_revenue(self, followers, platform):
        rates = {"douyin": 3.0, "bilibili": 2.0, "rednote": 2.5}
        return int(followers * rates.get(platform, 2.0) * 0.03)

    def _calc_private_revenue(self, followers):
        return int(followers * 0.01)
