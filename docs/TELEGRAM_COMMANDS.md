# Telegram Commands

## User commands

| Command | Description |
| --- | --- |
| `/start` | Opens the main menu. |
| `/setlang` | Opens the language selector. |
| `/help` | Shows usage instructions. |

## Main menu buttons

| Button | Description |
| --- | --- |
| `🔎 Check Locket` | Prompts for a username or link. |
| `🌐 Change Language` | Switches between Vietnamese and English. |
| `🆘 Help` | Shows usage help. |

## Admin commands

Admin access is controlled by `ADMIN_ID` in `.env`.

| Command | Description | Example |
| --- | --- | --- |
| `/stats` | Show aggregate request/user/queue statistics. | `/stats` |
| `/noti <message>` | Broadcast a message to known users. | `/noti Maintenance at 22:00` |
| `/rs <user_id>` | Reset daily usage for a user. | `/rs 123456789` |
| `/setdonate` | Reply to a photo to save it as the result image. | Reply to photo with `/setdonate` |

## Input examples

Supported examples:

```text
alice
@alice
https://locket.cam/alice
https://locket.cam/invites/ABCDEFGHIJKLMNOPQRSTUVWX1234
```

The bot only inspects public invite information and returns a legitimate personal-safety checklist.