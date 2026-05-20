from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from src.apriori_manual import (
    calculate_support,
    generate_association_rules,
    generate_frequent_itemsets,
    load_transactions,
    recommend_participants,
)


class AprioriAssociacaoTest(unittest.TestCase):
    def setUp(self):
        self.transactions = [
            frozenset(["Ana", "Bruno", "Carlos"]),
            frozenset(["Ana", "Bruno"]),
            frozenset(["Ana", "Carlos"]),
            frozenset(["Bruno", "Carlos"]),
        ]

    def test_load_transactions_ignores_id_and_description(self):
        with TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "test_transactions.csv"
            path.write_text(
                "id-1, Atividade A, Ana, Bruno, Carlos\n"
                "id-2, Atividade B, Ana, Daniela\n",
                encoding="utf-8",
            )

            self.assertEqual(
                load_transactions(path),
                [
                    frozenset(["Ana", "Bruno", "Carlos"]),
                    frozenset(["Ana", "Daniela"]),
                ],
            )

    def test_support_counts_transactions_containing_all_items(self):
        self.assertEqual(calculate_support(self.transactions, frozenset(["Ana"])), 0.75)
        self.assertEqual(calculate_support(self.transactions, frozenset(["Ana", "Bruno"])), 0.5)
        self.assertEqual(calculate_support(self.transactions, frozenset(["Ana", "Bruno", "Carlos"])), 0.25)

    def test_support_returns_zero_for_empty_transactions(self):
        self.assertEqual(calculate_support([], frozenset(["Ana"])), 0.0)

    def test_apriori_returns_only_frequent_itemsets_up_to_max_size(self):
        itemsets = generate_frequent_itemsets(self.transactions, min_support=0.5, max_size=3)

        self.assertIn(frozenset(["Ana", "Bruno"]), itemsets)
        self.assertIn(frozenset(["Ana", "Carlos"]), itemsets)
        self.assertNotIn(frozenset(["Ana", "Bruno", "Carlos"]), itemsets)
        self.assertAlmostEqual(itemsets[frozenset(["Ana", "Bruno"])], 0.5)

    def test_apriori_returns_empty_result_without_transactions(self):
        self.assertEqual(generate_frequent_itemsets([], min_support=0.5, max_size=3), {})

    def test_rules_include_support_confidence_and_lift(self):
        itemsets = generate_frequent_itemsets(self.transactions, min_support=0.25, max_size=3)
        rules = generate_association_rules(
            itemsets,
            min_confidence=0.50,
            max_union_size=3,
            antecedent_sizes={2},
            consequent_sizes={1},
        )

        rule = next(
            rule
            for rule in rules
            if rule.antecedent == frozenset(["Ana", "Bruno"])
            and rule.consequent == frozenset(["Carlos"])
        )

        self.assertEqual(rule.support, 0.25)
        self.assertAlmostEqual(rule.confidence, 0.5)
        self.assertAlmostEqual(rule.lift, 0.5 / 0.75)

    def test_recommend_participants_uses_rules_containing_known_participant(self):
        itemsets = generate_frequent_itemsets(self.transactions, min_support=0.25, max_size=3)
        rules = generate_association_rules(
            itemsets,
            min_confidence=0.50,
            max_union_size=3,
            antecedent_sizes={1, 2},
            consequent_sizes={1},
        )

        recommendations = recommend_participants(
            enrolled={"Ana", "Bruno"},
            rules=rules,
            top_n=3,
        )

        self.assertEqual(recommendations[0]["aluno"], "Carlos")
        self.assertGreaterEqual(recommendations[0]["confidence"], 0.5)


if __name__ == "__main__":
    unittest.main()
