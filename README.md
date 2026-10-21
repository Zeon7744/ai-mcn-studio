# ai-mcn-studio

> **AI MCN Studio v3.0** — 多 Agent 协作驱动的短剧/内容生产工作流：24 名数字员工（编剧/导演/运营/合规），分级管理、批量生成、合规审查、多平台分发，内置爱发电订阅变现链路。

English: An AI-driven MCN studio that runs short-drama and content pipelines with 24 specialized agents — screenwriter, director, operations, compliance. Built-in paywall, Afdian subscription, and multi-platform distribution for Douyin / Hongguo / Kuaishou.

[![GitHub Stars](https://img.shields.io/github/stars/Zeon7744/ai-mcn-studio?style=social)](https://github.com/Zeon7744/ai-mcn-studio)
[![Gitee Stars](https://gitee.com/Zeon7744/ai-mcn-studio/badge/star.svg?theme=gvp)](https://gitee.com/Zeon7744/ai-mcn-studio)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)

---

## 市场定位（2026-10-22 锁定）

**赛道**：AI 内容 / MCN 工具（GitHub 搜索 700+ 结果，成熟红海）。
**差异化**：不拼单点功能，拼 **"24 数字员工多 Agent 协同 + 合规前置 + 订阅变现全链路"** —— 市场上同类项目（inkos、skill、social-media-skills）多为单 Agent 或 skill 集合，缺少 MCN 级组织化生产管线。

**目标用户**：
1. 短剧/漫剧独立创作者（个人，¥39-99/月 档）
2. 小型 MCN 团队（团队，¥99/月 Pro 档）
3. 需要合规前置的内容平台方（企业，¥999/月 定制档）

**对标与差距**：赛道 Top1 inkos 10,416 stars、Top2 skill 8,472 stars，均为通用创作 Agent；ai-mcn-studio 走垂直组织化路线，靠爱发电订阅 + 企业定制变现，不争夺 stars 头部位置。

---

## 快速开始

```bash
pip install -r requirements.txt
python -m mcn_studio.demo
```

## 核心功能

- **多 Agent 协作**：24 名数字员工，涵盖编剧、导演、运营、合规等角色
- **配额闸门**：免费用户每日 3 条额度，超限自动触发 Pro 升级 CTA
- **合规审查**：平台敏感词检测 + 价值导向过滤（`batch_compliance.py`）
- **批量生成**：Pro 用户支持 10 集/次批量产出
- **多平台分发**：抖音/红果/快手一键同步
- **变现全链路**：4 收款网关（noop/wepay/aishouqian/afdian）+ paywall 配额闸门，个人到企业三档

## 定价

| 档位 | 价格 | 权益 |
|------|------|------|
| 免费 | ¥0 | 3 条/天、基础角色卡 |
| Pro | ¥99/月 | 无限额度、批量、合规审查、多平台分发 |
| 企业 | ¥999/月 起 | 私有部署、API 接入、SLA |

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
