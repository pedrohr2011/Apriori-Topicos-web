from pathlib import Path
import unittest

from apriori_associacao import (
    apriori,
    generate_association_rules,
    load_transactions,
    recommend_participants,
    support,
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
        path = Path("test_transactions.txt")
        path.write_text(
            "id-1, Atividade A, Ana, Bruno, Carlos\n"
            "id-2, Atividade B, Ana, Daniela\n",
            encoding="utf-8",
        )
        try:
            self.assertEqual(
                load_transactions(path),
                [
                    frozenset(["Ana", "Bruno", "Carlos"]),
                    frozenset(["Ana", "Daniela"]),
                ],
            )
        finally:
            path.unlink()

    def test_support_counts_transactions_containing_all_items(self):
        self.assertEqual(support(self.transactions, frozenset(["Ana"])), 0.75)
        self.assertEqual(support(self.transactions, frozenset(["Ana", "Bruno"])), 0.5)
        self.assertEqual(support(self.transactions, frozenset(["Ana", "Bruno", "Carlos"])), 0.25)

    def test_apriori_returns_only_frequent_itemsets_up_to_max_size(self):
        itemsets = apriori(self.transactions, min_support=0.5, max_size=3)

        self.assertIn(frozenset(["Ana", "Bruno"]), itemsets)
        self.assertIn(frozenset(["Ana", "Carlos"]), itemsets)
        self.assertNotIn(frozenset(["Ana", "Bruno", "Carlos"]), itemsets)
        self.assertAlmostEqual(itemsets[frozenset(["Ana", "Bruno"])], 0.5)

    def test_rules_include_support_confidence_and_leverage(self):
        itemsets = apriori(self.transactions, min_support=0.25, max_size=3)
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
        self.assertAlmostEqual(rule.leverage, 0.25 - (0.5 * 0.75))

    def test_recommend_participants_uses_rules_containing_known_participant(self):
        itemsets = apriori(self.transactions, min_support=0.25, max_size=3)
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
