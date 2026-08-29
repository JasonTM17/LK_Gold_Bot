"""Local health check for configuration, imports, and SQLite availability."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

load_dotenv()

from app import config, database


def main() -> None:
    config_errors = config.validate_config()
    database.init_db()
    stats = database.get_stats()

    result = {
        "ok": not any(error == "BOT_TOKEN is required" for error in config_errors),
        "config_errors": config_errors,
        "database": str(config.DB_PATH),
        "stats": stats,
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()