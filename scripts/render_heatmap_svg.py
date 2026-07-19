import json, datetime

with open("data/contributions.json") as f:
    data = json.load(f)

days = data["days"]
dates = [datetime.date.fromisoformat(d["date"]) for d in days]
min_date = min(dates)
# back up to the preceding Sunday so weeks align like GitHub's grid
first_sunday = min_date - datetime.timedelta(days=(min_date.weekday() + 1) % 7)

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]

CELL = 11
GAP = 3
LEFT_PAD = 28
TOP_PAD = 30

cells = []
max_week = 0
for d in days:
    dt = datetime.date.fromisoformat(d["date"])
    delta = (dt - first_sunday).days
    week = delta // 7
    dow = dt.weekday()
    dow = (dow + 1) % 7  # convert Mon=0 -> Sun=0
    max_week = max(max_week, week)
    level = d["level"]
    color = PALETTE[min(level, len(PALETTE) - 1)]
    x = LEFT_PAD + week * (CELL + GAP)
    y = TOP_PAD + dow * (CELL + GAP)
    delay = (week * 7 + dow) * 0.0022
    cells.append((x, y, color, delay))

width = LEFT_PAD + (max_week + 1) * (CELL + GAP) + 20
height = TOP_PAD + 7 * (CELL + GAP) + 55

months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
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
    f'<rect class="cell" x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2.5" ry="2.5" '
    f'fill="{color}" style="animation-delay:{delay:.3f}s" />'
    for x, y, color, delay in cells
)

month_svg = "\n".join(
    f'<text x="{x}" y="{TOP_PAD - 10}" class="month">{label}</text>'
    for x, label in month_labels
)

total = data.get("total_contributions", sum(1 for d in days if d["level"] > 0))

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" font-family="'Segoe UI', Helvetica, Arial, sans-serif">
  <style>
    .bg {{ fill: #0d1117; }}
    .cell {{ opacity: 0; transform-origin: center; animation: reveal 0.5s ease-out forwards; }}
    @keyframes reveal {{
      0% {{ opacity: 0; transform: translate(-6px,-6px) scale(0.4); }}
      100% {{ opacity: 1; transform: translate(0,0) scale(1); }}
    }}
    .month {{ fill: #8b949e; font-size: 11px; }}
    .footer {{ fill: #8b949e; font-size: 12px; }}
    .legend-label {{ fill: #8b949e; font-size: 10px; }}
    .title {{ fill: #58a6ff; font-size: 12px; font-family: 'Fira Code', monospace; }}
  </style>
  <rect class="bg" x="0" y="0" width="{width}" height="{height}" rx="8"/>
  <text x="{LEFT_PAD}" y="16" class="title">mrpandeyshubham@github ~ $ ./contributions.sh</text>
  {month_svg}
  {rects}
  <text x="{LEFT_PAD}" y="{height - 26}" class="footer">{total} contributions in the last year</text>
  <text x="{width - 150}" y="{height - 26}" class="legend-label">Less</text>
  {"".join(f'<rect x="{width - 128 + i*14}" y="{height - 36}" width="10" height="10" rx="2" fill="{PALETTE[i]}"/>' for i in range(len(PALETTE)))}
  <text x="{width - 20}" y="{height - 26}" class="legend-label">More</text>
</svg>'''

with open("contrib-heatmap.svg", "w") as f:
    f.write(svg)

print("wrote contrib-heatmap.svg", width, height, "total:", total)
