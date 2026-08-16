"""Test cases with known-correct answers, verified against sales.csv."""

EVAL_CASES = [
    {
        "id": "region_revenue",
        "csv": "sales.csv",
        "question": "Which region has the highest revenue? Plot revenue by region.",
        "expect_contains": ["North", "219,500"],
    },
    {
        "id": "product_units",
        "csv": "sales.csv",
        "question": "Which product sells the most units?",
        "expect_contains": ["Phone", "95"],
    },
    {
        "id": "total_revenue",
        "csv": "sales.csv",
        "question": "What is the total revenue across all sales?",
        "expect_contains": ["566,000"],
    },
]
