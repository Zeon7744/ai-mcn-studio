#!/usr/bin/env bash
# ai-mcn-studio 冒烟：import paywall + billing + 门控校验
set -uo pipefail
cd "$(dirname "$0")"
PASS=0; FAIL=0
python3 -c "import paywall; print('paywall import OK')" \
  && PASS=$((PASS+1)) || { echo "FAIL: paywall import"; FAIL=$((FAIL+1)); }
python3 -c "import billing; print('billing import OK')" \
  && PASS=$((PASS+1)) || { echo "FAIL: billing import"; FAIL=$((FAIL+1)); }
python3 -c "import ast; ast.parse(open('paywall.py').read()); print('paywall.py 语法 OK')" \
  && PASS=$((PASS+1)) || { echo "FAIL: paywall 语法"; FAIL=$((FAIL+1)); }
python3 -m pytest tests/test_billing_gate_unified.py -q \
  && PASS=$((PASS+1)) || { echo "FAIL: billing/paywall 门控一致性测试"; FAIL=$((FAIL+1)); }
python3 -c "import billing; r=billing.check_access(plan='pro'); assert r['allowed'] and r['remaining']==-1; print('billing.check_access OK')" \
  && PASS=$((PASS+1)) || { echo "FAIL: billing.check_access 代理"; FAIL=$((FAIL+1)); }
echo "smoke_test: PASS=$PASS FAIL=$FAIL"
[ "$FAIL" -eq 0 ] && echo "=== SMOKE PASS ===" && exit 0 || { echo "=== SMOKE FAIL ==="; exit 1; }
