# Configuration

Configuration is loaded from environment variables. For local development, copy `.env.example` to `.env`.

```bash
cp .env.example .env
```

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

## Required variables

| Variable | Example | Description |
| --- | --- | --- |
| `BOT_TOKEN` | `123456:ABC...` | Telegram bot token from [@BotFather](https://t.me/BotFather). |
| `ADMIN_ID` | `123456789` | Your Telegram numeric user id for admin-only commands. |

## Common variables

| Variable | Default | Description |
| --- | --- | --- |
| `PROJECT_NAME` | `Locket Personal Assistant Bot` | Name shown in Telegram messages. |
| `DEFAULT_LANG` | `VI` | Default language. Supported values: `VI`, `EN`. |
| `NUM_WORKERS` | `2` | Number of async queue workers. Minimum is `1`. |
| `DAILY_LIMIT` | `5` | Daily checklist limit per non-admin user. Minimum is `1`. |
| `DONATE_PHOTO` | empty | Optional Telegram `file_id` for a final result image. |

## Optional NextDNS variables

| Variable | Default | Description |
| --- | --- | --- |
| `ENABLE_NEXTDNS` | `false` | Enables creation/reuse of a personal NextDNS profile. |
| `NEXTDNS_KEY` | empty | API key from your own NextDNS account. Required only when enabled. |
| `NEXTDNS_BLOCKLIST` | empty | Comma-separated domains to add to the profile denylist. |

## Path variables

| Variable | Default | Description |
| --- | --- | --- |
| `DATA_DIR` | `./data` | Directory for local runtime data. |
| `DB_PATH` | `./data/bot_data.db` | SQLite database path. |

## Validation behavior

At startup, the bot validates required configuration. Missing `BOT_TOKEN` stops startup because Telegram polling cannot run without it. Missing `ADMIN_ID` is logged as a configuration warning because user commands can still work, but admin commands will not be available.