#!/usr/bin/env bash

set -euo pipefail

echo "=========================================="
echo " Running All Operational Stack Proofs"
echo "=========================================="

FAILED=0
PASSED=0

for proof in proofs/*.py; do
    if [ -f "$proof" ]; then
        echo -n "Running ${proof}... "
        if python3 "$proof" > /dev/null 2>&1; then
            echo "[PASS]"
            PASSED=$((PASSED + 1))
        else
            echo "[FAIL]"
            FAILED=$((FAILED + 1))
        fi
    fi
done

echo "=========================================="
echo "Summary: ${PASSED} Passed, ${FAILED} Failed"
echo "=========================================="

if [ "$FAILED" -ne 0 ]; then
    exit 1
fi
