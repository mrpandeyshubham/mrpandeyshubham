"""
Fetches real-time GitHub contribution calendar data for mrpandeyshubham.
Uses GitHub GraphQL API when GITHUB_TOKEN is available (exact daily counts),
and falls back to GitHub's public /users/<user>/contributions calendar HTML
when running without a token.
"""
import datetime
import json
import os
import re
import requests

USERNAME = "mrpandeyshubham"
OUT_PATH = "data/contributions.json"
HEADERS = {"User-Agent": "Mozilla/5.0 (profile-readme-bot)"}


def fetch_via_graphql(token: str) -> tuple[list[dict], int]:
    query = """
    query($login: String!) {
      user(login: $login) {
        contributionsCollection {
          contributionCalendar {
            totalContributions
            weeks {
              contributionDays {
                date
                contributionCount
                contributionLevel
              }
            }
          }
        }
      }
    }"""
    level_map = {
        "NONE": 0,
        "FIRST_QUARTILE": 1,
        "SECOND_QUARTILE": 2,
        "THIRD_QUARTILE": 3,
        "FOURTH_QUARTILE": 4,
    }
    resp = requests.post(
        "https://api.github.com/graphql",
        json={"query": query, "variables": {"login": USERNAME}},
        headers={**HEADERS, "Authorization": f"Bearer {token}"},
        timeout=20,
    )
    resp.raise_for_status()
    payload = resp.json()
    if "errors" in payload:
        raise RuntimeError(payload["errors"])
    cal = payload["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    days = []
    for week in cal["weeks"]:
        for day in week["contributionDays"]:
            days.append({
                "date": day["date"],
                "level": level_map.get(day["contributionLevel"], 0),
                "count": day["contributionCount"],
            })
    days.sort(key=lambda d: d["date"])
    return days, int(cal["totalContributions"])


def fetch_via_html() -> tuple[list[dict], int]:
    url = f"https://github.com/users/{USERNAME}/contributions"
    resp = requests.get(url, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    html = resp.text

    total_contributions = 0
    m_h2 = re.search(
        r'id="js-contribution-activity-description"[^>]*>(.*?)</h2>',
        html,
        re.S,
    )
    if m_h2:
        h2_text = re.sub(r"<[^>]+>", " ", m_h2.group(1))
        m_num = re.search(r"([\d,]+)\s+contribution", h2_text)
        if m_num:
            total_contributions = int(m_num.group(1).replace(",", ""))

    # Map tooltip id -> exact contribution count if present
    tip_counts = {}
    for m_tip in re.finditer(
        r'<tool-tip[^>]*\bfor="([^"]+)"[^>]*>(.*?)</tool-tip>', html, re.S
    ):
        tip_id, tip_text = m_tip.group(1), m_tip.group(2).strip()
        m_cnt = re.match(r"(\d+)\s+contribution", tip_text)
        tip_counts[tip_id] = int(m_cnt.group(1)) if m_cnt else 0

    days = []
    for cell_html in re.findall(
        r'<td[^>]*class="[^"]*ContributionCalendar-day[^"]*"[^>]*>', html
    ):
        m_date = re.search(r'data-date="([^"]+)"', cell_html)
        if not m_date:
            continue
        m_level = re.search(r'data-level="(\d+)"', cell_html)
        m_id = re.search(r'\bid="([^"]+)"', cell_html)
        level = int(m_level.group(1)) if m_level else 0
        count = tip_counts.get(m_id.group(1)) if m_id else None
        entry = {"date": m_date.group(1), "level": level}
        if count is not None:
            entry["count"] = count
        days.append(entry)

    days.sort(key=lambda d: d["date"])
    if total_contributions == 0 and any("count" in d for d in days):
        total_contributions = sum(d.get("count", 0) for d in days)
    return days, total_contributions


def compute_streaks(days: list[dict]) -> tuple[int, int]:
    if not days:
        return 0, 0

    # Current streak: if today has 0 so far, allow streak to continue from yesterday
    idx = len(days) - 1
    if days[idx]["level"] == 0 and idx > 0:
        idx -= 1
    current_streak = 0
    while idx >= 0 and days[idx]["level"] > 0:
        current_streak += 1
        idx -= 1

    longest = run_len = 0
    for d in days:
        if d["level"] > 0:
            run_len += 1
            if run_len > longest:
                longest = run_len
        else:
            run_len = 0

    return current_streak, longest


def main():
    token = os.environ.get("GITHUB_TOKEN")
    days, total_contributions = None, 0

    if token:
        try:
            days, total_contributions = fetch_via_graphql(token)
            print("[ok] fetched contributions via GitHub GraphQL")
        except Exception as e:
            print(f"[warn] GraphQL failed ({e}); falling back to public HTML")

    if not days:
        days, total_contributions = fetch_via_html()
        print("[ok] fetched contributions via public HTML")

    current_streak, longest_streak = compute_streaks(days)
    active_days = sum(1 for d in days if d["level"] > 0)
    last_30_active = sum(1 for d in days[-30:] if d["level"] > 0)

    prev = {}
    if os.path.exists(OUT_PATH):
        try:
            with open(OUT_PATH, encoding="utf-8") as f:
                prev = json.load(f)
        except Exception:
            prev = {}

    core = {
        "username": USERNAME,
        "total_contributions": total_contributions,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "active_days": active_days,
        "last_30_active": last_30_active,
        "total_days_tracked": len(days),
        "days": days,
    }
    prev_core = {k: prev.get(k) for k in core}
    today_utc = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    prev_date = (prev.get("updated_at") or "")[:10]

    if core == prev_core and prev_date == today_utc:
        print("No contribution changes since last sync; keeping updated_at unchanged.")
        return

    data = {
        **core,
        "updated_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(
        f"Fetched {len(days)} days, {total_contributions} contributions, "
        f"current streak {current_streak}, longest streak {longest_streak}, active {active_days}"
    )


if __name__ == "__main__":
    main()
