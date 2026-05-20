from __future__ import annotations

import argparse
from pathlib import Path

from src.apriori_manual import (
    DEFAULT_MAX_SIZE,
    DEFAULT_MIN_CONFIDENCE,
    DEFAULT_MIN_SUPPORT,
    generate_association_rules,
    generate_frequent_itemsets,
    recommend_participants,
    write_itemsets,
    write_recommendations,
    write_rules,
)
from src.apriori_mlxtend import run_with_mlxtend
from src.data_loader import DEFAULT_DATA_FILE, load_transactions


def run_analysis(
    data_file: str | Path = DEFAULT_DATA_FILE,
    min_support: float = DEFAULT_MIN_SUPPORT,
    min_confidence: float = DEFAULT_MIN_CONFIDENCE,
    output_dir: str | Path = "outputs",
) -> dict[str, int]:
    transactions = load_transactions(data_file)
    output_path = Path(output_dir)

    manual_itemsets = generate_frequent_itemsets(
        transactions,
        min_support=min_support,
        max_size=DEFAULT_MAX_SIZE,
    )
    manual_rules = generate_association_rules(
        manual_itemsets,
        min_confidence=min_confidence,
        max_union_size=DEFAULT_MAX_SIZE,
        antecedent_sizes={1, 2},
        consequent_sizes={1},
    )
    recommendations = recommend_participants(
        enrolled={"Ana Silva", "Bruno Costa"},
        rules=manual_rules,
        top_n=5,
    )

    write_itemsets(output_path / "itemsets_manuais.csv", manual_itemsets)
    write_rules(output_path / "regras_manuais.csv", manual_rules)
    write_recommendations(output_path / "recomendacoes_exemplo.csv", recommendations)

    mlxtend_itemsets, mlxtend_rules = run_with_mlxtend(
        data_file=data_file,
        min_support=min_support,
        min_confidence=min_confidence,
        output_dir=output_path,
    )

    return {
        "transactions": len(transactions),
        "manual_itemsets": len(manual_itemsets),
        "manual_rules": len(manual_rules),
        "mlxtend_itemsets": len(mlxtend_itemsets),
        "mlxtend_rules": len(mlxtend_rules),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Executa a analise de regras de associacao com Apriori.")
    parser.add_argument("--data", default=str(DEFAULT_DATA_FILE), help="Arquivo de transacoes.")
    parser.add_argument("--min-support", type=float, default=DEFAULT_MIN_SUPPORT)
    parser.add_argument("--min-confidence", type=float, default=DEFAULT_MIN_CONFIDENCE)
    parser.add_argument("--output-dir", default="outputs")
    args = parser.parse_args()

    summary = run_analysis(
        data_file=args.data,
        min_support=args.min_support,
        min_confidence=args.min_confidence,
        output_dir=args.output_dir,
    )

    print("Analise concluida com sucesso.")
    print()
    print(f"Transacoes processadas: {summary['transactions']}")
    print(f"Itemsets frequentes gerados na implementacao manual: {summary['manual_itemsets']}")
    print(f"Regras de associacao geradas na implementacao manual: {summary['manual_rules']}")
    print(f"Itemsets frequentes gerados com mlxtend: {summary['mlxtend_itemsets']}")
    print(f"Regras de associacao geradas com mlxtend: {summary['mlxtend_rules']}")
    print(f"Arquivos exportados para a pasta {Path(args.output_dir).resolve()}")


if __name__ == "__main__":
    main()
