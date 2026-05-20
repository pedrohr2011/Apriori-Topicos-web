from __future__ import annotations

import csv
from pathlib import Path


def format_itemset(itemset: frozenset[str] | set[str]) -> str:
    return "{" + ", ".join(sorted(itemset)) + "}"


def write_csv(path: str | Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)

    with target.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
