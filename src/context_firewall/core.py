from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Iterable

class Trust(str, Enum):
    SYSTEM='system'; OPERATOR='operator'; TOOL='tool'; RETRIEVED='retrieved'; UNTRUSTED='untrusted'

@dataclass(frozen=True)
class Chunk:
    text: str
    source: str
    trust: Trust
    labels: frozenset[str]=frozenset()

@dataclass(frozen=True)
class SinkPolicy:
    name: str
    allowed: frozenset[Trust]
    forbidden_labels: frozenset[str]=frozenset()

@dataclass(frozen=True)
class Decision:
    allowed: bool
    sink: str
    reasons: tuple[str,...]
    contributing_sources: tuple[str,...]
    def as_dict(self): return {'allowed':self.allowed,'sink':self.sink,'reasons':list(self.reasons),'contributing_sources':list(self.contributing_sources)}

def evaluate(chunks: Iterable[Chunk], policy: SinkPolicy) -> Decision:
    chunks=tuple(chunks); reasons=[]
    for c in chunks:
        if c.trust not in policy.allowed:
            reasons.append(f'{c.source}: trust={c.trust.value} is not allowed for {policy.name}')
        blocked=sorted(c.labels & policy.forbidden_labels)
        if blocked: reasons.append(f"{c.source}: forbidden labels={','.join(blocked)}")
    return Decision(not reasons, policy.name, tuple(reasons), tuple(c.source for c in chunks))

def from_json(data):
    chunks=[Chunk(x['text'],x['source'],Trust(x['trust']),frozenset(x.get('labels',[]))) for x in data['chunks']]
    p=data['policy']; policy=SinkPolicy(p['name'],frozenset(Trust(x) for x in p['allowed']),frozenset(p.get('forbidden_labels',[])))
    return chunks, policy
