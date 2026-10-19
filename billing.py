# -*- coding: utf-8 -*-
"""
ai-mcn-studio 收款模块（内嵌版）
兼容 jianzhu-saas billing.py 接口，支持爱发电 + 爱收钱 + 微信商户 + noop占位。
密钥走环境变量，不落代码。
"""
from __future__ import annotations

import os
import time
import uuid
import json
import urllib.request
from typing import Optional

# ── 配置 ─────────────────────────────────────────────────────────────────────
DEFAULT_BASE = "https://afdian.com/api"

_BILLING_GATEWAY = os.environ.get("AI_MCN_BILLING_GATEWAY", os.environ.get("JZ_SAAS_BILLING_GATEWAY", "noop"))

BUILTIN_REGISTRY = {}


def _secret(*names):
    """从环境变量取密钥，优先 AI_MCN_* 前缀，其次 JZ_SAAS_*。"""
    for n in names:
        v = os.environ.get(f"AI_MCN_{n}") or os.environ.get(f"JZ_SAAS_{n}")
        if v:
            return v
    return None


def register_gateway(cls):
    BUILTIN_REGISTRY[cls.name] = cls
    return cls


# ── Gateway 基类 ──────────────────────────────────────────────────────────────
class Gateway:
    name = "base"

    def create_order(self, tenant_id: str, amount_cents: int, product: str, plan: str, order_meta: dict = None) -> dict:
        raise NotImplementedError

    def query_callback(self, order_id: str) -> dict:
        raise NotImplementedError

    def refund(self, order_id: str, amount_cents: int, reason: str = "") -> dict:
        raise NotImplementedError


# ── NoopGateway（占位）────────────────────────────────────────────────────────
@register_gateway
class NoopGateway(Gateway):
    name = "noop"

    def create_order(self, tenant_id, amount_cents, product, plan, order_meta=None):
        oid = "noop_" + str(uuid.uuid4())[:12]
        return {
            "order_id": oid, "status": "created", "amount_cents": amount_cents,
            "plan": plan, "product": product, "gateway": "noop",
            "note": "占位订单，未接真实支付网关",
        }

    def query_callback(self, order_id):
        return {"order_id": order_id, "status": "unverified", "paid": False, "gateway": "noop"}

    def refund(self, order_id, amount_cents, reason=""):
        return {"order_id": order_id, "ok": False, "note": "noop网关不支持退款"}


# ── AfdianGateway（爱发电）───────────────────────────────────────────────────
@register_gateway
class AfdianGateway(Gateway):
    name = "afdian"

    def _cred(self) -> dict:
        return {
            "user_id": _secret("AFDIAN_USER_ID", "JZ_SAAS_AFDIAN_USER_ID") or "",
            "token":  _secret("AFDIAN_TOKEN",  "JZ_SAAS_AFDIAN_TOKEN")  or "",
            "base":   os.environ.get("AFDIAN_BASE", DEFAULT_BASE),
        }

    def _post(self, path: str, payload: dict) -> dict:
        c = self._cred()
        body = dict(payload)
        if c.get("token"):
            body["token"] = c["token"]
        req = urllib.request.Request(
            f"{c['base']}{path}",
            data=json.dumps(body).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def _missing(self, c: dict) -> list:
        return [k for k in ("user_id", "token") if not c.get(k)]

    def create_order(self, tenant_id, amount_cents, product, plan, order_meta=None):
        c = self._cred()
        missing = self._missing(c)
        if missing:
            oid = "afdian_" + str(uuid.uuid4())[:12]
            return {
                "order_id": oid, "status": "created_pending_key",
                "amount_cents": amount_cents, "plan": plan,
                "product": product, "gateway": "afdian",
                "needs_secret": [f"AFDIAN_{k.upper()}" for k in missing],
                "note": "user_id/token 未配，无法真实下单",
            }
        price = round(amount_cents / 100.0, 2)
        out_trade_no = "mcn_" + str(uuid.uuid4())[:16]
        payload = {
            "user_id": c["user_id"], "price": str(price),
            "name": f"{product}({plan})"[:42],
            "out_trade_no": out_trade_no,
        }
        try:
            result = self._post("/payment/create", payload)
        except Exception as e:
            return {"order_id": out_trade_no, "status": "gateway_error",
                    "amount_cents": amount_cents, "plan": plan,
                    "gateway": "afdian", "error": str(e)}
        code = result.get("code", -1)
        if code != 0:
            return {"order_id": out_trade_no, "status": "gateway_rejected",
                    "amount_cents": amount_cents, "plan": plan,
                    "gateway": "afdian", "code": code,
                    "msg": result.get("message", "")}
        data = result.get("data", {})
        return {
            "order_id": out_trade_no, "status": "created",
            "amount_cents": amount_cents, "plan": plan,
            "product": product, "gateway": "afdian",
            "pay_url": data.get("url", ""),
            "qrcode_url": data.get("qrcode_url", ""),
            "out_trade_no": out_trade_no,
            "ts": int(time.time()),
        }

    def query_callback(self, order_id: str) -> dict:
        c = self._cred()
        if not c.get("user_id") or not c.get("token"):
            return {"order_id": order_id, "status": "pending_key", "paid": False, "gateway": "afdian"}
        try:
            result = self._post("/payment/query", {"user_id": c["user_id"], "out_trade_no": order_id})
            code = result.get("code", -1)
            if code != 0:
                return {"order_id": order_id, "status": "query_error", "paid": False,
                        "gateway": "afdian", "code": code, "msg": result.get("message", "")}
            data = result.get("data", {})
            paid = data.get("status") in ("paid", "success")
            return {"order_id": order_id, "status": data.get("status", "unknown"),
                    "paid": paid, "gateway": "afdian"}
        except Exception as e:
            return {"order_id": order_id, "status": "query_failed", "paid": False,
                    "error": str(e), "gateway": "afdian"}

    def verify_callback(self, payload: dict) -> bool:
        c = self._cred()
        if not c.get("token"):
            return False
        return payload.get("token") == c["token"]

    def refund(self, order_id, amount_cents, reason=""):
        c = self._cred()
        if not c.get("user_id") or not c.get("token"):
            return {"order_id": order_id, "ok": False, "note": "user_id/token 未配", "gateway": "afdian"}
        price = round(amount_cents / 100.0, 2)
        payload = {"user_id": c["user_id"], "out_trade_no": order_id, "price": str(price)}
        if reason:
            payload["reason"] = reason
        try:
            result = self._post("/payment/refund", payload)
            ok = result.get("code", -1) == 0
            return {"order_id": order_id, "ok": ok, "refunded_cents": amount_cents if ok else 0,
                    "reason": reason, "gateway": "afdian",
                    "code": result.get("code"), "msg": result.get("message", "")}
        except Exception as e:
            return {"order_id": order_id, "ok": False, "error": str(e), "gateway": "afdian"}


# ── 工厂函数 ──────────────────────────────────────────────────────────────────
def get_gateway(name: str = None) -> Gateway:
    """返回当前配置的网关实例。"""
    cls_name = name or _BILLING_GATEWAY
    cls = BUILTIN_REGISTRY.get(cls_name, NoopGateway)
    return cls()


def create_order(tenant_id, amount_cents, product, plan, order_meta=None):
    return get_gateway().create_order(tenant_id, amount_cents, product, plan, order_meta)


def query_callback(order_id):
    return get_gateway().query_callback(order_id)


def refund(order_id, amount_cents, reason=""):
    return get_gateway().refund(order_id, amount_cents, reason)
