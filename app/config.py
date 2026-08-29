import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = Path(os.environ.get("DATA_DIR", BASE_DIR / "data")).resolve()
DATA_DIR.mkdir(parents=True, exist_ok=True)

BOT_TOKEN = os.environ.get("BOT_TOKEN", "").strip()
NEXTDNS_KEY = os.environ.get("NEXTDNS_KEY", "").strip()
DB_PATH = Path(os.environ.get("DB_PATH", DATA_DIR / "bot_data.db")).resolve()


def _as_int(name: str, default: int) -> int:
    raw_value = os.environ.get(name)
    if raw_value is None or raw_value.strip() == "":
        return default
    try:
        return int(raw_value)
    except ValueError:
        return default


def _as_bool(name: str, default: bool = False) -> bool:
    raw_value = os.environ.get(name)
    if raw_value is None:
        return default
    return raw_value.strip().lower() in {"1", "true", "yes", "on"}


ADMIN_ID = _as_int("ADMIN_ID", 0)
NUM_WORKERS = max(1, _as_int("NUM_WORKERS", 2))
DAILY_LIMIT = max(1, _as_int("DAILY_LIMIT", 5))
DEFAULT_LANG = os.environ.get("DEFAULT_LANG", "VI").strip().upper() or "VI"
if DEFAULT_LANG not in {"VI", "EN"}:
    DEFAULT_LANG = "VI"

DONATE_PHOTO = os.environ.get("DONATE_PHOTO", "").strip()
ENABLE_NEXTDNS = _as_bool("ENABLE_NEXTDNS", False)

NEXTDNS_BLOCKLIST = [
    domain.strip()
    for domain in os.environ.get("NEXTDNS_BLOCKLIST", "").split(",")
    if domain.strip()
]

PROJECT_NAME = os.environ.get("PROJECT_NAME", "Locket Personal Assistant Bot").strip()

E_LOADING = '<tg-emoji emoji-id="5350752364246606166">✍️</tg-emoji>'
E_LIMIT = '<tg-emoji emoji-id="5424857974784925603">🚫</tg-emoji>'
E_SUCCESS = '<tg-emoji emoji-id="5260463209562776385">✅</tg-emoji>'
E_ERROR = '<tg-emoji emoji-id="5318840353510408444">🔴</tg-emoji>'
E_TIP = '<tg-emoji emoji-id="4968003407315993509">💡</tg-emoji>'
E_MENU = '<tg-emoji emoji-id="5449601904147440135">👑</tg-emoji>'

E_USER = '<tg-emoji emoji-id="5974048815789903111">👤</tg-emoji>'
E_ID = '<tg-emoji emoji-id="5974526806995242353">🆔</tg-emoji>'
E_TAG = '<tg-emoji emoji-id="5240228673738527951">🏷️</tg-emoji>'
E_STAT = '<tg-emoji emoji-id="4967519884192777037">📊</tg-emoji>'
E_GLOBE = '<tg-emoji emoji-id="5231489647946768652">🌐</tg-emoji>'
E_SOS = '<tg-emoji emoji-id="6301027265899661025">🆘</tg-emoji>'
E_SHIELD = '<tg-emoji emoji-id="5352888345972187597">🛡️</tg-emoji>'
E_CALENDAR = '<tg-emoji emoji-id="5413879192267805083">📅</tg-emoji>'
E_IOS = '<tg-emoji emoji-id="5350556204500263431">🍏</tg-emoji>'
E_ANDROID = '<tg-emoji emoji-id="5303145396254563405">🤖</tg-emoji>'


