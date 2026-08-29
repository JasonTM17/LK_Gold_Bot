# FAQ

## Is this an official Locket project?

No. This is an independent personal Telegram bot project.

## Does it unlock paid features?

No. It provides public-link parsing, local usage tracking, admin tools, and legitimate personal-safety checklists. Subscriptions should be managed through official App Store or Google Play flows.

## Can I publish this repository?

Yes, but remove `.env`, database files, logs, and any private screenshots before publishing.

## Why is NextDNS optional?

Not every owner needs DNS profile automation. It is disabled by default and only uses your own API key when enabled.

## Which Python version should I use?

Python 3.10 or newer. CI validates Python 3.10, 3.11, and 3.12.

## Where is data stored?

By default: `data/bot_data.db`. You can override it with `DATA_DIR` or `DB_PATH`.