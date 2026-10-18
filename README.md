# ai-mcn-studio · AI 短剧/MCN 创作引擎

AI 短剧/MCN 全链路创作引擎：剧本生成 → 角色设定 → 分镜 → 视频提示词 → 合规审查 → 多平台分发。

## 快速上手

```bash
pip install -r requirements.txt
python main.py --generate "霸道总裁短剧" --platform douyin
```

## 变现路径

**免费**（3 条/天）→ **Pro**（¥99/月）→ **企业**（定制）
- 个人：爱发电赞助
- 企业：虎皮椒/爱收钱/微信商户网关
- 详见 [pricing.md](pricing.md) 与 [FUNDING.yml](FUNDING.yml)
- **付费门可演示**：`python3 paywall.py`（免费配额闸门 + 升级 Pro CTA + Pro 不限量放行）

## ⚖️ 法控声明（内容与数据）

- **内容免责**：本引擎产出的剧本/分镜/提示词**仅供创作参考**，发布前必须由人工完成合规审查与平台备案；AI 生成内容可能含违规/撞脸/版权风险，发布责任由使用者承担。
- **合规卡点**：`batch_compliance.py` 提供批量违规词扫描 + 投流/打回判定 + 变现钩子前置，作为发布前合规闸口，不替代法务审查。
- **数据脱敏**：引擎不采集/存储任何真实用户个人信息或账号凭据；示例内容走 CC-BY-NC 授权。

## License

MIT（代码）+ CC-BY-NC（示例内容）

> 内容仅供创作参考，发布前需人工合规审查。
