# Architecture

LK Gold Bot is a small asynchronous Telegram bot written in Python. The design keeps runtime state local, moves secrets into environment variables, and isolates external integrations behind service modules.

## High-level flow

```text
Telegram user
    │
    ▼
python-telegram-bot handlers in app/bot.py
    │
    ├── app/services/locket.py   -> parses username/link and public invite id
    ├── app/services/nextdns.py  -> optional user-controlled DNS profile
    └── app/database.py          -> SQLite usage/config/request logs
```

## Modules

### `main.py`

Loads environment variables and starts the bot.

### `app/config.py`

Owns configuration defaults, translation strings, emoji constants, and config validation.

### `app/bot.py`

Registers Telegram commands, callback handlers, user prompts, admin tools, and the async request queue.

### `app/database.py`

Provides a small SQLite access layer with WAL mode enabled for smoother concurrent reads/writes.

### `app/services/locket.py`

Normalizes user input and extracts public invite identifiers from Locket links/pages.

### `app/services/nextdns.py`

Creates or reuses a daily NextDNS profile when explicitly enabled by the owner.

## Runtime data

The bot stores data under `data/` by default. This folder is ignored by Git because it can contain local usage logs and Telegram user ids.

## Design principles

- Keep secrets out of source control.
- Use public data only.
- Prefer explicit configuration.
- Keep Telegram handlers thin and service modules testable.
- Make local validation easy with compile and unit-test commands.