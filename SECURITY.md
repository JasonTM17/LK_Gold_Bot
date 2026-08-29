# Security Policy

LK Gold Bot is maintained as a safe personal Telegram assistant for public Locket links, account-safety checklists, local usage tracking, and optional NextDNS profile creation.

## Supported versions

The `main` branch is the actively maintained version. Security fixes should target `main` first.

## Reporting a vulnerability

Please open a private report if GitHub private vulnerability reporting is enabled. If it is not enabled, create an issue with a minimal description and avoid including secrets or exploit details publicly.

Include:

- The affected file or command.
- Steps to reproduce without exposing real tokens.
- Expected and actual behavior.
- Your Python version and operating system.

Do not include:

- Telegram bot tokens.
- NextDNS API keys.
- OTP codes, receipts, cookies, or private account identifiers.
- Database files from production.

## Security boundaries

This project intentionally does not implement subscription bypassing, credential collection, receipt tampering, or unauthorized access to third-party services. Feature requests that require those behaviors should be rejected.

## Secret rotation checklist

If a secret is accidentally exposed:

1. Revoke or rotate the secret immediately.
2. Remove the secret from `.env` and any logs/screenshots.
3. Check `git log` and rewrite history only if the secret was committed.
4. Re-create the secret through the official provider.
5. Restart the bot with the new value.