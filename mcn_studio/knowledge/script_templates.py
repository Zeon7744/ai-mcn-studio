# -*- coding: utf-8 -*-
"""
AI MCN Studio - 脚本模板库
可复用的脚本模板，覆盖短视频/直播/口播等多种场景
"""

SCRIPT_TEMPLATES = {
    # ─── 短视频脚本模板 ───────────────────────────────────────────────
    "short_video_knowledge": {
        "name": "知识类短视频脚本",
        "duration": "30-60秒",
        "structure": {
            "0-3s": {"type": "hook", "content": "反常识钩子/痛点提问", "example": "90%的人都不知道，手机这个功能能省一半电量"},
            "3-15s": {"type": "context", "content": "问题展开+背景说明", "example": "很多人手机用一年就卡顿，其实是因为…"},
            "15-45s": {"type": "solution", "content": "干货输出，3个要点", "example": "教你3个设置，手机续航直接翻倍：第一…第二…第三…"},
            "45-55s": {"type": "summary", "content": "总结回顾", "example": "总结一下：关闭后台刷新+降低自动亮度+限制定位"},
            "55-60s": {"type": "cta", "content": "行动号召", "example": "试试这个方法，回去设置一下，记得关注我"},
        },
    },
    "short_video_review": {
        "name": "测评类短视频脚本",
        "duration": "60-120秒",
        "structure": {
            "0-5s": {"type": "hook", "content": "产品名+核心卖点/槽点", "example": "这款网红空气净化器，到底是不是智商税？"},
            "5-20s": {"type": "intro", "content": "产品介绍+测评标准", "example": "今天我们从净化效率、噪音、耗电量三个维度实测"},
            "20-80s": {"type": "test", "content": "逐项测评+数据展示", "example": "第一项：甲醛净化测试，1小时数值从0.3降到…"},
            "80-100s": {"type": "verdict", "content": "优缺点总结+打分", "example": "优点：净化效率高；缺点：噪音偏大。综合评分：7.5/10"},
            "100-120s": {"type": "cta", "content": "购买建议+关注引导", "example": "性价比不错，适合有孩子的家庭。关注我，下期测…"},
        },
    },
    "short_video_story": {
        "name": "剧情类短视频脚本",
        "duration": "60-90秒",
        "structure": {
            "0-5s": {"type": "hook", "content": "冲突/悬念开场", "example": "她以为老公出差了，直到看到了这条消息…"},
            "5-25s": {"type": "setup", "content": "背景铺垫+人物关系", "example": "小张和老公结婚三年，一直以为是模范夫妻…"},
            "25-60s": {"type": "conflict", "content": "冲突升级+转折", "example": "直到那天，她发现了一个秘密…"},
            "60-80s": {"type": "climax", "content": "高潮+反转", "example": "原来这一切是一场误会…"},
            "80-90s": {"type": "ending", "content": "收尾+情感升华", "example": "有时候，信任比真相更重要"},
        },
    },
    "short_video_vlog": {
        "name": "Vlog类脚本",
        "duration": "3-10分钟",
        "structure": {
            "opening": {"type": "hook", "content": "当日亮点预告", "example": "今天带你们去看我梦寐以求的房子…"},
            "body": {"type": "process", "content": "按时间线记录，保留真实感", "example": "早上8点出发→中午到达→下午看房…"},
            "climax": {"type": "highlight", "content": "最精彩的部分", "example": "当我推开这扇门的那一刻…"},
            "ending": {"type": "reflection", "content": "感悟+下期预告", "example": "今天的看房之旅结束了，你们觉得这套房子值吗？"},
        },
    },

    # ─── 口播脚本模板 ───────────────────────────────────────────────
    "talking_head_opinion": {
        "name": "观点类口播脚本",
        "duration": "60-90秒",
        "structure": {
            "0-5s": {"type": "hook", "content": "抛出争议性观点", "example": "我认为，努力是最大的谎言"},
            "5-20s": {"type": "thesis", "content": "亮明观点+原因", "example": "不是努力没用，而是方向错了，努力就是白费"},
            "20-60s": {"type": "arguments", "content": "3个论据+案例", "example": "第一个论据…第二个论据…第三个论据…"},
            "60-80s": {"type": "counter", "content": "预判反驳+回应", "example": "可能有人说那就不努力了吗？不，努力的方向很重要"},
            "80-90s": {"type": "cta", "content": "金句总结+关注", "example": "记住：方向不对，努力白费。关注我，说点真话"},
        },
    },
    "talking_head_tutorial": {
        "name": "教程类口播脚本",
        "duration": "2-5分钟",
        "structure": {
            "0-5s": {"type": "hook", "content": "结果承诺", "example": "学会了这个技巧，你的PPT直接提升一个档次"},
            "5-15s": {"type": "intro", "content": "问题+解决方案概述", "example": "很多人做PPT花了3小时，其实用这个方法30分钟搞定"},
            "15-90s": {"type": "steps", "content": "分步骤教学", "example": "第一步…第二步…第三步…"},
            "90-110s": {"type": "tips", "content": "进阶技巧/常见错误", "example": "注意不要犯这个错误…"},
            "110-120s": {"type": "cta", "content": "总结+关注", "example": "收藏起来慢慢练，关注我学更多技巧"},
        },
    },

    # ─── 直播脚本模板 ───────────────────────────────────────────────
    "live_stream_opener": {
        "name": "直播开场脚本",
        "duration": "开场5-10分钟",
        "structure": {
            "0-1min": {"type": "warmup", "content": "欢迎+今日主题预告", "example": "欢迎新进直播间的宝宝们！今天给大家准备了…"},
            "1-3min": {"type": "hook", "content": "互动+留人", "example": "先做个小调查，有没有人遇到过…的？有的扣1"},
            "3-5min": {"type": "value", "content": "今日福利预告", "example": "今天直播间有3轮抽奖，还有特价福利款…"},
            "5-10min": {"type": "flow", "content": "进入正题", "example": "好，废话不多说，直接上今天的主角…"},
        },
    },
    "live_stream_product_intro": {
        "name": "带货产品介绍脚本",
        "duration": "单品5-15分钟",
        "structure": {
            "0-1min": {"type": "hook", "content": "价格/效果震撼开场", "example": "这个产品价格只要99！比超市便宜一半！"},
            "1-3min": {"type": "pain", "content": "痛点挖掘", "example": "大家是不是也有这样的困扰…"},
            "3-8min": {"type": "demo", "content": "产品展示+使用演示", "example": "我来给大家现场演示一下…"},
            "8-12min": {"type": "social_proof", "content": "评价背书+销量证明", "example": "已经卖了10万单，好评率98%…"},
            "12-15min": {"type": "urgency", "content": "限时限量+下单引导", "example": "库存只有500单，3、2、1，上链接！"},
        },
    },
    "live_stream_closing": {
        "name": "直播结尾脚本",
        "duration": "最后5-10分钟",
        "structure": {
            "5min前": {"type": "recap", "content": "今日爆款回顾", "example": "今天最受欢迎的三款产品再介绍一下…"},
            "3min前": {"type": "福利", "content": "粉丝福利/抽奖", "example": "最后再抽一轮，关注我的粉丝优先…"},
            "1min前": {"type": "预告", "content": "下次直播预告", "example": "明天晚上8点，给大家准备了…"},
            "end": {"type": "farewell", "content": "感谢+下期再见", "example": "感谢大家的陪伴，我们明天见！"},
        },
    },

    # ─── 小红书笔记模板 ───────────────────────────────────────────────
    "rednote_review": {
        "name": "小红书测评笔记",
        "structure": {
            "标题": "[产品名]+[评价词]+[数字/对比]",
            "正文": [
                "开头：一句话概括使用感受",
                "中间：优点（配图）+ 缺点（配图）+ 适用人群",
                "结尾：总结评分+购买建议",
            ],
            "标签": "#产品名 #测评 #种草 #避雷 #好物分享",
        },
    },
    "rednote_guide": {
        "name": "小红书攻略笔记",
        "structure": {
            "标题": "[场景]+[数字]个[方法]+[结果]",
            "正文": [
                "开头：场景代入+痛点共鸣",
                "中间：分步骤讲解（每步配图）",
                "结尾：总结+互动提问",
            ],
            "标签": "#攻略 #教程 #干货 #分享",
        },
    },
}


# ─── 标题生成助手 ─────────────────────────────────────────────────────────

TITLE_GENERATOR_GUIDE = """
标题生成三步法：
1. 确定目标：用户为什么要点开？（好奇/利益/共鸣/紧迫感）
2. 选择公式：从模板库中选择最匹配的标题公式
3. 填充内容：将具体内容填入公式，检查是否通顺、是否有吸引力

注意事项：
- 标题长度：抖音/快手≤20字，B站≤30字，小红书≤20字
- 避免：堆砌关键词、过度夸张、与内容不符
- 必须：包含核心关键词、有信息增量、引发好奇
"""
