from insightbot.tools.data_tools import load_csv_summary


def test_summary_contains_shape():
    out = load_csv_summary("sales.csv")
    assert "SHAPE: 10 rows x 5 columns" in out


def test_missing_file():
    assert load_csv_summary("nope.csv").startswith("ERROR")
