# -*- coding: utf-8 -*-
"""
AI MCN Studio - 知识索引与检索API
统一管理所有知识库模块，提供查询接口
"""

import sys
import os

# 确保同目录可导入（兼容直接运行 mcn_studio/demo.py 等场景）
_repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _repo_root not in sys.path:
    sys.path.insert(0, _repo_root)

# 优先用相对导入（包模式），兜底用绝对路径（脚本模式）
try:
    from .platform_algorithms import (
        PLATFORM_ALGORITHMS,
        PLATFORM_ALGORITHMS_EXTENDED,
        PLATFORM_COMPARISON,
        MULTI_PLATFORM_STRATEGY,
    )
    from .content_formulas import (
        CONTENT_FORMULAS,
        TRENDING_CONTENT,
    )
    from .script_templates import (
        SCRIPT_TEMPLATES,
        TITLE_GENERATOR_GUIDE,
    )
    from .industry_trends import (
        INDUSTRY_TRENDS,
        COMPLIANCE_RED_LINES,
        AD_LAW_KEYWORDS,
    )
    from .compliance_checklist import (
        PLATFORM_COMPLIANCE_CHECKLISTS,
        ADLAW_FORBIDDEN_WORDS,
        get_checklist,
        scan_text,
    )
    from .hot_report import build_hot_topic_report, next_suggestion
    from .ai_labeling import check_ai_labeling, AI_LABELING_RULES
    from .matrix_dashboard import build_matrix_dashboard, next_optimization
    from .team_board import team_efficiency_report, project_board
except ImportError:
    # 兜底：脚本模式下（mcn_studio/ 在 sys.path 中）的绝对导入
    from knowledge.platform_algorithms import (
        PLATFORM_ALGORITHMS,
        PLATFORM_ALGORITHMS_EXTENDED,
        PLATFORM_COMPARISON,
        MULTI_PLATFORM_STRATEGY,
    )
    from knowledge.content_formulas import (
        CONTENT_FORMULAS,
        TRENDING_CONTENT,
    )
    from knowledge.script_templates import (
        SCRIPT_TEMPLATES,
        TITLE_GENERATOR_GUIDE,
    )
    from knowledge.industry_trends import (
        INDUSTRY_TRENDS,
        COMPLIANCE_RED_LINES,
        AD_LAW_KEYWORDS,
    )
    from knowledge.compliance_checklist import (
        PLATFORM_COMPLIANCE_CHECKLISTS,
        ADLAW_FORBIDDEN_WORDS,
        get_checklist,
        scan_text,
    )
    from knowledge.hot_report import build_hot_topic_report, next_suggestion
    from knowledge.ai_labeling import check_ai_labeling, AI_LABELING_RULES
    from knowledge.matrix_dashboard import build_matrix_dashboard, next_optimization
    from knowledge.team_board import team_efficiency_report, project_board


def get_platform_checklist(platform: str) -> dict:
    """获取平台红线清单（发布前合规审查依据）"""
    return get_checklist(platform)


def quick_compliance_scan(platform: str, text: str) -> dict:
    """文本快扫：平台高危词 + 广告法词，返回命中与建议"""
    return scan_text(text, platform)


def search_platform_info(platform: str) -> dict:
    """搜索平台算法信息"""
    return PLATFORM_ALGORITHMS.get(platform, {})


def get_content_formula(formula_type: str, formula_name: str) -> dict:
    """获取内容公式"""
    return CONTENT_FORMULAS.get(formula_type, {}).get(formula_name, {})


def get_script_template(template_name: str) -> dict:
    """获取脚本模板"""
    return SCRIPT_TEMPLATES.get(template_name, {})


