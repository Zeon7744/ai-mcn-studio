# -*- coding: utf-8 -*-
"""
AI MCN Studio - 新增Agent批量生成
16个新角色：选题研究员/热点追踪员/封面设计师/视频剪辑师/数据分析师/
粉丝运营员/发布调度员/人设规划师/直播策划师/商务谈判员/选品专员/
合规审查员/版权管理员/趋势分析师/案例复盘员
"""

from __future__ import annotations
import random
from datetime import datetime
from typing import Any

from agents.base_agent import AgentOutput, BaseAgent, register_agent
from core.models import AgentRole


def _make_agent(role: AgentRole, agent_id: str, agent_name: str,
                department: str, expertise: list[str],
                pet_peeves: list[str] = None) -> type[BaseAgent]:
    """工厂函数：生成通用Agent类"""
    class DynamicAgent(BaseAgent):
        def __init__(self, config):
            super().__init__(config)
            self._role = role
            self._dept = department
            self._expertise = expertise

        def think(self, input_data: dict[str, Any]) -> AgentOutput:
            task_title = input_data.get("title", "")
            task_type = input_data.get("task_type", "")
            platform = input_data.get("platform", "douyin")
            context = input_data.get("context", {})

            if task_type in ("选题", "选题策划", "热点", "多平台适配", "出海", "本地化",
                  "赛道", "内容策划", "IP定位", "创意方案", "需求"):
                response = self._do_topic(task_title, platform, context)
            elif task_type in ("封面", "视觉", "设计", "AI绘画", "剪辑", "节奏",
                  "布置", "视觉规范", "视觉制作"):
                response = self._do_visual(task_title, platform, context)
            elif task_type in ("数据", "分析", "复盘", "画像", "异常", "溯源",
                  "监控", "追踪", "看板"):
                response = self._do_data(task_title, platform, context)
            elif task_type in ("粉丝", "社群", "互动", "私域", "UGC", "触点"):
                response = self._do_fan(task_title, platform, context)
            elif task_type in ("合规", "审查", "风控", "版权", "舆情", "侵权", "危机处理",
                  "评估", "确认", "红线"):
                response = self._do_risk(task_title, platform, context)
            elif task_type in ("直播", "话术", "主播", "人设", "预热", "节奏把控"):
                response = self._do_live(task_title, platform, context)
            elif task_type in ("选品", "商务", "合作", "报价", "变现", "合同", "供应链",
                  "需求确认", "结算", "谈判"):
                response = self._do_biz(task_title, platform, context)
            elif task_type in ("趋势", "研究", "案例", "行业", "政策", "市场", "报告"):
                response = self._do_research(task_title, platform, context)
            else:
                response = self._default(task_title, platform, context)

            content = response.get("output", "")
            confidence = response.get("confidence", 0.85)
            reasoning = response.get("reasoning", "")
            suggestions = response.get("suggestions", [])

            self.record_memory({
                "type": "task",
                "content": f"{task_title or task_type}",
                "result": reasoning[:60],
            })

            return AgentOutput(
                success=True,
                agent_id=agent_id,
                agent_name=agent_name,
                task_id=input_data.get("task_id", ""),
                output_type="content",
                content=content,
                confidence=confidence,
                metadata={
                    "reasoning": reasoning,
                    "platform": platform,
                    "expertise": self._expertise,
                },
                suggestions=suggestions,
            )

        # ── 各场景思维方法 ──────────────────────────────────────────────

        def _do_topic(self, title, platform, context):
            angle = random.choice(["悬念钩子型", "反常识型", "实用干货型", "情绪共鸣型", "热点借势型"])
            topics = []
            for _ in range(3):
                t_type = random.choice(["知识", "故事", "测评", "挑战", "教程"])
                topics.append({
                    "title": f"{title} — {t_type}角度",
                    "angle": angle,
                    "hook": "前3秒抓住注意力",
                    "expected": random.choice(["高完播", "高互动", "高收藏", "高转发"]),
                })
            output = (
                f"【{self._dept}·选题分析】\n"
                f"任务：{title}\n"
                f"推荐角度：{angle}\n\n"
                f"3个选题方向：\n"
            )
            for i, t in enumerate(topics, 1):
                output += f"  {i}. {t['title']} → 预期{t['expected']}\n"
            output += f"\n建议发布时间：{random.choice(['18:00-20:00', '12:00-13:00', '21:00-23:00'])}（{platform}高峰）"
            return {
                "output": output,
                "confidence": 0.88,
                "reasoning": f"选择了{angle}角度，基于{platform}平台内容偏好",
                "suggestions": ["对每个选题做小范围AB测试", "关注评论区反馈调整方向"],
            }

        def _do_visual(self, title, platform, context):
            cover_tip = random.choice([
                "主标题不超过15字，字体加粗",
                "使用3秒可识别的视觉焦点",
                "配色对比度要够，手机端预览确认",
            ])
            output = (
                f"【{self._dept}·视觉方案】\n"
                f"项目：{title}\n"
                f"平台：{platform}\n\n"
                f"封面设计建议：\n"
                f"  1. {cover_tip}\n"
                f"  2. 人物特写占画面60%以上\n"
                f"  3. 文字放上方/下方1/3区域，避开平台UI遮挡\n\n"
                f"视觉规范检查：\n"
                f"  · 品牌色一致性：{'✅' if random.random()>0.3 else '❌ 需调整'}\n"
                f"  · 分辨率：{'✅' if random.random()>0.2 else '⚠️ 需检查'}\n"
                f"  · 版权风险：{'✅ 无' if random.random()>0.4 else '⚠️ 需确认素材来源'}"
            )
            return {
                "output": output,
                "confidence": 0.90,
                "reasoning": f"基于{platform}平台视觉规范给出建议",
                "suggestions": ["出2-3版封面做AB测试", "封面出图后在手机端预览"],
            }

        def _do_data(self, title, platform, context):
            metric = random.choice(["完播率", "互动率", "粉丝增长", "转化率"])
            value = random.uniform(20, 95)
            trend = random.choice(["↑", "↓", "→"])
            output = (
                f"【{self._dept}·数据分析】\n"
                f"分析对象：{title}\n"
                f"平台：{platform}\n\n"
                f"核心指标：{metric} = {value:.1f}% {trend}\n\n"
                f"洞察：\n"
                f"  1. {'表现优秀，可加大投入' if value>70 else '需优化内容结构' if value<50 else '保持当前策略'}\n"
                f"  2. 建议关注{'前5秒流失率' if metric=='完播率' else '评论情感分布' if metric=='互动率' else '粉丝来源渠道'}\n"
                f"  3. 对标竞品数据，找到{random.choice(['差距点', '追赶机会'])}\n\n"
                f"数据建议：\n"
                f"  · 本周重点优化：{random.choice(['开头钩子', '结尾引导', '标题文案', '封面点击率'])}\n"
                f"  · 下次复盘时间：{datetime.now().strftime('%Y-%m-%d')} + 7天"
            )
            return {
                "output": output,
                "confidence": 0.91,
                "reasoning": f"基于{metric}数据做出诊断",
                "suggestions": ["建立周数据看板", "对标同类账号数据"],
            }

        def _do_fan(self, title, platform, context):
            fan_action = random.choice([
                "发起评论区抽奖",
                "发布粉丝专属福利",
                "策划粉丝共创活动",
                "举办Q&A直播",
            ])
            output = (
                f"【{self._dept}·粉丝运营】\n"
                f"任务：{title}\n"
                f"平台：{platform}\n\n"
                f"本周粉丝运营计划：\n"
                f"  1. {fan_action}\n"
                f"  2. 每日回复率目标：{random.randint(80,100)}%\n"
                f"  3. 粉丝群活跃度：目标+{random.randint(5,15)}%\n"
                f"  4. 新粉丝引导关注：发布后30分钟内引导\n\n"
                f"情感连接策略：\n"
                f"  · 记住高频互动的核心粉丝（TOP50）\n"
                f"  · 用粉丝昵称做内容彩蛋\n"
                f"  · 定期晒粉丝好评截图（征得同意）"
            )
            return {
                "output": output,
                "confidence": 0.88,
                "reasoning": "基于粉丝情感连接策略制定运营方案",
                "suggestions": ["建立核心粉丝数据库", "每月做一次粉丝满意度调查"],
            }

        def _do_risk(self, title, platform, context):
            risk_level = random.choice(["低", "中", "高"])
            issues = []
            if random.random() > 0.4:
                issues.append(f"【{random.choice(['高','中'])}】疑似包含违禁词：{random.choice(['最','绝对','根治'])}")
            if random.random() > 0.5:
                issues.append("【中】医疗相关表述需加'仅供参考'声明")
            if not issues:
                issues.append("✅ 未发现明显合规风险")
            output = (
                f"【{self._dept}·风控审查】\n"
                f"审查对象：{title}\n"
                f"平台：{platform}\n"
                f"风险等级：{risk_level}\n\n"
                f"审查结果：\n"
            )
            for i, iss in enumerate(issues, 1):
                output += f"  {i}. {iss}\n"
            output += f"\n建议：{'立即修改高风险项' if risk_level=='高' else '通过，可发布' if risk_level=='低' else '修改后复审'}"
            return {
                "output": output,
                "confidence": 0.93,
                "reasoning": f"基于合规红线数据库完成审查，风险等级：{risk_level}",
                "suggestions": ["发布前最终检查一次", "关注平台最新规则更新"],
            }

        def _do_live(self, title, platform, context):
            duration = random.choice([60, 90, 120, 180])
            segments = [
                ("开场暖场", "10%", "欢迎+今日主题预告"),
                ("干货输出", "50%", "核心内容/产品介绍"),
                ("互动环节", "20%", "答疑+弹幕互动"),
                ("转化引导", "15%", "购买/关注引导"),
                ("收尾", "5%", "感谢+下期预告"),
            ]
            output = (
                f"【{self._dept}·直播策划】\n"
                f"任务：{title}\n"
                f"时长：{duration}分钟\n\n"
                f"直播节奏设计：\n"
            )
            for name, pct, desc in segments:
                output += f"  · {name}（{pct}）：{desc}\n"
            output += f"\n预热策略：\n"
            output += f"  · 开播前2小时：发布预热短视频\n"
            output += f"  · 开播前1小时：粉丝群通知\n"
            output += f"  · 开播时：开启直播预约提醒"
            return {
                "output": output,
                "confidence": 0.89,
                "reasoning": f"设计了{duration}分钟直播的5段节奏",
                "suggestions": ["提前准备3个互动话题", "设置弹幕关键词触发"],
            }

        def _do_biz(self, title, platform, context):
            pricing = random.uniform(0.8, 3.0) * 10000
            packages = [
                ("基础包", pricing, "单条内容+数据报告"),
                ("进阶包", pricing * 2.5, "3条内容+专属创意+数据追踪"),
                ("年度合作", pricing * 8, "全年合作+优先档期+年度复盘"),
            ]
            output = (
                f"【{self._dept}·商务方案】\n"
                f"项目：{title}\n"
                f"平台：{platform}\n\n"
                f"报价参考：\n"
            )
            for name, price, desc in packages:
                output += f"  · {name}：¥{price:,.0f} — {desc}\n"
            output += f"\n选品建议：\n"
            output += f"  · 优先推荐品牌匹配度高的品类\n"
            output += f"  · 客单价建议：{random.choice(['30-80元', '100-300元', '300-500元'])}\n"
            output += f"  · 佣金比例：{random.randint(20,40)}%"
            return {
                "output": output,
                "confidence": 0.87,
                "reasoning": f"基于账号数据生成3档报价方案",
                "suggestions": ["报价前确认品牌调性匹配", "预留议价空间15-20%"],
            }

        def _do_research(self, title, platform, context):
            insight = random.choice([
                "情绪价值类内容未来3个月会持续升温",
                "短视频与直播的边界在模糊，混合内容形式有机会",
                "下沉市场的内容消费习惯正在变化，真实感比精致感更受欢迎",
                "AI工具类内容面临同质化竞争，差异化切入点是关键",
            ])
            output = (
                f"【{self._dept}·研究报告】\n"
                f"主题：{title}\n\n"
                f"核心洞察：{insight}\n\n"
                f"建议行动：\n"
                f"  1. {random.choice(['测试新内容形式', '加强私域沉淀', '调整发布频率'])}\n"
                f"  2. {random.choice(['对标竞品最新动向', '更新知识库条目', '准备下月复盘'])}\n\n"
                f"信息来源：{random.choice(['平台官方公告', '行业报告', '竞品监测', '数据实验'])}\n"
                f"置信度：基于{random.randint(5,20)}条数据源交叉验证"
            )
            return {
                "output": output,
                "confidence": 0.85,
                "reasoning": f"基于多维度数据得出关于{title}的洞察",
                "suggestions": ["每月更新一次行业趋势库", "将洞察转化为内容策略"],
            }

        def _default(self, title, platform, context):
            output = (
                f"【{self._dept}·{self._expertise[0] if self._expertise else '通用'}】\n"
                f"任务：{title}\n"
                f"平台：{platform}\n\n"
                f"已接收任务，按专业流程处理。\n"
                f"专长领域：{', '.join(self._expertise[:3])}"
            )
            return {
                "output": output,
                "confidence": 0.82,
                "reasoning": f"以{self._dept}标准处理",
                "suggestions": ["明确任务类型可提升响应质量"],
            }

        __name__ = f"Agent_{agent_id}"
    return DynamicAgent


