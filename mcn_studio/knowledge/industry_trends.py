# -*- coding: utf-8 -*-
"""
AI MCN Studio - 行业趋势与热点追踪库
基于网络公开数据和行业报告整理的趋势知识库
"""

INDUSTRY_TRENDS = {
    "2025_2026_overview": {
        "macro_trends": [
            {
                "trend": "AI Agent内容生产规模化",
                "impact": "极高",
                "description": "多Agent协作内容生产进入成熟期，MCN行业全面数字化",
                "opportunity": "AI原生MCN机构效率远超传统团队，差异化竞争壁垒提高",
                "risk": "平台加强AI内容标注，纯AI生成内容面临限流",
            },
            {
                "trend": "短视频与直播电商深度闭环",
                "impact": "高",
                "description": "内容即货架，种草即转化，平台电商闭环持续优化",
                "opportunity": "TikTok Shop / 抖音小店 / 小红书直播电商三足鼎立",
                "risk": "流量成本持续上涨，ROI压力增大",
            },
            {
                "trend": "私域会员经济成熟",
                "impact": "高",
                "description": "公域获客成本高企，私域成为品牌必争之地",
                "opportunity": "社群运营+会员体系+复购转化，LTV持续提升",
                "risk": "私域运营需要持续投入，见效慢",
            },
            {
                "trend": "出海内容本地化加速",
                "impact": "高",
                "description": "TikTok/YouTube多语言矩阵成为出海标配",
                "opportunity": "多语言KOL矩阵+TikTok Shop电商出海",
                "risk": "文化雷区/数据合规/支付结算复杂度提升",
            },
        ],
    },
    "2024_2025_overview": {
        "macro_trends": [
            {
                "trend": "AI内容创作普及化",
                "impact": "高",
                "description": "AIGC工具大幅降低内容创作门槛，但也带来同质化竞争",
                "opportunity": "AI+人工结合的差异化内容",
                "risk": "平台可能加强AI内容标注和限流",
            },
            {
                "trend": "短视频直播电商深度融合",
                "impact": "极高",
                "description": "短视频引流+直播带货转化的闭环模式成为主流",
                "opportunity": "内容即电商，种草即转化",
                "risk": "流量成本持续上涨，ROI压力增大",
            },
            {
                "trend": "私域流量价值重估",
                "impact": "高",
                "description": "公域流量越来越贵，私域成为品牌必争之地",
                "opportunity": "社群运营+会员体系+复购转化",
                "risk": "私域运营需要持续投入，见效慢",
            },
            {
                "trend": "下沉市场潜力释放",
                "impact": "中高",
                "description": "三线及以下城市用户增速超过一二线城市",
                "opportunity": "接地气的内容在快手/视频号表现优异",
                "risk": "下沉用户对价格更敏感，客单价低",
            },
            {
                "trend": "情绪价值成为核心竞争力",
                "impact": "高",
                "description": "用户在疲惫生活中寻求情绪疗愈和陪伴",
                "opportunity": "治愈系、陪伴型内容需求激增",
                "risk": "过度煽情可能引发用户疲劳",
            },
        ],
    },
    "platform_updates": {
        "douyin": [
            {"date": "2024Q4", "update": "加大中视频投入，1分钟以上内容流量倾斜", "action": "适当延长视频时长，提升内容深度"},
            {"date": "2025Q1", "update": "电商闭环优化，小店权重提升", "action": "优先布局抖音小店，减少站外跳转"},
            {"date": "2025Q2", "update": "本地生活服务板块扩张", "action": "探店/本地商家类内容有机会"},
        ],
        "bilibili": [
            {"date": "2024Q4", "update": "充电计划改革，创作者收益分成优化", "action": "强化粉丝付费转化，设计专属福利"},
            {"date": "2025Q1", "update": "Story模式（短视频）流量扶持", "action": "将长视频剪辑为短版在Story分发"},
        ],
        "xiaohongshu": [
            {"date": "2024Q4", "update": "搜索权重进一步提升", "action": "优化笔记关键词，布局长尾搜索词"},
            {"date": "2025Q1", "update": "直播带货加大投入", "action": "尝试图文种草+直播转化组合拳"},
        ],
    },
}


# ─── 平台合规红线数据库 ───────────────────────────────────────────────────

COMPLIANCE_RED_LINES = {
    "douyin": {
        "forbidden_words": [
            "最顶级", "第一品牌", "国家级", "最高级", "绝对", "100%有效", "根治",
            "百分百", "绝无仅有", "史无前例", "独一无二", "最强", "最佳",
        ],
        "forbidden_behaviors": [
            "诱导点赞/关注/评论",
            "展示危险行为（无防护）",
            "低俗擦边内容",
            "虚假宣传医疗功效",
            "未经认证的健康建议",
            "传播未经证实的社会新闻",
        ],
        "age_restricted": ["赌博相关内容", "成人用品", "暴力内容"],
    },
    "bilibili": {
        "forbidden_words": ["极限词", "虚假承诺", "封建迷信"],
        "forbidden_behaviors": [
            "剧透关键情节",
            "搬运未授权内容",
            "引战对立言论",
            "未成年人不宜内容",
        ],
        "copyright_sensitive": True,
    },
    "xiaohongshu": {
        "forbidden_words": ["最便宜", "绝对有效", "根治", "神效", "包治"],
        "forbidden_behaviors": [
            "虚假种草（无真实体验）",
            "夸大产品功效",
            "医疗/美容效果承诺",
            "诱导私下交易",
        ],
        "review_sensitive": True,
    },
    "kuaishou": {
        "forbidden_words": ["传销词汇", "金融承诺", "赌博相关"],
        "forbidden_behaviors": [
            "虚假宣传",
            "诱导充值",
            "低俗内容",
            "侵犯肖像权",
        ],
    },
    "wechat_video": {
        "forbidden_words": ["政治敏感", "违规金融", "虚假养生"],
        "forbidden_behaviors": [
            "传播虚假信息",
            "诱导分享",
            "侵权内容",
            "低俗营销",
        ],
        "social_sensitive": True,
    },
}


# ─── 广告法重点词汇检查表 ──────────────────────────────────────────────────

AD_LAW_KEYWORDS = {
    "absolute_terms": {
        "words": ["最", "第一", "顶级", "国家级", "最高级", "唯一", "首个", "独家", "金牌", "影帝", "女王"],
        "legal_risk": "违反《广告法》第九条，不得使用国家级、最高级等用语",
        "safe_alternative": ["优质的", "领先的", "专业的", "口碑好的", "经典的"],
    },
    "health_claims": {
        "words": ["根治", "治愈", "疗效", "药到病除", "百分百有效", "无副作用"],
        "legal_risk": "非医疗器械/药品不得宣称治疗功效",
        "safe_alternative": ["有助于", "辅助改善", "适合", "推荐"],
    },
    "investment_claims": {
        "words": ["稳赚", "保本", "零风险", " guaranteed回报", "躺着赚钱"],
        "legal_risk": "金融投资类宣传禁止承诺收益",
        "safe_alternative": ["历史数据仅供参考", "投资有风险", "过往业绩不代表未来"],
    },
    "time_limits": {
        "words": ["最后一天", "仅限今天", "错过不再"],
        "legal_risk": "虚假限时营销构成欺诈",
        "safe_alternative": ["本周特惠", "活动期间", "限量供应"],
    },
}
