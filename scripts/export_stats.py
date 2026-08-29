"""Export aggregate bot statistics without exposing per-user request logs."""

import json
import sys
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

load_dotenv()

from app import database as db


def main() -> None:
    print(json.dumps(db.get_stats(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()