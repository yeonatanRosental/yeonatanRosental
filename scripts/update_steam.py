"""Render public Steam activity as a self-contained GitHub README card."""

from datetime import datetime, timezone
from html import escape, unescape
import re
from pathlib import Path
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

PROFILE_URL = "https://steamcommunity.com/id/oppoo12/?xml=1"
STEAM_ID = "76561198241017990"
OUTPUT = Path(__file__).resolve().parents[1] / "assets" / "steam.svg"


def activity(document):
    profile = ET.fromstring(document)
    if profile.tag != "profile" or profile.findtext("steamID64") != STEAM_ID:
        raise ValueError("Steam did not return the expected profile; keeping the existing card")
    if profile.findtext("privacyState") != "public":
        return "PROFILE PRIVATE", "Game activity is not public", []
    state = profile.findtext("onlineState", "offline")
    current = profile.findtext("inGameInfo/gameName", "").strip()
    if state == "in-game" and not current:
        message = profile.findtext("stateMessage", "")
        parts = re.split(r"<br\s*/?>", message, maxsplit=1, flags=re.IGNORECASE)
        if len(parts) == 2:
            current = unescape(parts[1]).strip()
    recent = [
        (game.findtext("gameName", "").strip(), game.findtext("hoursPlayed", "").strip())
        for game in profile.findall("mostPlayedGames/mostPlayedGame")
        if game.findtext("gameName", "").strip()
    ][:3]
    if state == "in-game" and current:
        return "NOW PLAYING", current, recent
    if recent:
        return "RECENT ACTIVITY", "Currently " + state.replace("-", " "), recent
    return state.upper(), "No public game activity available", []


def render(document, updated):
    status, headline, games = activity(document)

    def label(value, x, y, size=13, color="#cbd9ce", limit=62):
        value = " ".join(value.split())
        if len(value) > limit:
            value = value[: limit - 1] + "…"
        return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}">{escape(value)}</text>'

    rows = [label(status, 24, 65, 12, "#86efac"), label(headline, 24, 98, 19, "#e4f8e8", 46)]
    if games:
        rows.append(label("RECENT GAMES / HOURS IN THE LAST 2 WEEKS", 24, 133, 10))
        for index, (name, hours) in enumerate(games):
            rows.append(label(name, 24, 158 + index * 25, limit=49))
            rows.append(label(f"{hours} h" if hours else "—", 500, 158 + index * 25, limit=10))
    else:
        rows.append(label("Current and recent games appear when shared by Steam.", 24, 145, 11))
    rows.append(label(f"CHECKED {updated} UTC / HOURLY", 24, 244, 10))
    return '\n'.join([
        '<svg xmlns="http://www.w3.org/2000/svg" width="600" height="264" viewBox="0 0 600 264" role="img" aria-labelledby="title desc">',
        '<title id="title">oppoo12 / Steam activity</title>',
        f'<desc id="desc">{escape(status + ": " + headline)}. Updated {escape(updated)} UTC.</desc>',
        '<rect width="600" height="264" fill="#27372b"/>',
        '<path d="M1 263V1h598" fill="none" stroke="#afc3a7" stroke-width="2"/>',
        '<path d="M1 263h598V1" fill="none" stroke="#071009" stroke-width="2"/>',
        '<rect x="5" y="5" width="590" height="24" fill="#174c30"/>',
        '<rect x="12" y="37" width="576" height="191" fill="#0d140f"/>',
        '<g font-family="Courier New,ui-monospace,monospace">',
        label("steam.exe / oppoo12", 15, 22, 12, "#e4f8e8"),
        label("─ □ ×", 541, 22, 12),
        *rows,
        '</g></svg>\n',
    ])


def main():
    checked = datetime.now(timezone.utc)
    request = Request(
        f"{PROFILE_URL}&t={int(checked.timestamp())}",
        headers={"User-Agent": "GitHub-Profile-Steam-Card/1.0", "Cache-Control": "no-cache"},
    )
    with urlopen(request, timeout=30) as response:
        document = response.read()
    card = render(document, datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M"))
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(card, encoding="utf-8")


if __name__ == "__main__":
    main()
