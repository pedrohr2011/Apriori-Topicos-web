from __future__ import annotations

import csv
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA_FILE = PROJECT_ROOT / "data" / "input" / "transactions.csv"


def load_transactions(path: str | Path = DEFAULT_DATA_FILE) -> list[frozenset[str]]:
    """Load transactions and ignore the id/description columns from the input file."""
    transactions: list[frozenset[str]] = []

    with Path(path).open(newline="", encoding="utf-8") as file:
        reader = csv.reader(file, skipinitialspace=True)
        for row in reader:
            if len(row) < 3:
                continue

            items = frozenset(item.strip() for item in row[2:] if item.strip())
            if items:
                transactions.append(items)

    return transactions
