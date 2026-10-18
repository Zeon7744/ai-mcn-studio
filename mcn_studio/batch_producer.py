# -*- coding: utf-8 -*-
"""
批量生产 Demo：输入 1 个短剧 IP + 选题方向 → 输出 30 集内容大纲（可下载）

P0 验收标准：
- 输入：1 个短剧 IP + 选题方向
- 输出：30 集内容大纲（可下载 .md/.txt）
- 用户可在 3 天内独立完成从 IP 到 30 集大纲的全流程
- 纯 Python 标准库实现，无需 LLM，离线可用

运行：
    python batch_producer.py --ip "重生之我在末世当首富" --topic "逆袭爽剧"
    python batch_producer.py --ip "闪婚甜宠总裁大人" --topic "甜宠"
    python batch_producer.py --help
"""
from __future__ import annotations

import argparse
import os
import sys
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

# 所在目录，用于绝对路径解析
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _REPO_ROOT)


# ─── 大纲模板库（纯数据，离线可用）────────────────────────────────────────────
EPISODE_TEMPLATES = {
    "逆袭爽剧": {
        "arc": [
            "被辱开局", "觉醒契机", "首战小胜", "对手反击",
            "低谷蛰伏", "暗藏杀机", "绝地反击", "初露锋芒",
            "获得认可", "强敌压境", "生死一线", "破茧成蝶",
            "登顶巅峰", "隐藏Boss", "最终对决", "胜利加冕",
            "新危机伏笔", "调查真相", "联手盟友", "决战前夕",
            "终极一战", "世界重塑", "回归平凡", "彩蛋暗示",
            "番外：前传", "番外：配角视角", "番外：平行世界", "大结局：未来展望",
            "特别篇：幕后花絮", "特别篇：未收录片段"
        ],
        "tone": "爽、燃、逆袭",
        "hook_style": "每集以强冲突开场，结尾留悬念",
    },
    "甜宠": {
        "arc": [
            "意外相遇", "误会不断", "彼此试探", "心动瞬间",
            "暧昧升温", "外部阻力", "误解分离", "各自成长",
            "命运重逢", "表白成功", "甜蜜日常", "家庭阻挠",
            "共同面对", "危机考验", "真爱告白", "求婚时刻",
            "婚礼筹备", "新婚生活", "事业携手", "幸福升华",
            "孩子话题", "婆媳/翁婿", "旧情人现身", "信任危机",
            "和解加深", "番外：恋爱日记", "番外：如果当初", "番外：另一方视角",
            "特别篇：节日特辑", "大结局：十年后"
        ],
        "tone": "甜、暖、治愈",
        "hook_style": "每集以甜蜜互动开场，结尾以小悬念收尾",
    },
    "悬疑推理": {
        "arc": [
            "离奇命案", "调查开始", "线索浮现", "嫌疑人A",
            "嫌疑人B", "误导方向", "真相一角", "死者秘密",
            "新的受害者", "关联发现", "警方介入", "内部怀疑",
            "关键证据", "反转一", "反转二", "真凶浮出",
            "追凶过程", "最终对峙", "真相大白", "法律裁决",
            "余波处理", "彩蛋悬念", "番外：警探往事", "番外：凶手动机",
            "番外：目击者", "特别篇：平行案", "大结局：多年后",
            "特别篇：导演剪辑版", "特别篇：幕后揭秘"
        ],
        "tone": "紧凑、反转、烧脑",
        "hook_style": "每集以新线索或反转开场，结尾留终极悬念",
    },
}

DEFAULT_ARC_TEMPLATES = [
    "开局钩子：异常事件引入", "世界观铺垫", "主角登场",
    "首个冲突", "成长试炼", "伙伴相遇",
    "第一次胜利", "强敌出现", "内部矛盾",
    "低谷危机", "关键转折", "绝地反击",
    "真相揭示", "高潮对决", "胜利结算",
    "新危机伏笔", "调查延伸", "盟友集结",
    "最终准备", "终极一战", "世界重建",
    "平凡回归", "番外篇：前史", "番外篇：配角视角",
    "番外篇：平行世界", "特别篇：幕后花絮", "大结局：未来展望",
    "彩蛋：续集暗示", "特别篇：未公开片段"
]


# ─── 数据模型 ─────────────────────────────────────────────────────────────────
@dataclass
class EpisodeOutline:
    """单集内容大纲。"""
    episode_no: int
    title: str
    hook: str          # 开场钩子
    core_event: str    # 核心事件
    conflict: str      # 冲突点
    cliffhanger: str   # 结尾悬念
    duration_sec: int  # 预估时长（秒）
    compliance_notes: List[str] = field(default_factory=list)


@dataclass
class ProductionResult:
    """批量生产结果。"""
    ip: str
    topic: str
    total_episodes: int
    episodes: List[EpisodeOutline]
    created_at: str
    download_paths: List[str] = field(default_factory=list)

    def summary(self) -> str:
        lines = [
            f"=== 批量生产完成 ===",
            f"IP：{self.ip}",
            f"选题方向：{self.topic}",
            f"总集数：{self.total_episodes} 集",
            f"生成时间：{self.created_at}",
            "",
            "前5集预览：",
        ]
        for ep in self.episodes[:5]:
            lines.append(f"  第{ep.episode_no:02d}集《{ep.title}》— {ep.hook[:30]}...")
        lines.append(f"\n完整大纲已保存至下载目录。")
        return "\n".join(lines)


