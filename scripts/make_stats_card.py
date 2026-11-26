import json
from html import escape


def load_json(path: str) -> dict:
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


stats = load_json("data/stats.json")
contrib = load_json("data/contributions.json")

gh = stats.get("github", {})
lc = stats.get("leetcode", {})
cc = stats.get("codechef", {})

repos = gh.get("public_repos", 13)
followers = gh.get("followers", 4)
total_contribs = contrib.get("total_contributions", 280)
lc_solved = lc.get("solved", 296)
lc_rating = lc.get("rating", 1753)
lc_contests = lc.get("contests", 25)
cc_rating = cc.get("rating", 1431)
cc_contests = cc.get("contests", 12)

languages = gh.get("languages") or [
    {"name": "JavaScript", "pct": 38.0},
    {"name": "Python", "pct": 28.0},
    {"name": "TypeScript", "pct": 14.0},
    {"name": "HTML", "pct": 10.0},
    {"name": "CSS", "pct": 6.0},
]
languages = languages[:6]

LANG_COLORS = {
    "JavaScript": "#f1e05a",
    "TypeScript": "#3178c6",
    "HTML": "#e34c26",
    "CSS": "#a371f7",
    "Python": "#3572A5",
    "Java": "#b07219",
    "Jupyter Notebook": "#DA5B0B",
    "C": "#6e7681",
    "C++": "#f34b7d",
    "Shell": "#89e051",
    "Dockerfile": "#384d54",
    "EJS": "#a91e50",
    "SCSS": "#c6538c",
}

WIDTH = 866
TITLE_H = 38
ROW_H = 27
HEIGHT = max(246, TITLE_H + 48 + len(languages) * ROW_H + 24)

# Left column: 4 metric tiles (2x2)
tiles = [
    ("Public Repos", f"{repos}", f"{followers} followers", "#58a6ff"),
    ("Contributions (1Y)", f"{total_contribs}", f"{contrib.get('active_days', 0)} active days", "#3fb950"),
    ("LeetCode", f"{lc_solved} solved", f"{lc_rating} rating · {lc_contests}c", "#ffa657"),
    ("CodeChef", f"{cc_rating}", f"2★ · {cc_contests} contests", "#a371f7"),
]

tiles_svg = ""
tile_w, tile_h = 180, 78
gap = 12
start_x, start_y = 24, TITLE_H + 22
for i, (lbl, val, sub, col) in enumerate(tiles):
    col_i = i % 2
    row_i = i // 2
    tx = start_x + col_i * (tile_w + gap)
    ty = start_y + row_i * (tile_h + gap)
    delay = 0.1 + i * 0.08
    tiles_svg += f'''
  <g class="fade" style="animation-delay:{delay:.2f}s">
    <rect x="{tx}" y="{ty}" width="{tile_w}" height="{tile_h}" rx="8" fill="#161b22" stroke="#21262d"/>
    <rect x="{tx}" y="{ty + 14}" width="3" height="50" rx="1.5" fill="{col}"/>
    <text x="{tx + 14}" y="{ty + 24}" class="tile-lbl">{escape(lbl)}</text>
    <text x="{tx + 14}" y="{ty + 50}" class="tile-val" fill="{col}">{escape(val)}</text>
    <text x="{tx + 14}" y="{ty + 67}" class="tile-sub">{escape(sub)}</text>
  </g>'''

# Right column: Language distribution
div_x = start_x + tile_w * 2 + gap + 24
rx = div_x + 24
bar_x = rx + 132
bar_max = WIDTH - bar_x - 74

lang_svg = f'<text x="{rx}" y="{TITLE_H + 34}" class="section-hdr">Top Languages (Repo-Balanced)</text>'
for i, lang in enumerate(languages):
    y = TITLE_H + 62 + i * ROW_H
    name = lang["name"]
    pct = lang["pct"]
    color = LANG_COLORS.get(name, "#8b949e")
    bar_w = max(4.0, bar_max * pct / 100.0)
    delay = 0.25 + i * 0.07
    lang_svg += f'''
  <g class="fade" style="animation-delay:{delay:.2f}s">
    <circle cx="{rx + 5}" cy="{y - 4}" r="4.5" fill="{color}"/>
    <text x="{rx + 17}" y="{y}" class="lang-name">{escape(name)}</text>
    <rect x="{bar_x}" y="{y - 10}" width="{bar_max}" height="8" rx="4" fill="#161b22" stroke="#21262d" stroke-width="0.6"/>
    <rect class="lang-bar" x="{bar_x}" y="{y - 10}" width="{bar_w:.1f}" height="8" rx="4" fill="{color}" style="animation-delay:{delay:.2f}s"/>
    <text x="{WIDTH - 24}" y="{y}" text-anchor="end" class="lang-pct">{pct:.1f}%</text>
  </g>'''

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">
  <style>
    .bg {{ fill: #0d1117; stroke: #30363d; stroke-width: 1; }}
    .titlebar {{ fill: #161b22; }}
    .path {{ fill: #8b949e; font: 12px 'JetBrains Mono', 'Fira Code', ui-monospace, monospace; }}
    .tile-lbl {{ fill: #8b949e; font: 600 11px 'Segoe UI', Helvetica, Arial, sans-serif; }}
    .tile-val {{ font: 700 21px 'JetBrains Mono', 'Fira Code', ui-monospace, monospace; }}
    .tile-sub {{ fill: #8b949e; font: 11px 'JetBrains Mono', 'Fira Code', ui-monospace, monospace; }}
    .section-hdr {{ fill: #f0f6fc; font: 700 13px 'Segoe UI', Helvetica, Arial, sans-serif; }}
    .lang-name {{ fill: #c9d1d9; font: 12.5px 'Segoe UI', Helvetica, Arial, sans-serif; }}
    .lang-pct {{ fill: #8b949e; font: 12px 'JetBrains Mono', 'Fira Code', ui-monospace, monospace; }}
    .fade {{ opacity: 0; animation: fadeIn 0.45s ease-out forwards; }}
    .lang-bar {{ transform-box: view-box; transform-origin: {bar_x}px 0; transform: scaleX(0); animation: growBar 0.6s ease-out forwards; }}
    @keyframes fadeIn {{ to {{ opacity: 1; }} }}
    @keyframes growBar {{ to {{ transform: scaleX(1); }} }}
  </style>
  <rect class="bg" x="0.5" y="0.5" width="{WIDTH-1}" height="{HEIGHT-1}" rx="10"/>
  <rect class="titlebar" x="1" y="1" width="{WIDTH-2}" height="{TITLE_H}" rx="10"/>
  <rect x="1" y="{TITLE_H - 7}" width="{WIDTH-2}" height="8" fill="#161b22"/>
  <line x1="1" y1="{TITLE_H + 1}" x2="{WIDTH-1}" y2="{TITLE_H + 1}" stroke="#21262d"/>
  <circle cx="20" cy="19" r="5.5" fill="#ff5f56"/>
  <circle cx="38" cy="19" r="5.5" fill="#ffbd2e"/>
  <circle cx="56" cy="19" r="5.5" fill="#27c93f"/>
  <text x="{WIDTH/2}" y="23" text-anchor="middle" class="path">mrpandeyshubham@github ~ $ ./analytics.sh</text>

  {tiles_svg}
  <line x1="{div_x}" y1="{TITLE_H + 18}" x2="{div_x}" y2="{HEIGHT - 20}" stroke="#21262d"/>
  {lang_svg}
</svg>
'''

with open("stats-card.svg", "w", encoding="utf-8") as f:
    f.write(svg)
print("wrote stats-card.svg", WIDTH, HEIGHT)