TEXTS = {
    "VI": {
        "welcome": (
            f"{E_SUCCESS} <b>{PROJECT_NAME}</b>\n\n"
            "Chào mừng bạn! Bot này giúp quản lý link/username Locket, kiểm tra thông tin công khai "
            "và gửi checklist sử dụng hợp lệ cho tài khoản cá nhân."
        ),
        "menu_msg": f"{E_MENU} <b>Bảng Điều Khiển</b>\n\n👇 Chọn một chức năng bên dưới.",
        "btn_input": "🔎 Kiểm tra Locket",
        "btn_lang": "🌐 Đổi Ngôn Ngữ",
        "btn_help": "🆘 Hỗ Trợ",
        "prompt_input": (
            f"{E_LOADING} Vui lòng nhập <b>username</b> hoặc <b>link Locket</b> vào tin nhắn trả lời bên dưới:"
        ),
        "lang_select": "🌐 Vui lòng chọn ngôn ngữ / Please select language:",
        "lang_set": f"{E_SUCCESS} Đã cài đặt ngôn ngữ: Tiếng Việt",
        "help_msg": (
            f"<b>{E_MENU} Danh Sách Lệnh:</b>\n\n"
            "/start - Khởi động bot & menu chính\n"
            "/setlang - Đổi ngôn ngữ (VI/EN)\n"
            "/help - Xem trợ giúp này\n\n"
            f"<b>{E_TIP} Cách dùng:</b>\n"
            "1. Bấm '🔎 Kiểm tra Locket'\n"
            "2. Gửi username hoặc link Locket\n"
            "3. Bot phân tích link và trả checklist thao tác hợp lệ."
        ),
        "resolving": f"{E_LOADING} <b>Đang phân tích link/username...</b>",
        "not_found": f"{E_ERROR} Không tìm thấy mã mời công khai từ link/username này.",
        "limit_reached": f"{E_LIMIT} Đã đạt giới hạn trong ngày ({DAILY_LIMIT}/{DAILY_LIMIT}).",
        "queue_almost": f"{E_LOADING} <b>Sắp đến lượt bạn!</b>\nCòn <b>2 người</b> nữa là đến lượt bạn.",
        "admin_noti_sent": f"{E_SUCCESS} Đã gửi thông báo đến tất cả user.",
        "admin_reset": f"{E_SUCCESS} Đã reset lượt dùng cho user {{}}.",
        "admin_only": f"{E_ERROR} Bạn không có quyền sử dụng lệnh này.",
        "checking_status": f"{E_LOADING} <b>Đang tạo báo cáo an toàn...</b>",
        "free_status": "Chưa có dữ liệu subscription công khai",
        "gold_active": f"{E_SUCCESS} <b>Đã ghi nhận trạng thái từ API</b> (Hết hạn: {{}})",
        "user_info_title": f"{E_USER} <b>Thông Tin Locket</b>",
        "btn_upgrade": "📋 TẠO CHECKLIST",
        "queued": (
            f"{E_LOADING} <b>Đã thêm vào hàng chờ</b>\n"
            "Target: <code>{0}</code>\n"
            "Vị trí: <b>#{1}</b> (Còn {2} người trước bạn)..."
        ),
        "processing": f"{E_LOADING} <b>Đang xử lý yêu cầu cá nhân...</b>",
        "success_title": f"{E_SUCCESS} <b>CHECKLIST ĐÃ SẴN SÀNG</b>",
        "generating_dns": f"{E_SHIELD} Đang chuẩn bị cấu hình DNS cá nhân...",
        "fail_title": f"{E_ERROR} <b>Không thể tạo checklist</b>",
        "dns_msg": (
            f"{E_SHIELD} <b>DNS cá nhân (tùy chọn)</b>:\n"
            f"{E_IOS} <b>iOS</b>: <a href='{{}}'>Mở link cấu hình</a>\n"
            f"{E_ANDROID} <b>Android</b>: <code>{{}}.dns.nextdns.io</code>\n\n"
            f"{E_TIP} Chỉ dùng DNS cho mục đích riêng tư/lọc nội dung hợp lệ của bạn."
        ),
        "personal_checklist": (
            "<b>Checklist hợp lệ:</b>\n"
            "• Kiểm tra lại username/link trước khi chia sẻ.\n"
            "• Đăng nhập Locket trên thiết bị của bạn.\n"
            "• Quản lý gói đăng ký qua App Store/Google Play chính thức.\n"
            "• Không chia sẻ token, receipt hoặc mã OTP cho bất kỳ ai."
        ),
        "nextdns_disabled": f"{E_TIP} DNS tự động đang tắt. Bật ENABLE_NEXTDNS=true nếu bạn muốn tạo profile NextDNS cá nhân.",
        "config_error": (
            f"{E_ERROR} Thiếu cấu hình bắt buộc. Hãy tạo file <code>.env</code> từ <code>.env.example</code> "
            "và đặt BOT_TOKEN trước khi chạy bot."
        ),
    },
    "EN": {
        "welcome": (
            f"{E_SUCCESS} <b>{PROJECT_NAME}</b>\n\n"
            "Welcome! This bot helps you manage Locket usernames/links, inspect public invite data, "
            "and generate a legitimate personal-use checklist."
        ),
        "menu_msg": f"{E_MENU} <b>Control Panel</b>\n\n👇 Choose an action below.",
        "btn_input": "🔎 Check Locket",
        "btn_lang": "🌐 Change Language",
        "btn_help": "🆘 Help",
        "prompt_input": (
            f"{E_LOADING} Please enter your <b>username</b> or <b>Locket link</b> in the reply below:"
        ),
        "lang_select": "🌐 Please select language:",
        "lang_set": f"{E_SUCCESS} Language set: English",
        "help_msg": (
            f"<b>{E_MENU} Commands:</b>\n\n"
            "/start - Main menu\n"
            "/setlang - Change language\n"
            "/help - Show this help\n\n"
            f"<b>{E_TIP} How to use:</b>\n"
            "1. Click '🔎 Check Locket'\n"
            "2. Send a username or Locket link\n"
            "3. The bot analyzes the link and returns a legitimate action checklist."
        ),
        "resolving": f"{E_LOADING} <b>Analyzing link/username...</b>",
        "not_found": f"{E_ERROR} Could not find a public invite id from this link/username.",
        "limit_reached": f"{E_LIMIT} Daily limit reached ({DAILY_LIMIT}/{DAILY_LIMIT}).",
        "queue_almost": f"{E_LOADING} <b>Almost your turn!</b>\n<b>2 people</b> ahead of you.",
        "admin_noti_sent": f"{E_SUCCESS} Notification sent to all users.",
        "admin_reset": f"{E_SUCCESS} Usage reset for user {{}}.",
        "admin_only": f"{E_ERROR} You don't have permission.",
        "checking_status": f"{E_LOADING} <b>Preparing safety report...</b>",
        "free_status": "No public subscription data available",
        "gold_active": f"{E_SUCCESS} <b>Status observed from API</b> (Exp: {{}})",
        "user_info_title": f"{E_USER} <b>Locket Information</b>",
        "btn_upgrade": "📋 CREATE CHECKLIST",
        "queued": (
            f"{E_LOADING} <b>Added to Queue</b>\n"
            "Target: <code>{0}</code>\n"
            "Position: <b>#{1}</b> ({2} people ahead)..."
        ),
        "processing": f"{E_LOADING} <b>Processing personal request...</b>",
        "success_title": f"{E_SUCCESS} <b>CHECKLIST READY</b>",
        "generating_dns": f"{E_SHIELD} Preparing personal DNS settings...",
        "fail_title": f"{E_ERROR} <b>Could not create checklist</b>",
        "dns_msg": (
            f"{E_SHIELD} <b>Personal DNS (optional)</b>:\n"
            f"{E_IOS} <b>iOS</b>: <a href='{{}}'>Open configuration link</a>\n"
            f"{E_ANDROID} <b>Android</b>: <code>{{}}.dns.nextdns.io</code>\n\n"
            f"{E_TIP} Use DNS only for your own lawful privacy/content-filtering needs."
        ),
        "personal_checklist": (
            "<b>Legitimate checklist:</b>\n"
            "• Verify the username/link before sharing it.\n"
            "• Sign in to Locket on your own device.\n"
            "• Manage subscriptions via the official App Store/Google Play flow.\n"
            "• Never share tokens, receipts, or OTP codes with anyone."
        ),
        "nextdns_disabled": f"{E_TIP} Automatic DNS is disabled. Set ENABLE_NEXTDNS=true to create your personal NextDNS profile.",
        "config_error": (
            f"{E_ERROR} Missing required configuration. Create <code>.env</code> from <code>.env.example</code> "
            "and set BOT_TOKEN before running the bot."
        ),
    },
}


def T(key: str, lang: str | None = None) -> str:
    if not lang:
        lang = DEFAULT_LANG
    return TEXTS.get(lang, TEXTS["VI"]).get(key, key)


def validate_config() -> list[str]:
    errors: list[str] = []
    if not BOT_TOKEN:
        errors.append("BOT_TOKEN is required")
    if ENABLE_NEXTDNS and not NEXTDNS_KEY:
        errors.append("NEXTDNS_KEY is required when ENABLE_NEXTDNS=true")
    if ADMIN_ID <= 0:
        errors.append("ADMIN_ID should be set to your Telegram user id for admin commands")
    return errors