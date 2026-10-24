# CHANGELOG

> ai-mcn-studio 变更日志（Keep a Changelog 结构，随 patch/feat/chore commit 补充）

## [Unreleased] — 2026-10-24

本周三端巡检自动补全（billing 收款层 / paywall 门控 / 文档 / 冒烟测试）

## 近期变更摘要

### 10-24

- `d7abd90` chore(probe): 三端同步探测探针文件（临时）
### 10-23

- `e487af4` feat(paywall): 入口接入有偿授权门控（check_access/paywall，免费版拉满+超限拦截）
- `b9bb05f` docs(week3): 补 QUICKSTART/ARCHITECTURE/BILLING + smoke_test.sh + run.sh
### 10-22

- `d96ab6a` ci: 三端全自动镜像（Gitee SSH + GitCode token）
- `c4c3544` docs(readme): 先体验后付费 + 用户回馈驱动迭代
- `e5f8083` docs(readme): 统一补「爱发电收款+社区发布」双区块（全仓共存）
- `f41e2e3` compliance: 补齐变现合规件 - LICENSE + 商用声明 + 定价规范

## 维护说明

- 遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/) 结构
- 格式：`commit_sha` 简述（feat/fix/chore/docs/refactor/test）
- 生成时间：2026-10-24