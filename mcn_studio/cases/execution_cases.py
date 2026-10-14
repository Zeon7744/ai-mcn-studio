# -*- coding: utf-8 -*-
"""
AI MCN Studio - 执行案例库
真实MCN成功案例与失败教训，用于训练和参考
"""

SUCCESS_CASES = {
    "case_001_douyin_food": {
        "id": "case_001",
        "platform": "douyin",
        "category": "美食",
        "account_type": "个人IP",
        "timeline": "2023.03-2024.06",
        "result": {
            "followers_start": 0,
            "followers_end": 2800000,
            "avg_views": 500000,
            "best_video_views": 45000000,
            "monetization": "直播带货+品牌广告",
            "annual_revenue": "约1200万",
        },
        "key_strategies": [
            "差异化定位：'农村奶奶的厨房'——真实、温暖、有故事感",
            "内容公式：传统美食制作+祖孙互动+情感故事",
            "视觉风格：暖色调、自然光、手写字幕",
            "更新频率：日更，固定时间发布",
            "互动策略：每条评论必回，建立粉丝归属感",
        ],
        "turning_points": [
            {"time": "第3个月", "event": "一条'奶奶的手擀面'视频爆火，单条播放2000万"},
            {"time": "第6个月", "event": "开启直播带货，首战GMV破100万"},
            {"time": "第12个月", "event": "品牌广告合作，月入50万+"},
        ],
        "lessons": [
            "真实感是美食赛道的核心竞争力",
            "情感故事比单纯展示厨艺更有传播力",
            "保持日更建立算法信任",
        ],
    },
    "case_002_bilibili_tech": {
        "id": "case_002",
        "platform": "bilibili",
        "category": "科技数码",
        "account_type": "专业UP主",
        "timeline": "2022.09-2024.08",
        "result": {
            "followers_start": 5000,
            "followers_end": 850000,
            "avg_views": 150000,
            "best_video_views": 12000000,
            "monetization": "商业合作+充电+会员",
            "annual_revenue": "约400万",
        },
        "key_strategies": [
            "深度测评：每期视频平均时长15分钟，数据详实",
            "系列化：'千元机大战'系列建立追更习惯",
            "弹幕互动：设计弹幕触发点（如'懂的都懂'）",
            "封面统一风格：黑色背景+产品+大字标题",
        ],
        "turning_points": [
            {"time": "第4个月", "event": "'2024旗舰机横评'单集播放800万"},
            {"time": "第10个月", "event": "获得品牌年度合作，单条报价20万"},
        ],
        "lessons": [
            "B站用户偏好深度内容，3分钟视频很难出圈",
            "系列化是建立粉丝粘性的关键",
            "封面标题直接影响点击率",
        ],
    },
    "case_003_xiaohongshu_beauty": {
        "id": "case_003",
        "platform": "xiaohongshu",
        "category": "美妆护肤",
        "account_type": "KOC转型KOL",
        "timeline": "2023.01-2024.09",
        "result": {
            "followers_start": 200,
            "followers_end": 1500000,
            "avg_views": 80000,
            "best_post_views": 5000000,
            "monetization": "品牌种草+自营品牌",
            "annual_revenue": "约600万",
        },
        "key_strategies": [
            "真实测评：不接广时直言缺点，建立信任",
            "封面统一：粉色系+大字报风格",
            "关键词布局：每篇笔记覆盖5-8个搜索词",
            "评论区运营：每条笔记回复率90%+",
        ],
        "turning_points": [
            {"time": "第5个月", "event": "'干皮救星'测评笔记收藏破50万"},
            {"time": "第12个月", "event": "启动自营品牌，月销破百万"},
        ],
        "lessons": [
            "真实是小红书的核心竞争力",
            "收藏率比点赞率更重要（代表实用价值）",
            "KOC真实感比KOL专业度更吃香",
        ],
    },
    "case_004_douyin_kuaishou_live": {
        "id": "case_004",
        "platform": "kuaishou",
        "category": "带货直播",
        "account_type": "团队直播",
        "timeline": "2023.06-2024.12",
        "result": {
            "followers_start": 0,
            "followers_end": 5200000,
            "avg_live_gmv": 500000,
            "best_live_gmv": 15000000,
            "monetization": "直播带货",
            "annual_revenue": "约3000万（GMV约2亿）",
        },
        "key_strategies": [
            "人设：'实在大哥'——接地气、会砍价、为粉丝谋福利",
            "选品：性价比优先，客单价50-200元",
            "直播节奏：每15分钟一轮爆款，保持热度",
            "私域：建立粉丝群，开播前预热",
        ],
        "lessons": [
            "快手的私域流量价值极高",
            "主播人设比产品更重要",
            "高频直播建立用户习惯",
        ],
    },
}


