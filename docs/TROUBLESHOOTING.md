# Troubleshooting

## `BOT_TOKEN is required`

Create `.env` from `.env.example` and fill `BOT_TOKEN`.

```powershell
Copy-Item .env.example .env
notepad .env
```

## Bot starts but does not respond

- Confirm the token belongs to the bot you are messaging.
- Ensure only one process is polling the same bot token.
- Restart the bot after editing `.env`.
- Check your network connection.

## Admin commands do nothing

- Set `ADMIN_ID` to your numeric Telegram user id.
- Restart the bot.
- Use `/start` once after changing language or admin settings.

## `Could not find a public invite id`

- Confirm the Locket username/link is public and typed correctly.
- Try the full profile link instead of only the username.
- Some profiles may not expose invite data in public HTML.

## NextDNS does not create a profile

- Set `ENABLE_NEXTDNS=true`.
- Set `NEXTDNS_KEY` to your own valid API key.
- Check whether your NextDNS account allows API profile creation.
- Review logs for HTTP status details.

## Tests fail after editing files

Run:

```bash
python -m compileall -q app main.py tests
python -m unittest discover -s tests -v
```

If import paths fail, run commands from the repository root.