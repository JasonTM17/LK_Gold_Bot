# Privacy Notes

This bot is intended for personal use and keeps runtime data local by default.

## Data stored locally

The SQLite database may contain:

- Telegram user ids.
- Preferred language settings.
- Daily usage counters.
- Request log status and public invite ids.
- Bot configuration values saved by admin commands, such as an optional Telegram photo `file_id`.

## Data not intentionally stored

The bot should not store:

- Telegram bot tokens.
- NextDNS API keys.
- Locket passwords.
- OTP codes.
- App Store or Google Play receipts.
- Private account data.

## Sharing and backups

Do not publish the `data/` folder. If you need to share logs for debugging, redact user ids, invite ids, and any configuration values first.

## External requests

The Locket service module may request public profile pages to extract public invite identifiers. The NextDNS module only runs when explicitly enabled with your own API key.