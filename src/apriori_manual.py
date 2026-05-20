from __future__ import annotations

import argparse
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
from typing import Iterable

from src.data_loader import DEFAULT_DATA_FILE, load_transactions
from src.utils import format_itemset, write_csv

DEFAULT_MIN_SUPPORT = 0.10
DEFAULT_MIN_CONFIDENCE = 0.50
DEFAULT_MAX_SIZE = 3
DEFAULT_OUTPUT_DIR = Path("outputs")


@dataclass(frozen=True)
class Rule:
    antecedent: frozenset[str]
    consequent: frozenset[str]
    support: float
    confidence: float
    lift: float

    @property
    def union_size(self) -> int:
        return len(self.antecedent | self.consequent)


def calculate_support(transactions: Iterable[frozenset[str]], itemset: frozenset[str]) -> float:
    transactions_list = list(transactions)
    if not transactions_list:
        return 0.0

    count = sum(1 for transaction in transactions_list if itemset <= transaction)
    return count / len(transactions_list)


def calculate_confidence(itemset_support: float, antecedent_support: float) -> float:
    if antecedent_support == 0:
        return 0.0

    return itemset_support / antecedent_support


def calculate_lift(confidence: float, consequent_support: float) -> float:
    if consequent_support == 0:
        return 0.0

    return confidence / consequent_support


def generate_frequent_itemsets(
    transactions: list[frozenset[str]],
    min_support: float,
    max_size: int = DEFAULT_MAX_SIZE,
) -> dict[frozenset[str], float]:
    frequent_itemsets: dict[frozenset[str], float] = {}
    items = sorted({item for transaction in transactions for item in transaction})
    candidates = {frozenset([item]) for item in items}

    size = 1
    while candidates and size <= max_size:
        current_frequents = {
            candidate: calculate_support(transactions, candidate)
            for candidate in candidates
        }
        current_frequents = {
            itemset: value
            for itemset, value in current_frequents.items()
            if value >= min_support
        }
        frequent_itemsets.update(current_frequents)

        size += 1
        candidates = _next_candidates(set(current_frequents), size)

    return frequent_itemsets


apriori = generate_frequent_itemsets
support = calculate_support


def _next_candidates(previous_frequents: set[frozenset[str]], size: int) -> set[frozenset[str]]:
    candidates: set[frozenset[str]] = set()
    previous_list = sorted(previous_frequents, key=lambda itemset: sorted(itemset))

    for left, right in combinations(previous_list, 2):
        candidate = left | right
        if len(candidate) != size:
            continue
        if all(frozenset(subset) in previous_frequents for subset in combinations(candidate, size - 1)):
            candidates.add(candidate)

    return candidates


def generate_association_rules(
    frequent_itemsets: dict[frozenset[str], float],
    min_confidence: float = DEFAULT_MIN_CONFIDENCE,
    max_union_size: int = DEFAULT_MAX_SIZE,
    antecedent_sizes: set[int] | None = None,
    consequent_sizes: set[int] | None = None,
) -> list[Rule]:
    rules: list[Rule] = []

    for itemset, itemset_support in frequent_itemsets.items():
        if len(itemset) < 2 or len(itemset) > max_union_size:
            continue

        for antecedent_size in range(1, len(itemset)):
            if antecedent_sizes is not None and antecedent_size not in antecedent_sizes:
                continue

            for antecedent_tuple in combinations(sorted(itemset), antecedent_size):
                antecedent = frozenset(antecedent_tuple)
                consequent = itemset - antecedent

                if consequent_sizes is not None and len(consequent) not in consequent_sizes:
                    continue

                antecedent_support = frequent_itemsets.get(antecedent)
                consequent_support = frequent_itemsets.get(consequent)
                if not antecedent_support or consequent_support is None:
                    continue

                confidence = calculate_confidence(itemset_support, antecedent_support)
                if confidence < min_confidence:
                    continue

                lift = calculate_lift(confidence, consequent_support)
                rules.append(
                    Rule(
                        antecedent=antecedent,
                        consequent=consequent,
                        support=itemset_support,
                        confidence=confidence,
                        lift=lift,
                    )
                )

    return sorted(
        rules,
        key=lambda rule: (
            -rule.confidence,
            -rule.lift,
            -rule.support,
            format_itemset(rule.antecedent),
            format_itemset(rule.consequent),
        ),
    )


