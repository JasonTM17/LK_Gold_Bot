import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Iterator

from app.config import DB_PATH


Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)


@contextmanager
def get_connection() -> Iterator[sqlite3.Connection]:
    conn = sqlite3.connect(DB_PATH, timeout=30)
    conn.row_factory = sqlite3.Row
    try:
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA foreign_keys=ON")
        yield conn
        conn.commit()
    finally:
        conn.close()


def today_key() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def init_db() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS usage_logs (
                user_id INTEGER,
                date TEXT,
                count INTEGER NOT NULL DEFAULT 0,
                PRIMARY KEY (user_id, date)
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS user_settings (
                user_id INTEGER PRIMARY KEY,
                language TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS bot_config (
                key TEXT PRIMARY KEY,
                value TEXT
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS request_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                uid TEXT,
                status TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def get_user_usage(user_id: int) -> int:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT count FROM usage_logs WHERE user_id = ? AND date = ?",
            (user_id, today_key()),
        ).fetchone()
    return int(row["count"]) if row else 0


def increment_usage(user_id: int) -> None:
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO usage_logs (user_id, date, count)
            VALUES (?, ?, 1)
            ON CONFLICT(user_id, date)
            DO UPDATE SET count = count + 1
            """,
            (user_id, today_key()),
        )


def check_can_request(user_id: int, max_limit: int = 5) -> bool:
    return get_user_usage(user_id) < max_limit


def set_lang(user_id: int, lang: str) -> None:
    with get_connection() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO user_settings (user_id, language) VALUES (?, ?)",
            (user_id, lang),
        )


def get_lang(user_id: int) -> str | None:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT language FROM user_settings WHERE user_id = ?",
            (user_id,),
        ).fetchone()
    return row["language"] if row else None


def get_all_users() -> list[int]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT DISTINCT user_id FROM usage_logs UNION SELECT user_id FROM user_settings"
        ).fetchall()
    return [int(row["user_id"]) for row in rows]


def reset_usage(user_id: int) -> None:
    with get_connection() as conn:
        conn.execute(
            "DELETE FROM usage_logs WHERE user_id = ? AND date = ?",
            (user_id, today_key()),
        )


def set_config(key: str, value: str) -> None:
    with get_connection() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO bot_config (key, value) VALUES (?, ?)",
            (key, value),
        )


def get_config(key: str, default: str | None = None) -> str | None:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT value FROM bot_config WHERE key = ?",
            (key,),
        ).fetchone()
    return row["value"] if row else default


def log_request(user_id: int, uid: str, status: str) -> None:
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO request_logs (user_id, uid, status) VALUES (?, ?, ?)",
            (user_id, uid, status),
        )


def get_stats() -> dict[str, int]:
    with get_connection() as conn:
        total = conn.execute("SELECT COUNT(*) AS value FROM request_logs").fetchone()["value"]
        success = conn.execute(
            "SELECT COUNT(*) AS value FROM request_logs WHERE status = 'SUCCESS'"
        ).fetchone()["value"]
        fail = conn.execute(
            "SELECT COUNT(*) AS value FROM request_logs WHERE status != 'SUCCESS'"
        ).fetchone()["value"]
        unique_users = conn.execute(
            "SELECT COUNT(DISTINCT user_id) AS value FROM request_logs"
        ).fetchone()["value"]

    return {
        "total": int(total),
        "success": int(success),
        "fail": int(fail),
        "unique_users": int(unique_users),
    }


init_db()