FAILURE_CASES = {
    "case_fail_001_compliance": {
        "id": "case_fail_001",
        "platform": "douyin",
        "category": "美妆",
        "timeline": "2024.01-2024.03",
        "result": {
            "followers_peak": 320000,
            "outcome": "账号被封禁30天",
            "fine": "品牌赔偿损失约50万",
        },
        "root_cause": "使用了'根治湿疹'、'100%有效'等违规医疗宣称词汇",
        "violation_details": [
            {"content": "视频中宣称产品'根治过敏'", "rule": "违反《广告法》第十七条，非医疗器械不得宣称治疗功效"},
            {"content": "展示'使用前vs使用后'对比图", "rule": "构成虚假/引人误解的宣传"},
        ],
        "lessons": [
            "合规审查必须在内容发布前完成",
            "医疗/健康类内容需要额外谨慎",
            "'before/after'对比图在多个平台受限",
        ],
    },
    "case_fail_002_quality": {
        "id": "case_fail_002",
        "platform": "bilibili",
        "category": "知识科普",
        "timeline": "2023.09-2024.01",
        "result": {
            "followers_start": 50000,
            "followers_end": 48000,
            "outcome": "粉丝流失，商业合作终止",
        },
        "root_cause": "内容质量下滑，抄袭争议",
        "violation_details": [
            {"content": "某视频被指抄袭海外频道内容", "impact": "核心粉丝大量取关"},
            {"content": "更新频率从周更变为日更，质量下降", "impact": "完播率从45%降至20%"},
        ],
        "lessons": [
            "质量>数量，降质更新比不更新更伤账号",
            "原创性是长期竞争力的基础",
            "粉丝流失后恢复成本极高",
        ],
    },
    "case_fail_003_monetization": {
        "id": "case_fail_003",
        "platform": "xiaohongshu",
        "category": "生活方式",
        "timeline": "2024.02-2024.06",
        "result": {
            "followers_peak": 680000,
            "outcome": "商业合作口碑崩塌，品牌方停止合作",
        },
        "root_cause": "过度接广，粉丝信任破裂",
        "violation_details": [
            {"content": "一周内发布12条广告笔记", "impact": "粉丝认为'只会割韭菜'"},
            {"content": "推广产品与实际体验不符", "impact": "评论区大量负面反馈"},
        ],
        "lessons": [
            "广告比例控制在30%以内，否则伤害粉丝信任",
            "只推广自己真正使用过的产品",
            "粉丝信任比短期收益更重要",
        ],
    },
    "case_fail_004_algorithm": {
        "id": "case_fail_004",
        "platform": "douyin",
        "category": "剧情",
        "timeline": "2023.11-2024.02",
        "result": {
            "followers_peak": 150000,
            "outcome": "内容方向错误，账号沉寂",
        },
        "root_cause": "盲目追热点，内容定位模糊",
        "violation_details": [
            {"content": "今天做美食，明天做剧情，后天做测评", "impact": "算法无法给账号打标签"},
            {"content": "每条内容都追热点但无独特角度", "impact": "同质化严重，无法脱颖而出"},
        ],
        "lessons": [
            "账号定位必须清晰，频繁换赛道会丢失算法推荐",
            "追热点需要有独特角度，而非简单复制",
            "垂直领域比泛内容更容易建立竞争力",
        ],
    },
}



# ─── 补充成功案例（第5-8） ─────────────────────────────────────────────

