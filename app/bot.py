import asyncio
import logging
from html import escape

from telegram import ForceReply, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from app import database as db
from app.config import (
    ADMIN_ID,
    BOT_TOKEN,
    DAILY_LIMIT,
    DEFAULT_LANG,
    DONATE_PHOTO,
    ENABLE_NEXTDNS,
    E_ANDROID,
    E_ERROR,
    E_GLOBE,
    E_ID,
    E_LOADING,
    E_STAT,
    E_SUCCESS,
    E_TAG,
    E_USER,
    NEXTDNS_BLOCKLIST,
    NEXTDNS_KEY,
    NUM_WORKERS,
    T,
    validate_config,
)
from app.services import locket, nextdns


logger = logging.getLogger(__name__)

request_queue: asyncio.Queue[dict] = asyncio.Queue()
pending_items: list[dict] = []
queue_lock = asyncio.Lock()


async def update_pending_positions(app) -> None:
    for index, item in enumerate(pending_items):
        position = index + 1
        ahead = index
        try:
            await app.bot.edit_message_text(
                chat_id=item["chat_id"],
                message_id=item["message_id"],
                text=T("queued", item["lang"]).format(escape(item["username"]), position, ahead),
                parse_mode=ParseMode.HTML,
            )

            if ahead == 2:
                await app.bot.send_message(
                    chat_id=item["chat_id"],
                    text=T("queue_almost", item["lang"]),
                    parse_mode=ParseMode.HTML,
                )
        except Exception as exc:
            logger.debug("Could not update queue position: %s", exc)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    lang = db.get_lang(user_id) or DEFAULT_LANG
    db.set_lang(user_id, lang)

    await update.message.reply_text(
        T("welcome", lang),
        parse_mode=ParseMode.HTML,
        reply_markup=get_main_menu_keyboard(lang),
    )


async def setlang_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await show_language_select(update)


def build_admin_help() -> str:
    return (
        "\n\n<b>👑 Admin Control:</b>\n"
        "/noti [msg] - Broadcast message\n"
        "/rs [id] - Reset usage limit\n"
        "/setdonate - Set success photo\n"
        "/stats - View detailed statistics"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    lang = db.get_lang(user_id) or DEFAULT_LANG

    help_text = T("help_msg", lang)
    if user_id == ADMIN_ID:
        help_text += build_admin_help()

    await update.message.reply_text(help_text, parse_mode=ParseMode.HTML)


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        return

    stats = db.get_stats()
    msg = (
        f"{E_STAT} <b>SYSTEM STATISTICS</b>\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        f"{E_USER} <b>Active Users</b>: {stats['unique_users']}\n"
        f"{E_GLOBE} <b>Total Requests</b>: {stats['total']}\n"
        f"{E_SUCCESS} <b>Success</b>: {stats['success']}\n"
        f"{E_ERROR} <b>Failed</b>: {stats['fail']}\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        f"{E_ANDROID} <b>Active Workers</b>: {NUM_WORKERS}\n"
        f"📌 <b>Daily Limit</b>: {DAILY_LIMIT}\n"
        f"⏳ <b>Queue Size</b>: {request_queue.qsize()}\n"
    )
    await update.message.reply_text(msg, parse_mode=ParseMode.HTML)


async def broadcast_worker(bot, users: list[int], text: str, chat_id: int, message_id: int) -> None:
    success = 0
    fail = 0
    total = len(users)

    for index, uid in enumerate(users):
        try:
            await bot.send_message(
                chat_id=uid,
                text=f"📢 <b>ADMIN NOTIFICATION</b>\n\n{escape(text)}",
                parse_mode=ParseMode.HTML,
            )
            success += 1
        except Exception:
            fail += 1

        if (index + 1) % 5 == 0 or (index + 1) == total:
            try:
                await bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=message_id,
                    text=(
                        f"{E_LOADING} <b>Broadcasting...</b>\n"
                        "━━━━━━━━━━━━━━━━━━━\n"
                        f"🔄 <b>Progress</b>: {index + 1}/{total}\n"
                        f"{E_SUCCESS} <b>Success</b>: {success}\n"
                        f"{E_ERROR} <b>Failed</b>: {fail}"
                    ),
                    parse_mode=ParseMode.HTML,
                )
            except Exception as exc:
                logger.debug("Could not update broadcast progress: %s", exc)

        await asyncio.sleep(0.05)

    try:
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=(
                f"{E_SUCCESS} <b>Broadcast Complete!</b>\n"
                "━━━━━━━━━━━━━━━━━━━\n"
                f"👥 <b>Total</b>: {total}\n"
                f"{E_SUCCESS} <b>Success</b>: {success}\n"
                f"{E_ERROR} <b>Failed</b>: {fail}"
            ),
            parse_mode=ParseMode.HTML,
        )
    except Exception as exc:
        logger.debug("Could not update broadcast completion: %s", exc)


