# -*- coding: utf-8 -*-
"""
AI MCN Studio P0 整改验收测试

验证项：
1. batch_producer.py — 输入 IP → 输出 30 集大纲（可下载）
2. compliance_checker.py — 红果/抖音 ≥5 条规则，通过/不通过 + 原因 + 建议
3. hupipay_gateway.py — 网关骨架可用，query_callback 主动查单
4. paywall.py — 付费门 + Hupipay 集成
"""
import sys
import os
import json
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _check(label, ok, detail=""):
    mark = "PASS" if ok else "FAIL"
    print(f"  [{mark}] {label}" + (f" — {detail}" if detail and not ok else ""))
    return ok


def test_batch_producer():
    print("\n=== 1. batch_producer.py ===")
    all_ok = True

    from mcn_studio.batch_producer import generate_batch_outline, save_to_md, save_to_txt

    # 1a 生成 30 集大纲
    result = generate_batch_outline("重生之我在末世当首富", "逆袭爽剧", total_episodes=30)
    ok = _check("生成 30 集大纲", result.total_episodes == 30, f"实际 {result.total_episodes}")
    all_ok &= ok

    # 1b 每集有基本字段
    ep = result.episodes[0]
    ok = _check("第1集字段完整", all([ep.title, ep.hook, ep.core_event, ep.conflict, ep.cliffhanger]),
                f"title={bool(ep.title)} hook={bool(ep.hook)}")
    all_ok &= ok

    # 1c 全部 30 集都有标题
    all_have_title = all(ep.title for ep in result.episodes)
    ok = _check("30 集均有标题", all_have_title)
    all_ok &= ok

    # 1d 保存 md 文件
    with tempfile.NamedTemporaryFile(suffix=".md", delete=False, mode="w", encoding="utf-8") as f:
        tmp_md = f.name
    try:
        path = save_to_md(result, tmp_md)
        size = os.path.getsize(path)
        ok = _check("保存 MD 文件", size > 1000, f"大小 {size} bytes")
        all_ok &= ok
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        ok = _check("MD 含第01集标题", "第01集" in content)
        all_ok &= ok
    finally:
        os.unlink(path)

    # 1e 保存 txt 文件
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False, mode="w", encoding="utf-8") as f:
        tmp_txt = f.name
    try:
        path = save_to_txt(result, tmp_txt)
        size = os.path.getsize(path)
        ok = _check("保存 TXT 文件", size > 500, f"大小 {size} bytes")
        all_ok &= ok
    finally:
        os.unlink(path)

    # 1f 不同选题方向模板
    result2 = generate_batch_outline("闪婚甜宠总裁大人", "甜宠", total_episodes=30)
    ok = _check("甜宠选题生成", result2.total_episodes == 30)
    all_ok &= ok

    result3 = generate_batch_outline("迷雾追踪", "悬疑推理", total_episodes=30)
    ok = _check("悬疑选题生成", result3.total_episodes == 30)
    all_ok &= ok

    # 1g 自定义集数
    result4 = generate_batch_outline("测试IP", "逆袭爽剧", total_episodes=10)
    ok = _check("自定义集数=10", result4.total_episodes == 10)
    all_ok &= ok

    return all_ok


def test_compliance_checker():
    print("\n=== 2. compliance_checker.py ===")
    all_ok = True

    from mcn_studio.compliance_checker import compliance_check, ComplianceResult

    # 2a 抖音：违规文本 → 不通过
    bad_text = "这款面霜全网第一，100%有效，根治湿疹！"
    r = compliance_check(bad_text, platform="douyin")
    ok = _check("抖音违规文本 → 不通过", not r.passed, f"passed={r.passed}")
    all_ok &= ok

    # 2b 违规文本有原因和建议
    ok = _check("违规文本有 issues", r.failed_count > 0, f"issues={r.failed_count}")
    all_ok &= ok

    if r.issues:
        iss = r.issues[0]
        ok = _check("issue 有 suggestion", bool(iss.suggestion), f"suggestion={iss.suggestion[:30]}")
        all_ok &= ok
        ok = _check("issue 有 detail", bool(iss.detail))
        all_ok &= ok

    # 2c 抖音：干净文本 → 通过
    clean_text = "大家好，今天分享三款好用的效率工具，提升工作效率"
    r2 = compliance_check(clean_text, platform="douyin")
    ok = _check("抖音干净文本 → 通过", r2.passed, f"passed={r2.passed}, issues={r2.failed_count}")
    all_ok &= ok

    # 2d 红果：≥5 条规则检查
    r3 = compliance_check("测试内容", platform="红果")
    ok = _check("红果总规则数 ≥ 5", r3.total_rules_checked >= 5, f"total_rules={r3.total_rules_checked}")
    all_ok &= ok

    # 2e 红果：违规文本 → 不通过（含 AI 标注检查）
    r4 = compliance_check("AI生成内容 全网第一 根治颈椎病", platform="红果")
    ok = _check("红果违规文本 → 不通过", not r4.passed, f"passed={r4.passed}")
    all_ok &= ok

    # 2f 结果可序列化
    d = r3.summary_dict()
    ok = _check("summary_dict 可序列化", isinstance(d, dict) and "passed" in d and "issues" in d)
    all_ok &= ok

    # 2g to_text 输出可读
    txt = r3.to_text()
    ok = _check("to_text 输出非空", len(txt) > 10)
    all_ok &= ok

    return all_ok


