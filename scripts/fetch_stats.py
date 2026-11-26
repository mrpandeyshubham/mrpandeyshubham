"""
Pulls live data for the info card and stats card:
  - LeetCode: rating + solved + contests via GraphQL
  - CodeChef: rating via public profile page
  - GitHub: repo count, followers, total stars, and balanced language breakdown
    via the REST API (caps per-repo bytes so vendored/env commits in any single
    repo don't distort the portfolio language distribution).
If a source fails or is blocked, keeps the last known-good value in data/stats.json.
"""
import datetime
import json
import os
import re
import requests

LEETCODE_USER = "its_shubham_jee"
CODECHEF_USER = "shubham_jee"
GITHUB_USER = "mrpandeyshubham"
STATS_PATH = "data/stats.json"

# Cap each repository's total byte weight so committed dependencies/venvs
# in a single repo cannot overwhelm the rest of the codebase.
MAX_REPO_LANG_BYTES = 350_000
IGNORED_LANGS = {"Batchfile", "Roff", "Meson", "Fortran", "Go Template", "Lua", "Cython"}

HEADERS = {"User-Agent": "Mozilla/5.0 (profile-readme-bot)"}

GH_TOKEN = os.environ.get("GITHUB_TOKEN")
GH_HEADERS = {**HEADERS, "Accept": "application/vnd.github+json"}
if GH_TOKEN:
    GH_HEADERS["Authorization"] = f"Bearer {GH_TOKEN}"


def load_previous():
    try:
        with open(STATS_PATH, encoding="utf-8") as f:
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
        headers={
            **HEADERS,
            "Referer": f"https://leetcode.com/{LEETCODE_USER}/",
            "Content-Type": "application/json",
        },
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
    resp = requests.get(
        f"https://www.codechef.com/users/{CODECHEF_USER}",
        headers=HEADERS,
        timeout=15,
    )
    resp.raise_for_status()
    m = re.search(r'rating-number">\s*([\d]+)', resp.text)
    rating = int(m.group(1)) if m else None
    return {"rating": rating}


def fetch_github():
    resp = requests.get(
        f"https://api.github.com/users/{GITHUB_USER}",
        headers=GH_HEADERS,
        timeout=15,
    )
    resp.raise_for_status()
    profile = resp.json()

    repos_resp = requests.get(
        f"https://api.github.com/users/{GITHUB_USER}/repos",
        params={"per_page": 100, "type": "owner"},
        headers=GH_HEADERS,
        timeout=15,
    )
    repos_resp.raise_for_status()
    repos = repos_resp.json()

    total_stars = 0
    lang_bytes = {}
    lang_complete = True
    for repo in repos:
        if repo.get("fork"):
            continue
        total_stars += repo.get("stargazers_count", 0)
        lang_url = repo.get("languages_url")
        if not lang_url:
            continue
        lr = requests.get(lang_url, headers=GH_HEADERS, timeout=15)
        if lr.status_code != 200:
            lang_complete = False
            continue
        repo_langs = {k: v for k, v in lr.json().items() if k not in IGNORED_LANGS and v > 0}
        repo_total = sum(repo_langs.values())
        if repo_total <= 0:
            continue
        scale = min(1.0, MAX_REPO_LANG_BYTES / repo_total)
        for lang, count in repo_langs.items():
            lang_bytes[lang] = lang_bytes.get(lang, 0.0) + count * scale

    languages = []
    if lang_complete and lang_bytes:
        total_bytes = sum(lang_bytes.values()) or 1.0
        top_langs = sorted(lang_bytes.items(), key=lambda kv: kv[1], reverse=True)[:6]
        languages = [
            {"name": name, "pct": round(count / total_bytes * 100, 1)}
            for name, count in top_langs
            if (count / total_bytes * 100) >= 0.5
        ]

    return {
        "public_repos": profile.get("public_repos"),
        "followers": profile.get("followers"),
        "total_stars": total_stars,
        "languages": languages,
    }


def main():
    prev = load_previous()
    stats = json.loads(json.dumps(prev)) if prev else {}
    stats.setdefault("leetcode", {})
    stats.setdefault("codechef", {})
    stats.setdefault("github", {})

    for name, fn in (
        ("leetcode", fetch_leetcode),
        ("codechef", fetch_codechef),
        ("github", fetch_github),
    ):
        try:
            fresh = fn()
            for k, v in fresh.items():
                if v is not None and v != []:
                    stats[name][k] = v
            print(f"[ok] {name}: {fresh}")
        except Exception as e:
            print(f"[warn] {name} fetch failed ({e}); keeping previous value {stats[name]}")

    today_utc = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    prev_core = {k: v for k, v in prev.items() if k != "updated_at"}
    new_core = {k: v for k, v in stats.items() if k != "updated_at"}
    if new_core != prev_core or (prev.get("updated_at") or "")[:10] != today_utc:
        stats["updated_at"] = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    elif "updated_at" in prev:
        stats["updated_at"] = prev["updated_at"]

    os.makedirs(os.path.dirname(STATS_PATH), exist_ok=True)
    with open(STATS_PATH, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)


if __name__ == "__main__":
    main()
