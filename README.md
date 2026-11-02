# Trace Accountant

Explain where elapsed time was spent in a nested trace. Overlapping child spans count only once against their parent and missing end timestamps are reported separately.

## Run locally

Use Python 3.12. The project uses the standard library. From the repository root:

```sh
python cli.py example.json
python -m unittest -v
```

The included example is synthetic. Pass a different UTF-8 JSON file to inspect your own input. The command prints JSON to stdout. Invalid input returns status 2 and an explanation on stderr. See [CONTRACT.md](CONTRACT.md) for input fields and interpretation.

## Operational limits

Requires nested synchronous spans with a shared clock. Longest exclusive span identifies the largest measured self-time, not a distributed causal critical path. Disconnected roots are supported.

## Resumen en español

Atribuye tiempo exclusivo a cada operación y señala tramos incompletos que impiden atribuir latencia con certeza.
