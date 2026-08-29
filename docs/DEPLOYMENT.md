# Deployment

This guide describes practical deployment options for a personal Telegram bot.

## Local Windows service style

For a simple personal setup, keep a PowerShell window open and run:

```powershell
.\run.ps1
```

For longer-running usage, run it inside Windows Terminal, PowerShell 7, or a process manager of your choice.

## Linux VPS

```bash
git clone https://github.com/JasonTM17/LK_Gold_Bot.git
cd LK_Gold_Bot
python3 -m venv .venv
./.venv/bin/python -m pip install --upgrade pip
./.venv/bin/python -m pip install -r requirements.txt
cp .env.example .env
nano .env
./.venv/bin/python main.py
```

## systemd

Use `deploy/locket-bot.service.example` as a starting point. Update `WorkingDirectory`, `ExecStart`, and `User` before enabling it.

```bash
sudo cp deploy/locket-bot.service.example /etc/systemd/system/locket-bot.service
sudo systemctl daemon-reload
sudo systemctl enable --now locket-bot
sudo systemctl status locket-bot
```

## Docker

Build and run manually:

```bash
docker build -t lk-gold-bot .
docker run --env-file .env -v "$PWD/data:/app/data" lk-gold-bot
```

Or use the example compose file:

```bash
cp docker-compose.example.yml docker-compose.yml
docker compose up -d --build
```

## Deployment checklist

- `.env` exists on the server.
- `BOT_TOKEN` is valid.
- `ADMIN_ID` is your own Telegram user id.
- Runtime `data/` is persisted.
- Logs do not expose secrets.
- `python -m unittest discover -s tests -v` passes before deployment.