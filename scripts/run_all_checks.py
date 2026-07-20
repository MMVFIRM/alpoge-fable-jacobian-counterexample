#!/usr/bin/env python3
"""Run the six independent frozen verification checks in order."""

from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKS = [
    ROOT / "checks" / "check_1_determinant.py",
    ROOT / "checks" / "check_2_collision.py",
    ROOT / "checks" / "check_3_degree.py",
    ROOT / "checks" / "check_4_jelonek_surface.py",
    ROOT / "checks" / "check_5_stratification.py",
    ROOT / "checks" / "check_6_galois.py",
]


def main() -> int:
    started = time.perf_counter()
    failures: list[str] = []

    for check in CHECKS:
        relative = check.relative_to(ROOT)
        print(f"\n=== {relative} ===", flush=True)
        result = subprocess.run([sys.executable, str(check)], cwd=ROOT, check=False)
        if result.returncode != 0:
            failures.append(str(relative))

    elapsed = time.perf_counter() - started
    print(f"\nCompleted {len(CHECKS)} checks in {elapsed:.2f}s.")
    if failures:
        print("FAILED:")
        for failure in failures:
            print(f"  - {failure}")
        return 1

    print("ALL FROZEN CHECKS PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
