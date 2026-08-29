# Operations Runbook

## Start the bot

Windows:

```powershell
.\run.ps1
```

Linux/macOS:

```bash
chmod +x run.sh
./run.sh
```

## Stop the bot

Use `Ctrl+C` in the terminal. If running under systemd:

```bash
sudo systemctl stop locket-bot
```

## Restart after config changes

Environment variables are read at process startup, so restart the bot after editing `.env`.

## Backup runtime data

The default database is `data/bot_data.db`.

```bash
sqlite3 data/bot_data.db ".backup data/bot_data.backup.db"
```

If `sqlite3` is not installed, stop the bot first and copy the `data/` folder.

## Admin commands

- `/stats` shows aggregate bot statistics.
- `/noti <message>` broadcasts to known users.
- `/rs <user_id>` resets a user's daily usage count.
- `/setdonate` stores a Telegram photo `file_id` when replying to an image.

## Incident checklist

1. Stop the bot if secrets or unexpected behavior are involved.
2. Rotate affected tokens/API keys.
3. Review recent logs.
4. Check `git status --short` to ensure no private files are staged.
5. Restart with corrected configuration.