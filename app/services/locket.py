import logging
import re
from urllib.parse import unquote, urlparse

import aiohttp


logger = logging.getLogger(__name__)

INVITE_ID_PATTERN = re.compile(r"/invites/([A-Za-z0-9]{20,40})")
USERNAME_PATTERN = re.compile(r"^[A-Za-z0-9_.-]{1,50}$")
REQUEST_TIMEOUT_SECONDS = 10
USER_AGENT = "Mozilla/5.0 (compatible; LocketPersonalAssistant/1.0)"


def clean_username_candidate(value: str) -> str:
    """Return a display-safe username candidate without common user prefixes."""
    return (value or "").strip().strip("/@")


def normalize_username(raw_value: str) -> str:
    """Extract a reasonable Locket username from user-provided text."""
    value = (raw_value or "").strip()
    if not value:
        return ""

    if "locket.cam/" in value:
        parsed = urlparse(value if value.startswith(("http://", "https://")) else f"https://{value}")
        path = parsed.path.strip("/")
        if path:
            return clean_username_candidate(path.split("/")[-1])

    return clean_username_candidate(value.split()[0])


def extract_invite_id(*texts: str) -> str | None:
    for text in texts:
        if not text:
            continue

        decoded = unquote(text)
        match = INVITE_ID_PATTERN.search(decoded)
        if match:
            return match.group(1)

    return None


async def resolve_uid(username: str) -> str | None:
    """Return the public invite id found on a Locket profile page, if present."""
    direct_invite_id = extract_invite_id(username)
    if direct_invite_id:
        return direct_invite_id

    username = normalize_username(username)
    if not USERNAME_PATTERN.match(username):
        return None

    url = f"https://locket.cam/{username}"
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml",
    }

    try:
        timeout = aiohttp.ClientTimeout(total=REQUEST_TIMEOUT_SECONDS)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url, headers=headers, allow_redirects=True) as response:
                html = await response.text(errors="ignore")
                return extract_invite_id(str(response.url), html)
    except aiohttp.ClientError as exc:
        logger.warning("Could not fetch Locket profile %s: %s", username, exc)
        return None


async def check_status(uid: str) -> dict[str, str | bool]:
    """Return a local, privacy-preserving status summary for the provided public id."""
    if not uid:
        return {"active": False, "expires": "N/A"}

    return {
        "active": False,
        "expires": "N/A",
        "note": "Only public invite information is checked by this personal assistant.",
    }


async def create_personal_checklist(
    uid: str,
    username: str,
    log_callback=None,
) -> tuple[bool, str]:
    """Create a safe personal-use checklist for a Locket profile."""

    def log(message: str) -> None:
        if log_callback:
            log_callback(message)

    safe_username = username or "unknown"
    safe_uid = uid or "unknown"

    log("Validating public Locket identifier...")
    if not safe_uid or safe_uid == "unknown":
        return False, "Missing public invite identifier"

    log("Preparing account-safety checklist...")
    checklist = (
        f"Target: {safe_username}\n"
        f"Public invite id: {safe_uid}\n"
        "Recommendations:\n"
        "- Keep your account credentials private.\n"
        "- Manage subscriptions only through official app-store channels.\n"
        "- Review connected devices and remove unknown sessions.\n"
        "- Avoid sharing private account data in chats or screenshots."
    )
    log("Checklist generated successfully.")
    return True, checklist