# -*- coding: utf-8 -*-
"""billing.check_access 统一门控代理 vs paywall.check_free_quota 行为一致性测试。

契约（向后兼容，paywall.py 原逻辑不变）：
  1. Pro/team/enterprise → allowed=True 不限（remaining=-1）
  2. 免费版拉满：前 3 次调用放行且 remaining 递减
  3. 超限：第 4 次调用 allowed=False + upgrade_url + http_status=402
  4. paywall.check_free_quota 原行为：Pro 返回 100000；免费超额抛 QuotaExceededError
  5. 两个入口结论一致：billing.check_access 拒绝 ⇔ paywall.check_free_quota 抛错
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest


@pytest.fixture(autouse=True)
def _reset_state():
    """每个用例前重置 billing 门控计数状态，保证用例独立。"""
    import billing
    billing._STATE["date"] = ""
    billing._STATE["count"] = 0
    yield


def test_paid_plans_unlimited():
    import billing
    for plan in ("pro", "team", "enterprise"):
        r = billing.check_access(plan=plan)
        assert r["allowed"] is True
        assert r["remaining"] == -1
        assert r["plan"] == plan


def test_free_quota_then_limit():
    import billing
    # 免费版拉满：3 条内放行
    for expect_remaining in (2, 1, 0):
        r = billing.check_access(plan="free")
        assert r["allowed"] is True, r
        assert r["remaining"] == expect_remaining, r
    # 第 4 条超限 → 结构化拒绝
    r = billing.check_access(plan="free")
    assert r["allowed"] is False
    assert r["remaining"] == 0
    assert r["http_status"] == 402
    assert "afdian.net" in r["upgrade_url"]


def test_paywall_free_quota_contract():
    """paywall.check_free_quota 原契约不变：Pro 软上限、免费超额抛 QuotaExceededError。"""
    import paywall
    assert paywall.check_free_quota(0, is_pro=True) == 100000
    assert paywall.check_free_quota(2, is_pro=False) == 1
    with pytest.raises(paywall.QuotaExceededError):
        paywall.check_free_quota(3, is_pro=False)


def test_two_entries_agree():
    """一致性：billing.check_access 结构化拒绝 ⇔ paywall.check_free_quota 抛错。"""
    import billing
    import paywall

    # 拉满免费额度
    for _ in range(paywall.FREE_DAILY_QUOTA):
        r = billing.check_access(plan="free")
        assert r["allowed"] is True

    # 超限：billing 返回结构化拒绝
    r = billing.check_access(plan="free")
    assert r["allowed"] is False

    # 同一额度状态：paywall 侧 check_free_quota(used=quota, is_pro=False) 也应抛错
    with pytest.raises(paywall.QuotaExceededError):
        paywall.check_free_quota(used_today=billing.PAYWALL_RULES["free"]["daily_limit"],
                                 is_pro=False)

    # 额度内：两边结论一致（billing 放行 + paywall 返回剩余额度）
    billing._STATE["date"] = ""
    billing._STATE["count"] = 0
    assert billing.check_access(plan="free")["allowed"] is True
    assert paywall.check_free_quota(used_today=0, is_pro=False) == paywall.FREE_DAILY_QUOTA
