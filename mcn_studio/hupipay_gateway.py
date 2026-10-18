# -*- coding: utf-8 -*-
"""
虎皮椒（Hupipay）收款网关 — ai-mcn-studio 专用

P0 改造项：接虎皮椒收款，¥99/月 Pro 订阅
复用 jianzhu-saas billing.py 的 HupipayGateway 骨架模式（统一接口 Gateway）

5 Secrets 配置（环境变量，不落代码）：
  HUPIPAY_APPID        — 虎皮椒应用 ID（必填）
  HUPIPAY_APPSECRET    — 虎皮椒应用密钥（必填，敏感）
  HUPIPAY_GATEWAY      — 虎皮椒 API 基址（默认 https://api.hupipay.com）
  HUPIPAY_NOTIFY_URL   — 异步通知地址（留空，走 query_callback 主动查单）
  HUPIPAY_RETURN_URL   — 支付成功跳转地址（填 GitHub Pages success 页）

前端 query_callback 主动查单：
  notify 留空 → 不依赖服务端回调
  return 填 GitHub Pages success 页（如 https://Zeon7744.github.io/ai-mcn-studio/hpj/success.html）
  前端支付成功后主动调 /billing/query?order_id=xxx 查询订单状态

设计原则：
- 与 jianzhu-saas billing.py 的 Gateway 接口完全对齐（create_order / query_callback / refund）
- 密钥未配时返回占位 order（不报错，便于 MVP 演示）
- 幂等：同一 order_id 重复查询返回相同结果
"""
from __future__ import annotations

import os
import time
import uuid
import hmac
import hashlib
import json
import urllib.request
from typing import Any, Dict, Optional

# ─── 统一网关基类（与 jianzhu-saas billing.py 对齐）──────────────────────────
class Gateway:
    name = "base"

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def create_order(self, tenant_id: str, amount_cents: int, product: str, plan: str, order_meta: Optional[Dict] = None) -> Dict[str, Any]:
        raise NotImplementedError

    def query_callback(self, order_id: str) -> Dict[str, Any]:
        raise NotImplementedError

    def refund(self, order_id: str, amount_cents: int, reason: str = "") -> Dict[str, Any]:
        raise NotImplementedError


# ─── HupipayGateway ───────────────────────────────────────────────────────────
def _secret(*names: str) -> Optional[str]:
    """从环境变量取第一个非空值。"""
    for n in names:
        v = os.environ.get(n)
        if v:
            return v
    return None


