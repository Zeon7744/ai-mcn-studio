# -*- coding: utf-8 -*-
"""
AI MCN Studio - 各平台社区公约与红线检查清单库
制度库扩充：发布前合规审查依据，供守法（合规审查员）/镜鉴（风控总监）调用
数据基准：各平台社区公约与广告法公开要求整理（2026-09 版），随平台规则更新迭代
"""

# ─── 各平台红线清单 ─────────────────────────────────────────────────
PLATFORM_COMPLIANCE_CHECKLISTS: dict[str, dict] = {
    "douyin": {
        "name": "抖音",
        "redlines": [
            "严禁未成年人出镜带货（16周岁以下禁止）",
            "严禁医疗、药品功效宣称（'根治''治愈'等绝对化表述）",
            "直播带货必须显著标注'广告'；口播商品不得夸大功效",
            "金融/保险/理财类内容需机构资质，个人不得荐股、承诺收益",
            "教育类内容不得打擦边球做违规引流（校外培训广告限制）",
            "账号矩阵行为：批量注册、多账号互刷数据属违规，可能被限流/封号",
            "涉政、涉军、涉未成年人隐私内容零容忍",
        ],
        "high_risk_words": [
            "最", "第一", "顶级", "绝对", "100%", "根治", "治愈", "秒杀",
            "无副作用", "稳赚", "保本", "国家级", "特供",
        ],
        "posting_rules": [
            "广告/合作内容必须报备（巨量星图任务），未报备商单有处罚风险",
            "直播间挂链商品与口播内容必须一致",
            "封面/标题不得诱导性造假（标题党夸大）",
        ],
    },
    "bilibili": {
        "name": "B站",
        "redlines": [
            "视频商广必须使用花火平台报备，未报备商业化内容可能限流",
            "严禁低俗化、标题党封面（'震惊体'封面会被扣分）",
            "UP主不得虚构人设（如伪造真实身份、年龄）",
            "转载/二创需注明素材来源，侵权投诉将下架",
            "医疗/健康类科普不得替代诊疗建议，须标注免责声明",
        ],
        "high_risk_words": [
            "最", "第一", "绝对", "官方认证", "内部消息", "百分百",
        ],
        "posting_rules": [
            "中长视频建议完播率与三连率平衡，标题避免敏感词",
            "充电/充电专属内容须遵守付费内容社区规范",
        ],
    },
    "xiaohongshu": {
        "name": "小红书",
        "redlines": [
            "种草笔记若为付费合作必须报备（蒲公英平台），暗广是重点打击对象",
            "医美/护肤不得做前后对比疗效承诺",
            "严禁医疗诊断式表述（'包治''断根'）",
            "金融类内容：个人不得提供投资建议（'带单''荐股'违规）",
            "矩阵批量搬运同文案不同账号属违规，会被判低质",
        ],
        "high_risk_words": [
            "最", "第一", "绝对有效", "包好", "断根", "无副作用", "稳赚",
        ],
        "posting_rules": [
            "笔记标题/正文含合作需带'合作'标识或蒲公英报备",
            "图文/视频封面不得含第三方平台导流信息（微信/外链）",
        ],
    },
    "kuaishou": {
        "name": "快手",
        "redlines": [
            "直播打赏不得诱导未成年人充值",
            "严禁虚假人设（如'扮富''伪装贫困'卖惨带货）",
            "带货商品必须与类目资质匹配（食品/化妆品需资质）",
            "低俗擦边内容（衣着/动作暗示）会被断播",
        ],
        "high_risk_words": [
            "最", "第一", "神药", "包治", "绝对", "100%",
        ],
        "posting_rules": [
            "老铁信任经济：退货率与口碑权重高，选品须先行验货",
            "直播切片二创需授权，盗播他人直播内容属侵权",
        ],
    },
    "video_account": {
        "name": "视频号",
        "redlines": [
            "私域导流内容（加V/群）不得强制引导，封禁高风险",
            "严禁涉政谣言、封建迷信内容",
            "直播带货违规宣称（功效/收益）按广告法追责",
        ],
        "high_risk_words": [
            "最", "第一", "祖传", "神效", "绝对", "稳赚不赔",
        ],
        "posting_rules": [
            "视频号与公众号/企微联动内容需保持信息一致性",
            "付费内容（课程/会员）需完成类目报备",
        ],
    },
    "tiktok": {
        "name": "TikTok（海外）",
        "redlines": [
            "广告内容需走 TikTok Shop / Creator Marketplace 报备",
            "Health Claims 限制：保健品不得宣称疗效（FDA 口径）",
            "金融/加密类内容限制严格，不得提供投资建议",
            "未成年人保护：13岁以下禁止，16岁以下限制直播功能",
            "数据合规：注意 GDPR（欧盟受众）对粉丝数据处理的要求",
        ],
        "high_risk_words": [
            "guaranteed", "cure", "miracle", "#1", "risk-free",
        ],
        "posting_rules": [
            "出海内容需本地化审核（文化禁忌/宗教/政治敏感）",
            "多语言字幕建议使用平台官方自动字幕+人工校对",
        ],
    },
    "youtube": {
        "name": "YouTube（海外）",
        "redlines": [
            "商业化内容需声明'Paid promotion'，否则违反 YP 政策",
            "Clickbait（封面标题诱导）降权，重复内容判低质",
            "健康声明需符合平台政策（不得替代医疗建议）",
            "版权：音乐/影视片段使用需授权，三次版权警告封号",
        ],
        "high_risk_words": [
            "guaranteed", "proven cure", "#1", "no side effects",
        ],
        "posting_rules": [
            "社区规范分级：'可变现'内容不得涉及争议议题",
            " Shorts 与长视频分开评估，完播率权重不同",
        ],
    },
}