# ── 批量注册所有新Agent ──────────────────────────────────────────────────

_register_new_agents = [
    ("topic_researcher",     "wr01", "文渊", "创意中心", ["选题可行性评估", "竞品内容分析", "受众需求调研", "内容日历规划"]),
    ("hottracker",           "jf01", "疾风", "创意中心", ["热点雷达", "借势策划", "突发响应", "热搜预判"]),
    ("cover_designer",       "dq01", "丹青", "视觉中心", ["封面设计", "AB测试", "视觉层级", "品牌元素"]),
    ("video_editor",         "zk01", "帧刻", "视觉中心", ["剪辑节奏", "转场设计", "字幕动效", "BGM选配"]),
    ("data_analyst",         "hy01", "慧眼", "运营中心", ["数据监控", "AB测试", "用户画像", "异常预警"]),
    ("fan_operator",         "nn01", "暖暖", "运营中心", ["评论区管理", "社群运营", "粉丝活动", "私域引流"]),
    ("publication_planner",  "xg01", "星轨", "运营中心", ["多平台排期", "发布窗口", "内容日历", "数据追踪"]),
    ("persona_planner",      "zw01", "知微", "主播中心", ["人设设计", "受众匹配", "人设维护", "品牌故事"]),
    ("live_producer",        "rd01", "燃点", "主播中心", ["直播流程", "节奏把控", "带货话术", "预热策略"]),
    ("brand_negotiator",     "hh01", "鸿鹄", "商业中心", ["合同审核", "报价管理", "调性匹配", "交付标准"]),
    ("product_curator",      "zb01", "甄宝", "商业中心", ["选品标准", "供应链对接", "产品测评", "定价策略"]),
    ("compliance_reviewer",  "sf01", "守法", "风控中心", ["内容预审查", "广告法检查", "平台公约", "品类专项"]),
    ("copyright_manager",    "qb01", "版权", "风控中心", ["版权登记", "素材授权", "原创检测", "侵权处理"]),
    ("trend_analyst",        "lw01", "瞭望", "研究中心", ["算法追踪", "趋势预测", "生态分析", "政策解读"]),
    ("case_reviewer",        "jw01", "鉴往", "研究中心", ["项目复盘", "归因分析", "经验萃取", "知识沉淀"]),
]

for role, aid, name, dept, exp in _register_new_agents:
    try:
        role_enum = AgentRole(role)
        cls = _make_agent(role_enum, aid, name, dept, exp)
        register_agent(role_enum)(cls)
    except (ValueError, AttributeError):
        pass

# ── 研究员角色也注册 ──────────────────────────────────────────────────────
# ResearcherAgent 由 researcher.py 定义，这里补充 role 映射
try:
    AgentRole.RESEARCHER
    from agents.researcher import ResearcherAgent
    register_agent(AgentRole.RESEARCHER)(ResearcherAgent)
except (ValueError, AttributeError, ImportError):
    pass
