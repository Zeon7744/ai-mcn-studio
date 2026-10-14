# -*- coding: utf-8 -*-
"""
创意总监 Agent - 墨言
负责内容选题策划、热点追踪、IP孵化、创意方案
"""

from __future__ import annotations

import random
from datetime import datetime
from typing import Any

from agents.base_agent import AgentOutput, BaseAgent, register_agent
from core.models import AgentRole


@register_agent(AgentRole.CREATIVE_DIRECTOR)
class CreativeDirectorAgent(BaseAgent):
    """
    墨言 - 创意总监
    性格：思维敏捷，视野开阔，善用类比，追问"这个故事想告诉观众什么"
    """

    def think(self, input_data: dict[str, Any]) -> AgentOutput:
        """创意总监的思考逻辑：从需求出发，寻找最具传播力的创意角度"""
        task_title = input_data.get("title", "")
        task_type = input_data.get("task_type", "")
        platform = input_data.get("platform", "")
        context = input_data.get("context", {})

        # 创意总监的思维方式
        creative_reasoning = self._generate_creative_response(
            task_title=task_title,
            task_type=task_type,
            platform=platform,
            context=context,
        )

        output = AgentOutput(
            success=True,
            agent_id=self.config.id,
            agent_name=self.config.name,
            task_id=input_data.get("task_id", ""),
            output_type="content",
            content=creative_reasoning["output"],
            confidence=creative_reasoning["confidence"],
            metadata={
                "reasoning": creative_reasoning["reasoning"],
                "keywords": creative_reasoning.get("keywords", []),
                "platform": platform,
                "creative_angle": creative_reasoning.get("angle", ""),
            },
            suggestions=creative_reasoning.get("suggestions", []),
        )

        self.record_memory({
            "type": "creative_task",
            "content": f"完成创意策划: {task_title}",
            "result": creative_reasoning["reasoning"][:80],
        })

        return output

    def _generate_creative_response(self, task_title, task_type, platform, context):
        """根据任务类型生成创意响应"""

        # 创意角度的"数据库"
        angles_db = {
            "douyin": ["情绪共鸣型", "反差冲击型", "悬念钩子型", "实用干货型", "热点借势型"],
            "bilibili": ["深度解析型", "趣味科普型", "故事叙述型", "挑战实验型", "文化解读型"],
            "rednote": ["生活方式型", "美妆穿搭型", "探店测评型", "知识分享型", "情感治愈型"],
            "wechat_official": ["深度观点型", "行业洞察型", "故事叙述型", "实用指南型", "情感共鸣型"],
        }

        platform_angles = angles_db.get(platform, angles_db["douyin"])
        selected_angle = random.choice(platform_angles)

        # 根据任务类型生成不同内容
        if task_type == "选题策划":
            response = self._plan_topic_selection(task_title, platform, selected_angle, context)
        elif task_type == "内容策划":
            response = self._plan_content(task_title, platform, selected_angle, context)
        elif task_type == "IP定位":
            response = self._plan_ip_positioning(task_title, platform, context)
        elif task_type == "热点追踪":
            response = self._track_hot_topics(task_title, platform, context)
        else:
            response = self._default_creative_thinking(task_title, platform, selected_angle, context)

        return response

    def _plan_topic_selection(self, title, platform, angle, context):
        """选题策划思维"""
        topics = self._generate_topic_ideas(platform, angle, context)

        reasoning = (
            f"【墨言的创意思考】\n\n"
            f"接到任务：{title}\n"
            f"我首先问自己一个问题：这个选题的'魂'是什么？\n\n"
            f"经过分析，我认为最适合的传播角度是「{angle}」。\n"
            f"理由是：{self._explain_angle_choice(angle, platform)}\n\n"
            f"基于此，我提出以下{len(topics)}个具体选题方向：\n"
        )

        for i, topic in enumerate(topics, 1):
            reasoning += f"\n  {i}. 【{topic['title']}】\n"
            reasoning += f"     切入点：{topic['hook']}\n"
            reasoning += f"     预期效果：{topic['expected']}\n"

        recommendations = [
            f"优先尝试「{topics[0]['title']}」，这个角度最具传播潜力",
            "建议在脚本中强化开头3秒的钩子设计",
            "可考虑做系列化内容，增强粉丝粘性",
        ]

        return {
            "output": reasoning,
            "confidence": 0.92,
            "reasoning": reasoning[:200],
            "keywords": [t["title"] for t in topics[:3]],
            "angle": angle,
            "suggestions": recommendations,
        }

    def _plan_content(self, title, platform, angle, context):
        """内容策划思维"""
        structure = self._get_content_structure(platform)
        reasoning = (
            f"【墨言的内容策划】\n\n"
            f"针对「{title}」，我采用「{angle}」策略。\n\n"
            f"内容结构设计（{platform}平台适配）：\n"
        )

        for i, step in enumerate(structure, 1):
            reasoning += f"  {i}. {step['phase']}: {step['description']}\n"
            reasoning += f"     时间占比: {step['time']}\n"

        reasoning += "\n核心创意点："
        reasoning += self._generate_hook(platform)

        return {
            "output": reasoning,
            "confidence": 0.89,
            "reasoning": reasoning[:200],
            "keywords": [s["phase"] for s in structure],
            "angle": angle,
            "suggestions": ["建议准备3个不同开场版本进行A/B测试", "结尾引导互动是关键，不要跳过"],
        }

    def _plan_ip_positioning(self, title, platform, context):
        """IP定位思维"""
        reasoning = (
            f"【墨言的IP定位思考】\n\n"
            f"打造一个IP，我首先要回答三个问题：\n\n"
            f"1. 这个人是谁？—— 找到真实且独特的个性标签\n"
            f"2. 为什么关注他？—— 提供不可替代的价值\n"
            f"3. 凭什么记住他？—— 建立差异化的记忆点\n\n"
            f"基于「{title}」的方向，我建议的定位框架：\n\n"
            f"  · 人设核心：{self._suggest_persona_core(platform, context)}\n"
            f"  · 内容风格：{self._suggest_content_style(platform)}\n"
            f"  · 差异化标签：{self._suggest_differentiator(platform)}\n"
            f"  · 目标受众：{self._suggest_target_audience(platform)}\n\n"
            f"记住：好的IP是'做'出来的，不是'设计'出来的。\n"
            f"先找到创作者的真实特质，再围绕它构建内容体系。"
        )

        return {
            "output": reasoning,
            "confidence": 0.85,
            "reasoning": reasoning[:200],
            "keywords": ["人设", "差异化", "目标受众"],
            "angle": "IP定位",
            "suggestions": [
                "建议先做10条试水内容，根据数据反馈调整定位",
                "人设要真实，过度包装容易崩",
                "找到一个竞品差异点，然后把它放大10倍",
            ],
        }

    def _track_hot_topics(self, title, platform, context):
        """热点追踪思维"""
        reasoning = (
            f"【墨言的热点追踪报告】\n\n"
            f"针对「{title}」，我分析了当前{platform}平台的热点趋势：\n\n"
            f"  📈 热门话题趋势：\n"
            f"     1. 情感共鸣类内容持续走高\n"
            f"     2. 实用干货类内容搜索量上升\n"
            f"     3. 跨平台热点联动是新的增长机会\n\n"
            f"  💡 切入建议：\n"
            f"     不要追热点本身，要追热点背后的'情绪'。\n"
            f"     哪个热点最能引发目标受众的情感共鸣？\n"
            f"     从这个角度切入，你的内容才有独特的价值。\n\n"
            f"  ⚠️ 风险提醒：\n"
            f"     热点有时效性，建议T+1执行，避免热度消退后发布。"
        )

        return {
            "output": reasoning,
            "confidence": 0.87,
            "reasoning": reasoning[:200],
            "keywords": ["热点", "趋势", "情绪共鸣"],
            "angle": "热点追踪",
            "suggestions": ["建议24小时内完成内容产出", "关注评论区反馈，及时调整方向"],
        }

    def _default_creative_thinking(self, title, platform, angle, context):
        """默认创意思考"""
        reasoning = (
            f"【墨言的创意回应】\n\n"
            f"关于「{title}」，我从「{angle}」角度来思考：\n\n"
            f"核心观点：每一个好内容都有一个'为什么'——\n"
            f"观众为什么要看？为什么要看完？为什么要分享？\n\n"
            f"基于平台「{platform}」的生态特点，我建议：\n"
            f"1. 找到内容与目标受众的情感连接点\n"
            f"2. 用一句话概括内容的核心价值（电梯测试）\n"
            f"3. 设计一个让人忍不住分享的'高光时刻'\n\n"
            f"创意不只是灵光一现，而是有方法可循的系统工程。"
        )

        return {
            "output": reasoning,
            "confidence": 0.83,
            "reasoning": reasoning[:200],
            "keywords": [angle],
            "angle": angle,
            "suggestions": ["继续细化脚本和执行细节", "完成后交笔灵审核文案质量"],
        }

    # ── 辅助方法 ──────────────────────────────────────────────────────

    def _generate_topic_ideas(self, platform, angle, context):
        """生成选题创意"""
        templates = {
            "douyin": [
                {"title": f"{angle}类情感故事", "hook": "用真实故事引发共鸣", "expected": "高转发率"},
                {"title": f"{angle}类挑战实验", "hook": "制造悬念和期待感", "expected": "高完播率"},
                {"title": f"{angle}类知识干货", "hook": "实用价值驱动收藏", "expected": "高收藏率"},
            ],
            "bilibili": [
                {"title": f"{angle}深度解析", "hook": "满足好奇心", "expected": "高评论互动"},
                {"title": f"{angle}趣味科普", "hook": "知识娱乐化", "expected": "高转发率"},
                {"title": f"{angle}系列纪录片", "hook": "故事连载", "expected": "高粉丝增长"},
            ],
        }
        return templates.get(platform, templates["douyin"])

    def _explain_angle_choice(self, angle, platform):
        """解释角度选择理由"""
        reasons = {
            "情绪共鸣型": f"在{platform}上，情绪是传播的第一驱动力",
            "反差冲击型": f"强烈的视觉或认知反差能在前3秒抓住注意力",
            "悬念钩子型": f"悬念是最好的完播率保证器",
            "实用干货型": f"干货内容具有长尾效应，持续带来流量",
            "热点借势型": f"借势热门话题可以快速获得初始流量",
            "深度解析型": f"B站用户偏好深度内容，满足求知欲",
            "趣味科普型": f"让知识变得有趣，是最好的传播方式",
            "故事叙述型": f"好的故事跨越平台，具有普适的感染力",
            "生活方式型": f"展示理想生活状态，激发向往和认同",
            "知识分享型": f"实用价值是小红书用户的核心诉求",
        }
        return reasons.get(angle, "这个角度在当前平台上表现最佳")

    def _get_content_structure(self, platform):
        """获取平台内容结构"""
        structures = {
            "douyin": [
                {"phase": "黄金3秒", "description": "强钩子开场，制造悬念或冲突", "time": "0-3s"},
                {"phase": "核心展开", "description": "快速推进，不拖泥带水", "time": "3-45s"},
                {"phase": "高潮收尾", "description": "金句/反转/行动号召", "time": "45-60s"},
            ],
            "bilibili": [
                {"phase": "开场引入", "description": "标题党但不骗点击", "time": "0-30s"},
                {"phase": "内容展开", "description": "层层递进，信息密度高", "time": "30s-3min"},
                {"phase": "深度升华", "description": "观点提炼，引发思考", "time": "3-5min"},
                {"phase": "互动引导", "description": "三连引导+评论区话题", "time": "最后30s"},
            ],
        }
        return structures.get(platform, structures["douyin"])

    def _generate_hook(self, platform):
        """生成钩子——集成内容公式库"""
        from knowledge.content_formulas import CONTENT_FORMULAS

        hooks_db = CONTENT_FORMULAS.get("hooks", {})
        hook_names = list(hooks_db.keys())

        platform_preferred = {
            "douyin": ["反常识钩子", "悬念钩子", "利益钩子", "情绪钩子"],
            "bilibili": ["反常识钩子", "提问钩子", "冲突钩子"],
            "xiaohongshu": ["利益钩子", "共鸣钩子", "反常识钩子"],
            "kuaishou": ["利益钩子", "共鸣钩子", "情绪钩子"],
        }
        preferred = platform_preferred.get(platform, hook_names)
        selected = random.choice(preferred if preferred else hook_names)
        hook = hooks_db.get(selected, {})

        hook_formula = hook.get("formula", "N/A")
        hook_example = hook.get("example", "N/A")
        hook_for = ", ".join(hook.get("best_for", []))

        reasoning = (
            "【钩子生成（基于内容公式库）】\n"
            f"选择公式：{selected}\n"
            f"公式结构：{hook_formula}\n"
            f"适用场景：{hook_for}\n"
            f"参考示例：{hook_example}\n"
        )
        return reasoning


    def _generate_hook(self, platform):
        """生成钩子——集成内容公式库"""
        from knowledge.content_formulas import CONTENT_FORMULAS

        hooks_db = CONTENT_FORMULAS.get("hooks", {})
        hook_names = list(hooks_db.keys())

        platform_preferred = {
            "douyin": ["反常识钩子", "悬念钩子", "利益钩子", "情绪钩子"],
            "bilibili": ["反常识钩子", "提问钩子", "冲突钩子"],
            "xiaohongshu": ["利益钩子", "共鸣钩子", "反常识钩子"],
            "kuaishou": ["利益钩子", "共鸣钩子", "情绪钩子"],
        }
        preferred = platform_preferred.get(platform, hook_names)
        selected = random.choice(preferred if preferred else hook_names)
        hook = hooks_db.get(selected, {})

        hook_formula = hook.get("formula", "N/A")
        hook_example = hook.get("example", "N/A")
        hook_for = ", ".join(hook.get("best_for", []))

        reasoning = (
            "【钩子生成（基于内容公式库）】" + "\n"
            f"选择公式：{selected}" + "\n"
            f"公式结构：{hook_formula}" + "\n"
            f"适用场景：{hook_for}" + "\n"
            f"参考示例：{hook_example}" + "\n"
        )
        return reasoning

    def _suggest_persona_core(self, platform, context):
        cores = {
            "douyin": "真诚但有态度的内容创作者",
            "bilibili": "有深度但不说教的UP主",
            "rednote": "热爱生活、善于发现的分享者",
        }
        return cores.get(platform, "有独特视角的内容创作者")

    def _suggest_content_style(self, platform):
        styles = {
            "douyin": "快节奏、强节奏感、情绪化",
            "bilibili": "有梗有料、节奏适中、深度与趣味并重",
            "rednote": "精致、真实、生活化",
        }
        return styles.get(platform, "自然真实、有个人风格")

    def _suggest_differentiator(self, platform):
        diff = {
            "douyin": "找到你与其他同类账号最不一样的一个点，然后把它做到极致",
            "bilibili": "你的观点深度或独特视角，就是你的护城河",
            "rednote": "你的生活方式本身就是最好的差异化",
        }
        return diff.get(platform, "人无我有，人有我优")

    def _suggest_target_audience(self, platform):
        audiences = {
            "douyin": "18-35岁，追求新鲜感和情绪价值的用户",
            "bilibili": "16-30岁，有求知欲和表达欲的年轻群体",
            "rednote": "18-35岁，追求品质和生活方式的女性为主",
        }
        return audiences.get(platform, "追求优质内容的年轻用户群体")