async def noti_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        return

    msg = " ".join(context.args).strip()
    if not msg:
        await update.message.reply_text("Usage: /noti {message}")
        return

    users = db.get_all_users()
    if not users:
        await update.message.reply_text("No users found.")
        return

    status_msg = await update.message.reply_text(
        f"{E_LOADING} <b>Starting broadcast to {len(users)} users...</b>",
        parse_mode=ParseMode.HTML,
    )

    asyncio.create_task(
        broadcast_worker(context.bot, users, msg, status_msg.chat_id, status_msg.message_id)
    )


async def reset_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    lang = db.get_lang(user_id) or DEFAULT_LANG

    if user_id != ADMIN_ID:
        return

    if not context.args:
        await update.message.reply_text("Usage: /rs {user_id}")
        return

    try:
        target_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("Invalid User ID")
        return

    db.reset_usage(target_id)
    await update.message.reply_text(T("admin_reset", lang).format(target_id))


async def set_donate_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        return

    photo = None
    if update.message.reply_to_message and update.message.reply_to_message.photo:
        photo = update.message.reply_to_message.photo[-1]
    elif update.message.photo:
        photo = update.message.photo[-1]

    if photo:
        file_id = photo.file_id
        db.set_config("donate_photo", file_id)
        await update.message.reply_text(
            f"✅ Updated Photo ID:\n<code>{escape(file_id)}</code>",
            parse_mode=ParseMode.HTML,
        )
    else:
        await update.message.reply_text("❌ Please reply to a photo with /setdonate to set it.")


