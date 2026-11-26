import json
import os
from html import escape

STATIC = os.environ.get("STATIC") == "1"


def load_json(path: str) -> dict:
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


stats = load_json("data/stats.json")
contrib = load_json("data/contributions.json")

lc = stats.get("leetcode", {})
cc = stats.get("codechef", {})
gh = stats.get("github", {})

lc_rating = lc.get("rating", 1753)
lc_solved = lc.get("solved", 296)
lc_contests = lc.get("contests", 25)
cc_rating = cc.get("rating", 1431)
repos = gh.get("public_repos", 13)

total_contribs = contrib.get("total_contributions", 280)
cur_streak = contrib.get("current_streak", 0)
best_streak = contrib.get("longest_streak", 0)
updated_at = (contrib.get("updated_at") or stats.get("updated_at") or "")[:10] or "live"

WIDTH, HEIGHT = 520, 350
PAD_X = 24
TITLE_H = 36
ROW_H = 24
START_Y = TITLE_H + 34

ROWS = [
    ("Role",       "Final-Year CSE · Full-Stack & AI", "#79c0ff"),
    ("Host",       "Parul University (B.Tech 2023–27)", "#79c0ff"),
    ("Flagship",   "TrueEyeball · UniBill · BachatPay", "#7ee787"),
    ("Stack",      "Python, JS/TS, React, Node, Mongo", "#d2a8ff"),
    ("AI & CV",    "OpenCV, MediaPipe, Watsonx.ai, RAG", "#d2a8ff"),
    ("Cloud",      "IBM Cloud, GCP, Docker, GH Actions", "#a5d6ff"),
    ("LeetCode",   f"{lc_rating} rating · {lc_solved} solved ({lc_contests}c)", "#ffa657"),
    ("CodeChef",   f"{cc_rating} rating · 9+ contests", "#ffa657"),
    ("GitHub",     f"{repos} public repos · {total_contribs} contribs (1y)", "#3fb950"),
    ("Streak",     f"{cur_streak}d current · {best_streak}d longest", "#ff7b72"),
    ("Synced",     f"{updated_at} (automated daily)", "#8b949e"),
]

rows_svg = []
for i, (label, value, color) in enumerate(ROWS):
    y = START_Y + i * ROW_H
    delay = 0.25 + i * 0.06
    cls = "" if STATIC else f' style="animation-delay:{delay:.2f}s"'
    row_class = "row static" if STATIC else "row"
    rows_svg.append(
        f'<g class="{row_class}"{cls}>'
        f'<text x="{PAD_X}" y="{y}" class="label" fill="{color}">{escape(label)}</text>'
        f'<text x="{PAD_X + 94}" y="{y}" class="sep">:</text>'
        f'<text x="{PAD_X + 108}" y="{y}" class="value">{escape(value)}</text>'
        f'</g>'
    )

bar_colors = ["#ff5f56", "#ffbd2e", "#3fb950", "#38bdf8", "#a371f7", "#f778ba", "#5ee6c9", "#ffa657"]
bar_y = HEIGHT - 24
bars = "".join(
    f'<rect x="{PAD_X + i * 16}" y="{bar_y}" width="12" height="10" rx="2.5" fill="{c}"/>'
    for i, c in enumerate(bar_colors)
)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">
  <style>
    .bg {{ fill: #0d1117; stroke: #30363d; stroke-width: 1; }}
    .titlebar {{ fill: #161b22; }}
    .path {{ fill: #8b949e; font: 12px 'JetBrains Mono', 'Fira Code', ui-monospace, monospace; }}
    .label {{ font: 700 12.5px 'JetBrains Mono', 'Fira Code', ui-monospace, monospace; }}
    .sep {{ fill: #484f58; font: 12.5px 'JetBrains Mono', 'Fira Code', ui-monospace, monospace; }}
    .value {{ fill: #c9d1d9; font: 12.5px 'JetBrains Mono', 'Fira Code', ui-monospace, monospace; }}
    .row {{ opacity: 0; animation: fadeSlide 0.45s ease-out forwards; }}
    .row.static {{ opacity: 1; }}
    @keyframes fadeSlide {{
      0% {{ opacity: 0; transform: translateX(-8px); }}
      100% {{ opacity: 1; transform: translateX(0); }}
    }}
  </style>
  <rect class="bg" x="0.5" y="0.5" width="{WIDTH-1}" height="{HEIGHT-1}" rx="10"/>
  <rect class="titlebar" x="1" y="1" width="{WIDTH-2}" height="{TITLE_H}" rx="10"/>
  <rect x="1" y="{TITLE_H - 7}" width="{WIDTH-2}" height="8" fill="#161b22"/>
  <line x1="1" y1="{TITLE_H + 1}" x2="{WIDTH-1}" y2="{TITLE_H + 1}" stroke="#21262d"/>
  <circle cx="20" cy="19" r="5.5" fill="#ff5f56"/>
  <circle cx="38" cy="19" r="5.5" fill="#ffbd2e"/>
  <circle cx="56" cy="19" r="5.5" fill="#27c93f"/>
  <text x="{WIDTH/2 + 12}" y="23" text-anchor="middle" class="path">mrpandeyshubham@github ~ $ neofetch</text>
  {''.join(rows_svg)}
  {bars}
</svg>
'''

out = "info-card-static.svg" if STATIC else "info-card.svg"
with open(out, "w", encoding="utf-8") as f:
    f.write(svg)
print("wrote", out, WIDTH, HEIGHT)
