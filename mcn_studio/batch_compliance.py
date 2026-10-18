"""ai-mcn-studio: 批量内容生产 + 平台合规卡点 + 变现钩子（P0 提效缺口补齐）

对应"结合市场景气度补提效缺口"：
调研结论——AI 短剧赛道总量爆发但单价下行、供给过剩，红利在"能快速出量 + 过平台合规"。
本模块补齐三条卡点（纯编排层，不改动既有 agent 行为，复用 mcn_studio 现有能力）：

1. 批量生产 pipeline：给定 N 个选题/剧本，批量走 合规扫描 生成排期表
2. 平台合规卡点：批量合规自检（片名违规词/备案提示/敏感词），输出可投流/打回判定
   —— 对应"过审 + 快出片"的付费点
3. 变现钩子前置：批量产能数字（"3 天出 30 集"）+ 国内收款入口（支付宝个人/BufPay）提示
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


# 平台片名/备案 违规词（轻量内置；生产环境应从 regulations 加载）
_FORBIDDEN_TITLE_WORDS = [
    "最全", "第一", "国家级", "绝对", "100%", "根治", "特效",
    "保证", "承诺", "秒杀", "独家", "顶级", "最好", "最坏",
]
_BACKUP_HINT = "需按《网络微短剧创作指引》完成备案/报备"


@dataclass
class BatchItem:
    """批量生产的一条内容单元。"""
    index: int
    title: str
    platform: str = "douyin"
    script: str = ""
    compliance_passed: bool = False
    compliance_issues: List[str] = field(default_factory=list)
    schedule_day: int = 0


@dataclass
class BatchResult:
    total: int
    passed: int
    rejected: int
    items: List[BatchItem]
    schedule_days: int

    def summary(self) -> Dict[str, Any]:
        return {
            'total': self.total,
            'passed': self.passed,
            'rejected': self.rejected,
            'pass_rate': round(self.passed / self.total, 3) if self.total else 0.0,
            'schedule_days': self.schedule_days,
            'rejected_titles': [it.title for it in self.items if not it.compliance_passed],
        }


def _scan_compliance(title: str, platform: str = "douyin") -> List[str]:
    """对单条片名/内容做合规扫描，返回违规项（空列表=通过）。"""
    issues: List[str] = []
    text = f"{title}"
    try:
        # 复用既有 compliance_checklist 的 scan_text（如可用）
        from mcn_studio.knowledge.compliance_checklist import scan_text
        res = scan_text(text, platform=platform)
        for v in (res.get('violations') or res.get('issues') or []):
            issues.append(str(v))
    except Exception:
        # 内置兜底词扫描
        for w in _FORBIDDEN_TITLE_WORDS:
            if w in text:
                issues.append(f"片名含违规词『{w}』")
    return issues


def batch_produce_and_compliance(
    topics: List[Dict[str, Any]],
    platform: str = "douyin",
    per_day_capacity: int = 3,
    auto_schedule: bool = True,
) -> BatchResult:
    """
    批量生产 + 合规卡点。

    Args:
        topics: 选题列表，每项 dict 含 title（必填）、script（可选）、platform（可选）
        platform: 默认投流平台
        per_day_capacity: 每天可投流产能（用于排期表）
        auto_schedule: 是否按产能排期（仅合规通过的进排期表）

    Returns:
        BatchResult：含每条合规判定 + 排期天次 + 汇总
    """
    items: List[BatchItem] = []
    passed = 0
    for i, topic in enumerate(topics, 1):
        t = str(topic.get('title', '')).strip()
        plat = str(topic.get('platform', platform))
        script = str(topic.get('script', ''))
        issues = _scan_compliance(t, plat)
        ok = len(issues) == 0
        if ok:
            passed += 1
        items.append(BatchItem(
            index=i, title=t, platform=plat, script=script,
            compliance_passed=ok, compliance_issues=issues,
            schedule_day=((i - 1) // per_day_capacity + 1) if ok and auto_schedule else 0,
        ))

    total = len(items)
    return BatchResult(
        total=total,
        passed=passed,
        rejected=total - passed,
        items=items,
        schedule_days=(max(it.schedule_day for it in items) if items else 0),
    )


def build_release_dashboard(result: BatchResult) -> str:
    """生成可投流排期看板文本（合规通过才进，标注产能）。"""
    lines = [f"=== AI 短剧投流排期看板（合规通过 {result.passed}/{result.total}） ==="]
    lines.append(f"预计投流周期：{result.schedule_days} 天")
    by_day: Dict[int, List[str]] = {}
    for it in result.items:
        if it.compliance_passed:
            by_day.setdefault(it.schedule_day, []).append(it.title)
    for day in sorted(by_day):
        lines.append(f"Day {day}: " + "、".join(by_day[day]))
    rejected = [it for it in result.items if not it.compliance_passed]
    if rejected:
        lines.append(f"\n=== 打回 {len(rejected)} 条（合规未过） ===")
        for it in rejected:
            lines.append(f"  {it.title} :: {('; '.join(it.compliance_issues)) or '备案提示'}")
    lines.append(f"\n提示：{len(rejected)} 条需{_BACKUP_HINT} 后再投")
    return "\n".join(lines)


def build_monetization_hook(
    result: BatchResult,
    per_episode_price_cny: float = 500.0,
    payment_channels: Optional[List[str]] = None,
) -> str:
    """
    变现钩子前置（P1）：把"批量产能数字 + 收入估算 + 国内收款入口"直接给用户看。

    Args:
        result: batch_produce_and_compliance 的结果
        per_episode_price_cny: 单集报价（默认 500 元）
        payment_channels: 收款渠道提示（默认 支付宝个人/BufPay）
    """
    n_eps = result.passed
    days = result.schedule_days
    revenue = n_eps * per_episode_price_cny
    chan = "、".join(payment_channels or ["支付宝个人码", "BufPay"])
    lines = [
        "=== 变现钩子（给客户看的产能卡片） ===",
        f"  ⚡ {days} 天合规出片 {n_eps} 集  —— 'N 天出 N 集' 直接可投",
        f"  💰 按单集 ¥{per_episode_price_cny:,.0f} 计，本期可收款 ≈ ¥{revenue:,.0f}",
        f"  💳 收款入口：{chan}",
        "  （对应行业叙事：AI 漫剧制作成本降 50-75%，产能是核心卖点）",
    ]
    return "\n".join(lines)


# ---------------- demo ----------------

if __name__ == '__main__':
    topics = [
        {'title': '重生之我在末世当首富', 'script': '末世+逆袭'},
        {'title': '全网第一的逆天神医', 'platform': 'kuaishou'},
        {'title': '闪婚甜宠总裁大人'},
        {'title': '国漫封神榜：觉醒', 'script': '国风+神话'},
        {'title': '绝对治好的祖传秘方', 'platform': 'douyin'},
        {'title': '逆袭人生：从零到一'},
    ]
    res = batch_produce_and_compliance(topics, platform='douyin', per_day_capacity=2)
    print(build_release_dashboard(res))
    print("\n" + build_monetization_hook(res))
    print("\n--- summary ---")
    for k, v in res.summary().items():
        print(f"  {k}: {v}")
