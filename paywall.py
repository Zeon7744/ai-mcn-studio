# -*- coding: utf-8 -*-
"""付费门 / 配额闸门（ai-mcn-studio 变现 P0：把"免费 3 条/天 → Pro ¥99"做成可演示闭环）。

市场判断（2026）：AI 短剧供给过剩、万次播放收益崩到 5–10 元，付费点集中在
"快出量 + 过合规 + 收款"。免费配额闸门就是直接收钱的开关：免费用户当日生成
内容条数到上限（默认 3 条/天）时，被拦住并吐出"升级 Pro ¥99/月"的 CTA，
而不是静默跑满。

本模块只加**可演示的配额闸门 + 升级 CTA**，不改 orchestrator/agent 核心代码。

运行：
    python3 paywall.py
"""
from __future__ import annotations

from datetime import date
from typing import Optional

# 免费层配额（与 README "免费 3 条/天" 对齐）
FREE_DAILY_QUOTA = 3
PRO_PRICE_CNY = 99


class QuotaExceededError(Exception):
    """免费用户当日配额用尽，必须升级 Pro（或直接调用 paid API）才能继续。"""

    def __init__(self, used: int, quota: int):
        self.used = used
        self.quota = quota
        super().__init__(f"free tier quota reached ({used}/{quota} today)")


def check_free_quota(used_today: int, is_pro: bool = False) -> int:
    """配额闸门：Pro 用户不限量；免费用户返回剩余额度，超额抛 QuotaExceededError。

    返回：本次还允许生成的条数（免费层为 quota-used，Pro 层为大数上限 100000）。
    """
    if is_pro:
        return 100000  # Pro 视为不限量（软上限防误用）
    remaining = FREE_DAILY_QUOTA - used_today
    if remaining <= 0:
        raise QuotaExceededError(used=used_today, quota=FREE_DAILY_QUOTA)
    return remaining


def build_upgrade_cta(used_today: int, is_pro: bool = False) -> str:
    """免费用户配额满时，吐出的"升级 Pro"CTA（含国内收款入口）。"""
    if is_pro:
        return "[Pro] 不限条数/天，可直接批量跑。"
    return (
        f"今日免费 {FREE_DAILY_QUOTA} 条已用完（已用 {used_today} 条）。\n"
        f"  升级 Pro（¥{PRO_PRICE_CNY}/月，不限条数 + 合规审查 + 收款入口）："
        f" 支付宝个人码 / BufPay，见 pricing.md。"
    )


def produce_episodes(
    topics: list[str],
    used_today: int = 0,
    is_pro: bool = False,
    on_episode=None,
) -> dict:
    """带配额闸门的批量产出演示：免费层到上限即停并附 CTA，Pro 层全跑。

    on_episode(topic, idx) 为可选回调（模拟 orchestrator 生产一条内容），
    默认只做计数占位，不真跑 agent，保证可离线演示。
    """
    allow = check_free_quota(used_today, is_pro=is_pro)
    planned = min(len(topics), allow)
    produced = 0
    for i, t in enumerate(topics[:planned]):
        if on_episode:
            on_episode(t, i)
        produced += 1
    hit_quota = produced < len(topics) and not is_pro
    return {
        "requested": len(topics),
        "produced": produced,
        "hit_free_quota": hit_quota,
        "cta": build_upgrade_cta(used_today + produced, is_pro=is_pro) if hit_quota else None,
        "date": date.today().isoformat(),
    }


if __name__ == "__main__":
    print("=== 付费门演示：免费 3 条/天 → Pro ¥99 可演示闭环 ===\n")

    print("[1] 免费用户，今天已用 2 条，再请求 5 条 → 只放行 1 条并附 CTA：")
    r = produce_episodes(["t1", "t2", "t3", "t4", "t5"], used_today=2, is_pro=False)
    print(f"  请求 {r['requested']} / 产出 {r['produced']} / 触顶 {r['hit_free_quota']}")
    if r["cta"]:
        print("  " + r["cta"].replace("\n", "\n  "))

    print("\n[2] 免费用户，今天已用满 3 条，再请求 3 条 → 全被闸门拦住：")
    try:
        produce_episodes(["a", "b", "c"], used_today=3, is_pro=False)
    except QuotaExceededError as e:
        print(f"  拦截成功：{e}")
        print("  " + build_upgrade_cta(3).replace("\n", "\n  "))

    print("\n[3] Pro 用户，请求 5 条 → 全跑（不限量）：")
    r2 = produce_episodes(["t1", "t2", "t3", "t4", "t5"], used_today=0, is_pro=True)
    print(f"  请求 {r2['requested']} / 产出 {r2['produced']} / CTA {r2['cta']}")

    print("\n✅ 付费门闭环完成：免费配额闸门 + 升级 Pro CTA + Pro 不限量放行")
