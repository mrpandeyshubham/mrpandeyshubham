import json
import requests
from bs4 import BeautifulSoup

USERNAME = "mrpandeyshubham"
URL = f"https://github.com/users/{USERNAME}/contributions"

resp = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=20)
resp.raise_for_status()
soup = BeautifulSoup(resp.text, "html.parser")

h2 = soup.find("h2", id="js-contribution-activity-description")
total_contributions = 0
if h2:
    for token in h2.get_text().split():
        if token.isdigit():
            total_contributions = int(token)
            break

cells = soup.select("td.ContributionCalendar-day")
days = []
for c in cells:
    date = c.get("data-date")
    level = int(c.get("data-level", 0))
    if date:
        days.append({"date": date, "level": level})
days.sort(key=lambda d: d["date"])

run = 0
for d in reversed(days):
    if d["level"] > 0:
        run += 1
    else:
        break
current_streak = run

longest = run_len = 0
for d in days:
    if d["level"] > 0:
        run_len += 1
        longest = max(longest, run_len)
    else:
        run_len = 0

data = {
    "days": days,
    "current_streak": current_streak,
    "longest_streak": longest,
    "active_days": sum(1 for d in days if d["level"] > 0),
    "total_days_tracked": len(days),
    "total_contributions": total_contributions,
}

with open("data/contributions.json", "w") as f:
    json.dump(data, f, indent=2)

print(f"Fetched {len(days)} days, {total_contributions} total contributions, "
      f"current streak {current_streak}, longest streak {longest}")