EXTRA_SUCCESS_CASES = {
    "case_005_tiktok_overseas": {
        "id": "case_005",
        "platform": "tiktok",
        "category": "海外出海",
        "account_type": "品牌矩阵",
        "timeline": "2024.05-2025.06",
        "result": {
            "followers_start": 0,
            "followers_end": 1200000,
            "avg_views": 350000,
            "monetization": "TikTok Shop 电商 + 品牌赞助",
            "annual_revenue": "约800万（海外结算）",
        },
        "key_strategies": [
            "多语言矩阵：英语/西语/日语/泰语 4个账号同步分发",
            "本地化内容：聘请当地KOL做文化顾问，避免文化雷区",
            "TikTok Shop 优先布局，减少站外跳转",
            "利用 #TikTokMadeMeBuyIt 等热门标签借势",
        ],
        "turning_points": [
            {"time": "第2个月", "event": "一条产品开箱视频被TikTok官方推荐，单条播放800万"},
            {"time": "第4个月", "event": "TikTok Shop 上线，首月GMV突破50万"},
        ],
    },
    "case_006_bilibili_knowledge_ip": {
        "id": "case_006",
        "platform": "bilibili",
        "category": "知识IP",
        "account_type": "个人UP主",
        "timeline": "2023.06-2025.06",
        "result": {
            "followers_start": 1000,
            "followers_end": 1500000,
            "avg_views": 200000,
            "monetization": "充电计划 + 知识付费 + 品牌商单",
            "annual_revenue": "约500万",
        },
        "key_strategies": [
            "系列化内容：固定栏目《XX科普》，每周一期建立追更习惯",
            "深度+趣味结合：硬核知识用轻松表达，弹幕互动设计精妙",
            "长视频为主（10-20分钟），满足B站用户深度消费习惯",
            "充电计划设计专属福利，粉丝付费转化率高",
        ],
        "turning_points": [
            {"time": "第6个月", "event": "一期视频被B站首页推荐，粉丝单周增长5万"},
            {"time": "第12个月", "event": "知识付费课程上线，月均收入突破10万"},
        ],
    },
    "case_007_xiaohongshu_micro_koc": {
        "id": "case_007",
        "platform": "xiaohongshu",
        "category": "美妆护肤",
        "account_type": "素人KOC矩阵",
        "timeline": "2024.01-2024.12",
        "result": {
            "followers_start": 0,
            "followers_end": 350000,
            "avg_views": 80000,
            "monetization": "品牌种草 + 小红书直播带货",
            "annual_revenue": "约300万",
        },
        "key_strategies": [
            "素人真实感：不精修、不滤镜，强调亲测体验",
            "搜索词布局：每篇笔记覆盖3-5个长尾搜索关键词",
            "评论区互动：48小时内回复所有评论，建立信任",
            "图文+视频双格式：同一内容出图文笔记和视频笔记双版本",
        ],
        "turning_points": [
            {"time": "第3个月", "event": "一篇真实测评笔记被品牌方主动联系合作"},
            {"time": "第8个月", "event": "小红书直播首秀，单场GMV突破15万"},
        ],
    },
    "case_008_video_account_senior": {
        "id": "case_008",
        "platform": "video_account",
        "category": "中老年健康",
        "account_type": "个人IP",
        "timeline": "2024.03-2025.03",
        "result": {
            "followers_start": 0,
            "followers_end": 800000,
            "avg_views": 150000,
            "monetization": "视频号小店 + 社群会员 + 健康产品带货",
            "annual_revenue": "约600万",
        },
        "key_strategies": [
            "正向价值观：内容强调积极生活态度，符合视频号调性",
            "社交链传播：引导用户转发至朋友圈，形成裂变",
            "视频号+公众号+社群三位一体，私域转化效率高",
            "视频号小店打通，带货闭环无需跳转",
        ],
        "turning_points": [
            {"time": "第2个月", "event": "一条养生视频被大量中老年用户转发，粉丝单周增长10万"},
            {"time": "第5个月", "event": "社群会员体系上线，月均复购率达35%"},
        ],
    },
}

# ─── 补充失败案例（第5-8） ─────────────────────────────────────────────