def test_hupipay_gateway():
    print("\n=== 3. hupipay_gateway.py ===")
    all_ok = True

    from mcn_studio.hupipay_gateway import HupipayGateway, get_hupipay_gateway, create_pro_order, query_order

    # 3a 网关实例化
    g = get_hupipay_gateway()
    ok = _check("HupipayGateway 实例化", isinstance(g, HupipayGateway))
    all_ok &= ok

    # 3b 创建订单（密钥未配 → 占位）
    order = g.create_order("test_user", 9900, "ai-mcn-studio-pro", "pro_monthly")
    ok = _check("create_order 返回 order_id", bool(order.get("order_id")))
    all_ok &= ok
    ok = _check("create_order 含 gateway=hupipay", order.get("gateway") == "hupipay")
    all_ok &= ok
    ok = _check("create_order 含 amount_cents=9900", order.get("amount_cents") == 9900)
    all_ok &= ok

    # 3c 主动查单（密钥未配 → pending_key）
    q = g.query_callback(order.get("order_id", "test_oid"))
    ok = _check("query_callback 返回 paid 字段", "paid" in q)
    all_ok &= ok

    # 3d 便捷入口 create_pro_order
    order2 = create_pro_order("demo_user")
    ok = _check("create_pro_order 便捷入口", order2.get("amount_cents") == 9900)
    all_ok &= ok

    # 3e 退款接口存在
    ref = g.refund(order.get("order_id", "test_oid"), 9900, "用户申请")
    ok = _check("refund 接口可用", "order_id" in ref and "ok" in ref)
    all_ok &= ok

    return all_ok


def test_paywall_integration():
    print("\n=== 4. paywall.py + Hupipay 集成 ===")
    all_ok = True

    import paywall

    # 4a 基本配额闸门逻辑不变
    r = paywall.produce_episodes(["a", "b", "c", "d", "e"], used_today=2, is_pro=False)
    ok = _check("配额闸门：剩1条", r["produced"] == 1 and r["hit_free_quota"])
    all_ok &= ok

    # 4b Pro 用户不限量
    r2 = paywall.produce_episodes(["a", "b", "c", "d", "e"], used_today=0, is_pro=True)
    ok = _check("Pro 用户不限量", r2["produced"] == 5 and not r2["hit_free_quota"])
    all_ok &= ok

    # 4c 集成 Hupipay create_pro_order
    order = paywall.create_pro_order("test_user_001")
    ok = _check("create_pro_order 返回 order_id", bool(order.get("order_id")))
    all_ok &= ok
    ok = _check("create_pro_order 金额正确", order.get("amount_cents") == 9900)
    all_ok &= ok
    ok = _check("create_pro_order 网关=hupipay", order.get("gateway") == "hupipay")
    all_ok &= ok

    # 4d query_order_status
    oid = order.get("order_id", "test")
    status = paywall.query_order_status(oid)
    ok = _check("query_order_status 返回 paid", "paid" in status)
    all_ok &= ok

    # 4e activate_pro_benefit
    benefit = paywall.activate_pro_benefit("test_user_001")
    ok = _check("activate_pro_benefit 返回 pro=True", benefit.get("pro") is True)
    all_ok &= ok
    ok = _check("activate_pro_benefit 有 3 项权益", len(benefit.get("benefits", [])) == 3)
    all_ok &= ok

    return all_ok


def main():
    print("=" * 60)
    print("AI MCN Studio P0 整改验收测试")
    print("=" * 60)

    results = {
        "batch_producer": test_batch_producer(),
        "compliance_checker": test_compliance_checker(),
        "hupipay_gateway": test_hupipay_gateway(),
        "paywall_integration": test_paywall_integration(),
    }

    print("\n" + "=" * 60)
    all_pass = all(results.values())
    for k, v in results.items():
        mark = "✔" if v else "✘"
        print(f"  {mark} {k}")
    print(f"\n结果：{'全部通过 ✔' if all_pass else '存在失败项 ✘'}")
    print("=" * 60)
    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
