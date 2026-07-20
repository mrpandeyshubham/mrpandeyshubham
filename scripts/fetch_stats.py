"""
Pulls live data for the info card and stats card:
  - LeetCode: rating + contests via the public (unauthenticated) GraphQL endpoint
  - CodeChef: rating via the public profile page
  - GitHub: repo count, followers, total stars, and language breakdown via the
    public REST API (uses GITHUB_TOKEN if present, to avoid the low anonymous
    rate limit -- Actions provides this automatically via secrets.GITHUB_TOKEN)
No tokens are *required*, but GITHUB_TOKEN makes the GitHub calls reliable.
If a source fails or changes its markup, we keep the last known-good value
from data/stats.json instead of writing a zero.
"""
import json
import os
import re
import requests

LEETCODE_USER = "its_shubham_jee"
CODECHEF_USER = "shubham_jee"
GITHUB_USER = "mrpandeyshubham"
STATS_PATH = "data/stats.json"

HEADERS = {"User-Agent": "Mozilla/5.0 (profile-readme-bot)"}

GH_TOKEN = os.environ.get("GITHUB_TOKEN")
GH_HEADERS = {**HEADERS, "Accept": "application/vnd.github+json"}
if GH_TOKEN:
    GH_HEADERS["Authorization"] = f"Bearer {GH_TOKEN}"


def load_previous():
    try:
        with open(STATS_PATH) as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def fetch_leetcode():
    query = """
    query userProfile($username: String!) {
      matchedUser(username: $username) {
        submitStats: submitStatsGlobal { acSubmissionNum { difficulty count } }
      }
      userContestRanking(username: $username) { attendedContestsCount rating }
    }"""
    resp = requests.post(
        "https://leetcode.com/graphql",
        json={"query": query, "variables": {"username": LEETCODE_USER}},
        headers={**HEADERS, "Referer": f"https://leetcode.com/{LEETCODE_USER}/",
                 "Content-Type": "application/json"},
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()["data"]
    solved = 0
    for row in data["matchedUser"]["submitStats"]["acSubmissionNum"]:
        if row["difficulty"] == "All":
            solved = row["count"]
    rating = round(data["userContestRanking"]["rating"])
    contests = data["userContestRanking"]["attendedContestsCount"]
    return {"solved": solved, "rating": rating, "contests": contests}


def fetch_codechef():
    resp = requests.get(f"https://www.codechef.com/users/{CODECHEF_USER}",
                         headers=HEADERS, timeout=15)
    resp.raise_for_status()
    html = resp.text
    m = re.search(r'rating-number">\s*([\d]+)', html)
    rating = int(m.group(1)) if m else None
    return {"rating": rating}


def fetch_github():
    """Profile basics + total stars + aggregated language bytes across
    non-fork public repos."""
    resp = requests.get(f"https://api.github.com/users/{GITHUB_USER}",
                         headers=GH_HEADERS, timeout=15)
    resp.raise_for_status()
    profile = resp.json()

    repos_resp = requests.get(
        f"https://api.github.com/users/{GITHUB_USER}/repos",
        params={"per_page": 100, "type": "owner"},
        headers=GH_HEADERS, timeout=15,
    )
    repos_resp.raise_for_status()
    repos = repos_resp.json()

    total_stars = 0
    lang_bytes = {}
    for repo in repos:
        if repo.get("fork"):
            continue
        total_stars += repo.get("stargazers_count", 0)
        lang_url = repo.get("languages_url")
        if not lang_url:
            continue
        lr = requests.get(lang_url, headers=GH_HEADERS, timeout=15)
        if lr.status_code != 200:
            continue
        for lang, count in lr.json().items():
            lang_bytes[lang] = lang_bytes.get(lang, 0) + count

    total_bytes = sum(lang_bytes.values()) or 1
    top_langs = sorted(lang_bytes.items(), key=lambda kv: kv[1], reverse=True)[:6]
    languages = [
        {"name": name, "pct": round(count / total_bytes * 100, 1)}
        for name, count in top_langs
    ]

    return {
        "public_repos": profile.get("public_repos"),
        "followers": profile.get("followers"),
        "total_stars": total_stars,
        "languages": languages,
    }


def main():
    stats = load_previous()
    stats.setdefault("leetcode", {})
    stats.setdefault("codechef", {})
    stats.setdefault("github", {})

    for name, fn in (("leetcode", fetch_leetcode),
                      ("codechef", fetch_codechef),
                      ("github", fetch_github)):
        try:
            fresh = fn()
            # only overwrite fields that came back non-null / non-empty
            for k, v in fresh.items():
                if v is not None and v != []:
                    stats[name][k] = v
            print(f"[ok] {name}: {fresh}")
        except Exception as e:
            print(f"[warn] {name} fetch failed ({e}); keeping previous value {stats[name]}")

    with open(STATS_PATH, "w") as f:
        json.dump(stats, f, indent=2)


if __name__ == "__main__":
    main()
