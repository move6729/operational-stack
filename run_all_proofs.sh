#!/bin/sh
''''[ -z "$PYTHON_EXECUTABLE" ] && PYTHON_EXECUTABLE=python3
exec "$PYTHON_EXECUTABLE" "$0" "$@"
'''

import glob
import subprocess
import sys

def main():
    print("==========================================")
    print(" Running All Operational Stack Proofs")
    print("==========================================")

    failed = 0
    passed = 0

    proof_files = sorted(glob.glob("proofs/*.py"))

    for proof in proof_files:
        print(f"Running {proof}... ", end="", flush=True)
        res = subprocess.run([sys.executable, proof], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if res.returncode == 0:
            print("[PASS]")
            passed += 1
        else:
            print("[FAIL]")
            failed += 1

    print("==========================================")
    print(f"Summary: {passed} Passed, {failed} Failed")
    print("==========================================")

    if failed != 0:
        sys.exit(1)

if __name__ == '__main__':
    main()
