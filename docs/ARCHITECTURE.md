# ai-mcn-studio 模块结构

## 目录
```
ai-mcn-studio/
├── paywall.py        # 免费 3 条/天 配额闸门 + 升级 CTA
├── billing.py        # 收款层：NoopGateway/WxPay/Aishouqian/Afdian 四网关
├── store.py          # 租户内存存储（匹配 jianzhu-saas 接口）
├── index.html        # 变现展示页（hero + 定价 + CTA）
├── pricing.md        # 定价档位
└── docs/
```

## 数据流
1. 用户 → 免费 3 条/天 → 超限触发 402 CTA
2. 付费 → Pro ¥99/月 / 企业 ¥999/月
3. `billing.py` 根据 `JZ_SAAS_BILLING_GATEWAY` 选择网关（默认 noop）

## 门控模型
- `FREE_DAILY_QUOTA=3`；`PRO_PRICE_CNY=99`；企业定制 ¥999/月
