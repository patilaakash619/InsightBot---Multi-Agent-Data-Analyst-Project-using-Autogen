"""Plain functions for now; in Week 3 you will register these as agent tools."""
import pandas as pd
from insightbot.config.settings import UPLOADS_DIR


def load_csv_summary(file_name: str) -> str:
    """Return schema + sample rows + stats of a CSV so agents understand the data."""
    path = UPLOADS_DIR / file_name
    if not path.exists():
        return f"ERROR: {file_name} not found in {UPLOADS_DIR}"
    df = pd.read_csv(path)
    return (
        f"FILE: uploads/{file_name}\n"
        f"SHAPE: {df.shape[0]} rows x {df.shape[1]} columns\n\n"
        f"COLUMNS & DTYPES:\n{df.dtypes.to_string()}\n\n"
        f"FIRST 5 ROWS:\n{df.head().to_string()}\n\n"
        f"NUMERIC SUMMARY:\n{df.describe().to_string()}"
    )
