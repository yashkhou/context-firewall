# Architecture

Context chunks remain separate records instead of being flattened into one prompt. A sink policy declares accepted trust levels and forbidden labels; the firewall evaluates every contributing chunk and emits an auditable decision.

## Design constraints

- deterministic offline behavior
- explicit machine-readable inputs and outputs
- small standard-library surface area
- failures are surfaced rather than hidden

## V1 limitation

V1 uses explicit labels supplied by the caller; automatic provenance extraction and model-integrated taint propagation are intentionally out of scope.
