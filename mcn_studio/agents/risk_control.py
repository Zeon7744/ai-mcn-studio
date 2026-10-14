# -*- coding: utf-8 -*-
"""
舆情风控 Agent - 镜鉴
负责合规审查、舆情监控、危机处理
"""

from __future__ import annotations

import random
from datetime import datetime
from typing import Any

from agents.base_agent import AgentOutput, BaseAgent, register_agent
from core.models import AgentRole


@register_agent(AgentRole.RISK_CONTROL)
class RiskControlAgent(BaseAgent):
    """
    镜鉴 - 舆情风控总监
    性格：谨慎敏锐，指出问题时给法规依据和替代方案
    """

    def think(self, input_data: dict[str, Any]) -> AgentOutput:
        task_title = input_data.get("title", "")
        task_type = input_data.get("task_type", "")
        platform = input_data.get("platform", "")
        context = input_data.get("context", {})
        content_to_review = input_data.get("content", "")

        if task_type == "合规审查":
            response = self._review_compliance(task_title, platform, context, content_to_review)
        elif task_type == "舆情监控":
            response = self._monitor_sentiment(task_title, platform, context, content_to_review)
        elif task_type == "危机处理":
            response = self._handle_crisis(task_title, platform, context, content_to_review)
        elif task_type == "版权审核":
            response = self._review_copyright(task_title, platform, context, content_to_review)
        else:
            response = self._default_risk_thinking(task_title, platform, context, content_to_review)

        output = AgentOutput(
            success=True,
            agent_id=self.config.id,
            agent_name=self.config.name,
            task_id=input_data.get("task_id", ""),
            output_type="review",
            content=response["output"],
            confidence=response["confidence"],
            metadata={
                "reasoning": response["reasoning"],
                "risk_level": response.get("risk_level", "low"),
                "violations": response.get("violations", []),
                "platform": platform,
            },
            suggestions=response.get("suggestions", []),
        )

        self.record_memory({
            "type": "risk_task",
            "content": f"完成风控审查: {task_title}",
            "result": response["reasoning"][:80],
        })

        return output

    def _review_compliance(self, title, platform, context, content):
        """合规审查"""
        violations = self._check_violations(content, platform)
        risk_level = self._assess_risk_level(violations)

        reasoning = (
            f"【镜鉴的合规审查】\n\n"
            f"审查对象：{title}\n"
            f"平台：{platform}\n"
            f"风险等级：{risk_level}\n\n"
        )

        if not violations:
            reasoning += "  ✅ 审查通过，未发现明显违规内容。\n\n"
            reasoning += "  但仍建议：\n"
            reasoning += "  · 发布前再次人工确认\n"
            reasoning += "  · 关注平台规则更新\n"
        else:
            reasoning += f"  ⚠️ 发现 {len(violations)} 处潜在违规：\n\n"
            for i, v in enumerate(violations, 1):
                reasoning += f"  {i}. 【{v['level']}】 {v['issue']}\n"
                reasoning += f"     法规依据：{v['basis']}\n"
                reasoning += f"     修改建议：{v['fix']}\n\n"

            reasoning += (
                f"  📌 红线提醒：\n"
                f"  · 绝对不可触碰：违反法律法规、侵犯他人权益\n"
                f"  · 谨慎使用：夸大宣传、极限词汇\n"
                f"  · 注意规避：版权素材、敏感话题\n"
            )

        return {
            "output": reasoning,
            "confidence": 0.93,
            "reasoning": reasoning[:200],
            "risk_level": risk_level,
            "violations": violations,
            "suggestions": [
                "修改完成后重新提交审查",
                "重要项目建议请外部律师审核合同条款",
            ],
        }

    def _monitor_sentiment(self, title, platform, context, content):
        """舆情监控"""
        risks = self._identify_sentiment_risks(platform, context)

        reasoning = (
            f"【镜鉴的舆情监控】\n\n"
            f"监控对象：{title}\n"
            f"平台：{platform}\n\n"
            f"舆情就像天气预报——预防永远比补救成本低。\n\n"
            f"潜在舆情风险：\n"
        )

        if not risks:
            reasoning += "  ✅ 当前舆情态势平稳，无异常风险。\n"
        else:
            for i, risk in enumerate(risks, 1):
                emoji = "🔴" if risk["severity"] == "high" else "🟡" if risk["severity"] == "medium" else "🟢"
                reasoning += f"  {emoji} [{risk['severity'].upper()}] {risk['description']}\n"
                reasoning += f"     建议应对：{risk['response']}\n\n"

        reasoning += (
            f"日常监控要点：\n"
            f"  · 每日关注评论区高频关键词\n"
            f"  · 监测竞品和相关话题的动态\n"
            f"  · 留意平台政策变化\n"
            f"  · 建立舆情预警机制（设定关键词告警）"
        )

        return {
            "output": reasoning,
            "confidence": 0.85,
            "reasoning": reasoning[:200],
            "risk_level": "medium",
            "violations": [],
            "suggestions": ["建立舆情日报机制", "设置敏感关键词自动告警"],
        }

    def _handle_crisis(self, title, platform, context, content):
        """危机处理"""
        crisis_type = context.get("crisis_type", "")
        severity = context.get("severity", "medium")

        response_plan = self._get_crisis_response_plan(crisis_type, severity)

        reasoning = (
            f"【镜鉴的危机处理预案】\n\n"
            f"事件：{title}\n"
            f"类型：{crisis_type}\n"
            f"严重程度：{severity}\n\n"
            f"危机处理的原则：快、准、稳。\n"
            f"快：第一时间响应，不拖延\n"
            f"准：准确判断性质，对症下药\n"
            f"稳：稳定情绪，不激化矛盾\n\n"
            f"应对方案：\n"
        )

        for phase, action in response_plan:
            reasoning += f"  📌 {phase}：{action}\n"

        reasoning += (
            f"\n危机处理后的复盘要点：\n"
            f"  1. 危机根源是什么？\n"
            f"  2. 哪些环节出了问题？\n"
            f"  3. 如何避免同类危机？\n"
            f"  4. 更新风控手册和应急预案"
        )

        return {
            "output": reasoning,
            "confidence": 0.88,
            "reasoning": reasoning[:200],
            "risk_level": severity,
            "violations": [],
            "suggestions": ["危机处理后48小时内完成复盘报告", "必要时邀请外部公关专家介入"],
        }

    def _review_copyright(self, title, platform, context, content):
        """版权审核"""
        issues = self._check_copyright_issues(content, platform)

        reasoning = (
            f"【镜鉴的版权审核】\n\n"
            f"审核对象：{title}\n\n"
            f"版权是无形的资产，也是无形的风险。\n\n"
        )

        if not issues:
            reasoning += "  ✅ 版权审查通过，未发现明显侵权风险。\n\n"
            reasoning += "  建议使用渠道：\n"
            reasoning += "  · 官方授权音乐库（抖音音乐库/B站音频库）\n"
            reasoning += "  · 免版税素材网站（Pexels/Unsplash等）\n"
            reasoning += "  · 购买正版素材授权"
        else:
            for i, issue in enumerate(issues, 1):
                reasoning += f"  ⚠️ {i}. 【{issue['type']}】{issue['description']}\n"
                reasoning += f"     替代方案：{issue['alternative']}\n\n"

        return {
            "output": reasoning,
            "confidence": 0.90,
            "reasoning": reasoning[:200],
            "risk_level": "low" if not issues else "medium",
            "violations": issues,
            "suggestions": ["建立素材白名单制度", "定期更新版权素材库"],
        }

    def _default_risk_thinking(self, title, platform, context, content):
        reasoning = (
            f"【镜鉴的回应】\n\n"
            f"项目：{title}\n\n"
            f"风控不是束缚创作的枷锁，而是保护创作的铠甲。\n"
            f"好的风控让创作者在安全的边界内自由发挥。\n\n"
            f"请告诉我具体需求（合规审查/舆情监控/危机处理/版权审核），\n"
            f"我会给出更有针对性的方案。"
        )
        return {"output": reasoning, "confidence": 0.80, "reasoning": reasoning[:200],
                "risk_level": "low", "violations": [], "suggestions": ["补充具体需求"]}

    # ── 辅助方法 ──────────────────────────────────────────────────────

    def _check_violations(self, content, platform):
        """检查违规内容——集成合规数据库"""
        from knowledge.industry_trends import COMPLIANCE_RED_LINES, AD_LAW_KEYWORDS

        violations = []

        # 使用知识库中的完整违禁词库
        red_lines = COMPLIANCE_RED_LINES.get(platform, {})
        forbidden_words = red_lines.get("forbidden_words", [])

        for word in forbidden_words:
            if word in content:
                violations.append({
                    "level": "高",
                    "issue": f"包含违禁词：'{word}'",
                    "basis": f"{platform}平台社区公约及《广告法》相关规定",
                    "fix": f"建议替换为中性表述，如'优质的'、'专业的'",
                })

        # 广告法关键词检查（跨平台通用）
        for category, data in AD_LAW_KEYWORDS.items():
            for word in data.get("words", []):
                if word in content and not any(v["issue"].startswith(f"包含违禁词：'{word}'") for v in violations):
                    violations.append({
                        "level": "高" if category in ["absolute_terms", "health_claims"] else "中",
                        "issue": f"疑似{category.replace('_', ' ')}类表述：'{word}'",
                        "basis": data.get("legal_risk", "可能违反广告法规"),
                        "fix": data.get("safe_alternative", ["建议修改"])[0],
                    })

        # 平台特定行为检查
        for behavior in red_lines.get("forbidden_behaviors", []):
            if behavior in content:
                violations.append({
                    "level": "高",
                    "issue": f"涉嫌违规行为：{behavior}",
                    "basis": f"{platform}社区公约",
                    "fix": f"删除或重构涉及'{behavior}'的内容",
                })

        return violations

    def _assess_risk_level(self, violations):
        if not violations:
            return "低"
        high_count = sum(1 for v in violations if v["level"] == "高")
        if high_count > 0:
            return "高"
        return "中"

    def _identify_sentiment_risks(self, platform, context):
        """识别舆情风险"""
        risks = []
        triggers = context.get("triggers", [])
        for trigger in triggers:
            risks.append({
                "severity": "medium",
                "description": f"潜在舆情触发点：{trigger}",
                "response": f"提前准备应对话术，监控评论区动向",
            })
        if not risks:
            risks.append({
                "severity": "low",
                "description": "当前无明显舆情风险",
                "response": "保持日常监控即可",
            })
        return risks

    def _get_crisis_response_plan(self, crisis_type, severity):
        """获取危机应对方案"""
        plans = {
            "内容争议": [
                ("1-2小时", "确认事实，评估影响范围"),
                ("2-4小时", "发布澄清声明或致歉"),
                ("4-24小时", "持续监控舆论走向"),
                ("24-48小时", "发布复盘报告"),
            ],
            "版权纠纷": [
                ("立即", "下架争议内容"),
                ("2小时内", "联系法务确认责任"),
                ("24小时内", "与权利方沟通协商"),
                ("48小时内", "完成整改并记录"),
            ],
            "人设崩塌": [
                ("立即", "暂停相关内容发布"),
                ("24小时内", "内部调查确认情况"),
                ("48小时内", "决定是否道歉或终止合作"),
                ("一周内", "根据决定执行并更新策略"),
            ],
        }
        return plans.get(crisis_type, plans["内容争议"])

    def _check_copyright_issues(self, content, platform):
        """检查版权风险"""
        issues = []
        copyright_keywords = ["背景音乐", "图片素材", "字体", "视频片段"]
        for kw in copyright_keywords:
            if kw in content and "授权" not in content:
                issues.append({
                    "type": f"{kw}版权",
                    "description": f"内容中涉及{kw}，请确认是否已获得授权",
                    "alternative": f"使用{kw}的免版税替代品或购买授权",
                })
        return issues
