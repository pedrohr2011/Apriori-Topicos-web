from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder

from src.apriori_manual import (
    DEFAULT_DATA_FILE,
    DEFAULT_MAX_SIZE,
    DEFAULT_MIN_CONFIDENCE,
    DEFAULT_MIN_SUPPORT,
)
from src.data_loader import load_transactions
from src.utils import format_itemset, write_csv


DEFAULT_OUTPUT_DIR = Path("outputs")


def run_with_mlxtend(
    data_file: str | Path = DEFAULT_DATA_FILE,
    min_support: float = DEFAULT_MIN_SUPPORT,
    min_confidence: float = DEFAULT_MIN_CONFIDENCE,
    output_dir: str | Path = DEFAULT_OUTPUT_DIR,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    transactions = [sorted(transaction) for transaction in load_transactions(data_file)]
    if not transactions:
        empty_itemsets = pd.DataFrame(columns=["support", "itemsets", "tamanho"])
        empty_rules = pd.DataFrame(columns=["antecedents", "consequents", "support", "confidence", "lift", "tipo"])
        return empty_itemsets, empty_rules

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

    try:
        rules = association_rules(
            itemsets,
            num_itemsets=len(transactions),
            metric="confidence",
            min_threshold=min_confidence,
        )
    except TypeError:
        rules = association_rules(
            itemsets,
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
                "itemset": format_itemset(row["itemsets"]),
                "suporte": round(float(row["support"]), 6),
            }
        )
    write_csv(path, ["tamanho", "itemset", "suporte"], rows)


def _write_rules(path: Path, rules: pd.DataFrame) -> None:
    rows = []
    for _, row in rules.iterrows():
        rows.append(
            {
                "antecedente": format_itemset(row["antecedents"]),
                "consequente": format_itemset(row["consequents"]),
                "suporte": round(float(row["support"]), 6),
                "confianca": round(float(row["confidence"]), 6),
                "lift": round(float(row["lift"]), 6),
                "tipo": row["tipo"],
            }
        )
    rows.sort(
        key=lambda row: (
            -float(row["confianca"]),
            -float(row["lift"]),
            -float(row["suporte"]),
            str(row["antecedente"]),
            str(row["consequente"]),
        )
    )
    write_csv(path, ["antecedente", "consequente", "suporte", "confianca", "lift", "tipo"], rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Apriori com mlxtend para regras de associacao.")
    parser.add_argument("--data", default=str(DEFAULT_DATA_FILE), help="Arquivo de transacoes.")
    parser.add_argument("--min-support", type=float, default=DEFAULT_MIN_SUPPORT)
    parser.add_argument("--min-confidence", type=float, default=DEFAULT_MIN_CONFIDENCE)
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
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

    print("Analise com mlxtend concluida com sucesso.")
    print(f"Itemsets frequentes gerados: {len(itemsets)}")
    print(f"Regras de associacao geradas: {len(rules)}")
    print(f"Regras de pares: {len(pair_rules)}")
    print(f"Regras de pares com terceiro item: {len(triple_rules)}")
    print(f"Arquivos exportados para: {Path(args.output_dir).resolve()}")


if __name__ == "__main__":
    main()
