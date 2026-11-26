import datetime
import json

with open("data/contributions.json", encoding="utf-8") as f:
    data = json.load(f)

days = data["days"]
dates = [datetime.date.fromisoformat(d["date"]) for d in days]
min_date = min(dates)
first_sunday = min_date - datetime.timedelta(days=(min_date.weekday() + 1) % 7)

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]

CELL = 11.5
GAP = 3.2
LEFT_PAD = 46
TITLE_H = 38
KPI_H = 44
TOP_PAD = TITLE_H + KPI_H + 22

cells = []
max_week = 0
for d in days:
    dt = datetime.date.fromisoformat(d["date"])
    delta = (dt - first_sunday).days
    week = delta // 7
    dow = (dt.weekday() + 1) % 7
    max_week = max(max_week, week)
    level = d["level"]
    color = PALETTE[min(level, len(PALETTE) - 1)]
    x = LEFT_PAD + week * (CELL + GAP)
    y = TOP_PAD + dow * (CELL + GAP)
    delay = (week * 7 + dow) * 0.0018
    cells.append((x, y, color, delay))

grid_right = LEFT_PAD + (max_week + 1) * (CELL + GAP)
WIDTH = max(866, int(grid_right + 24))
HEIGHT = int(TOP_PAD + 7 * (CELL + GAP) + 46)

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
month_labels = []
seen_months = set()
for d in days:
    dt = datetime.date.fromisoformat(d["date"])
    delta = (dt - first_sunday).days
    week = delta // 7
    key = (dt.year, dt.month)
    if dt.day <= 7 and key not in seen_months:
        seen_months.add(key)
        month_labels.append((LEFT_PAD + week * (CELL + GAP), months[dt.month - 1]))

rects = "\n".join(
    f'<rect class="cell" x="{x:.1f}" y="{y:.1f}" width="{CELL}" height="{CELL}" rx="2.5" ry="2.5" '
    f'fill="{color}" stroke="#1b2028" stroke-width="0.6" style="animation-delay:{delay:.3f}s"/>'
    for x, y, color, delay in cells
)

month_svg = "\n".join(
    f'<text x="{x:.1f}" y="{TOP_PAD - 8}" class="month">{label}</text>'
    for x, label in month_labels
)

dow_labels = [(1, "Mon"), (3, "Wed"), (5, "Fri")]
dow_svg = "\n".join(
    f'<text x="{LEFT_PAD - 8}" y="{TOP_PAD + dow * (CELL + GAP) + 9.5:.1f}" text-anchor="end" class="month">{lbl}</text>'
    for dow, lbl in dow_labels
)

total = data.get("total_contributions", sum(1 for d in days if d["level"] > 0))
cur_streak = data.get("current_streak", 0)
best_streak = data.get("longest_streak", 0)
active_days = data.get("active_days", 0)
updated_at = (data.get("updated_at") or "")[:10] or "live"

kpis = [
    ("Total (1Y)", f"{total}", "#3fb950"),
    ("Current Streak", f"{cur_streak} days", "#58a6ff"),
    ("Longest Streak", f"{best_streak} days", "#a371f7"),
    ("Active Days", f"{active_days}", "#ffa657"),
]
kpi_w = (WIDTH - 48) / len(kpis)
kpi_svg = ""
for i, (lbl, val, col) in enumerate(kpis):
    kx = 24 + i * kpi_w
    kpi_svg += f'''
  <g>
    <rect x="{kx:.1f}" y="{TITLE_H + 10}" width="{kpi_w - 10:.1f}" height="34" rx="7" fill="#161b22" stroke="#21262d"/>
    <circle cx="{kx + 14:.1f}" cy="{TITLE_H + 27}" r="3.5" fill="{col}"/>
    <text x="{kx + 24:.1f}" y="{TITLE_H + 31}" class="kpi-lbl">{lbl}:</text>
    <text x="{kx + kpi_w - 22:.1f}" y="{TITLE_H + 31}" text-anchor="end" class="kpi-val" fill="{col}">{val}</text>
  </g>'''

legend_x = WIDTH - 142
legend_y = HEIGHT - 28
legend_boxes = "".join(
    f'<rect x="{legend_x + 30 + i * 14}" y="{legend_y}" width="10" height="10" rx="2" fill="{PALETTE[i]}" stroke="#21262d" stroke-width="0.6"/>'
    for i in range(len(PALETTE))
)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">
  <style>
    .bg {{ fill: #0d1117; stroke: #30363d; stroke-width: 1; }}
    .titlebar {{ fill: #161b22; }}
    .path {{ fill: #8b949e; font: 12px 'JetBrains Mono', 'Fira Code', ui-monospace, monospace; }}
    .live-pill {{ fill: #3fb950; font: 600 10.5px 'JetBrains Mono', 'Fira Code', ui-monospace, monospace; }}
    .kpi-lbl {{ fill: #8b949e; font: 11.5px 'Segoe UI', Helvetica, Arial, sans-serif; }}
    .kpi-val {{ font: 700 12.5px 'JetBrains Mono', 'Fira Code', ui-monospace, monospace; }}
    .cell {{ opacity: 0; animation: reveal 0.4s ease-out forwards; }}
    @keyframes reveal {{
      0% {{ opacity: 0; }}
      100% {{ opacity: 1; }}
    }}
    .month {{ fill: #8b949e; font: 10.5px 'Segoe UI', Helvetica, Arial, sans-serif; }}
    .footer {{ fill: #8b949e; font: 11.5px 'JetBrains Mono', 'Fira Code', ui-monospace, monospace; }}
    .legend-label {{ fill: #8b949e; font: 10.5px 'Segoe UI', Helvetica, Arial, sans-serif; }}
  </style>
  <rect class="bg" x="0.5" y="0.5" width="{WIDTH-1}" height="{HEIGHT-1}" rx="10"/>
  <rect class="titlebar" x="1" y="1" width="{WIDTH-2}" height="{TITLE_H}" rx="10"/>
  <rect x="1" y="{TITLE_H - 7}" width="{WIDTH-2}" height="8" fill="#161b22"/>
  <line x1="1" y1="{TITLE_H + 1}" x2="{WIDTH-1}" y2="{TITLE_H + 1}" stroke="#21262d"/>
  <circle cx="20" cy="19" r="5.5" fill="#ff5f56"/>
  <circle cx="38" cy="19" r="5.5" fill="#ffbd2e"/>
  <circle cx="56" cy="19" r="5.5" fill="#27c93f"/>
  <text x="{WIDTH/2}" y="23" text-anchor="middle" class="path">mrpandeyshubham@github ~ $ ./contributions.sh --live</text>
  <rect x="{WIDTH - 94}" y="9" width="76" height="20" rx="10" fill="#0e4429" stroke="#238636"/>
  <circle cx="{WIDTH - 80}" cy="19" r="3" fill="#39d353"/>
  <text x="{WIDTH - 72}" y="22.5" class="live-pill">LIVE</text>

  {kpi_svg}
  {month_svg}
  {dow_svg}
  {rects}

  <text x="24" y="{HEIGHT - 19}" class="footer">Synced from GitHub calendar · {updated_at}</text>
  <text x="{legend_x}" y="{HEIGHT - 19}" class="legend-label">Less</text>
  {legend_boxes}
  <text x="{legend_x + 104}" y="{HEIGHT - 19}" class="legend-label">More</text>
</svg>
'''

with open("contrib-heatmap.svg", "w", encoding="utf-8") as f:
    f.write(svg)
print("wrote contrib-heatmap.svg", WIDTH, HEIGHT, "total:", total)
