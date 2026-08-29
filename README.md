# Locket Personal Assistant Bot

Bot Telegram cá nhân giúp bạn quản lý username/link Locket, phân tích mã mời công khai và tạo checklist sử dụng tài khoản an toàn. Dự án đã được dọn lại để phù hợp làm project cá nhân: cấu hình qua `.env`, không commit dữ liệu runtime, có script chạy cho Windows/Linux và có cấu trúc Python package rõ ràng.

> Lưu ý: bot này chỉ phục vụ mục đích quản lý cá nhân và hướng dẫn thao tác hợp lệ. Hãy quản lý đăng ký/gói trả phí qua App Store hoặc Google Play chính thức.

## Tính năng

- Menu Telegram song ngữ Việt/Anh.
- Nhận username hoặc link Locket và trích xuất invite id công khai nếu có.
- Hàng đợi xử lý bất đồng bộ với nhiều worker.
- Giới hạn số lượt dùng mỗi ngày cho user thường.
- Lưu ngôn ngữ, lượt dùng và lịch sử yêu cầu bằng SQLite.
- Lệnh admin: thống kê, broadcast, reset lượt dùng, đổi ảnh kết quả.
- Tùy chọn tạo profile NextDNS cá nhân cho mục đích riêng tư/lọc nội dung hợp lệ.

## Yêu cầu

- Python 3.10+
- Telegram bot token từ [@BotFather](https://t.me/BotFather)
- Optional: NextDNS API key nếu bật `ENABLE_NEXTDNS=true`

## Cài đặt nhanh

```bash
git clone <repo-cua-ban>
cd Locket-Gold-BOT-main
python -m venv .venv

# Windows PowerShell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

# macOS/Linux
./.venv/bin/python -m pip install -r requirements.txt
```

Hoặc dùng script:

```powershell
# Windows PowerShell
.\run.ps1
```

```bash
# macOS/Linux
chmod +x run.sh
./run.sh
```

## Cấu hình

Sao chép file mẫu:

```bash
cp .env.example .env
```

Trên Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Điền các biến quan trọng trong `.env`:

```env
BOT_TOKEN=your_telegram_bot_token
ADMIN_ID=123456789
DEFAULT_LANG=VI
NUM_WORKERS=2
DAILY_LIMIT=5
```

Tùy chọn NextDNS:

```env
ENABLE_NEXTDNS=false
NEXTDNS_KEY=
NEXTDNS_BLOCKLIST=example.com
```

## Chạy bot

```bash
python main.py
```

Nếu dùng virtual environment Windows:

```powershell
.\.venv\Scripts\python.exe main.py
```

## Lệnh Telegram

### User

| Lệnh | Mô tả |
| --- | --- |
| `/start` | Mở menu chính |
| `/setlang` | Đổi ngôn ngữ |
| `/help` | Xem hướng dẫn |

### Admin

Admin được xác định bằng `ADMIN_ID` trong `.env`.

| Lệnh | Mô tả |
| --- | --- |
| `/stats` | Xem thống kê request/user/hàng đợi |
| `/noti <nội dung>` | Gửi thông báo tới toàn bộ user đã dùng bot |
| `/rs <user_id>` | Reset lượt dùng trong ngày cho user |
| `/setdonate` | Reply vào ảnh để dùng ảnh đó cho kết quả checklist |

## Cấu trúc dự án

```text
.
├── app/
│   ├── bot.py              # Handler Telegram và queue worker
│   ├── config.py           # Cấu hình từ biến môi trường
│   ├── database.py         # SQLite helper
│   └── services/
│       ├── locket.py       # Phân tích link/username công khai
│       └── nextdns.py      # Tạo profile DNS cá nhân tùy chọn
├── data/                   # Runtime database (không commit)
├── main.py                 # Entry point
├── requirements.txt
├── run.ps1
├── run.sh
└── .env.example
```

## Kiểm tra chất lượng

Compile toàn bộ source:

```bash
python -m compileall -q app main.py
```

Chạy test parser/link helper:

```bash
python -m unittest discover -s tests
```

Kiểm tra trạng thái Git trước khi commit:

```bash
git status --short
```

## Ghi chú bảo mật

- Không commit `.env`, database SQLite hoặc file cache Python.
- Không chia sẻ `BOT_TOKEN`, `NEXTDNS_KEY`, OTP hoặc dữ liệu tài khoản riêng tư.
- Nếu token Telegram bị lộ, hãy vào @BotFather để revoke token ngay.

## License

Bạn có thể thêm `LICENSE` riêng cho dự án cá nhân của mình nếu muốn public repository.