async def show_language_select(update: Update) -> None:
    keyboard = [
        [InlineKeyboardButton("Tiếng Việt 🇻🇳", callback_data="setlang_VI")],
        [InlineKeyboardButton("English 🇺🇸", callback_data="setlang_EN")],
    ]
    text = T("lang_select", "EN")

    if update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message.reply_to_message or not update.message.reply_to_message.from_user.is_bot:
        return

    user_id = update.effective_user.id
    text = update.message.text.strip()
    lang = db.get_lang(user_id) or DEFAULT_LANG
    username = locket.normalize_username(text)

    msg = await update.message.reply_text(T("resolving", lang), parse_mode=ParseMode.HTML)

    uid = await locket.resolve_uid(username)
    if not uid:
        await msg.edit_text(T("not_found", lang), parse_mode=ParseMode.HTML)
        return

    if user_id != ADMIN_ID and not db.check_can_request(user_id, DAILY_LIMIT):
        await msg.edit_text(T("limit_reached", lang), parse_mode=ParseMode.HTML)
        return

    await msg.edit_text(T("checking_status", lang), parse_mode=ParseMode.HTML)
    status = await locket.check_status(uid)

    status_text = T("free_status", lang)
    if status and status.get("active"):
        status_text = T("gold_active", lang).format(status.get("expires", "N/A"))

    safe_username = username[:30]
    keyboard = [[InlineKeyboardButton(T("btn_upgrade", lang), callback_data=f"report|{uid}|{safe_username}")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await msg.edit_text(
        f"{T('user_info_title', lang)}\n"
        f"{E_ID}: <code>{escape(uid)}</code>\n"
        f"{E_TAG}: <code>{escape(username)}</code>\n"
        f"{E_STAT} <b>Status</b>: {status_text}\n\n"
        "👇",
        parse_mode=ParseMode.HTML,
        reply_markup=reply_markup,
    )


async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    data = query.data or ""
    user_id = query.from_user.id
    lang = db.get_lang(user_id) or DEFAULT_LANG

    if data.startswith("setlang_"):
        new_lang = data.split("_")[1]
        db.set_lang(user_id, new_lang)
        await query.answer(f"Language: {new_lang}")
        await query.message.edit_text(
            T("menu_msg", new_lang),
            parse_mode=ParseMode.HTML,
            reply_markup=get_main_menu_keyboard(new_lang),
        )
        return

    if data == "menu_lang":
        await show_language_select(update)
        return

    if data == "menu_help":
        help_text = T("help_msg", lang)
        if user_id == ADMIN_ID:
            help_text += build_admin_help()

        await query.edit_message_text(
            help_text,
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="menu_back")]]),
        )
        return

    if data == "menu_back":
        await query.message.edit_text(
            T("menu_msg", lang),
            parse_mode=ParseMode.HTML,
            reply_markup=get_main_menu_keyboard(lang),
        )
        return

    if data == "menu_input":
        try:
            await query.answer()
        except Exception:
            pass
        await query.message.reply_text(
            T("prompt_input", lang),
            parse_mode=ParseMode.HTML,
            reply_markup=ForceReply(selective=True, input_field_placeholder="Username or link..."),
        )
        return

    if data.startswith("report|"):
        parts = data.split("|", 2)
        if len(parts) < 2:
            await query.answer("Invalid request", show_alert=True)
            return

        uid = parts[1]
        username = parts[2] if len(parts) > 2 else uid

        if user_id != ADMIN_ID and not db.check_can_request(user_id, DAILY_LIMIT):
            try:
                await query.answer(T("limit_reached", lang), show_alert=True)
            except Exception:
                pass
            return

        try:
            await query.answer("📋 Queue...")
        except Exception:
            pass

        item = {
            "user_id": user_id,
            "uid": uid,
            "username": username,
            "chat_id": query.message.chat_id,
            "message_id": query.message.message_id,
            "lang": lang,
        }

        async with queue_lock:
            pending_items.append(item)
            position = len(pending_items)
            ahead = position - 1

        await query.edit_message_text(
            T("queued", lang).format(escape(username), position, ahead),
            parse_mode=ParseMode.HTML,
        )

        await request_queue.put(item)


