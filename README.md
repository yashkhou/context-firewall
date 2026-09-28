# context-firewall

Provenance-aware trust boundaries for agent context before it reaches privileged tool or system sinks.

## What it does

- labels every context chunk with source, trust level and sensitivity tags
- evaluates sink policies without executing retrieved instructions
- returns machine-readable allow/block decisions with exact reasons
- ships a JSON CLI for CI and agent-runtime integration

## Quick start

```bash
PYTHONPATH=src python -m context_firewall examples/request.json
```

No model API, network service, or third-party package is required.

## Architecture

Context chunks remain separate records instead of being flattened into one prompt. A sink policy declares accepted trust levels and forbidden labels; the firewall evaluates every contributing chunk and emits an auditable decision.

See [`docs/architecture.md`](docs/architecture.md) for the data model and trade-offs.

## V1 boundary

V1 uses explicit labels supplied by the caller; automatic provenance extraction and model-integrated taint propagation are intentionally out of scope.

## Development

```bash
python -m unittest discover -s tests -v
```

MIT licensed.


## v0.1.1

**Tamper-aware provenance traversal.** Derived context can now name parent sources; evaluation walks the provenance graph, detects missing ancestors/cycles, and fails closed with structured violation codes.

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```
