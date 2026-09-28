import unittest,sys; sys.path.insert(0,'src')
from context_firewall.core import *
class T(unittest.TestCase):
 def test_trusted_passes(self): self.assertTrue(evaluate([Chunk('x','op',Trust.OPERATOR)],SinkPolicy('tool',frozenset({Trust.OPERATOR}))).allowed)
 def test_untrusted_blocks(self): self.assertFalse(evaluate([Chunk('x','web',Trust.UNTRUSTED)],SinkPolicy('tool',frozenset({Trust.OPERATOR}))).allowed)
 def test_label_blocks(self): self.assertIn('forbidden labels=secret',evaluate([Chunk('x','tool',Trust.TOOL,frozenset({'secret'}))],SinkPolicy('sink',frozenset({Trust.TOOL}),frozenset({'secret'}))).reasons[0])
