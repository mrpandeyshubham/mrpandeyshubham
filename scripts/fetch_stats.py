"""
Pulls live data for the info card:
  - LeetCode: rating + contests via the public (unauthenticated) GraphQL endpoint
  - CodeChef: rating via the public profile page
  - GitHub: public repo count via the public REST API
No tokens required for any of these. If a source fails or changes its markup,
we keep the last known-good value from data/stats.json instead of writing a zero.
"""
import json
import re
import requests

LEETCODE_USER = "its_shubham_jee"
CODECHEF_USER = "shubham_jee"
GITHUB_USER = "mrpandeyshubham"
STATS_PATH = "data/stats.json"

HEADERS = {"User-Agent": "Mozilla/5.0 (profile-readme-bot)"}


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
    resp = requests.get(f"https://api.github.com/users/{GITHUB_USER}",
                         headers=HEADERS, timeout=15)
    resp.raise_for_status()
    d = resp.json()
    return {"public_repos": d.get("public_repos"), "followers": d.get("followers")}


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
            # only overwrite fields that came back non-null
            for k, v in fresh.items():
                if v is not None:
                    stats[name][k] = v
            print(f"[ok] {name}: {fresh}")
        except Exception as e:
            print(f"[warn] {name} fetch failed ({e}); keeping previous value {stats[name]}")

    with open(STATS_PATH, "w") as f:
        json.dump(stats, f, indent=2)


if __name__ == "__main__":
    main()
