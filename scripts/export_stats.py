"""Export aggregate bot statistics without exposing per-user request logs."""

import json

from app import database as db


def main() -> None:
    print(json.dumps(db.get_stats(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()