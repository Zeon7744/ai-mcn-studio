# ai-mcn-studio 收款与门控（爱发电/爱收钱）

## 定位
免费 3 条/天；Pro ¥99/月；企业 ¥999/月，通过爱发电 + 爱收钱双通道变现。

## 定价档位（与 pricing.md 对齐）
| 档位 | 价格 | 限制 |
|---|---|---|
| Free | ¥0 | 3 条/天 |
| Pro | ¥99/月 | 无限额度 + 批量 10 集/次 |
| 企业 | ¥999/月 | 私有部署 + API + SLA 99.9% |

## 收款流程（先体验后付费）
1. 免费 3 条/天，超限 402 + 升级 CTA
2. 爱发电赞赏码：https://afdian.net/@Zeon7744
3. 网关选择：`JZ_SAAS_BILLING_GATEWAY=noop|wepay|aishouqian|afdian`（默认 noop）

## 环境变量
`JZ_SAAS_AFDIAN_TOKEN` / `JZ_SAAS_AISHOUQIAN_MERCHANT` / `JZ_SAAS_BILLING_GATEWAY`