def recommend_participants(
    enrolled: set[str],
    rules: list[Rule],
    top_n: int = 5,
) -> list[dict[str, float | str]]:
    scores: dict[str, dict[str, float | str]] = {}
    enrolled_set = set(enrolled)

    for rule in rules:
        if not rule.antecedent <= enrolled_set:
            continue

        for student in rule.consequent:
            if student in enrolled_set:
                continue

            current = scores.get(student)
            if current is None or (rule.confidence, rule.lift, rule.support) > (
                float(current["confidence"]),
                float(current["lift"]),
                float(current["support"]),
            ):
                scores[student] = {
                    "aluno": student,
                    "confidence": rule.confidence,
                    "support": rule.support,
                    "lift": rule.lift,
                    "regra": f"{format_itemset(rule.antecedent)} -> {format_itemset(rule.consequent)}",
                }

    return sorted(
        scores.values(),
        key=lambda item: (
            -float(item["confidence"]),
            -float(item["lift"]),
            -float(item["support"]),
            str(item["aluno"]),
        ),
    )[:top_n]


def write_itemsets(path: str | Path, itemsets: dict[frozenset[str], float]) -> None:
    rows = [
        {
            "tamanho": len(itemset),
            "itemset": format_itemset(itemset),
            "suporte": round(value, 6),
        }
        for itemset, value in itemsets.items()
    ]
    rows.sort(key=lambda row: (int(row["tamanho"]), -float(row["suporte"]), str(row["itemset"])))
    write_csv(path, ["tamanho", "itemset", "suporte"], rows)


def write_rules(path: str | Path, rules: list[Rule]) -> None:
    rows = [
        {
            "antecedente": format_itemset(rule.antecedent),
            "consequente": format_itemset(rule.consequent),
            "suporte": round(rule.support, 6),
            "confianca": round(rule.confidence, 6),
            "lift": round(rule.lift, 6),
            "tipo": "par" if rule.union_size == 2 else "par_com_terceiro",
        }
        for rule in rules
    ]
    write_csv(
        path,
        ["antecedente", "consequente", "suporte", "confianca", "lift", "tipo"],
        rows,
    )


def write_recommendations(path: str | Path, recommendations: list[dict[str, float | str]]) -> None:
    write_csv(path, ["aluno", "confidence", "support", "lift", "regra"], recommendations)


def main() -> None:
    parser = argparse.ArgumentParser(description="Apriori manual para regras de associacao.")
    parser.add_argument("--data", default=str(DEFAULT_DATA_FILE), help="Arquivo de transacoes.")
    parser.add_argument("--min-support", type=float, default=DEFAULT_MIN_SUPPORT)
    parser.add_argument("--min-confidence", type=float, default=DEFAULT_MIN_CONFIDENCE)
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    args = parser.parse_args()

    transactions = load_transactions(args.data)
    itemsets = generate_frequent_itemsets(transactions, min_support=args.min_support, max_size=DEFAULT_MAX_SIZE)
    rules = generate_association_rules(
        itemsets,
        min_confidence=args.min_confidence,
        max_union_size=DEFAULT_MAX_SIZE,
        antecedent_sizes={1, 2},
        consequent_sizes={1},
    )
    recommendations = recommend_participants(
        enrolled={"Ana Silva", "Bruno Costa"},
        rules=rules,
        top_n=5,
    )

    output_dir = Path(args.output_dir)
    write_itemsets(output_dir / "itemsets_manuais.csv", itemsets)
    write_rules(output_dir / "regras_manuais.csv", rules)
    write_recommendations(output_dir / "recomendacoes_exemplo.csv", recommendations)

    pair_rules = [rule for rule in rules if rule.union_size == 2]
    triple_rules = [rule for rule in rules if rule.union_size == 3 and len(rule.antecedent) == 2]

    print("Analise manual concluida com sucesso.")
    print(f"Transacoes processadas: {len(transactions)}")
    print(f"Itemsets frequentes gerados: {len(itemsets)}")
    print(f"Regras de associacao geradas: {len(rules)}")
    print(f"Regras de pares: {len(pair_rules)}")
    print(f"Regras de pares com terceiro item: {len(triple_rules)}")
    print(f"Arquivos exportados para: {output_dir.resolve()}")


if __name__ == "__main__":
    main()
