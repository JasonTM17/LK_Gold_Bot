# Contributing

Thanks for improving LK Gold Bot. This repository is designed to be easy to run locally and safe to publish as a personal project.

## Development workflow

1. Fork or clone the repository.
2. Create a virtual environment.
3. Install dependencies from `requirements.txt`.
4. Copy `.env.example` to `.env` and add your local Telegram test bot token.
5. Run validation commands before committing.

```bash
python -m compileall -q app main.py tests
python -m unittest discover -s tests -v
```

## Commit style

Use small, descriptive commits. Recommended prefixes:

- `docs:` documentation changes.
- `chore:` repository maintenance.
- `ci:` GitHub Actions and automation.
- `feat:` user-visible functionality.
- `fix:` bug fixes.
- `test:` tests only.
- `refactor:` code structure changes without behavior changes.

## Safety rules

- Do not commit `.env`, database files, logs, or screenshots with private data.
- Do not add features that bypass subscriptions or abuse Locket/NextDNS APIs.
- Keep API usage limited to public data and official user-controlled configuration.
- Prefer clear error messages over silent failures.

## Pull request checklist

- Explain what changed and why.
- Include tests or documentation updates where appropriate.
- Confirm compile and unit tests pass.
- Confirm no secrets or runtime data were committed.