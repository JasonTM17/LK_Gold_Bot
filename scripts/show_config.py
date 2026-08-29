"""Print a redacted configuration summary for local debugging."""

from app import config


def mask(value: str) -> str:
    if not value:
        return "<empty>"
    if len(value) <= 8:
        return "********"
    return f"{value[:4]}...{value[-4:]}"


def main() -> None:
    rows = {
        "PROJECT_NAME": config.PROJECT_NAME,
        "BOT_TOKEN": mask(config.BOT_TOKEN),
        "ADMIN_ID": str(config.ADMIN_ID),
        "DEFAULT_LANG": config.DEFAULT_LANG,
        "NUM_WORKERS": str(config.NUM_WORKERS),
        "DAILY_LIMIT": str(config.DAILY_LIMIT),
        "ENABLE_NEXTDNS": str(config.ENABLE_NEXTDNS),
        "NEXTDNS_KEY": mask(config.NEXTDNS_KEY),
        "DATA_DIR": str(config.DATA_DIR),
        "DB_PATH": str(config.DB_PATH),
    }
    width = max(len(key) for key in rows)
    for key, value in rows.items():
        print(f"{key:<{width}} : {value}")


if __name__ == "__main__":
    main()