async def queue_worker(app, worker_id: int) -> None:
    logger.info("Worker #%s started", worker_id)

    while True:
        item = await request_queue.get()
        try:
            user_id = item["user_id"]
            uid = item["uid"]
            username = item["username"]
            chat_id = item["chat_id"]
            message_id = item["message_id"]
            lang = item["lang"]

            async with queue_lock:
                if item in pending_items:
                    pending_items.remove(item)
                await update_pending_positions(app)

            async def edit(text: str) -> None:
                try:
                    await app.bot.edit_message_text(
                        chat_id=chat_id,
                        message_id=message_id,
                        text=text,
                        parse_mode=ParseMode.HTML,
                        disable_web_page_preview=True,
                    )
                except Exception as exc:
                    if "Message is not modified" not in str(exc) and "Message to edit not found" not in str(exc):
                        logger.error("Edit message error: %s", exc)

            if user_id != ADMIN_ID and not db.check_can_request(user_id, DAILY_LIMIT):
                await edit(T("limit_reached", lang))
                continue

            logs = [f"[Worker #{worker_id}] Processing request..."]
            loop = asyncio.get_running_loop()

            def safe_log_callback(message: str) -> None:
                logs.append(message)
                asyncio.run_coroutine_threadsafe(update_log_ui(), loop)

            async def update_log_ui() -> None:
                display_logs = "\n".join(escape(line) for line in logs[-10:])
                await edit(f"{T('processing', lang)}\n<pre>{display_logs}</pre>")

            await update_log_ui()

            success, checklist = await locket.create_personal_checklist(uid, username, safe_log_callback)
            db.log_request(user_id, uid, "SUCCESS" if success else "FAIL")

            if success:
                if user_id != ADMIN_ID:
                    db.increment_usage(user_id)

                dns_text = T("nextdns_disabled", lang)
                if ENABLE_NEXTDNS:
                    pid, link = await nextdns.create_profile(
                        NEXTDNS_KEY,
                        NEXTDNS_BLOCKLIST,
                        safe_log_callback,
                    )
                    if link and pid:
                        dns_text = T("dns_msg", lang).format(link, pid)
                    else:
                        dns_text = f"{E_ERROR} NextDNS Error: Check API Key"

                final_msg = (
                    f"{T('success_title', lang)}\n\n"
                    f"{E_TAG}: <code>{escape(username)}</code>\n"
                    f"{E_ID}: <code>{escape(uid)}</code>\n\n"
                    f"{T('personal_checklist', lang)}\n\n"
                    f"<pre>{escape(checklist)}</pre>\n\n"
                    f"{dns_text}"
                )

                current_photo = db.get_config("donate_photo", DONATE_PHOTO)
                if current_photo:
                    try:
                        await app.bot.delete_message(chat_id=chat_id, message_id=message_id)
                    except Exception:
                        pass

                    try:
                        await app.bot.send_photo(
                            chat_id=chat_id,
                            photo=current_photo,
                            caption=final_msg,
                            parse_mode=ParseMode.HTML,
                        )
                    except Exception as exc:
                        logger.error("Send photo error: %s", exc)
                        await app.bot.send_message(
                            chat_id=chat_id,
                            text=final_msg,
                            parse_mode=ParseMode.HTML,
                            disable_web_page_preview=True,
                        )
                else:
                    await edit(final_msg)
            else:
                await edit(f"{T('fail_title', lang)}\nInfo:\n<code>{escape(checklist)}</code>")
        except Exception as exc:
            logger.exception("Worker #%s exception: %s", worker_id, exc)
        finally:
            request_queue.task_done()


def get_main_menu_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(T("btn_input", lang), callback_data="menu_input")],
            [
                InlineKeyboardButton(T("btn_lang", lang), callback_data="menu_lang"),
                InlineKeyboardButton(T("btn_help", lang), callback_data="menu_help"),
            ],
        ]
    )


def configure_logging() -> None:
    logging.basicConfig(
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        level=logging.INFO,
    )
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("telegram").setLevel(logging.WARNING)
    logging.getLogger("aiohttp").setLevel(logging.WARNING)


def run_bot() -> None:
    configure_logging()

    config_errors = validate_config()
    if config_errors:
        for error in config_errors:
            logger.error("Configuration error: %s", error)
        if not BOT_TOKEN:
            raise RuntimeError("BOT_TOKEN is required. Copy .env.example to .env and fill it in.")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("setlang", setlang_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("noti", noti_command))
    app.add_handler(CommandHandler("rs", reset_command))
    app.add_handler(CommandHandler("setdonate", set_donate_command))
    app.add_handler(CommandHandler("stats", stats_command))

    app.add_handler(CallbackQueryHandler(callback_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    async def post_init(application) -> None:
        for index in range(1, NUM_WORKERS + 1):
            asyncio.create_task(queue_worker(application, index))

    app.post_init = post_init
    logger.info("Bot is running with %s worker(s)", NUM_WORKERS)
    app.run_polling()