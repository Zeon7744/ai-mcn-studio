# ai-mcn-studio

## 💰 价值主张 & 定价
> **能卖什么**：AI 短剧批量生产引擎 — 选题→剧本→分镜→多平台分发，10 分钟出 1 部 30s 短视频，24 名数字员工 + 合规审查内置。
>
> **定价**：免费（3 条/天 + 基础角色卡）/ **Pro ¥99/月**（不限条数 + 批量 10 集/次 + 合规 + 多平台分发）/ **企业 ¥999/月**（私有部署 + API + SLA 99.9%）。付费渠道：[爱发电 @Zeon7744](https://afdian.net/@Zeon7744)


> AI MCN Studio v3.0 — 多 Agent 协作驱动的短剧/内容生产工作流，支持 24 名数字员工、分级管理、批量生成与合规审查。

[![GitHub Stars](https://img.shields.io/github/stars/Zeon7744/ai-mcn-studio?style=social)](https://github.com/Zeon7744/ai-mcn-studio)
[![Gitee Stars](https://gitee.com/Zeon7744/ai-mcn-studio/badge/star.svg?theme=gvp)](https://gitee.com/Zeon7744/ai-mcn-studio)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)

## 快速开始

```bash
pip install -r requirements.txt
python -m mcn_studio.demo
```

## 核心功能

- **多 Agent 协作**：24 名数字员工，涵盖编剧、导演、运营、合规等角色
- **配额闸门**：免费用户每日 3 条额度，超限自动触发 Pro 升级 CTA
- **合规审查**：平台敏感词检测 + 价值导向过滤
- **批量生成**：Pro 用户支持 10 集/次批量产出
- **多平台分发**：抖音/红果/快手一键同步

## 定价

| 档位 | 价格 | 权益 |
|------|------|------|
| 免费 | ¥0 | 3 条/天、基础角色卡 |
| Pro | ¥99/月 | 无限额度、批量、合规审查、多平台分发 |
| 企业 | 定制 | 私有部署、API 接入、SLA |

详见 [pricing.md](pricing.md)。

## 收款通道

- **个人**：爱发电（afdian.net）— 零备案域名，token 鉴权，推荐首选
- **企业**：爱收钱 / 微信商户（需企业主体）

## 法控声明

- **内容免责**：本引擎产出的剧本/分镜/提示词**仅供创作参考**，发布前必须由人工完成合规审查与平台备案
- **合规卡点**：`batch_compliance.py` 提供批量违规词扫描 + 投流/打回判定 + 变现钩子前置
- **数据脱敏**：引擎不采集/存储任何真实用户个人信息或账号凭据

## License

MIT（代码）+ CC-BY-NC（示例内容）

> 内容仅供创作参考，发布前需人工合规审查。


---

## 💰 订阅支持

| 档位 | 价格 | 核心权益 |
|------|------|----------|
| 免费 | ¥0 | 3 条/天、基础角色卡 |
| Pro | ¥99/月 | 无限额度 + 批量 + 多平台分发 |
| 企业 | ¥999/月 | 私有部署 + API + SLA |

👉 **[立即订阅 — 爱发电](https://afdian.net/@Zeon7744)**（支付宝 / 微信支付）

> 详细定价见 [pricing.md](pricing.md)
