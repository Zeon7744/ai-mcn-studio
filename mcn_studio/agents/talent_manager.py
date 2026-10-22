# -*- coding: utf-8 -*-
"""
主播管理 Agent - 声优
负责主播人设打造、直播策划、粉丝运营
"""

from __future__ import annotations

import random
from datetime import datetime
from typing import Any

from agents.base_agent import AgentOutput, BaseAgent, register_agent
from core.models import AgentRole


@register_agent(AgentRole.TALENT_MANAGER)
class TalentManagerAgent(BaseAgent):
    """
    声优 - 主播管理总监
    性格：温暖有力量，善于发现每个人的独特光芒
    """

    def think(self, input_data: dict[str, Any]) -> AgentOutput:
        task_title = input_data.get("title", "")
        task_type = input_data.get("task_type", "")
        platform = input_data.get("platform", "")
        context = input_data.get("context", {})

        if task_type == "主播人设":
            response = self._design_persona(task_title, platform, context)
        elif task_type == "直播策划":
            response = self._plan_live_stream(task_title, platform, context)
        elif task_type == "粉丝运营":
            response = self._plan_fan_operation(task_title, platform, context)
        elif task_type == "成长规划":
            response = self._plan_growth(task_title, platform, context)
        else:
            response = self._default_talent_thinking(task_title, platform, context)

        output = AgentOutput(
            success=True,
            agent_id=self.config.id,
            agent_name=self.config.name,
            task_id=input_data.get("task_id", ""),
            output_type="content",
            content=self.llm_enhance(input_data, response["output"]),
            confidence=response["confidence"],
            metadata={
                "reasoning": response["reasoning"],
                "persona_tags": response.get("tags", []),
                "platform": platform,
            },
            suggestions=response.get("suggestions", []),
        )

        self.record_memory({
            "type": "talent_task",
            "content": f"完成主播管理: {task_title}",
            "result": response["reasoning"][:80],
        })

        return output

    def _design_persona(self, title, platform, context):
        """主播人设打造"""
        personality = context.get("personality", "")
        skills = context.get("skills", [])
        interests = context.get("interests", [])
        target_audience = context.get("target_audience", "")

        persona_core = self._find_persona_core(personality, skills, interests, platform)

        reasoning = (
            f"【声优的人设打造】\n\n"
            f"项目名称：{title}\n"
            f"平台：{platform}\n\n"
            f"每个人都有自己的光，我要做的是找到那个开关。\n\n"
            f"基于对个人特质「{personality}」的分析，\n"
            f"我建议的人设框架：\n\n"
            f"  🎯 核心定位：{persona_core['positioning']}\n"
            f"  💎 性格标签：{', '.join(persona_core.get("tags", ["real", "attitude", "warmth"]))}\n"
            f"  🎨 内容风格：{persona_core['style']}\n"
            f"  🗣️ 口头禅/标志：'{persona_core['signature']}'\n"
            f"  🎭 反差萌点：{persona_core['contrast']}\n\n"
            f"目标受众：{target_audience or '与该人设匹配的精准用户群'}\n"
        )

        reasoning += (
            f"\n人设构建的三步法：\n"
            f"  1. 真实：从真实性格出发，不要扮演不是自己的角色\n"
            f"  2. 放大：把最独特的特质放大10倍，成为记忆点\n"
            f"  3. 一致：所有内容围绕人设展开，不要今天A明天B\n\n"
            f"⚠️ 提醒：人设是人，不是标签。保持真实，才能长久。"
        )

        return {
            "output": reasoning,
            "confidence": 0.90,
            "reasoning": reasoning[:200],
            "tags": persona_core.get("tags", ["real", "attitude", "warmth"]),
            "suggestions": [
                "人设确定后写一份《人设白皮书》作为团队共识",
                "建议拍摄3-5条试水内容验证人设接受度",
                "定期收集粉丝反馈，微调人设细节",
            ],
        }

    def _plan_live_stream(self, title, platform, context):
        """直播策划"""
        stream_type = context.get("stream_type", "带货")
        duration = context.get("duration", 120)
        products = context.get("products", [])
        anchor_name = context.get("anchor_name", "")

        reasoning = (
            f"【声优的直播策划】\n\n"
            f"直播主题：{title}\n"
            f"主播：{anchor_name or '待定'} | 类型：{stream_type} | 时长：{duration}分钟\n\n"
            f"一场好的直播 = 好的规划 + 好的执行 + 好的应变。\n\n"
            f"直播流程设计：\n"
        )

        # 直播脚本
        schedule = self._build_live_schedule(stream_type, duration, products)
        for time_slot, activity in schedule:
            reasoning += f"  {time_slot} — {activity}\n"

        reasoning += (
            f"\n直播前准备清单：\n"
            f"  □ 设备检查（灯光/音响/网络）\n"
            f"  □ 话术熟悉（产品介绍/互动话术/促销话术）\n"
            f"  □ 货品准备（样品/库存确认/价格核对）\n"
            f"  □ 预热发布（预告视频/社群通知）\n"
            f"  □ 运营配合（场控/客服/数据监控）\n"
        )

        return {
            "output": reasoning,
            "confidence": 0.88,
            "reasoning": reasoning[:200],
            "tags": ["直播策划"],
            "suggestions": [
                "直播前30分钟做设备最终检查",
                "准备Plan B（备用网络/备用话术）",
                "直播期间运营实时监控数据",
            ],
        }

    def _plan_fan_operation(self, title, platform, context):
        """粉丝运营策略"""
        fan_count = context.get("fan_count", 0)
        fan_age_range = context.get("fan_age_range", "")
        fan_interests = context.get("fan_interests", [])

        reasoning = (
            f"【声优的粉丝运营】\n\n"
            f"项目：{title}\n"
            f"当前粉丝：{fan_count:,} | 年龄段：{fan_age_range}\n\n"
            f"粉丝不是数字，是活生生的人。\n"
            f"运营的核心是建立真正的连接。\n\n"
            f"粉丝分层运营策略：\n\n"
            f"  🔴 核心粉（Top 5%）\n"
            f"     · 专属社群运营\n"
            f"     · 提前透露内容/活动信息\n"
            f"     · 定期1对1互动\n\n"
            f"  🟡 活跃粉（Next 15%）\n"
            f"     · 高频互动回复\n"
            f"     · 引导参与社区活动\n"
            f"     · 培养为核心粉\n\n"
            f"  🟢 普通粉（Remaining 80%）\n"
            f"     · 持续内容触达\n"
            f"     · 降低互动门槛\n"
            f"     · 通过优质内容转化\n"
        )

        return {
            "output": reasoning,
            "confidence": 0.86,
            "reasoning": reasoning[:200],
            "tags": ["粉丝运营"],
            "suggestions": [
                "建立粉丝标签体系，精细化运营",
                "每周至少一次与核心粉的深度互动",
                "关注粉丝增长质量而非数量",
            ],
        }

    def _plan_growth(self, title, platform, context):
        """成长规划"""
        current_stage = context.get("current_stage", "起步期")
        goals = context.get("goals", [])

        stage_map = {
            "起步期": {"next": "成长期", "milestones": ["突破1000粉丝", "找到稳定内容方向", "建立个人风格"]},
            "成长期": {"next": "成熟期", "milestones": ["突破1万粉丝", "形成内容IP", "开启初步变现"]},
            "成熟期": {"next": "爆发期", "milestones": ["突破10万粉丝", "多元变现", "团队化运营"]},
            "爆发期": {"next": "品牌期", "milestones": ["突破100万粉丝", "品牌化运营", "行业影响力"]},
        }

        current = stage_map.get(current_stage, stage_map["起步期"])

        reasoning = (
            f"【声优的成长规划】\n\n"
            f"项目：{title}\n"
            f"当前阶段：{current_stage} → 下一阶段：{current['next']}\n\n"
            f"成长不是一蹴而就的，但每一步都算数。\n\n"
            f"当前阶段关键里程碑：\n"
        )

        for i, ms in enumerate(current["milestones"], 1):
            reasoning += f"  {i}. {ms}\n"

        if goals:
            reasoning += f"\n目标设定：\n"
            for g in goals:
                reasoning += f"  · {g}\n"

        reasoning += (
            f"\n阶段切换标准：\n"
            f"  当连续{random.choice([2, 3, 4])}周数据稳定达到下一阶段门槛时，正式进入下一阶段。\n"
            f"  阶段切换时重新评估人设和策略。"
        )

        return {
            "output": reasoning,
            "confidence": 0.84,
            "reasoning": reasoning[:200],
            "tags": ["成长规划"],
            "suggestions": [
                "设定季度目标而非月度目标，减少短期波动的影响",
                "每个阶段结束做阶段性复盘",
                "关注创作者心理健康，避免 burnout",
            ],
        }

    def _default_talent_thinking(self, title, platform, context):
        reasoning = (
            f"【声优的回应】\n\n"
            f"项目：{title}\n\n"
            f"主播管理的核心：信任 + 专业 + 关怀。\n"
            f"没有信任就没有好的合作，没有专业就无法持续输出，\n"
            f"没有关怀就无法长久陪伴。\n\n"
            f"请告诉我具体需求（人设打造/直播策划/粉丝运营/成长规划），\n"
            f"我会给出更有针对性的方案。"
        )
        return {"output": reasoning, "confidence": 0.80, "reasoning": reasoning[:200],
                "tags": [], "suggestions": ["补充具体需求"]}

    # ── 辅助方法 ──────────────────────────────────────────────────────

    def _find_persona_core(self, personality, skills, interests, platform):
        """寻找人设核心"""
        cores = {
            "热情开朗": {"positioning": "带来快乐的内容伙伴", "tags": ["阳光", "活泼", "正能量"], "style": "活泼开朗，充满能量", "signature": "哈哈！这事儿有意思！", "contrast": "外表活泼内心细腻"},
            "冷静理性": {"positioning": "帮你理清思路的分析师", "tags": ["理性", "逻辑", "专业"], "style": "理性分析，数据说话", "signature": "让我来分析一下……", "contrast": "冷静外表下的幽默感"},
            "温柔治愈": {"positioning": "温暖陪伴的内容伙伴", "tags": ["温柔", "治愈", "耐心"], "style": "温柔治愈，如沐春风", "signature": "没关系，慢慢来", "contrast": "温柔外表下的坚定态度"},
            "幽默风趣": {"positioning": "让你笑出声的内容创作者", "tags": ["幽默", "风趣", "有趣"], "style": "幽默风趣，妙语连珠", "signature": "哈哈哈等等我再说！", "contrast": "搞笑之外的认真时刻"},
        }

        default_core = {
            "positioning": "真诚有态度的内容创作者",
            "tags": ["真实", "有态度", "有温度"],
            "style": "自然真实，有个人风格",
            "signature": "我是XXX，一个……的人",
            "contrast": "反差萌：严肃外表下的有趣灵魂",
        }

        return cores.get(personality, default_core)

    def _build_live_schedule(self, stream_type, duration, products):
        """构建直播流程"""
        schedule = []
        if stream_type == "带货":
            schedule = [
                (f"0-{min(10, duration//10)}分钟", "开场热身 + 今日福利预告"),
                (f"{min(10, duration//10)}-{min(30, duration//3)}分钟", "主推产品1介绍 + 试用展示"),
                (f"{min(30, duration//3)}-{min(40, duration//2)}分钟", "互动环节 + 抽奖"),
                (f"{min(40, duration//2)}-{min(70, duration//1.5)}分钟", "主推产品2介绍 + 优惠解读"),
                (f"{min(70, duration//1.5)}-{min(90, duration-10)}分钟", "促销冲刺 + 最后福利"),
                (f"{max(90, duration-10)}-{duration}分钟", "结束语 + 预告下次直播"),
            ]
        else:
            schedule = [
                ("0-10分钟", "开场热身 + 互动"),
                (f"10-{duration-10}分钟", "主要内容环节"),
                (f"{duration-10}-{duration}分钟", "结束语 + 预告"),
            ]
        return schedule
