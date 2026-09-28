# Implementation note

Working V1 scope: Provenance-aware trust boundaries for agent context before it reaches privileged tool or system sinks.

Verified with `python -m unittest discover -s tests -v`.

Known boundary: V1 uses explicit labels supplied by the caller; automatic provenance extraction and model-integrated taint propagation are intentionally out of scope.