# ─── 通用广告法高危词（全平台通用） ────────────────────────────────
ADLAW_FORBIDDEN_WORDS: dict[str, list[str]] = {
    "绝对化用语": [
        "最", "第一", "顶级", "极致", "独家", "唯一", "首选",
        "国家级", "世界级", "全网最低",
    ],
    "医疗功效宣称": [
        "根治", "治愈", "药到病除", "无副作用", "包治", "断根",
        "抗癌", "排毒", "消炎（非药品）",
    ],
    "金融诱导": [
        "稳赚", "保本", "零风险", "翻倍", "内幕消息", "带单",
        "推荐股票", "必涨",
    ],
    "限时营销造假": [
        "仅限今天（虚假倒计时）", "最后一件（库存造假）",
        "原价虚标", "虚假秒杀",
    ],
}


def get_checklist(platform: str) -> dict:
    """获取指定平台红线清单（未知平台返回通用项）"""
    return PLATFORM_COMPLIANCE_CHECKLISTS.get(platform, {
        "name": platform,
        "redlines": ["未覆盖平台，按通用广告法+平台社区公约人工审查"],
        "high_risk_words": [],
        "posting_rules": [],
    })


def scan_text(text: str, platform: str = "douyin") -> dict:
    """发布前文本快扫：命中平台高危词 + 广告法词，返回命中列表与建议"""
    plist = get_checklist(platform)
    hits = []
    for word in plist.get("high_risk_words", []):
        if word in text:
            hits.append({
                "word": word,
                "level": "high",
                "reason": f"{plist['name']}平台高危词",
                "suggestion": f"删除或替换为客观表述（如'效果显著'）",
            })
    for cat, words in ADLAW_FORBIDDEN_WORDS.items():
        for word in words:
            if word in text:
                hits.append({
                    "word": word,
                    "level": "high" if cat in ("绝对化用语", "金融诱导") else "medium",
                    "reason": f"广告法风险（{cat}）",
                    "suggestion": f"避免{cat}表述，使用可举证的说法",
                })
    seen = set()
    dedup = []
    for h in hits:
        key = (h["word"], h["reason"])
        if key not in seen:
            seen.add(key)
            dedup.append(h)
    return {
        "platform": platform,
        "safe": len(dedup) == 0,
        "hits": dedup,
        "posting_rules_reminder": plist.get("posting_rules", [])[:3],
    }
