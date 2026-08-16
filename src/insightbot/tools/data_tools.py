"""Data tools - registered with agents via register_function (Chapter 6 pattern)."""
import pandas as pd
from typing import Annotated
from insightbot.config.settings import UPLOADS_DIR


def list_datasets() -> str:
    """List all CSV files available in the uploads folder."""
    files = sorted(p.name for p in UPLOADS_DIR.glob("*.csv"))
    return "Available datasets: " + ", ".join(files) if files else "No CSV files found."


def load_csv_summary(
    file_name: Annotated[str, "Name of the CSV file inside the uploads folder, e.g. 'sales.csv'"]
) -> str:
    """Return schema + sample rows + stats of a CSV so agents understand the data."""
    path = UPLOADS_DIR / file_name
    if not path.exists():
        return f"ERROR: {file_name} not found. {list_datasets()}"
    df = pd.read_csv(path)
    return (
        f"FILE: uploads/{file_name}\n"
        f"SHAPE: {df.shape[0]} rows x {df.shape[1]} columns\n\n"
        f"COLUMNS & DTYPES:\n{df.dtypes.to_string()}\n\n"
        f"FIRST 5 ROWS:\n{df.head().to_string()}\n\n"
        f"NUMERIC SUMMARY:\n{df.describe().to_string()}"
    )
    
    
def recompute_aggregates(
    file_name: Annotated[str, "CSV file name in uploads/"]
) -> str:
    """Independently recompute groupby aggregates directly from the raw CSV -
    ground truth for the Verifier to cross-check the team's reported numbers."""
    path = UPLOADS_DIR / file_name
    if not path.exists():
        return f"ERROR: {file_name} not found."
    df = pd.read_csv(path)
    numeric_cols = df.select_dtypes("number").columns.tolist()
    cat_cols = [c for c in df.columns if c not in numeric_cols and df[c].nunique() <= 15]

    if not numeric_cols or not cat_cols:
        return "No categorical/numeric column pairs available to cross-check."

    out = ["INDEPENDENT RECOMPUTATION (ground truth, computed directly from raw CSV):"]
    for cat in cat_cols[:3]:
        for num in numeric_cols:
            agg = df.groupby(cat)[num].sum().sort_values(ascending=False)
            out.append(f"\nSum of {num} by {cat}:\n{agg.to_string()}")
    return "\n".join(out)