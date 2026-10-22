# -*- coding: utf-8 -*-
"""
视觉设计 Agent - 绘影
负责封面设计、视频剪辑指导、AI绘画提示词
"""

from __future__ import annotations

import random
from datetime import datetime
from typing import Any

from agents.base_agent import AgentOutput, BaseAgent, register_agent
from core.models import AgentRole


@register_agent(AgentRole.VISUAL_DESIGNER)
class VisualDesignerAgent(BaseAgent):
    """
    绘影 - 视觉设计总监
    性格：对画面极其敏感，沉稳坚持，善于从建筑/时尚中汲取灵感
    """

    def think(self, input_data: dict[str, Any]) -> AgentOutput:
        task_title = input_data.get("title", "")
        task_type = input_data.get("task_type", "")
        platform = input_data.get("platform", "")
        context = input_data.get("context", {})

        if task_type == "封面设计":
            response = self._design_cover(task_title, platform, context)
        elif task_type == "视觉规范":
            response = self._design_visual_system(task_title, platform, context)
        elif task_type == "AI绘画提示词":
            response = self._generate_ai_prompts(task_title, platform, context)
        elif task_type == "视频剪辑指导":
            response = self._guide_video_editing(task_title, platform, context)
        else:
            response = self._default_visual_thinking(task_title, platform, context)

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
                "visual_style": response.get("style", ""),
                "color_palette": response.get("colors", []),
                "platform": platform,
            },
            suggestions=response.get("suggestions", []),
        )

        self.record_memory({
            "type": "visual_task",
            "content": f"完成视觉设计: {task_title}",
            "result": response["reasoning"][:80],
        })

        return output

    def _design_cover(self, title, platform, context):
        """封面设计方案"""
        theme = context.get("theme", "通用")
        mood = context.get("mood", "积极")
        aspect_ratio = context.get("aspect_ratio", "9:16")

        # 平台规格
        specs = {
            "douyin": {"ratio": "9:16", "resolution": "1080×1920", "safe_zone": "上下各留10%"},
            "bilibili": {"ratio": "16:9", "resolution": "1920×1080", "safe_zone": "四周留5%"},
            "rednote": {"ratio": "3:4", "resolution": "1080×1440", "safe_zone": "底部留15%（文字区）"},
        }
        spec = specs.get(platform, specs["douyin"])

        # 配色方案
        palettes = self._get_color_palette(theme, mood)

        reasoning = (
            f"【绘影的封面设计】\n\n"
            f"项目：{title}\n"
            f"平台：{platform} | 规格：{spec['ratio']} | {spec['resolution']}\n"
            f"主题：{theme} | 氛围：{mood}\n\n"
            f"封面是内容的'第一印象'——观众在0.3秒内决定是否点击。\n"
            f"我的设计原则：一眼传达核心信息，二眼激发点击欲望。\n\n"
            f"配色方案：\n"
        )

        for name, colors in palettes.items():
            reasoning += f"  · {name}: {', '.join(colors)}\n"

        reasoning += f"""
布局方案：
  ┌{'─'*40}┐
  │                                          │
  │     【视觉焦点区】                       │
  │        （人物/产品/核心画面）              │
  │                                          │
  ├{'─'*40}┤
  │     【文字信息区】                       │
  │        主标题：{title[:12]}...                    │
  │        副标题：{context.get('subtitle', '吸引点击的描述')[:15]}...                 │
  │                                          │
  └{'─'*40}┘
  安全区：{spec['safe_zone']}

构图建议：
  · 使用三分法或黄金分割定位视觉焦点
  · 人物/产品占据画面40-60%面积
  · 文字区域与视觉区域形成对比（冷暖/明暗）
  · 关键元素避开平台UI遮挡区域
"""

        return {
            "output": reasoning,
            "confidence": 0.90,
            "reasoning": reasoning[:200],
            "style": f"封面设计-{platform}",
            "colors": list(palettes.keys()),
            "suggestions": [
                "建议制作2-3个不同版本的封面进行A/B测试",
                f"注意{platform}平台UI遮挡区域，避免关键信息被遮住",
                "封面色调与内容调性保持一致",
            ],
        }

    def _design_visual_system(self, title, platform, context):
        """视觉体系设计"""
        reasoning = (
            f"【绘影的视觉体系设计】\n\n"
            f"项目名称：{title}\n\n"
            f"统一的视觉体系比单条视频的惊艳更重要。\n"
            f"我为您设计了以下视觉规范：\n\n"
        )

        components = [
            ("品牌主色", self._get_brand_colors(platform)),
            ("辅助色", self._get_accent_colors(platform)),
            ("字体规范", self._get_font_spec(platform)),
            ("封面模板", self._get_cover_templates(platform)),
            ("视频动效", self._get_motion_style(platform)),
        ]

        for name, items in components:
            reasoning += f"  📌 {name}：\n"
            for item in items:
                reasoning += f"     · {item}\n"
            reasoning += "\n"

        reasoning += (
            f"💡 执行建议：\n"
            f"  · 所有输出素材严格遵守以上规范\n"
            f"  · 新成员入职时统一培训视觉规范\n"
            f"  · 每季度回顾一次，根据数据反馈微调"
        )

        return {
            "output": reasoning,
            "confidence": 0.88,
            "reasoning": reasoning[:200],
            "style": "视觉体系",
            "colors": ["品牌色系"],
            "suggestions": [
                "建立视觉素材库，方便快速复用",
                "规范文档分享给全体团队成员",
            ],
        }

    def _generate_ai_prompts(self, title, platform, context):
        """AI绘画提示词生成"""
        style = context.get("style", "写实")
        subject = context.get("subject", "")
        mood_desc = context.get("mood", "温馨")

        # 反向提示词
        negative_prompts = self._get_negative_prompts(style)

        reasoning = (
            f"【绘影的AI绘画提示词】\n\n"
            f"主题：{title}\n"
            f"风格：{style} | 主体：{subject}\n\n"
            f"AI绘画的核心是'精准描述'。\n"
            f"以下是生成的提示词：\n\n"
        )

        # 正面提示词
        positive = self._build_positive_prompt(title, style, subject, mood_desc)
        reasoning += "📝 正向提示词：\n"
        reasoning += f"  {positive}\n\n"

        reasoning += "🚫 反向提示词：\n"
        reasoning += f"  {negative_prompts}\n\n"

        reasoning += (
            f"💡 使用建议：\n"
            f"  · 可使用Midjourney / Stable Diffusion / DALL-E执行\n"
            f"  · 首次生成建议用低分辨率快速迭代，确定方向后放大\n"
            f"  · 可根据实际效果微调权重参数（如 (::) 或 ()）"
        )

        return {
            "output": reasoning,
            "confidence": 0.85,
            "reasoning": reasoning[:200],
            "style": "AI绘画提示词",
            "colors": [],
            "suggestions": [
                "建议先跑几张低分辨率测试图再定稿",
                f"根据{platform}平台特点，可调整构图比例",
            ],
        }

    def _guide_video_editing(self, title, platform, context):
        """视频剪辑指导"""
        duration = context.get("duration", 60)
        pacing = context.get("pacing", "快节奏")

        reasoning = (
            f"【绘影的视频剪辑指导】\n\n"
            f"项目：{title}\n"
            f"时长：{duration}秒 | 节奏：{pacing}\n\n"
            f"剪辑是视频的'第二次创作'。\n"
            f"节奏感比清晰度更重要。\n\n"
            f"剪辑方案：\n"
        )

        # 节奏指示
        if pacing == "快节奏":
            cuts = [
                ("0-3s", "开场：强冲击画面，快速切换2-3个镜头", "0.5-1s/镜头"),
                ("3-15s", "引入：稳定节奏，每3-4秒一切", "3-4s/镜头"),
                ("15-{0}-s".format(duration), "主体：信息密集，节奏不变", "2-3s/镜头"),
                ("{0}-{1}s".format(duration - 10, duration), "收尾：放慢节奏，情感沉淀", "4-5s/镜头"),
            ]
        else:
            cuts = [
                ("0-5s", "开场：慢节奏引入，建立氛围", "3-5s/镜头"),
                ("5-{0}s".format(duration - 10), "主体：平稳推进，留白思考", "5-8s/镜头"),
                ("{0}-{1}s".format(duration - 10, duration), "结尾：渐弱收尾", "5-8s/镜头"),
            ]

        for time_range, desc, interval in cuts:
            reasoning += f"  [{time_range}] {desc}（{interval}）\n"

        reasoning += f"""
转场建议：
  · 快节奏：硬切为主，少量速度 ramp（变速）
  · 慢节奏：淡入淡出，溶解转场
  · 关键节点可用zoom in/out增强冲击力

音效建议：
  · 节奏点配合音效（whoosh / click / pop）
  · 避免音效过多影响信息传递
"""

        return {
            "output": reasoning,
            "confidence": 0.87,
            "reasoning": reasoning[:200],
            "style": "视频剪辑指导",
            "colors": [],
            "suggestions": [
                "粗剪完成后先看一遍，标注需要调整的片段",
                "最终版本检查音画同步",
            ],
        }

    def _default_visual_thinking(self, title, platform, context):
        reasoning = (
            f"【绘影的视觉回应】\n\n"
            f"项目：{title}\n\n"
            f"视觉的第一原则：技术服务于表达。\n"
            f"不是越花哨越好，而是越精准越好。\n\n"
            f"请告诉我具体的视觉需求（封面/视频/海报/AI绘画），\n"
            f"我会给出针对性的设计方案。"
        )
        return {"output": reasoning, "confidence": 0.80, "reasoning": reasoning[:200],
                "style": "通用视觉", "colors": [], "suggestions": ["补充具体需求"]}

    def _get_color_palette(self, theme, mood):
        palettes = {
            ("科技", "积极"): {"主色调": ["#1a73e8", "#4285f4"], "辅助色": ["#34a853", "#fbbc04"], "点缀色": ["#ea4335"]},
            ("生活", "温馨"): {"主色调": ["#f5f5f5", "#ffffff"], "辅助色": ["#ff9800", "#ffc107"], "点缀色": ["#e91e63"]},
            ("美食", "诱人"): {"主色调": ["#ff5722", "#ff9800"], "辅助色": ["#4caf50", "#8bc34a"], "点缀色": ["#795548"]},
            ("时尚", "高级"): {"主色调": ["#212121", "#424242"], "辅助色": ["#ffd700", "#c0c0c0"], "点缀色": ["#ffffff"]},
        }
        return palettes.get((theme, mood), {"主色调": ["#333333", "#666666"], "辅助色": ["#ffffff", "#f0f0f0"], "点缀色": ["#ff4444"]})

    def _get_brand_colors(self, platform):
        colors = {
            "douyin": ["#000000（黑）", "#FE2C55（抖音红）", "#FFFFFF（白）"],
            "bilibili": ["#00AEEC（B站蓝）", "#FB7299（B站粉）", "#FFFFFF（白）"],
            "rednote": ["#FF2442（小红书红）", "#FFFFFF（白）", "#F5F5F5（浅灰）"],
        }
        return colors.get(platform, ["#333333", "#666666", "#FFFFFF"])

    def _get_accent_colors(self, platform):
        return ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7"]

    def _get_font_spec(self, platform):
        specs = {
            "douyin": ["标题：思源黑体 Bold 48-72pt", "正文：思源黑体 Regular 24-36pt"],
            "bilibili": ["标题：思源黑体 Bold 36-48pt", "正文：思源黑体 Regular 18-24pt"],
        }
        return specs.get(platform, ["标题：思源黑体 Bold", "正文：思源黑体 Regular"])

    def _get_cover_templates(self, platform):
        templates = {
            "douyin": ["人物特写+大字标题", "场景全景+文字叠加", "对比图（前后/左右）"],
            "bilibili": ["场景图+标题居中", "人物+气泡对话框", "信息图风格"],
        }
        return templates.get(platform, ["标准封面模板", "特色封面模板"])

    def _get_motion_style(self, platform):
        styles = {
            "douyin": ["快速缩放（zoom in/out）", "滑动转场", "闪烁强调"],
            "bilibili": ["平滑过渡", "字幕动效", "画面分割"],
        }
        return styles.get(platform, ["自然转场", "文字动效"])

    def _build_positive_prompt(self, title, style, subject, mood):
        prompts = {
            "写实": f"photorealistic, high detail, professional photography, 8k resolution, {subject}, {mood} atmosphere",
            "插画": f"digital illustration, artistic style, vibrant colors, {subject}, {mood} feeling, detailed background",
            "简约": f"minimalist design, clean composition, {subject}, {mood} mood, flat design, modern aesthetic",
        }
        base = prompts.get(style, prompts["写实"])
        return f"{base}, title text '{title}', balanced composition"

    def _get_negative_prompts(self, style):
        defaults = "blurry, low quality, distorted, watermark, text artifacts, bad anatomy"
        if style == "写实":
            return f"{defaults}, cartoon, anime, oversaturated"
        elif style == "插画":
            return f"{defaults}, photorealistic, photographic, 3d render"
        return defaults
