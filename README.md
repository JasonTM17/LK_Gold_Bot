# LK Gold Bot

[![CI](https://github.com/JasonTM17/LK_Gold_Bot/actions/workflows/ci.yml/badge.svg)](https://github.com/JasonTM17/LK_Gold_Bot/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**LK Gold Bot** là một Telegram bot cá nhân viết bằng Python, dùng để quản lý username/link Locket, phân tích invite id công khai, tạo checklist sử dụng tài khoản an toàn, theo dõi lượt dùng bằng SQLite và tuỳ chọn tạo profile NextDNS cá nhân.

Dự án đã được dọn lại để phù hợp làm **project cá nhân có thể public trên GitHub**: không hard-code token, có `.env.example`, có test, CI, Docker, tài liệu vận hành, security policy, issue templates và hướng dẫn triển khai rõ ràng.

> **Lưu ý quan trọng:** bot này chỉ hỗ trợ quản lý thông tin công khai và checklist thao tác hợp lệ. Bot không mở khoá gói trả phí, không bypass subscription, không thu thập mật khẩu/OTP/receipt và không truy cập trái phép dịch vụ bên thứ ba. Nếu cần quản lý gói Locket, hãy dùng App Store hoặc Google Play chính thức.

---

## Mục lục

- [Tính năng chính](#tính-năng-chính)
- [Demo luồng sử dụng](#demo-luồng-sử-dụng)
- [Công nghệ sử dụng](#công-nghệ-sử-dụng)
- [Yêu cầu hệ thống](#yêu-cầu-hệ-thống)
- [Cài đặt nhanh](#cài-đặt-nhanh)
- [Cấu hình `.env`](#cấu-hình-env)
- [Chạy bot](#chạy-bot)
- [Lệnh Telegram](#lệnh-telegram)
- [Cấu trúc thư mục](#cấu-trúc-thư-mục)
- [Kiểm tra chất lượng](#kiểm-tra-chất-lượng)
- [Triển khai](#triển-khai)
- [Bảo mật và quyền riêng tư](#bảo-mật-và-quyền-riêng-tư)
- [Tài liệu bổ sung](#tài-liệu-bổ-sung)
- [License](#license)

---

## Tính năng chính

### Cho người dùng

- Menu Telegram dễ dùng với inline keyboard.
- Hỗ trợ song ngữ Việt/Anh.
- Nhận username Locket hoặc link Locket.
- Chuẩn hoá input phổ biến như `alice`, `@alice`, `https://locket.cam/alice`.
- Trích xuất invite id công khai nếu link/profile có expose dữ liệu public.
- Trả về checklist sử dụng tài khoản cá nhân an toàn.
- Giới hạn lượt dùng mỗi ngày cho user thường để tránh spam.

### Cho admin

- `/stats` xem thống kê tổng quan.
- `/noti <nội dung>` broadcast thông báo tới user đã dùng bot.
- `/rs <user_id>` reset lượt dùng trong ngày.
- `/setdonate` lưu Telegram photo `file_id` để gửi kèm kết quả.
- Admin được miễn daily limit.

### Kỹ thuật

- Queue xử lý bất đồng bộ với nhiều worker.
- SQLite local database, bật WAL mode.
- Cấu hình qua environment variables.
- Runtime data được tách vào `data/` và bị ignore khỏi Git.
- Có unit test cho parser, config, database và NextDNS path cơ bản.
- Có GitHub Actions CI cho Python 3.10, 3.11, 3.12.
- Có Dockerfile, docker-compose example và systemd service example.

---

## Demo luồng sử dụng

1. User mở bot và bấm `/start`.
2. Bot hiển thị menu chính.
3. User bấm `🔎 Check Locket`.
4. Bot yêu cầu user reply bằng username hoặc link.
5. User gửi ví dụ:

```text
@alice
```

hoặc:

```text
https://locket.cam/alice
```

6. Bot cố gắng tìm public invite id từ link/profile.
7. Bot hiển thị thông tin công khai và nút tạo checklist.
8. Request được đưa vào queue.
9. Worker xử lý và trả kết quả checklist hợp lệ.

---

## Công nghệ sử dụng

| Thành phần | Vai trò |
| --- | --- |
| Python 3.10+ | Ngôn ngữ chính |
| python-telegram-bot | Telegram Bot API framework |
| aiohttp | HTTP client bất đồng bộ |
| python-dotenv | Load `.env` khi chạy local |
| SQLite | Lưu usage, language, request logs, bot config |
| unittest | Unit test không cần dependency ngoài |
| GitHub Actions | CI compile/test tự động |
| Docker | Tuỳ chọn đóng gói deployment |

---

## Yêu cầu hệ thống

- Python `3.10` trở lên.
- Git.
- Telegram bot token từ [@BotFather](https://t.me/BotFather).
- Telegram numeric user id của bạn để làm admin.
- Optional: NextDNS API key nếu muốn bật `ENABLE_NEXTDNS=true`.

Kiểm tra Python:

```bash
python --version
```

Trên Linux/macOS có thể là:

```bash
python3 --version
```

---

## Cài đặt nhanh

### Clone repository

```bash
git clone https://github.com/JasonTM17/LK_Gold_Bot.git
cd LK_Gold_Bot
```

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
notepad .env
```

Hoặc dùng script:

```powershell
.\scripts\setup.ps1
```

### Linux/macOS

```bash
python3 -m venv .venv
./.venv/bin/python -m pip install --upgrade pip
./.venv/bin/python -m pip install -r requirements.txt
cp .env.example .env
nano .env
```

Hoặc dùng script:

```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

---

## Cấu hình `.env`

Tạo file `.env` từ mẫu:

```bash
cp .env.example .env
```

Windows:

```powershell
Copy-Item .env.example .env
```

Ví dụ cấu hình tối thiểu:

```env
BOT_TOKEN=123456789:AAExampleTelegramBotToken
ADMIN_ID=123456789
DEFAULT_LANG=VI
NUM_WORKERS=2
DAILY_LIMIT=5
PROJECT_NAME=LK Gold Bot
```

### Bảng biến môi trường

| Biến | Bắt buộc | Mặc định | Mô tả |
| --- | --- | --- | --- |
| `BOT_TOKEN` | Có | rỗng | Token bot từ @BotFather. |
| `ADMIN_ID` | Nên có | `0` | Telegram user id của admin. |
| `DEFAULT_LANG` | Không | `VI` | Ngôn ngữ mặc định: `VI` hoặc `EN`. |
| `NUM_WORKERS` | Không | `2` | Số worker xử lý queue. Tối thiểu `1`. |
| `DAILY_LIMIT` | Không | `5` | Số lượt/ngày cho user thường. |
| `DONATE_PHOTO` | Không | rỗng | Telegram photo `file_id` gửi kèm kết quả. |
| `PROJECT_NAME` | Không | `Locket Personal Assistant Bot` | Tên hiển thị trong bot. |
| `ENABLE_NEXTDNS` | Không | `false` | Bật tạo profile NextDNS cá nhân. |
| `NEXTDNS_KEY` | Khi bật NextDNS | rỗng | API key NextDNS của chính bạn. |
| `NEXTDNS_BLOCKLIST` | Không | rỗng | Danh sách domain, cách nhau bằng dấu phẩy. |
| `DATA_DIR` | Không | `./data` | Thư mục runtime data. |
| `DB_PATH` | Không | `./data/bot_data.db` | Đường dẫn SQLite database. |

### Xem cấu hình đã load mà không lộ token

```bash
python scripts/show_config.py
```

Script này sẽ mask token/API key trước khi in ra terminal.

---

## Chạy bot

### Cách trực tiếp

Windows:

```powershell
.\.venv\Scripts\python.exe main.py
```

Linux/macOS:

```bash
./.venv/bin/python main.py
```

### Dùng script có sẵn

Windows:

```powershell
.\run.ps1
```

Linux/macOS:

```bash
chmod +x run.sh
./run.sh
```

### Healthcheck local

```bash
python scripts/healthcheck.py
```

Healthcheck sẽ kiểm tra import, cấu hình cơ bản và SQLite.

---

## Lệnh Telegram

### User commands

| Lệnh | Mô tả |
| --- | --- |
| `/start` | Mở menu chính. |
| `/setlang` | Đổi ngôn ngữ VI/EN. |
| `/help` | Xem hướng dẫn sử dụng. |

### Admin commands

Admin được xác định bằng `ADMIN_ID` trong `.env`.

| Lệnh | Mô tả | Ví dụ |
| --- | --- | --- |
| `/stats` | Xem tổng user/request/success/fail/queue. | `/stats` |
| `/noti <message>` | Broadcast thông báo tới tất cả user đã dùng bot. | `/noti Bot sẽ bảo trì lúc 22:00` |
| `/rs <user_id>` | Reset daily limit cho user. | `/rs 123456789` |
| `/setdonate` | Reply vào ảnh để lưu ảnh gửi kèm kết quả. | Reply ảnh + `/setdonate` |

---

## Cấu trúc thư mục

```text
.
├── .github/
│   ├── ISSUE_TEMPLATE/        # Issue templates
│   └── workflows/ci.yml       # GitHub Actions CI
├── app/
│   ├── __init__.py
│   ├── bot.py                 # Telegram handlers, queue, admin commands
│   ├── config.py              # Environment config + texts
│   ├── database.py            # SQLite helper layer
│   └── services/
│       ├── __init__.py
│       ├── locket.py          # Locket input normalization/public invite parser
│       └── nextdns.py         # Optional NextDNS profile setup
├── deploy/
│   └── locket-bot.service.example
├── docs/                      # Detailed documentation
├── scripts/                   # Setup, check, healthcheck, backup helpers
├── tests/                     # unittest test suite
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.example.yml
├── main.py
├── Makefile
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
├── run.ps1
└── run.sh
```

---

## Kiểm tra chất lượng

### Compile toàn bộ source

```bash
python -m compileall -q app main.py tests scripts
```

### Chạy unit tests

```bash
python -m unittest discover -s tests -v
```

### Dùng script check

Windows:

```powershell
.\scripts\check.ps1
```

Linux/macOS:

```bash
chmod +x scripts/check.sh
./scripts/check.sh
```

### Optional lint

```bash
python -m pip install -r requirements-dev.txt
ruff check .
```

---

## Triển khai

### Docker

```bash
docker build -t lk-gold-bot .
docker run --env-file .env -v "$PWD/data:/app/data" lk-gold-bot
```

### Docker Compose

```bash
cp docker-compose.example.yml docker-compose.yml
docker compose up -d --build
```

### Linux systemd

Xem file mẫu:

```text
deploy/locket-bot.service.example
```

Các bước tổng quát:

```bash
sudo cp deploy/locket-bot.service.example /etc/systemd/system/locket-bot.service
sudo systemctl daemon-reload
sudo systemctl enable --now locket-bot
sudo systemctl status locket-bot
```

Nhớ sửa `WorkingDirectory`, `ExecStart`, `EnvironmentFile`, `User`, `Group` cho đúng server của bạn.

---

## Backup dữ liệu

Database mặc định:

```text
data/bot_data.db
```

Backup bằng script Python:

```bash
python scripts/backup_db.py
```

Hoặc nếu có sqlite3 CLI:

```bash
sqlite3 data/bot_data.db ".backup data/bot_data.backup.db"
```

Không commit thư mục `data/` lên GitHub.

---

## Bảo mật và quyền riêng tư

- Không commit `.env`.
- Không commit `data/`, `*.db`, log hoặc ảnh chụp màn hình chứa dữ liệu riêng tư.
- Nếu lộ `BOT_TOKEN`, hãy revoke token qua @BotFather ngay.
- Nếu lộ `NEXTDNS_KEY`, hãy rotate key trong tài khoản NextDNS.
- Không gửi mật khẩu, OTP, receipt hoặc token qua bot.
- Không dùng bot để bypass subscription hoặc truy cập trái phép.

Chi tiết hơn xem:

- [`SECURITY.md`](SECURITY.md)
- [`docs/PRIVACY.md`](docs/PRIVACY.md)

---

## Troubleshooting nhanh

### `BOT_TOKEN is required`

Bạn chưa tạo `.env` hoặc chưa điền `BOT_TOKEN`.

### Bot không phản hồi

- Kiểm tra token đúng bot chưa.
- Đảm bảo không có process khác đang polling cùng token.
- Restart bot sau khi sửa `.env`.

### Admin command không chạy

- Kiểm tra `ADMIN_ID` là numeric Telegram user id của bạn.
- Restart bot sau khi đổi `.env`.

### Không tìm thấy invite id

- Thử nhập full link thay vì username.
- Profile có thể không expose invite id công khai.
- Đây không phải lỗi token Telegram.

Xem thêm: [`docs/TROUBLESHOOTING.md`](docs/TROUBLESHOOTING.md)

---

## Tài liệu bổ sung

| Tài liệu | Nội dung |
| --- | --- |
| [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | Kiến trúc module và luồng xử lý. |
| [`docs/CONFIGURATION.md`](docs/CONFIGURATION.md) | Giải thích toàn bộ biến môi trường. |
| [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md) | Windows, VPS, Docker, systemd. |
| [`docs/OPERATIONS.md`](docs/OPERATIONS.md) | Runbook vận hành, backup, incident. |
| [`docs/TELEGRAM_COMMANDS.md`](docs/TELEGRAM_COMMANDS.md) | Danh sách lệnh Telegram. |
| [`docs/TESTING.md`](docs/TESTING.md) | Compile/test/lint. |
| [`docs/FAQ.md`](docs/FAQ.md) | Câu hỏi thường gặp. |
| [`docs/ROADMAP.md`](docs/ROADMAP.md) | Roadmap phát triển an toàn. |
| [`docs/GITHUB_METADATA.md`](docs/GITHUB_METADATA.md) | Description/topics đề xuất cho GitHub About. |

---

## Git workflow gợi ý

```bash
git status --short
python -m compileall -q app main.py tests scripts
python -m unittest discover -s tests -v
git add .
git commit -m "docs: update detailed README"
git push origin main
```

---

## License

Dự án dùng giấy phép [MIT](LICENSE).

---

## Credits

Maintained by [JasonTM17](https://github.com/JasonTM17) as a personal Python/Telegram bot project.