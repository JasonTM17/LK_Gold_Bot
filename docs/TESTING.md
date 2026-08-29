# Testing

The project uses the Python standard library `unittest` runner so tests work without extra dependencies.

## Run compile checks

```bash
python -m compileall -q app main.py tests
```

## Run unit tests

```bash
python -m unittest discover -s tests -v
```

## Optional dev tools

Install optional local tools:

```bash
python -m pip install -r requirements-dev.txt
```

Run Ruff if installed:

```bash
ruff check .
```

## Test scope

Current tests focus on deterministic logic:

- Locket username normalization.
- Invite-id extraction.
- Configuration helper behavior.
- NextDNS behavior when disabled/misconfigured.

Network-heavy Telegram/NextDNS integration should be tested manually with test credentials.