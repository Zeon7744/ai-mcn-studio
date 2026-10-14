# -*- coding: utf-8 -*-
"""
运营策略 Agent - 数策
负责数据分析、流量策略、发布优化
"""

from __future__ import annotations

import random
from datetime import datetime
from typing import Any

from agents.base_agent import AgentOutput, BaseAgent, register_agent
from core.models import AgentRole
from knowledge.platform_algorithms import PLATFORM_ALGORITHMS


@register_agent(AgentRole.OPERATIONS_STRATEGY)
class OperationsStrategyAgent(BaseAgent):
    """
    数策 - 运营策略总监
    性格：理性数据驱动，用数据说话，A/B测试代替争论
    """

    def think(self, input_data: dict[str, Any]) -> AgentOutput:
        task_title = input_data.get("title", "")
        task_type = input_data.get("task_type", "")
        platform = input_data.get("platform", "")
        context = input_data.get("context", {})
        data_input = input_data.get("data", {})

        if task_type == "数据分析":
            response = self._analyze_data(task_title, platform, context, data_input)
        elif task_type == "发布策略":
            response = self._plan_publishing(task_title, platform, context, data_input)
        elif task_type == "流量策略":
            response = self._plan_traffic(task_title, platform, context, data_input)
        elif task_type == "竞品分析":
            response = self._analyze_competitors(task_title, platform, context, data_input)
        elif task_type == "复盘报告":
            response = self._generate_review_report(task_title, platform, context, data_input)
        else:
            response = self._default_operations_thinking(task_title, platform, context, data_input)

        output = AgentOutput(
            success=True,
            agent_id=self.config.id,
            agent_name=self.config.name,
            task_id=input_data.get("task_id", ""),
            output_type="analysis",
            content=response["output"],
            confidence=response["confidence"],
            metadata={
                "reasoning": response["reasoning"],
                "key_metrics": response.get("metrics", {}),
                "recommendations": response.get("recommendations", []),
                "platform": platform,
            },
            suggestions=response.get("suggestions", []),
        )

        self.record_memory({
            "type": "operations_task",
            "content": f"完成运营分析: {task_title}",
            "result": response["reasoning"][:80],
        })

        return output

    def _analyze_data(self, title, platform, context, data_input):
        """数据分析"""
        metrics = data_input.get("metrics", {})
        views = metrics.get("views", 0)
        likes = metrics.get("likes", 0)
        comments = metrics.get("comments", 0)
        shares = metrics.get("shares", 0)
        follow_increase = metrics.get("follow_increase", 0)
        watch_time_avg = metrics.get("watch_time_avg", 0)

        # 计算核心指标
        engagement_rate = (likes + comments + shares) / max(views, 1) * 100
        follow_rate = follow_increase / max(views, 1) * 100

        reasoning = (
            f"【数策的数据分析】\n\n"
            f"分析对象：{title}\n"
            f"平台：{platform}\n"
            f"数据来源：{datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
            f"数据不说谎，但需要正确解读。\n\n"
            f"核心指标概览：\n"
            f"  · 播放量：{views:,} {'📈' if views > 10000 else '📊'}\n"
            f"  · 点赞：{likes:,} | 评论：{comments:,} | 分享：{shares:,}\n"
            f"  · 互动率：{engagement_rate:.2f}% {'✅优秀' if engagement_rate > 5 else '⚠️偏低' if engagement_rate > 2 else '❌需优化'}\n"
            f"  · 涨粉数：{follow_increase:,} | 涨粉率：{follow_rate:.2f}%\n"
            f"  · 平均观看时长：{watch_time_avg:.1f}秒"
        )

        # 诊断分析
        diagnosis = self._diagnose_performance(engagement_rate, follow_rate, watch_time_avg, platform)
        reasoning += f"\n\n{diagnosis}"

        recommendations = self._generate_recommendations(engagement_rate, follow_rate, watch_time_avg, platform)
        reasoning += f"\n\n核心建议：\n"
        for i, rec in enumerate(recommendations, 1):
            reasoning += f"  {i}. {rec}\n"

        return {
            "output": reasoning,
            "confidence": 0.91,
            "reasoning": reasoning[:200],
            "metrics": {
                "engagement_rate": round(engagement_rate, 2),
                "follow_rate": round(follow_rate, 2),
                "views": views,
                "benchmark": self._get_benchmark(platform),
            },
            "recommendations": recommendations,
            "suggestions": ["建议持续追踪3-7天数据趋势", "可与同类型账号数据进行横向对比"],
        }

    def _plan_publishing(self, title, platform, context, data_input):
        """发布策略制定"""
        target_audience = context.get("target_audience", "")
        content_type = context.get("content_type", "")

        peak_hours = self._get_peak_hours(platform)

        reasoning = (
            f"【数策的发布策略】\n\n"
            f"项目：{title}\n"
            f"平台：{platform} | 受众：{target_audience}\n\n"
            f"发布时间本质上是'在正确的时间出现在正确的地方'。\n\n"
            f"建议发布时间：\n"
        )

        for hour, reason in peak_hours:
            reasoning += f"  · {hour}:00 — {reason}\n"

        reasoning += f"""
推广策略：
  · 发布后1小时内：密切关注数据反馈
  · 发布后2小时：如数据低于预期，启动付费推广
  · 发布后24小时：根据数据表现决定是否追加投放

发布前检查清单：
  □ 标题经过A/B测试验证
  □ 封面在缩略图尺寸下清晰可读
  □ 话题标签选择3-5个精准标签
  □ 简介包含核心关键词
  □ 首条评论预埋互动话题
"""

        return {
            "output": reasoning,
            "confidence": 0.88,
            "reasoning": reasoning[:200],
            "metrics": {"peak_hours": peak_hours[:3]},
            "recommendations": ["建议固定发布时间形成用户期待", "周末与工作日的发布策略应有所区别"],
            "suggestions": ["发布后1小时内不要移动或编辑内容", "关注评论区前30分钟的用户反馈"],
        }

    def _plan_traffic(self, title, platform, context, data_input):
        """流量策略"""
        current_followers = context.get("followers", 0)
        budget = context.get("budget", 0)

        strategies = self._get_traffic_strategies(platform, current_followers)

        reasoning = (
            f"【数策的流量策略】\n\n"
            f"项目：{title}\n"
            f"当前粉丝：{current_followers:,} | 推广预算：{budget:,}元\n\n"
            f"流量的本质：算法认为你的内容值得推荐。\n"
            f"我们要做的，就是证明这一点。\n\n"
            f"策略矩阵：\n"
        )

        for name, description, expected_roi in strategies:
            reasoning += f"  📌 {name}\n"
            reasoning += f"     {description}\n"
            reasoning += f"     预期ROI：{expected_roi}\n\n"

        if budget > 0:
            reasoning += f"预算分配建议：\n"
            reasoning += f"  · 40% — 内容加热（投流到优质内容）\n"
            reasoning += f"  · 30% — 粉丝增长（投流到吸粉内容）\n"
            reasoning += f"  · 20% — 互动提升（投流到互动内容）\n"
            reasoning += f"  · 10% — 实验性投放（测试新方向）\n"

        return {
            "output": reasoning,
            "confidence": 0.85,
            "reasoning": reasoning[:200],
            "metrics": {"budget_allocation": "40/30/20/10"},
            "recommendations": strategies[:3],
            "suggestions": ["小预算多测试，找到最优投放组合后再放大", "关注ROI而非单纯播放量"],
        }

    def _analyze_competitors(self, title, platform, context, data_input):
        """竞品分析"""
        competitors = context.get("competitors", [])

        reasoning = (
            f"【数策的竞品分析】\n\n"
            f"分析对象：{title}\n"
            f"平台：{platform}\n\n"
            f"了解对手，不是为了模仿，而是为了找到差异化的突破口。\n\n"
            f"竞品监测结果：\n"
        )

        for comp in competitors[:5]:
            name = comp.get("name", "未知账号")
            followers = comp.get("followers", 0)
            avg_views = comp.get("avg_views", 0)
            strength = comp.get("strength", "")
            weakness = comp.get("weakness", "")

            reasoning += f"\n  📊 {name}\n"
            reasoning += f"     粉丝：{followers:,} | 均播：{avg_views:,}\n"
            reasoning += f"     优势：{strength}\n"
            reasoning += f"     劣势：{weakness}\n"
            reasoning += f"     可借鉴点：{comp.get('learnings', '')}\n"

        reasoning += (
            f"\n💡 差异化机会：\n"
            f"  1. 找到竞品覆盖不到的细分领域\n"
            f"  2. 用竞品不擅长的表达方式切入\n"
            f"  3. 在竞品薄弱的用户群中寻找机会"
        )

        return {
            "output": reasoning,
            "confidence": 0.83,
            "reasoning": reasoning[:200],
            "metrics": {"competitors_analyzed": len(competitors)},
            "recommendations": ["持续监测竞品动态，每周更新分析", "找出1-2个差异化方向并坚持执行"],
            "suggestions": ["关注竞品的评论区，了解用户真实需求"],
        }

    def _generate_review_report(self, title, platform, context, data_input):
        """复盘报告"""
        period = context.get("period", "本周")
        tasks_completed = context.get("tasks_completed", 0)
        kpis_achieved = context.get("kpis_achieved", 0)
        total_kpis = context.get("total_kpis", 0)

        reasoning = (
            f"【数策的复盘报告】\n\n"
            f"复盘周期：{period}\n"
            f"项目：{title}\n\n"
            f"复盘不是走过场，是下一次进步的基础。\n\n"
            f"一、目标回顾\n"
            f"  · 计划目标：{total_kpis}项KPI\n"
            f"  · 实际达成：{kpis_achieved}项\n"
            f"  · 达成率：{kpis_achieved/total_kpis*100:.1f}% {'✅达标' if kpis_achieved/total_kpis >= 0.8 else '⚠️未达标'}\n\n"
            f"二、执行概况\n"
            f"  · 完成任务：{tasks_completed}项\n"
            f"  · 延期任务：{max(0, tasks_completed - kpis_achieved)}项\n\n"
            f"三、关键发现\n"
        )

        insights = self._generate_insights(data_input)
        for i, insight in enumerate(insights, 1):
            reasoning += f"  {i}. {insight}\n"

        reasoning += (
            f"\n四、下一步行动\n"
            f"  1. 复制成功经验到下一个项目\n"
            f"  2. 针对未达标项制定改进计划\n"
            f"  3. 更新运营策略库"
        )

        return {
            "output": reasoning,
            "confidence": 0.87,
            "reasoning": reasoning[:200],
            "metrics": {"achievement_rate": f"{kpis_achieved/total_kpis*100:.1f}%", "tasks": tasks_completed},
            "recommendations": insights,
            "suggestions": ["复盘会议邀请全体成员参加", "记录经验教训到知识库"],
        }

    def _default_operations_thinking(self, title, platform, context, data_input):
        reasoning = (
            f"【数策的运营回应】\n\n"
            f"任务：{title}\n\n"
            f"数据驱动的核心：假设 → 验证 → 迭代。\n"
            f"每一次决策都应该是一个可验证的假设。\n\n"
            f"请告诉我具体分析需求（数据解读/发布策略/竞品分析/复盘），\n"
            f"我会给出针对性的运营方案。"
        )
        return {"output": reasoning, "confidence": 0.80, "reasoning": reasoning[:200],
                "metrics": {}, "recommendations": [], "suggestions": ["补充具体需求"]}

    # ── 辅助方法 ──────────────────────────────────────────────────────

    def _diagnose_performance(self, engagement_rate, follow_rate, watch_time, platform):
        """性能诊断"""
        issues = []
        strengths = []

        benchmarks = self._get_benchmark(platform)

        if engagement_rate < benchmarks.get("engagement_low", 2):
            issues.append("互动率偏低，建议优化开头钩子和结尾引导")
        elif engagement_rate >= benchmarks.get("engagement_good", 5):
            strengths.append(f"互动率{engagement_rate:.2f}%表现优秀")

        if follow_rate < benchmarks.get("follow_low", 0.5):
            issues.append("涨粉率偏低，内容吸粉能力待提升")
        else:
            strengths.append(f"涨粉率{follow_rate:.2f}%正常")

        if watch_time < benchmarks.get("watchtime_low", 15):
            issues.append(f"平均观看时长{watch_time:.1f}秒偏短，检查内容节奏")
        else:
            strengths.append(f"平均观看时长{watch_time:.1f}秒良好")

        result = "📊 性能诊断：\n"
        for s in strengths:
            result += f"  ✅ {s}\n"
        for issue in issues:
            result += f"  ⚠️ {issue}\n"

        return result

    def _generate_recommendations(self, engagement_rate, follow_rate, watch_time, platform):
        recs = []
        if engagement_rate < 3:
            recs.append("优化视频开头3秒，提高开场吸引力")
        if follow_rate < 1:
            recs.append("在视频结尾增加明确的关注引导")
        if watch_time < 20:
            recs.append("检查内容节奏，删除冗余片段")
        if not recs:
            recs.append("当前表现良好，继续保持当前策略")
            recs.append("可尝试加大推广力度进一步扩大影响")
        return recs

    def _get_peak_hours(self, platform):
        hours = {
            "douyin": [
                ("7:00", "早高峰通勤时段，用户刷手机高峰期"),
                ("12:00", "午休时段，浏览意愿强"),
                ("18:00", "下班高峰，放松浏览时间"),
                ("21:00", "黄金时段，用户活跃峰值"),
                ("23:00", "睡前时段，短视频消费高峰"),
            ],
            "bilibili": [
                ("12:00", "午休浏览"),
                ("18:00", "放学/下班后"),
                ("21:00", "黄金时段"),
                ("23:00", "深夜党活跃"),
            ],
            "rednote": [
                ("8:00", "通勤时段"),
                ("12:00", "午休浏览"),
                ("19:00", "晚间活跃"),
                ("22:00", "睡前浏览高峰"),
            ],
        }
        return hours.get(platform, hours["douyin"])

    def _get_traffic_strategies(self, platform, followers):
        strategies = []
        if followers < 1000:
            strategies.append(("冷启动扶持", "利用平台新号扶持期，加大内容产出频率", "低"))
            strategies.append(("社群扩散", "通过私域流量启动第一波传播", "中"))
        elif followers < 10000:
            strategies.append(("内容加热", "对优质内容进行付费推广，放大传播", "中"))
            strategies.append(("互推合作", "与同量级账号互推，交叉引流", "中高"))
        else:
            strategies.append(("精准投流", "基于用户画像精准投放", "高"))
            strategies.append(("矩阵联动", "多账号联动，形成流量矩阵", "高"))
        strategies.append(("热点借势", "结合平台热点话题，获得免费流量", "中"))
        return strategies

    def _get_benchmark(self, platform):
        benchmarks = {
            "douyin": {"engagement_low": 2, "engagement_good": 5, "follow_low": 0.5, "watchtime_low": 15},
            "bilibili": {"engagement_low": 3, "engagement_good": 8, "follow_low": 1, "watchtime_low": 120},
            "rednote": {"engagement_low": 4, "engagement_good": 8, "follow_low": 1, "watchtime_low": 30},
        }
        return benchmarks.get(platform, benchmarks["douyin"])

    def _generate_insights(self, data_input):
        """生成复盘洞察"""
        insights = []
        if data_input:
            top_performer = data_input.get("top_content", "")
            if top_performer:
                insights.append(f"表现最佳内容：「{top_performer}」，其共同特征是{data_input.get('top_content_traits', '强情绪+实用价值')}")
            worst_performer = data_input.get("worst_content", "")
            if worst_performer:
                insights.append(f"表现最差内容：「{worst_performer}」，主要问题：{data_input.get('worst_content_issues', '节奏拖沓')}")
        if not insights:
            insights.append("整体数据稳定，建议深入分析用户留存趋势")
            insights.append("关注长期价值指标（LTV），而非短期流量")
        return insights