def check_compliance(platform: str, content: str) -> dict:
    """合规检查"""
    # 平台别名归一化（兼容ContentPlatform全部12个值）
    _alias = {
        'rednote': 'xiaohongshu',
        'wechat_official': 'wechat_video',
        'kuaishou_life': 'kuaishou',
        'baidu_tieba': 'weibo',
        'tiktok_cn': 'tiktok',
        'tiktok': 'douyin',  # TikTok海外参照国内短视频标准
        'youtube': 'douyin',  # YouTube参照国内短视频标准
        'toutiao': 'douyin',
        'zhihu': 'bilibili',
    }
    platform = _alias.get(platform, platform)

    red_lines = COMPLIANCE_RED_LINES.get(platform, {})
    violations = []

    # 检查违禁词
    for word in red_lines.get("forbidden_words", []):
        if word in content:
            violations.append({
                "type": "forbidden_word",
                "word": word,
                "suggestion": f"替换为：{AD_LAW_KEYWORDS.get('absolute_terms', {}).get('safe_alternative', ['其他表述'])[0]}",
            })

    # 检查广告法关键词
    for category, data in AD_LAW_KEYWORDS.items():
        for word in data.get("words", []):
            if word in content:
                violations.append({
                    "type": f"ad_law_{category}",
                    "word": word,
                    "risk": data.get("legal_risk", ""),
                    "suggestion": data.get("safe_alternative", ["建议修改"])[0],
                })

    return {
        "platform": platform,
        "has_violations": len(violations) > 0,
        "violations": violations,
        "safe": len(violations) == 0,
    }


def get_best_posting_time(platform: str, is_weekday: bool = True) -> list:
    """获取最佳发布时间"""
    info = PLATFORM_ALGORITHMS.get(platform, {})
    times = info.get("best_posting_times", {})
    return times.get("工作日" if is_weekday else "周末", [])


def get_trending_content(period: str = "2024_q4_2025_q1") -> dict:
    """获取热门内容趋势"""
    return INDUSTRY_TRENDS.get(period, {})


def get_cross_platform_strategy() -> dict:
    """获取跨平台策略"""
    return MULTI_PLATFORM_STRATEGY


def get_title_suggestions(topic: str, platform: str, mood: str = "中性") -> list:
    """生成标题建议"""
    from knowledge.content_formulas import CONTENT_FORMULAS
    formulas = CONTENT_FORMULAS.get("title_formulas", {})
    suggestions = []
    for name, formula in formulas.items():
        pattern = formula.get("pattern", "")
        example = formula.get("example", "")
        # 简单替换示例中的关键词
        suggestion = example.replace("这个", topic[:4])
        suggestions.append({
            "formula": name,
            "template": pattern,
            "example": suggestion,
        })
    return suggestions[:5]


def get_compliance_guide(platform: str) -> dict:
    """获取平台合规指南"""
    red_lines = COMPLIANCE_RED_LINES.get(platform, {})
    return {
        "platform": platform,
        "forbidden_words": red_lines.get("forbidden_words", []),
        "forbidden_behaviors": red_lines.get("forbidden_behaviors", []),
        "special_notes": {
            "douyin": "对医疗/金融内容审核最严格",
            "bilibili": "版权审查严格，二创需注意",
            "xiaohongshu": "种草内容需真实，虚假宣传处罚重",
            "kuaishou": "对低俗/虚假信息零容忍",
            "wechat_video": "社交链传播，负面内容扩散快",
        }.get(platform, ""),
    }


def make_hot_report(raw_topics, platform="douyin", top_n=5):
    """生成结构化热点速报（研究中心·瞭望+疾风）"""
    return build_hot_topic_report(raw_topics, platform, top_n)


def hot_report_next_step(report):
    """热点速报下一步建议（供总调度分派）"""
    return next_suggestion(report)


def check_ai_content_labeling(platform="douyin", is_ai_generated=True, ai_disclosed=False):
    """AI内容标注合规核验（发布前，供守法调用）"""
    return check_ai_labeling(platform, is_ai_generated, ai_disclosed)


def build_matrix_board(accounts, platform="douyin"):
    """矩阵数据看板（运营中心·慧眼+鉴往）"""
    return build_matrix_dashboard(accounts)


def matrix_next_step(dashboard):
    """矩阵看板下一步优化动作（供总调度分派）"""
    return next_optimization(dashboard)


def team_efficiency(agents):
    """团队效能看板（CEO视角）"""
    return team_efficiency_report(agents)


def project_board_view(projects):
    """跨项目进度看板（CEO视角）"""
    return project_board(projects)
