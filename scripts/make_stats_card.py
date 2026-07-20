import json

try:
    with open("data/stats.json") as f:
        stats = json.load(f)
except FileNotFoundError:
    stats = {}

gh = stats.get("github", {})
repos = gh.get("public_repos", 12)
followers = gh.get("followers", 4)
stars = gh.get("total_stars", 4)
languages = gh.get("languages") or [
    {"name": "JavaScript", "pct": 38.0},
    {"name": "HTML", "pct": 24.0},
    {"name": "Jupyter Notebook", "pct": 18.0},
    {"name": "CSS", "pct": 12.0},
    {"name": "Python", "pct": 8.0},
]

LANG_COLORS = {
    "JavaScript": "#f1e05a", "TypeScript": "#3178c6", "HTML": "#e34c26",
    "CSS": "#563d7c", "Python": "#3572A5", "Java": "#b07219",
    "Jupyter Notebook": "#DA5B0B", "C": "#555555", "C++": "#f34b7d",
    "Shell": "#89e051", "Dockerfile": "#384d54", "EJS": "#a91e50",
}

WIDTH = 490
PAD_X = 26
TOP_STATS_Y = 78
LANG_START_Y = 128
ROW_H = 26
HEIGHT = LANG_START_Y + len(languages) * ROW_H + 30

BAR_MAX = WIDTH - PAD_X * 2 - 150

stat_blocks = [
    ("Public Repos", repos, "#79c0ff"),
    ("Followers", followers, "#7ee787"),
    ("Total Stars", stars, "#ffa657"),
]
block_w = (WIDTH - PAD_X * 2) / len(stat_blocks)
stats_svg = ""
for i, (label, value, color) in enumerate(stat_blocks):
    cx = PAD_X + block_w * i + block_w / 2
    stats_svg += f'''
  <g class="stat-block" style="animation-delay:{0.1 + i*0.1:.2f}s">
    <text x="{cx}" y="{TOP_STATS_Y}" text-anchor="middle" class="stat-value" fill="{color}">{value}</text>
    <text x="{cx}" y="{TOP_STATS_Y + 18}" text-anchor="middle" class="stat-label">{label}</text>
  </g>'''

lang_svg = ""
for i, lang in enumerate(languages):
    y = LANG_START_Y + i * ROW_H
    color = LANG_COLORS.get(lang["name"], "#8b949e")
    bar_w = BAR_MAX * lang["pct"] / 100
    delay = 0.4 + i * 0.08
    lang_svg += f'''
  <g class="lang-row" style="animation-delay:{delay:.2f}s">
    <circle cx="{PAD_X + 4}" cy="{y - 4}" r="5" fill="{color}"/>
    <text x="{PAD_X + 16}" y="{y}" class="lang-name">{lang["name"]}</text>
    <rect x="{PAD_X + 140}" y="{y - 11}" width="{BAR_MAX}" height="8" rx="4" fill="#21262d"/>
    <rect class="lang-bar" x="{PAD_X + 140}" y="{y - 11}" width="{bar_w:.1f}" height="8" rx="4" fill="{color}" style="animation-delay:{delay:.2f}s"/>
    <text x="{WIDTH - PAD_X}" y="{y}" text-anchor="end" class="lang-pct">{lang["pct"]}%</text>
  </g>'''

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">
  <style>
    .bg {{ fill: #0d1117; stroke: #30363d; stroke-width: 1; }}
    .titlebar {{ fill: #161b22; }}
    .path {{ fill: #8b949e; font: 12px 'Fira Code', monospace; }}
    .stat-value {{ font: 700 26px 'Fira Code', monospace; }}
    .stat-label {{ fill: #8b949e; font: 11px 'Segoe UI', sans-serif; }}
    .lang-name {{ fill: #c9d1d9; font: 13px 'Segoe UI', sans-serif; }}
    .lang-pct {{ fill: #8b949e; font: 12px 'Fira Code', monospace; }}
    .stat-block, .lang-row {{ opacity: 0; animation: fadeIn 0.5s ease-out forwards; }}
    .lang-bar {{ transform-origin: left; transform: scaleX(0); animation: growBar 0.6s ease-out forwards; }}
    @keyframes fadeIn {{ to {{ opacity: 1; }} }}
    @keyframes growBar {{ to {{ transform: scaleX(1); }} }}
  </style>
  <rect class="bg" x="0.5" y="0.5" width="{WIDTH-1}" height="{HEIGHT-1}" rx="8"/>
  <rect class="titlebar" x="0" y="0" width="{WIDTH}" height="34" rx="8"/>
  <rect x="0" y="26" width="{WIDTH}" height="8" fill="#161b22"/>
  <circle cx="20" cy="17" r="6" fill="#ff5f56"/>
  <circle cx="40" cy="17" r="6" fill="#ffbd2e"/>
  <circle cx="60" cy="17" r="6" fill="#27c93f"/>
  <text x="{WIDTH/2}" y="21" text-anchor="middle" class="path">mrpandeyshubham@github ~ $ ./analytics.sh</text>
  {stats_svg}
  <line x1="{PAD_X}" y1="{TOP_STATS_Y + 30}" x2="{WIDTH - PAD_X}" y2="{TOP_STATS_Y + 30}" stroke="#21262d"/>
  {lang_svg}
</svg>'''

with open("stats-card.svg", "w") as f:
    f.write(svg)
print("wrote stats-card.svg", WIDTH, HEIGHT)