class HupipayGateway(Gateway):
    """
    虎皮椒（Hupipay）支付网关。

    环境变量：
      HUPIPAY_APPID        — 应用 ID（必填）
      HUPIPAY_APPSECRET    — 应用密钥（必填，敏感，不落代码）
      HUPIPAY_GATEWAY      — API 基址（默认 https://api.hupipay.com）
      HUPIPAY_NOTIFY_URL   — 异步通知 URL（留空，走主动查单）
      HUPIPAY_RETURN_URL   — 支付成功跳转 URL（建议填 GitHub Pages success 页）

    接口文档（参考）：https://www.hupipay.com/docs/api
    """

    name = "hupipay"
    DEFAULT_BASE = "https://api.hupipay.com"

    def _cred(self) -> Dict[str, str]:
        return {
            "appid": _secret("HUPIPAY_APPID", "JZ_SAAS_XUNHU_APPID"),
            "appsecret": _secret("HUPIPAY_APPSECRET", "JZ_SAAS_XUNHU_APPSECRET"),
            "gateway": os.environ.get("HUPIPAY_GATEWAY",
                             os.environ.get("JZ_SAAS_XUNHU_GATEWAY", self.DEFAULT_BASE)),
            "notify": os.environ.get("HUPIPAY_NOTIFY_URL",
                       os.environ.get("JZ_SAAS_XUNHU_NOTIFY", "")),
            "return_url": os.environ.get("HUPIPAY_RETURN_URL",
                            os.environ.get("JZ_SAAS_XUNHU_RETURN", "")),
        }

    def _missing_keys(self, cred: Dict) -> list:
        return [k for k in ("appid", "appsecret") if not cred.get(k)]

    def _sign(self, payload: Dict, appsecret: str) -> str:
        """Hupipay 签名：对排序后的参数做 MD5，再拼接 appsecret 做 HMAC-SHA256。"""
        sorted_params = sorted(payload.items(), key=lambda x: x[0])
        sign_str = "&".join(f"{k}={v}" for k, v in sorted_params if v is not None)
        hmac_sig = hmac.new(
            appsecret.encode("utf-8"),
            sign_str.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        return hmac_sig

    def _post(self, path: str, payload: Dict) -> Dict:
        """POST 请求封装。"""
        url = self._cred()["gateway"].rstrip("/") + path
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def create_order(
        self,
        tenant_id: str,
        amount_cents: int,
        product: str,
        plan: str,
        order_meta: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """
        创建订单。

        返回字段（与 jianzhu-saas billing.py 对齐）：
          order_id, status, amount_cents, plan, product, ts, pay_url, meta
          needs_secret（密钥缺失时）
        """
        cred = self._cred()
        missing = self._missing_keys(cred)
        oid = "hp_" + str(uuid.uuid4())[:12]

        base_result = {
            "order_id": oid,
            "status": "created_pending_key" if missing else "created",
            "amount_cents": amount_cents,
            "plan": plan,
            "product": product,
            "ts": int(time.time()),
            "gateway": "hupipay",
            "meta": order_meta or {},
        }

        if missing:
            base_result["needs_secret"] = [
                f"HUPIPAY_{k.upper()}" if k in ("appid", "appsecret")
                else f"JZ_SAAS_XUNHU_{k.upper()}"
                for k in missing
            ]
            return base_result

        # 构造请求体
        timestamp = str(int(time.time()))
        nonce = str(uuid.uuid4())[:16]
        body = {
            "appid": cred["appid"],
            "out_trade_no": oid,
            "total_fee": amount_cents,
            "subject": f"{product}({plan})",
            "body": f"AI MCN Studio Pro {plan}",
            "notify_url": cred["notify"] or "",
            "return_url": cred["return_url"],
            "timestamp": timestamp,
            "nonce": nonce,
        }
        body["sign"] = self._sign(body, cred["appsecret"])

        try:
            resp = self._post("/v1/pay/create", body)
        except Exception as e:
            base_result["status"] = "gateway_error"
            base_result["error"] = str(e)
            return base_result

        code = resp.get("code", -1)
        if code != 0:
            base_result["status"] = "gateway_rejected"
            base_result["code"] = code
            base_result["msg"] = resp.get("message", "")
            return base_result

        data = resp.get("data", {})
        base_result["pay_url"] = data.get("pay_url", data.get("url", ""))
        base_result["qrcode_url"] = data.get("qrcode_url", "")
        return base_result

    def query_callback(self, order_id: str) -> Dict[str, Any]:
        """
        主动查单（notify 留空时的主要查询方式）。

        返回：{order_id, status, paid, gateway}
        """
        cred = self._cred()
        if self._missing_keys(cred):
            return {"order_id": order_id, "status": "pending_key", "paid": False, "note": "HUPIPAY_APPID/APPSECRET 未配"}

        timestamp = str(int(time.time()))
        nonce = str(uuid.uuid4())[:16]
        body = {
            "appid": cred["appid"],
            "out_trade_no": order_id,
            "timestamp": timestamp,
            "nonce": nonce,
        }
        body["sign"] = self._sign(body, cred["appsecret"])

        try:
            resp = self._post("/v1/pay/query", body)
        except Exception as e:
            return {"order_id": order_id, "status": "query_failed", "paid": False, "error": str(e)}

        code = resp.get("code", -1)
        if code != 0:
            return {"order_id": order_id, "status": "query_error", "paid": False, "code": code, "msg": resp.get("message", "")}

        data = resp.get("data", {})
        paid_status = data.get("trade_status", "")
        paid = paid_status in ("SUCCESS", "PAID", "FINISHED")
        return {
            "order_id": order_id,
            "status": paid_status,
            "paid": paid,
            "gateway": "hupipay",
            "trade_no": data.get("trade_no", ""),
        }

    def refund(self, order_id: str, amount_cents: int, reason: str = "") -> Dict[str, Any]:
        """退款（预留接口）。"""
        cred = self._cred()
        if self._missing_keys(cred):
            return {"order_id": order_id, "ok": False, "note": "HUPIPAY_APPID/APPSECRET 未配", "gateway": "hupipay"}

        timestamp = str(int(time.time()))
        nonce = str(uuid.uuid4())[:16]
        body = {
            "appid": cred["appid"],
            "out_trade_no": order_id,
            "refund_fee": amount_cents,
            "reason": reason or "用户申请退款",
            "timestamp": timestamp,
            "nonce": nonce,
        }
        body["sign"] = self._sign(body, cred["appsecret"])

        try:
            resp = self._post("/v1/pay/refund", body)
        except Exception as e:
            return {"order_id": order_id, "ok": False, "error": str(e), "gateway": "hupipay"}

        ok = resp.get("code", -1) == 0
        return {
            "order_id": order_id,
            "ok": ok,
            "refunded_cents": amount_cents if ok else 0,
            "reason": reason,
            "gateway": "hupipay",
        }


# ─── 注册到全局（与 jianzhu-saas billing.py 对齐）────────────────────────────
_BUILTIN_REGISTRY: Dict[str, type] = {}


def register_gateway(cls):
    _BUILTIN_REGISTRY[cls.name] = cls
    return cls


register_gateway(HupipayGateway)


def get_hupipay_gateway() -> HupipayGateway:
    """获取 Hupipay 网关实例（密钥未配时仍可调用，返回占位结果）。"""
    return HupipayGateway()


# ─── 便捷入口（与 jianzhu-saas billing.py 对齐）──────────────────────────────
def create_pro_order(
    user_id: str,
    amount_cents: int = 9900,   # ¥99
    product: str = "ai-mcn-studio-pro",
    plan: str = "pro_monthly",
) -> Dict[str, Any]:
    """
    创建 Pro 订阅订单（¥99/月）。

    便捷入口，与 paywall.py 的 produce_episodes 对接。
    """
    g = get_hupipay_gateway()
    return g.create_order(user_id, amount_cents, product, plan)


def query_order(order_id: str) -> Dict[str, Any]:
    """主动查单（notify 留空方案的核心查询方式）。"""
    g = get_hupipay_gateway()
    return g.query_callback(order_id)


# ─── CLI 测试入口 ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="HupipayGateway 测试")
    parser.add_argument("--action", choices=["create", "query", "refund"], default="create")
    parser.add_argument("--order-id", default=None, help="订单 ID（query/refund 用）")
    parser.add_argument("--user-id", default="demo_user", help="用户 ID")
    parser.add_argument("--amount", type=int, default=9900, help="金额（分）")
    args = parser.parse_args()

    g = get_hupipay_gateway()

    if args.action == "create":
        order = g.create_order(args.user_id, args.amount, "ai-mcn-studio-pro", "pro_monthly")
        print(json.dumps(order, ensure_ascii=False, indent=2))
    elif args.action == "query" and args.order_id:
        result = g.query_callback(args.order_id)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.action == "refund" and args.order_id:
        result = g.refund(args.order_id, args.amount)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        parser.print_help()
