import datetime as dt
import logging
from collections.abc import Callable, Iterable

import aiohttp


logger = logging.getLogger(__name__)
LogCallback = Callable[[str], None] | None


async def _add_denylist_domains(
    session: aiohttp.ClientSession,
    profile_id: str,
    domains: Iterable[str],
    log_callback: LogCallback = None,
) -> None:
    denylist_url = f"https://api.nextdns.io/profiles/{profile_id}/denylist"

    for domain in domains:
        domain = domain.strip()
        if not domain:
            continue

        try:
            async with session.post(denylist_url, json={"id": domain, "active": True}) as response:
                if 200 <= response.status < 300:
                    if log_callback:
                        log_callback(f"Added DNS denylist rule: {domain}")
                else:
                    body = await response.text()
                    logger.warning("NextDNS rule failed for %s: %s %s", domain, response.status, body)
        except aiohttp.ClientError as exc:
            logger.warning("NextDNS rule request failed for %s: %s", domain, exc)


async def create_profile(
    api_key: str,
    blocklist: Iterable[str] | None = None,
    log_callback: LogCallback = None,
) -> tuple[str | None, str | None]:
    """Create or reuse a daily personal NextDNS profile."""

    def log(message: str) -> None:
        if log_callback:
            log_callback(message)

    if not api_key:
        log("NEXTDNS_KEY is not configured.")
        return None, None

    headers = {
        "X-Api-Key": api_key,
        "Content-Type": "application/json",
    }
    profile_name = f"Personal-Locket-{dt.datetime.now().strftime('%Y-%m-%d')}"
    list_url = "https://api.nextdns.io/profiles"
    timeout = aiohttp.ClientTimeout(total=20)

    async with aiohttp.ClientSession(headers=headers, timeout=timeout) as session:
        try:
            log(f"Checking existing NextDNS profile: {profile_name}")
            async with session.get(list_url) as response:
                if response.status == 200:
                    data = await response.json()
                    for profile in data.get("data", []):
                        if profile.get("name") == profile_name:
                            profile_id = profile.get("id")
                            if profile_id and blocklist:
                                await _add_denylist_domains(session, profile_id, blocklist, log_callback)
                            log(f"Reusing profile: {profile_id}")
                            return profile_id, f"https://apple.nextdns.io/?profile={profile_id}"
        except aiohttp.ClientError as exc:
            logger.warning("Could not list NextDNS profiles: %s", exc)

        try:
            log(f"Creating NextDNS profile: {profile_name}")
            async with session.post(list_url, json={"name": profile_name}) as response:
                if response.status != 200:
                    body = await response.text()
                    logger.warning("NextDNS profile creation failed: %s %s", response.status, body)
                    return None, None

                data = await response.json()
                profile_id = data.get("data", {}).get("id")
                if not profile_id:
                    logger.warning("NextDNS profile response did not include an id")
                    return None, None

                if blocklist:
                    await _add_denylist_domains(session, profile_id, blocklist, log_callback)

                log(f"NextDNS profile ready: {profile_id}")
                return profile_id, f"https://apple.nextdns.io/?profile={profile_id}"
        except aiohttp.ClientError as exc:
            logger.warning("Could not create NextDNS profile: %s", exc)
            return None, None