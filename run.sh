#!/usr/bin/env bash
# ai-mcn-studio 一键启动演示
set -euo pipefail
cd "$(dirname "$0")"
python3 paywall.py
