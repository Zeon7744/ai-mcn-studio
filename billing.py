# -*- coding: utf-8 -*-
"""ai-mcn-studio 收款模块（轻量版，仅支持爱发电）。

从 jianzhu-saas billing.py 精简而来，去掉 store 依赖，保留 AfdianGateway。
环境变量与 jianzhu-saas 保持一致：
  JZ_SAAS_BILLING_GATEWAY  = afdian
  JZ_SAAS_AFDIAN_USER      = 爱发电 user_id
  JZ_SAAS_AFDIAN_TOKEN     = 爱发电 API token
  JZ_SAAS_AFDIAN_RETURN    = 支付成功跳转地址
  JZ_SAAS_AFDIAN_BASE      = 爱发电 API 基址（可选）
"""
import os
import time
import uuid
import json
import urllib.request

# 统一网关选择
BILLING_GATEWAY = os.environ.get("JZ_SAAS_BILLING_GATEWAY", "afdian")


def _secret(*names):
    for n in names:
        v = os.environ.get(n)
        if v:
            return v
    return None


class AfdianGateway:
    """爱发电支付网关（个人创作者推荐）。"""

    name = "afdian"
    DEFAULT_BASE = "https://afdian.net/api"

    def __init__(self):
        self.user_id = os.environ.get("JZ_SAAS_AFDIAN_USER", "")
        self.token = _secret("JZ_SAAS_AFDIAN_TOKEN")
        self.base = os.environ.get("JZ_SAAS_AFDIAN_BASE", self.DEFAULT_BASE)
        self.return_url = os.environ.get("JZ_SAAS_AFDIAN_RETURN", "")

    def _post(self, path: str, payload: dict) -> dict:
        body = dict(payload)
        if self.token:
            body["token"] = self.token
        req = urllib.request.Request(
            f"{self.base}{path}",
            data=json.dumps(body).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def create_order(self, tenant_id: str, amount_cents: int, product: str, plan: str, order_meta=None) -> dict:
        """创建订单。"""
        if not self.user_id or not self.token:
            oid = "afdian_" + str(uuid.uuid4())[:12]
            return {
                "order_id": oid,
                "status": "created_pending_key",
                "amount_cents": amount_cents,
                "plan": plan,
                "product": product,
                "gateway": "afdian",
                "needs_secret": ["JZ_SAAS_AFDIAN_USER", "JZ_SAAS_AFDIAN_TOKEN"],
                "note": "user_id/token 未配，无法真实下单",
            }

        price = round(amount_cents / 100.0, 2)
        out_trade_no = "mcn_" + str(uuid.uuid4())[:16]
        payload = {
            "user_id": self.user_id,
            "price": str(price),
            "name": f"{product}({plan})"[:42],
            "out_trade_no": out_trade_no,
        }
        if self.return_url:
            payload["return_url"] = self.return_url

        try:
            result = self._post("/payment/create", payload)
        except Exception as e:
            return {"order_id": out_trade_no, "status": "gateway_error", "error": str(e), "gateway": "afdian"}

        code = result.get("code", -1)
        if code != 0:
            return {"order_id": out_trade_no, "status": "gateway_rejected", "code": code, "msg": result.get("message", ""), "gateway": "afdian"}

        data = result.get("data", {})
        return {
            "order_id": out_trade_no,
            "status": "created",
            "amount_cents": amount_cents,
            "plan": plan,
            "product": product,
            "gateway": "afdian",
            "pay_url": data.get("url", ""),
            "qrcode_url": data.get("qrcode_url", ""),
            "out_trade_no": out_trade_no,
            "ts": int(time.time()),
        }

    def query_callback(self, order_id: str) -> dict:
        """查询订单状态。"""
        if not self.user_id or not self.token:
            return {"order_id": order_id, "status": "pending_key", "paid": False}
        try:
            result = self._post("/payment/query", {"user_id": self.user_id, "out_trade_no": order_id})
            data = result.get("data", {})
            paid = data.get("status") in ("paid", "success")
            return {"order_id": order_id, "status": data.get("status", "unknown"), "paid": paid, "gateway": "afdian"}
        except Exception as e:
            return {"order_id": order_id, "status": "query_failed", "paid": False, "error": str(e)}

    def verify_callback(self, payload: dict) -> bool:
        """验证回调 token。"""
        return payload.get("token") == self.token


# 注册表（供 paywall.py 使用）
_registries = {"afdian": AfdianGateway}

# 默认实例（兼容旧调用方式）
def get_gateway():
    return _registries.get(BILLING_GATEWAY, AfdianGateway)()
