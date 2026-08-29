# Roadmap

This roadmap keeps the project focused on safe personal-assistant features.

## Short term

- Keep README and setup docs accurate.
- Add tests for configuration parsing and database helpers.
- Improve admin statistics and observability.
- Add more robust input normalization for Locket links.

## Medium term

- Add structured logging options.
- Add optional Docker deployment documentation.
- Add backup/restore helper scripts for SQLite.
- Add more granular rate-limit settings.

## Long term

- Add a small web status page for the owner.
- Add i18n files outside Python source.
- Add a migration system if the database schema grows.

## Non-goals

- Subscription bypassing.
- Credential collection.
- Unauthorized account access.
- Abuse automation against third-party services.