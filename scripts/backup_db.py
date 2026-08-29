"""Create a timestamped SQLite backup in the data directory."""

from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path

from app.config import DATA_DIR, DB_PATH


def main() -> None:
    source = Path(DB_PATH)
    if not source.exists():
        raise SystemExit(f"Database not found: {source}")

    backup_dir = Path(DATA_DIR) / "backups"
    backup_dir.mkdir(parents=True, exist_ok=True)
    target = backup_dir / f"bot_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
    shutil.copy2(source, target)
    print(target)


if __name__ == "__main__":
    main()