# ─── 核心引擎 ─────────────────────────────────────────────────────────────────
def _generate_episode_title(ip: str, topic: str, ep_no: int, arc_index: int) -> str:
    """根据 IP + 集数 + 剧情弧生成集标题。"""
    ip_short = ip[:8] if len(ip) > 8 else ip
    prefixes = ["危机", "转折", "反击", "真相", "觉醒", "决战", "新生", "暗涌"]
    suffixes = ["第{}章".format(ep_no), "episode {}".format(ep_no), "上", "下"]
    arc_name = ["开局", "发展", "高潮", "结局", "番外"][min(arc_index // 8, 4)]
    return f"{ip_short}{arc_name}：{prefixes[ep_no % len(prefixes)]}"


def _generate_episode_content(
    ip: str, topic: str, ep_no: int, arc_index: int,
    template_arc: List[str],
) -> EpisodeOutline:
    """生成单集内容大纲（纯模板引擎，无需 LLM）。"""
    arc_theme = template_arc[min(arc_index, len(template_arc) - 1)]
    title = _generate_episode_title(ip, topic, ep_no, arc_index)

    hooks_map = {
        "开局": "开篇钩子：异常事件或强烈对比引入主角",
        "发展": "发展钩子：危机升级或新角色登场",
        "高潮": "高潮钩子：正面冲突或重大揭露",
        "结局": "结局钩子：收束与展望",
        "番外": "番外钩子：补充视角或平行故事",
    }
    default_hook = "开篇钩子：用强烈冲突或悬念吸引观众"
    hook = default_hook
    for k, v in hooks_map.items():
        if k in arc_theme:
            hook = v
            break

    # 用 _name_pool 使每集 core_event 有差异化描述
    _name_pool = ["命运", "强敌", "危机", "背叛", "真相"]
    core_events = [
        f"主角遭遇{_name_pool[ep_no % len(_name_pool)]}挑战，尝试用智慧/勇气解决",
        f"关键信息揭露，改变剧情走向",
        f"角色间关系发生质变，信任/背叛",
        f"外部势力介入，冲突升级",
        f"主角内心成长，完成认知转变",
    ]
    core_event = core_events[ep_no % len(core_events)]

    conflicts = [
        "人与人的冲突（对手/反派）",
        "人与环境的冲突（困境/逆境）",
        "人与自我的冲突（选择/信念）",
        "信息不对称带来的冲突（误会/欺骗）",
    ]
    conflict = conflicts[ep_no % len(conflicts)]

    cliffhangers = [
        "新的谜团出现，观众急于知道答案",
        "角色陷入两难选择，留下悬念",
        "反派露出真实面目，危机升级",
        "关键道具/信息被发现，剧情转折",
    ]
    cliffhanger = cliffhangers[ep_no % len(cliffhangers)]

    durations = [45, 60, 75, 90, 120]
    duration = durations[ep_no % len(durations)]

    return EpisodeOutline(
        episode_no=ep_no,
        title=title,
        hook=hook,
        core_event=core_event,
        conflict=conflict,
        cliffhanger=cliffhanger,
        duration_sec=duration,
    )


def generate_batch_outline(
    ip: str,
    topic: str = "逆袭爽剧",
    total_episodes: int = 30,
) -> ProductionResult:
    """
    批量生产：输入 IP + 选题方向，输出 N 集内容大纲。

    Args:
        ip: 短剧 IP 名称（如"重生之我在末世当首富"）
        topic: 选题方向，支持"逆袭爽剧"/"甜宠"/"悬疑推理"或自定义
        total_episodes: 总集数，默认 30

    Returns:
        ProductionResult
    """
    # 匹配模板
    if topic in EPISODE_TEMPLATES:
        tpl = EPISODE_TEMPLATES[topic]
        arc = tpl["arc"]
    else:
        arc = DEFAULT_ARC_TEMPLATES

    episodes = []
    for i in range(1, total_episodes + 1):
        ep = _generate_episode_content(ip, topic, i, i - 1, arc)
        episodes.append(ep)

    return ProductionResult(
        ip=ip,
        topic=topic,
        total_episodes=total_episodes,
        episodes=episodes,
        created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )


# ─── 导出/下载 ────────────────────────────────────────────────────────────────
def save_to_md(result: ProductionResult, output_path: Optional[str] = None) -> str:
    """
    将生产结果保存为 Markdown 文件（可下载）。

    Returns:
        保存的文件绝对路径
    """
    if output_path is None:
        safe_ip = "".join(c if c.isalnum() or c in "._-" else "_" for c in result.ip)[:30]
        output_path = os.path.join(_REPO_ROOT, f"output_{safe_ip}_{result.total_episodes}集.md")

    lines = [
        f"# {result.ip} — 批量生产大纲",
        f"",
        f"- **选题方向**：{result.topic}",
        f"- **总集数**：{result.total_episodes} 集",
        f"- **生成时间**：{result.created_at}",
        f"- **工具**：AI MCN Studio v3.0 — 批量生产 Demo",
        f"",
        f"---",
        f"",
    ]

    for ep in result.episodes:
        lines.extend([
            f"## 第{ep.episode_no:02d}集《{ep.title}》",
            f"",
            f"- **开场钩子**：{ep.hook}",
            f"- **核心事件**：{ep.core_event}",
            f"- **冲突点**：{ep.conflict}",
            f"- **结尾悬念**：{ep.cliffhanger}",
            f"- **预估时长**：{ep.duration_sec} 秒",
            f"",
            f"---",
            f"",
        ])

    lines.extend([
        f"",
        f"## 附录：使用指南",
        f"",
        f"1. 将本大纲导入 McnStudio 工作流（IP孵化加速流程）",
        f"2. 逐集调用 `笔灵`（文案主编）生成完整脚本",
        f"3. 逐集调用 `守法`（合规审查员）做平台合规自检",
        f"4. 调用 `绘影`（视觉总监）生成封面/分镜",
        f"5. 调用 `星轨`（发布调度员）排期发布",
        f"",
        f"> ⚠️ 免责声明：本大纲为 AI 自动生成，仅供参考，实际创作请结合人工审核。",
        f"> 📋 合规提示：发布前请使用 `python -m mcn_studio.compliance_checker` 做平台过审检查。",
    ])

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return os.path.abspath(output_path)


def save_to_txt(result: ProductionResult, output_path: Optional[str] = None) -> str:
    """保存为纯文本文件（轻量版本，方便快速查看）。"""
    if output_path is None:
        safe_ip = "".join(c if c.isalnum() or c in "._-" else "_" for c in result.ip)[:30]
        output_path = os.path.join(_REPO_ROOT, f"output_{safe_ip}_{result.total_episodes}集.txt")

    lines = [
        f"{result.ip} — {result.topic} — {result.total_episodes}集大纲",
        f"生成时间：{result.created_at}",
        "=" * 60,
    ]
    for ep in result.episodes:
        lines.append(f"\n【第{ep.episode_no:02d}集】{ep.title}")
        lines.append(f"  开场：{ep.hook}")
        lines.append(f"  核心：{ep.core_event}")
        lines.append(f"  冲突：{ep.conflict}")
        lines.append(f"  悬念：{ep.cliffhanger}")
        lines.append(f"  时长：{ep.duration_sec}s")
    lines.append("\n" + "=" * 60)
    lines.append("AI MCN Studio v3.0 · 批量生产 Demo")

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return os.path.abspath(output_path)


# ─── CLI 入口 ─────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="AI MCN Studio 批量生产 Demo：输入 IP + 选题方向 → 30 集内容大纲",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  python batch_producer.py --ip "重生之我在末世当首富" --topic "逆袭爽剧"
  python batch_producer.py --ip "闪婚甜宠总裁大人" --topic "甜宠" --episodes 30 --format md
        """,
    )
    parser.add_argument("--ip", required=True, help="短剧 IP 名称（必填）")
    parser.add_argument("--topic", default="逆袭爽剧",
                        help="选题方向：逆袭爽剧 / 甜宠 / 悬疑推理（默认：逆袭爽剧）")
    parser.add_argument("--episodes", type=int, default=30, help="总集数（默认：30）")
    parser.add_argument("--format", choices=["md", "txt"], default="md", help="输出格式（默认：md）")
    parser.add_argument("--output", default=None, help="输出文件路径（可选，默认自动生成）")
    args = parser.parse_args()

    print(f"\n🎬 AI MCN Studio 批量生产 Demo")
    print(f"   IP：{args.ip}")
    print(f"   选题方向：{args.topic}")
    print(f"   目标集数：{args.episodes}")
    print()

    # 生成大纲
    result = generate_batch_outline(args.ip, args.topic, args.episodes)
    print(f"✅ 生成 {result.total_episodes} 集内容大纲")
    print()

    # 保存文件
    if args.format == "md":
        path = save_to_md(result, args.output)
    else:
        path = save_to_txt(result, args.output)
    result.download_paths.append(path)

    print(f"📥 大纲已保存：{path}")
    print()
    print(result.summary())

    # 打印前3集预览
    print("\n📋 前3集预览：")
    for ep in result.episodes[:3]:
        print(f"  第{ep.episode_no:02d}集《{ep.title}》")
        print(f"    开场：{ep.hook}")
        print(f"    核心：{ep.core_event}")
        print(f"    悬念：{ep.cliffhanger}")
        print()

    print("💡 下一步：运行合规自检")
    print(f"   python -m mcn_studio.compliance_checker --ip \"{args.ip}\" --platform douyin")
    print()
    print("✅ 批量生产 Demo 完成！用户可在此基础上新增 IP，3 天内完成 30 集大纲。")


if __name__ == "__main__":
    main()
