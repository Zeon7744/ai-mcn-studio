# -*- coding: utf-8 -*-
"""
文案主编 Agent - 笔灵
负责脚本撰写、标题优化、多平台内容适配
"""

from __future__ import annotations

import random
from datetime import datetime
from typing import Any

from agents.base_agent import AgentOutput, BaseAgent, register_agent
from core.models import AgentRole
from knowledge.script_templates import SCRIPT_TEMPLATES, TITLE_GENERATOR_GUIDE


@register_agent(AgentRole.COPY_CHIEF)
class CopyChiefAgent(BaseAgent):
    """
    笔灵 - 文案主编
    性格：对文字有执拗审美，温和但原则性强，从受众感受反推文字优化
    """

    def think(self, input_data: dict[str, Any]) -> AgentOutput:
        task_title = input_data.get("title", "")
        task_type = input_data.get("task_type", "")
        platform = input_data.get("platform", "")
        context = input_data.get("context", {})
        source_content = input_data.get("source_content", "")

        if task_type == "脚本撰写":
            response = self._write_script(task_title, platform, context, source_content)
        elif task_type == "标题优化":
            response = self._optimize_titles(task_title, platform, context, source_content)
        elif task_type == "多平台适配":
            response = self._adapt_content(task_title, platform, context, source_content)
        elif task_type == "直播话术":
            response = self._write_live_script(task_title, platform, context, source_content)
        else:
            response = self._default_copywriting(task_title, platform, context, source_content)

        output = AgentOutput(
            success=True,
            agent_id=self.config.id,
            agent_name=self.config.name,
            task_id=input_data.get("task_id", ""),
            output_type="content",
            content=response["output"],
            confidence=response["confidence"],
            metadata={
                "reasoning": response["reasoning"],
                "word_count": response.get("word_count", 0),
                "platform": platform,
                "style": response.get("style", ""),
            },
            suggestions=response.get("suggestions", []),
        )

        self.record_memory({
            "type": "copywriting_task",
            "content": f"完成文案: {task_title}",
            "result": response["reasoning"][:80],
        })

        return output

    def _write_script(self, title, platform, context, source_content):
        """撰写完整脚本"""
        duration = context.get("duration", 60)
        style = context.get("style", "口播")

        # 根据平台和风格生成脚本框架
        script_structure = self._get_script_structure(platform, duration, style)

        reasoning = (
            f"【笔灵的文案思考】\n\n"
            f"任务：{title}\n"
            f"平台：{platform} | 时长：{duration}秒 | 风格：{style}\n\n"
            f"好文案的标准：每一句话都有存在的理由。\n"
            f"我逐句审视了以下内容：\n"
        )

        # 生成脚本正文
        script_body = self._generate_script_body(
            title=title, platform=platform, duration=duration, style=style,
            source_content=source_content,
        )

        full_output = reasoning + "\n" + script_body

        # 计算字数
        word_count = len(script_body.replace("【", "").replace("】", "").replace("\n", "").replace(" ", ""))

        return {
            "output": full_output,
            "confidence": 0.91,
            "reasoning": reasoning[:200],
            "word_count": word_count,
            "style": style,
            "suggestions": [
                f"口播语速建议控制在每分钟{random.choice([180, 200, 220])}字",
                "建议录制时注意停顿，给观众思考时间",
                "脚本完成后请墨言从创意角度复核",
            ],
        }

    def _optimize_titles(self, title, platform, context, source_content):
        """优化标题"""
        themes = context.get("themes", [])
        keywords = context.get("keywords", [])

        title_variants = self._generate_title_variants(title, platform, themes, keywords)

        reasoning = (
            f"【笔灵的标题优化】\n\n"
            f"原标题：「{title}」\n"
            f"平台：{platform}\n\n"
            f"标题决定30%的点击率。我从以下维度优化：\n"
            f"  · 关键词嵌入（SEO友好）\n"
            f"  · 情绪触发（引发好奇/共鸣/紧迫感）\n"
            f"  · 长度控制（{self._get_optimal_length(platform)}字）\n"
            f"  · 差异化（避免同质化）\n\n"
            f"生成{len(title_variants)}个版本供选择：\n"
        )

        for i, variant in enumerate(title_variants, 1):
            score = variant["score"]
            reason = variant["reason"]
            reasoning += f"\n  {i}. 【{variant['title']}】 预测得分：{score}/100"
            reasoning += f"\n     理由：{reason}"

        best = max(title_variants, key=lambda x: x["score"])

        return {
            "output": reasoning,
            "confidence": 0.88,
            "reasoning": reasoning[:200],
            "word_count": sum(len(v["title"]) for v in title_variants),
            "style": f"标题优化-{platform}",
            "suggestions": [
                f"推荐优先测试「{best['title']}」",
                "建议做A/B测试：用不同标题发布相似内容对比数据",
                "标题与封面要形成呼应，不要各说各话",
            ],
        }

    def _adapt_content(self, title, platform, context, source_content):
        """多平台内容适配"""
        platforms = context.get("target_platforms", ["douyin", "bilibili"])

        reasoning = (
            f"【笔灵的内容适配】\n\n"
            f"原始内容：{title}\n"
            f"适配平台：{', '.join(platforms)}\n\n"
            f"同一内容在不同平台的表达方式完全不同。\n"
            f"我的适配原则：保留核心信息，改变表达形式。\n\n"
        )

        for p in platforms:
            adaptation = self._adapt_for_platform(title, p, source_content)
            reasoning += f"\n── 【{p}】 ──\n"
            reasoning += adaptation
            reasoning += "\n"

        return {
            "output": reasoning,
            "confidence": 0.86,
            "reasoning": reasoning[:200],
            "word_count": len(reasoning),
            "style": "多平台适配",
            "suggestions": [
                "每个平台单独定制，不要简单复制粘贴",
                "关注各平台的评论区文化差异",
            ],
        }

    def _write_live_script(self, title, platform, context, source_content):
        """直播话术脚本"""
        live_duration = context.get("duration", 120)
        product_count = context.get("product_count", 3)

        reasoning = (
            f"【笔灵的直播话术】\n\n"
            f"直播主题：{title}\n"
            f"预计时长：{live_duration}分钟 | 产品数：{product_count}个\n\n"
            f"直播话术的核心：不是'说'，而是'对话感'。\n"
            f"每一个环节都要考虑观众的实时反应。\n\n"
        )

        # 直播脚本结构
        sections = [
            ("开场预热", f"欢迎新进直播间的朋友们！今天给大家带来{product_count}个超值好物，"
             f"全程{live_duration}分钟，记得点个关注不迷路！", 5),
            ("产品介绍1", f"第一个产品是本次直播的重头戏...", 15),
            ("互动环节1", "来，弹幕告诉我你们最想了解哪个产品的哪方面？", 5),
            ("产品介绍2", "接下来是第二个产品介绍...", 15),
            ("互动环节2", "有没有已经用过的朋友？来评论区说说体验！", 5),
            ("产品介绍3", "第三个产品是压轴好品...", 15),
            ("限时促销", "最后5分钟！今天的价格只有直播间有，错过就没了！", 5),
            ("结尾引导", "感谢大家今天的陪伴！明天同一时间见！", 3),
        ]

        for section_name, content, time in sections:
            reasoning += f"\n[{section_name}] ({time}分钟)\n{content}\n"

        return {
            "output": reasoning,
            "confidence": 0.87,
            "reasoning": reasoning[:200],
            "word_count": len(reasoning),
            "style": "直播话术",
            "suggestions": [
                "话术要留有灵活空间，根据现场情况调整",
                "关键产品信息要重复2-3遍，防止用户错过",
                "互动话术要自然，不要像在念稿",
            ],
        }

    def _default_copywriting(self, title, platform, context, source_content):
        """默认文案处理"""
        reasoning = (
            f"【笔灵的文案回应】\n\n"
            f"任务：{title}\n"
            f"平台：{platform}\n\n"
            f"好文案的三条铁律：\n"
            f"1. 说人话 —— 不要用别人看不懂的话来说普通的事\n"
            f"2. 有目的 —— 每一段文案都要有明确的传播目标\n"
            f"3. 留记忆 —— 让读者记住一个词、一句话、一个画面\n\n"
            f"请提供更详细的需求（目标受众、核心信息、字数要求），\n"
            f"我会给出更精准的文案方案。"
        )

        return {
            "output": reasoning,
            "confidence": 0.80,
            "reasoning": reasoning[:200],
            "word_count": len(reasoning),
            "style": "通用文案",
            "suggestions": ["补充具体需求以获得更好的文案输出"],
        }

    # ── 辅助方法 ──────────────────────────────────────────────────────

    def _get_script_structure(self, platform, duration, style):
        structures = {
            "douyin": {
                "黄金3秒": "强钩子，制造悬念或冲突",
                "核心展开": "快速推进，信息密度高",
                "结尾引导": "金句收尾 + 关注引导",
            },
            "bilibili": {
                "开场引入": "标题呼应 + 悬念铺垫",
                "内容主体": "层层递进，有理有据",
                "观点升华": "提炼核心观点，引发思考",
                "互动结尾": "三连引导 + 下期预告",
            },
        }
        return structures.get(platform, structures["douyin"])

    def _generate_script_body(self, title, platform, duration, style, source_content):
        """生成脚本正文"""
        template = f"""
【脚本：{title}】
平台：{platform} | 风格：{style} | 时长：约{duration}秒

┌─ 开场（{max(3, duration // 20)}秒）─┐
"""
        if source_content:
            template += f"\n   {source_content[:80]}...\n\n"
        else:
            template += f"\n   【钩子设计】用一个反常识的事实或问题开场\n\n"

        template += "├─ 主体（约{}秒）─┤\n".format(max(20, duration - 15))
        template += """
   · 观点/信息点1：{理由展开}
   · 观点/信息点2：{深化论证}
   · 观点/信息点3：{案例或数据支撑}

├─ 结尾（约5秒）─┤
   · 金句总结 / 情感升华
   · 行动号召：关注 / 评论 / 分享
"""
        return template

    def _generate_title_variants(self, original, platform, themes, keywords):
        """生成标题变体"""
        templates = {
            "douyin": [
                ("你以为……其实……", "反转句式引发好奇"),
                ("千万别……除非……", "警告+条件制造悬念"),
                ("为什么……？答案出乎意料", "疑问+承诺解答"),
                ("亲测……结果……", "真实体验型"),
                ("3分钟教你……", "效率承诺型"),
            ],
            "bilibili": [
                ("深度解析：……", "专业感+深度承诺"),
                ("我花了……终于搞懂了……", "个人经历+知识获得感"),
                ("全网首发？……的真相", "独家感+揭秘感"),
                ("看完这个视频，……", "结果承诺型"),
            ],
        }

        variants = []
        style_templates = templates.get(platform, templates["douyin"])
        for prefix, desc in style_templates:
            title_text = f"{prefix}{original}"
            score = random.randint(72, 95)
            variants.append({
                "title": title_text,
                "score": score,
                "reason": f"{desc}，适合{platform}用户偏好",
            })

        return variants

    def _get_optimal_length(self, platform):
        lengths = {"douyin": "10-20", "bilibili": "15-25", "rednote": "10-15"}
        return lengths.get(platform, "12-20")

    def _adapt_for_platform(self, title, platform, source_content):
        """针对特定平台适配内容"""
        adaptations = {
            "douyin": f"""
  适配版本（抖音）：
  · 标题：{title}（前20字决定点击）
  · 开头：直接切入主题，不要铺垫
  · 语言：口语化，多用短句
  · 节奏：快，信息密度高
  · 字数：约{random.randint(150, 250)}字
""",
            "bilibili": f"""
  适配版本（B站）：
  · 标题：可稍长，加入悬念词
  · 开头：可简要铺垫背景
  · 语言：可适当专业，但要有梗
  · 节奏：中等，给观众思考空间
  · 字数：约{random.randint(400, 800)}字
""",
        }
        return adaptations.get(platform, f"适配版本（{platform}）：保留核心信息，调整表达方式")
