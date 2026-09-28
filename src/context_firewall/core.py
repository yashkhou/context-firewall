from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from typing import Iterable


class Trust(str, Enum):
    SYSTEM = "system"
    OPERATOR = "operator"
    TOOL = "tool"
    RETRIEVED = "retrieved"
    UNTRUSTED = "untrusted"


@dataclass(frozen=True)
class Chunk:
    text: str
    source: str
    trust: Trust
    labels: frozenset[str] = frozenset()
    parents: tuple[str, ...] = ()


@dataclass(frozen=True)
class SinkPolicy:
    name: str
    allowed: frozenset[Trust]
    forbidden_labels: frozenset[str] = frozenset()
    require_complete_provenance: bool = True


@dataclass(frozen=True)
class Violation:
    source: str
    code: str
    detail: str

    def as_dict(self) -> dict[str, str]:
        return asdict(self)


@dataclass(frozen=True)
class Decision:
    allowed: bool
    sink: str
    reasons: tuple[str, ...]
    contributing_sources: tuple[str, ...]
    violations: tuple[Violation, ...] = ()

    def as_dict(self) -> dict[str, object]:
        return {
            "allowed": self.allowed,
            "sink": self.sink,
            "reasons": list(self.reasons),
            "contributing_sources": list(self.contributing_sources),
            "violations": [v.as_dict() for v in self.violations],
        }


def evaluate(chunks: Iterable[Chunk], policy: SinkPolicy) -> Decision:
    """Evaluate direct trust plus the complete provenance graph, failing closed."""
    chunks = tuple(chunks)
    by_source: dict[str, Chunk] = {}
    violations: dict[tuple[str, str, str], Violation] = {}

    def add(source: str, code: str, detail: str) -> None:
        violations[(source, code, detail)] = Violation(source, code, detail)

    for chunk in chunks:
        if chunk.source in by_source:
            add(chunk.source, "duplicate-source", f"duplicate provenance source {chunk.source!r}")
        by_source[chunk.source] = chunk

    checked: set[str] = set()

    def visit(source: str, stack: tuple[str, ...]) -> None:
        if source in stack:
            cycle = " -> ".join((*stack, source))
            add(source, "provenance-cycle", f"provenance cycle: {cycle}")
            return
        chunk = by_source.get(source)
        if chunk is None:
            if policy.require_complete_provenance:
                add(source, "missing-parent", f"missing provenance parent {source!r}")
            return
        if source in checked:
            return
        if chunk.trust not in policy.allowed:
            add(source, "trust-not-allowed", f"{source}: trust={chunk.trust.value} is not allowed for {policy.name}")
        blocked = sorted(chunk.labels & policy.forbidden_labels)
        if blocked:
            add(source, "forbidden-label", f"{source}: forbidden labels={','.join(blocked)}")
        for parent in chunk.parents:
            visit(parent, (*stack, source))
        checked.add(source)

    for chunk in chunks:
        visit(chunk.source, ())

    ordered = tuple(violations.values())
    return Decision(
        allowed=not ordered,
        sink=policy.name,
        reasons=tuple(v.detail for v in ordered),
        contributing_sources=tuple(by_source),
        violations=ordered,
    )


def from_json(data: dict[str, object]) -> tuple[list[Chunk], SinkPolicy]:
    rows = data["chunks"]
    assert isinstance(rows, list)
    chunks = [
        Chunk(
            str(x["text"]),
            str(x["source"]),
            Trust(x["trust"]),
            frozenset(x.get("labels", [])),
            tuple(x.get("parents", [])),
        )
        for x in rows
    ]
    p = data["policy"]
    assert isinstance(p, dict)
    policy = SinkPolicy(
        str(p["name"]),
        frozenset(Trust(x) for x in p["allowed"]),
        frozenset(p.get("forbidden_labels", [])),
        bool(p.get("require_complete_provenance", True)),
    )
    return chunks, policy
