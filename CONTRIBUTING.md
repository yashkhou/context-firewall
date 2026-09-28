# Contributing

Keep changes small and evidence-backed. Behavioral changes should include a regression test and explain the trust-boundary failure they address.

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
python3 -m compileall -q src tests
```
