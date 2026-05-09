from __future__ import annotations

import argparse
import csv
from pathlib import Path

import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder

from apriori_associacao import (
    DEFAULT_DATA_FILE,
    DEFAULT_MAX_SIZE,
    DEFAULT_MIN_CONFIDENCE,
    DEFAULT_MIN_SUPPORT,
    load_transactions,
)


def run_with_mlxtend(
    data_file: str | Path = DEFAULT_DATA_FILE,
    min_support: float = DEFAULT_MIN_SUPPORT,
    min_confidence: float = DEFAULT_MIN_CONFIDENCE,
    output_dir: str | Path = "resultados",
) -> tuple[pd.DataFrame, pd.DataFrame]:
    transactions = [sorted(transaction) for transaction in load_transactions(data_file)]
    encoder = TransactionEncoder()
    encoded = encoder.fit(transactions).transform(transactions)
    frame = pd.DataFrame(encoded, columns=encoder.columns_)

    itemsets = apriori(
        frame,
        min_support=min_support,
        use_colnames=True,
        max_len=DEFAULT_MAX_SIZE,
    )
    itemsets["tamanho"] = itemsets["itemsets"].map(len)

    rules = association_rules(
        itemsets,
        num_itemsets=len(transactions),
        metric="confidence",
        min_threshold=min_confidence,
    )
    rules = rules[
        rules.apply(
            lambda row: (
                len(row["antecedents"] | row["consequents"]) <= DEFAULT_MAX_SIZE
                and len(row["antecedents"]) in {1, 2}
                and len(row["consequents"]) == 1
            ),
            axis=1,
        )
    ].copy()
    rules["tipo"] = rules.apply(
        lambda row: "par" if len(row["antecedents"] | row["consequents"]) == 2 else "par_com_terceiro",
        axis=1,
    )

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    _write_itemsets(output_path / "itemsets_biblioteca.csv", itemsets)
    _write_rules(output_path / "regras_biblioteca.csv", rules)

    return itemsets, rules


def _write_itemsets(path: Path, itemsets: pd.DataFrame) -> None:
    rows = []
    for _, row in itemsets.sort_values(["tamanho", "support"], ascending=[True, False]).iterrows():
        rows.append(
            {
                "tamanho": int(row["tamanho"]),
                "itemset": _format_itemset(row["itemsets"]),
                "suporte": round(float(row["support"]), 6),
            }
        )
    _write_csv(path, ["tamanho", "itemset", "suporte"], rows)


def _write_rules(path: Path, rules: pd.DataFrame) -> None:
    ordered = rules.sort_values(
        ["confidence", "leverage", "support"],
        ascending=[False, False, False],
    )
    rows = []
    for _, row in ordered.iterrows():
        rows.append(
            {
                "antecedente": _format_itemset(row["antecedents"]),
                "consequente": _format_itemset(row["consequents"]),
                "suporte": round(float(row["support"]), 6),
                "confianca": round(float(row["confidence"]), 6),
                "alavancagem": round(float(row["leverage"]), 6),
                "tipo": row["tipo"],
            }
        )
    _write_csv(path, ["antecedente", "consequente", "suporte", "confianca", "alavancagem", "tipo"], rows)


def _write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _format_itemset(itemset: frozenset[str]) -> str:
    return "{" + ", ".join(sorted(itemset)) + "}"


def main() -> None:
    parser = argparse.ArgumentParser(description="Apriori com mlxtend para regras de associacao.")
    parser.add_argument("--data", default=str(DEFAULT_DATA_FILE), help="Arquivo de transacoes.")
    parser.add_argument("--min-support", type=float, default=DEFAULT_MIN_SUPPORT)
    parser.add_argument("--min-confidence", type=float, default=DEFAULT_MIN_CONFIDENCE)
    parser.add_argument("--output-dir", default="resultados")
    args = parser.parse_args()

    itemsets, rules = run_with_mlxtend(
        data_file=args.data,
        min_support=args.min_support,
        min_confidence=args.min_confidence,
        output_dir=args.output_dir,
    )

    pair_rules = rules[rules["tipo"] == "par"]
    triple_rules = rules[
        (rules["tipo"] == "par_com_terceiro")
        & (rules["antecedents"].map(len) == 2)
    ]

    print(f"Itemsets frequentes pela biblioteca: {len(itemsets)}")
    print(f"Regras de pares pela biblioteca: {len(pair_rules)}")
    print(f"Regras de pares com terceiro item pela biblioteca: {len(triple_rules)}")
    print(f"Arquivos gerados em: {Path(args.output_dir).resolve()}")


if __name__ == "__main__":
    main()
