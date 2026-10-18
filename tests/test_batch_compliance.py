"""ai-mcn-studio 批量合规 + 变现钩子 测试。"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcn_studio.batch_compliance import (
    batch_produce_and_compliance,
    build_release_dashboard,
    build_monetization_hook,
)


class TestBatchCompliance(unittest.TestCase):
    def test_batch_split_pass_reject(self):
        topics = [
            {'title': '正常片名一'},
            {'title': '全网第一神医'},   # 含违规词"第一"
            {'title': '闪婚甜宠'},
        ]
        res = batch_produce_and_compliance(topics, platform='douyin', per_day_capacity=2)
        self.assertEqual(res.total, 3)
        self.assertEqual(res.passed, 2)
        self.assertEqual(res.rejected, 1)
        # 打回的是含违规词那条
        self.assertEqual(res.summary()['rejected_titles'], ['全网第一神医'])

    def test_schedule_days_by_capacity(self):
        topics = [{'title': f'第{i}部好剧'} for i in range(5)]
        res = batch_produce_and_compliance(topics, per_day_capacity=2)
        # 5 条 / 每天 2 条 → 第 3 天
        self.assertEqual(res.schedule_days, 3)

    def test_empty_topics(self):
        res = batch_produce_and_compliance([])
        self.assertEqual(res.total, 0)
        self.assertEqual(res.passed, 0)
        self.assertEqual(res.schedule_days, 0)

    def test_dashboard_contains_rejected_hint(self):
        topics = [{'title': '正常'}, {'title': '绝对最好的药'}]
        res = batch_produce_and_compliance(topics)
        txt = build_release_dashboard(res)
        self.assertIn('打回 1 条', txt)
        self.assertIn('备案', txt)

    def test_monetization_hook_revenue(self):
        topics = [{'title': f'好剧{i}'} for i in range(4)]
        res = batch_produce_and_compliance(topics, per_day_capacity=2)
        hook = build_monetization_hook(res, per_episode_price_cny=500.0)
        # 4 集 × 500 = 2000
        self.assertIn('¥2,000', hook)
        self.assertIn('收款入口', hook)
        self.assertIn('BufPay', hook)

    def test_monetization_hook_payment_channels_override(self):
        topics = [{'title': '好剧'}]
        res = batch_produce_and_compliance(topics)
        hook = build_monetization_hook(res, payment_channels=['微信支付'])
        self.assertIn('微信支付', hook)


if __name__ == '__main__':
    unittest.main()
