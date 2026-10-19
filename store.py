# -*- coding: utf-8 -*-
"""
ai-mcn-studio 轻量租户存储（内存版，匹配 jianzhu-saas store.py 接口）
 billing.py 依赖 from store import tsvc
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


PLAN_CREDIT = {"free": 100, "pro": 10000, "enterprise": 999999}


@dataclass
class Tenant:
    tenant_id: str
    plan: str = "free"
    credits: int = 100
    is_pro: bool = False
    created: str = ""

    def to_dict(self):
        return {
            "tenant_id": self.tenant_id,
            "plan": self.plan,
            "credits": self.credits,
            "is_pro": self.is_pro,
            "created": self.created,
        }


class TenantService:
    def __init__(self):
        self._tenants: dict[str, Tenant] = {}

    def get(self, tenant_id: str) -> Optional[Tenant]:
        return self._tenants.get(tenant_id)

    def set_plan(self, tenant_id: str, plan: str, credits: Optional[int] = None) -> Optional[Tenant]:
        if plan not in PLAN_CREDIT:
            return None
        t = self._tenants.get(tenant_id)
        if not t:
            t = Tenant(tenant_id=tenant_id, plan=plan, credits=PLAN_CREDIT.get(plan, 100))
            self._tenants[tenant_id] = t
        else:
            t.plan = plan
            t.credits = PLAN_CREDIT.get(plan, 100) if credits is None else credits
            t.is_pro = plan in ("pro", "enterprise")
        return t

    def topup_credit(self, tenant_id: str, amount: int) -> Optional[Tenant]:
        if amount <= 0:
            return None
        t = self._tenants.get(tenant_id)
        if not t:
            return None
        t.credits += amount
        return t

    def deduct_credit(self, tenant_id: str, cost: int) -> bool:
        t = self._tenants.get(tenant_id)
        if not t or t.credits < cost:
            return False
        t.credits -= cost
        return True

    def list_tenants(self, limit: int = 100) -> list[dict]:
        return [t.to_dict() for t in self._tenants.values()[:limit]]


tsvc = TenantService()
