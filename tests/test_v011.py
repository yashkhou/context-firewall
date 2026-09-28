import unittest

from context_firewall.core import Chunk, SinkPolicy, Trust, evaluate


class ProvenanceTests(unittest.TestCase):
    def setUp(self):
        self.policy = SinkPolicy("shell", frozenset({Trust.SYSTEM, Trust.OPERATOR}), frozenset({"secret"}))

    def test_trusted_chain_is_allowed(self):
        chunks = [
            Chunk("root", "operator", Trust.OPERATOR),
            Chunk("derived", "plan", Trust.SYSTEM, parents=("operator",)),
        ]
        self.assertTrue(evaluate(chunks, self.policy).allowed)

    def test_untrusted_ancestor_blocks_derived_context(self):
        chunks = [
            Chunk("web", "page", Trust.UNTRUSTED),
            Chunk("summary", "summary", Trust.SYSTEM, parents=("page",)),
        ]
        decision = evaluate(chunks, self.policy)
        self.assertFalse(decision.allowed)
        self.assertIn("trust-not-allowed", {v.code for v in decision.violations})

    def test_missing_parent_fails_closed(self):
        decision = evaluate([Chunk("derived", "summary", Trust.SYSTEM, parents=("missing",))], self.policy)
        self.assertFalse(decision.allowed)
        self.assertIn("missing-parent", {v.code for v in decision.violations})

    def test_cycle_fails_closed(self):
        chunks = [
            Chunk("a", "a", Trust.SYSTEM, parents=("b",)),
            Chunk("b", "b", Trust.OPERATOR, parents=("a",)),
        ]
        self.assertIn("provenance-cycle", {v.code for v in evaluate(chunks, self.policy).violations})


if __name__ == "__main__":
    unittest.main()
