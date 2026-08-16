"""Automated eval: run_eval.py -> pass/fail scorecard against known answers.
Usage: uv run python -m tests.run_eval"""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from insightbot.workflows.analysis_flow import run_analysis
from tests.eval_cases import EVAL_CASES


def run():
    results = []
    for case in EVAL_CASES:
        start = time.time()
        try:
            answer = run_analysis(case["question"], case["csv"])
            error = None
        except Exception as e:
            answer, error = "", str(e)
        duration = time.time() - start

        missing = [s for s in case["expect_contains"] if s.lower() not in answer.lower()]
        passed = not missing and error is None
        results.append({"id": case["id"], "passed": passed,
                        "missing": missing, "error": error, "duration": duration})

    print("\n" + "=" * 60)
    print(f"{'ID':<20}{'RESULT':<10}{'TIME':<8}DETAIL")
    print("-" * 60)
    for r in results:
        status = "PASS" if r["passed"] else "FAIL"
        detail = r["error"] or (f"missing: {r['missing']}" if r["missing"] else "")
        print(f"{r['id']:<20}{status:<10}{r['duration']:<7.0f}s{detail}")

    total = len(results)
    passed_n = sum(r["passed"] for r in results)
    print("-" * 60)
    print(f"Score: {passed_n}/{total} ({passed_n/total*100:.0f}%)")
    return passed_n == total


if __name__ == "__main__":
    ok = run()
    sys.exit(0 if ok else 1)