EXTRA_FAILURE_CASES = {
    "case_fail_005_algorithm_ban": {
        "id": "case_fail_005",
        "platform": "douyin",
        "category": "娱乐",
        "timeline": "2024.04-2024.05",
        "result": {
            "followers_peak": 500000,
            "outcome": "账号被限流30天，粉丝流失20万",
        },
        "root_cause": "频繁搬运未授权内容，触发平台原创检测",
        "violation_details": [
            {"content": "多条视频与海外账号内容高度相似", "rule": "违反抖音原创规则，判定为搬运"},
            {"content": "短时间内集中发布20条搬运内容", "rule": "触发平台批量违规检测"},
        ],
        "lessons": [
            "搬运内容必须经过充分二创，加入原创评论/解说",
            "版权管理员（版权）应建立每日原创度检测机制",
            "账号被限流后立即停止发布，提交原创声明申诉",
        ],
    },
    "case_fail_006_trust_collapse": {
        "id": "case_fail_006",
        "platform": "douyin",
        "category": "美妆",
        "timeline": "2024.06-2024.08",
        "result": {
            "followers_peak": 2000000,
            "outcome": "粉丝信任崩塌，商业合作全部终止",
        },
        "root_cause": "推广产品与主播真实体验不符，被粉丝扒出虚假种草",
        "violation_details": [
            {"content": "推广某护肤品时称'使用一周白一个度'", "impact": "粉丝实测无效，评论区大量负面反馈"},
            {"content": "品牌方要求删除负面评论，主播未披露合作关系", "impact": "粉丝认为被欺骗，取关潮"},
        ],
        "lessons": [
            "只推广自己真正使用过的产品（甄宝·选品原则）",
            "广告必须明确标注'合作'或'广告'，不披露等于欺诈",
            "粉丝信任一旦崩塌，恢复成本是损失的10倍",
        ],
    },
    "case_fail_007_homogenization": {
        "id": "case_fail_007",
        "platform": "bilibili",
        "category": "游戏解说",
        "timeline": "2023.10-2024.06",
        "result": {
            "followers_peak": 100000,
            "outcome": "账号数据持续下滑，最终停更",
        },
        "root_cause": "内容同质化严重，缺乏差异化定位，被同类账号淹没",
        "violation_details": [
            {"content": "视频风格与头部UP主高度相似，无独特标签", "impact": "算法无法给账号打标签"},
            {"content": "更新频率高于质量，完播率从35%降至15%", "impact": "算法减少推荐"},
        ],
        "lessons": [
            "找到竞品覆盖不到的细分切入点，放大10倍",
            "质量>数量，降质更新比不更新更伤账号",
            "定期做竞品分析（数策），保持差异化敏感度",
        ],
    },
    "case_fail_008_data_fraud": {
        "id": "case_fail_008",
        "platform": "xiaohongshu",
        "category": "生活方式",
        "timeline": "2024.02-2024.04",
        "result": {
            "followers_peak": 500000,
            "outcome": "被品牌方发现数据造假，列入行业黑名单",
        },
        "root_cause": "购买虚假粉丝/点赞数据，被品牌方数据服务商识别",
        "violation_details": [
            {"content": "粉丝画像与目标受众严重不符（年龄/地域分布异常）", "impact": "品牌方数据审计发现异常"},
            {"content": "互动率远超行业平均水平，触发品牌方风控预警", "impact": "品牌方停止合作，行业通报"},
        ],
        "lessons": [
            "数据造假是MCN行业最严重的红线，一旦曝光行业信誉永久受损",
            "品牌方普遍使用第三方数据服务商（如新榜/克劳锐）核验账号真实数据",
            "运营中心（数策/慧眼）应建立账号数据健康度监控，避免异常波动",
        ],
    },
}

# ─── 案例复盘框架 ───────────────────────────────────────────────────────────

CASE_REVIEW_FRAMEWORK = """
【案例复盘四步法】

第一步：目标回顾
    · 原始目标是什么？
    · 实际结果如何？
    · 差距在哪？

第二步：差异分析
    · 成功因素：哪些做对了？
    · 失败原因：哪些做错了？
    · 外部因素：平台/时机/竞争的影响

第三步：经验总结
    · 可复用的方法论
    · 需要避免的坑
    · 新的发现/洞察

第四步：行动计划
    · 下一阶段的具体措施
    · 需要调整的策略
    · 预期目标和衡量标准
"""
