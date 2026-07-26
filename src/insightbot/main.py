"""Run: uv run python -m insightbot.main "your question" sales.csv"""
import sys
from insightbot.workflows.analysis_flow import run_analysis


def main():
    question = sys.argv[1] if len(sys.argv) > 1 else "Give me an overview of the data with one chart."
    csv_name = sys.argv[2] if len(sys.argv) > 2 else "sales.csv"

    result = run_analysis(question, csv_name)

    print("\n" + "=" * 60)
    print("FINAL SUMMARY:\n", result.summary)
    print("\nTOKEN COST:\n", result.cost)     # from video 7


if __name__ == "__main__":
    main()
