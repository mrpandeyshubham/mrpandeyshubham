import os

STATIC = os.environ.get("STATIC") == "1"

WIDTH, HEIGHT = 490, 400
PAD_X = 26
TITLE_H = 34
ROW_H = 21
START_Y = TITLE_H + 34

# label, value, color -- pulled from resume + LeetCode/CodeChef/Codolio profiles
ROWS = [
    ("OS",        "Final-Year CSE Student", "#79c0ff"),
    ("Host",      "Parul University", "#79c0ff"),
    ("Shell",     "JavaScript / MERN", "#79c0ff"),
    ("Now",       "Building UniBill (GST ERP)", "#7ee787"),
    ("Prev",      "CuraBot AI (Healthcare Chatbot)", "#7ee787"),
    ("Languages", "Java, Python, JS, C, SQL", "#d2a8ff"),
    ("LeetCode",  "1781 rating - 231 solved", "#ffa657"),
    ("CodeChef",  "1337 rating", "#ffa657"),
    ("Streak",    "22 current - 50 best", "#ff7b72"),
    ("Contests",  "33 total (24 LC + 9 CC)", "#ff7b72"),
    ("Packages",  "12 public repos", "#a5d6ff"),
]

HEIGHT = START_Y + len(ROWS) * ROW_H + 30

rows_svg = []
for i, (label, value, color) in enumerate(ROWS):
    y = START_Y + i * ROW_H
    delay = 0.5 + i * 0.09
    cls = "" if STATIC else f' style="animation-delay:{delay:.2f}s"'
    row_class = "row static" if STATIC else "row"
    rows_svg.append(
        f'<g class="{row_class}"{cls}>'
        f'<text x="{PAD_X}" y="{y}" class="label" fill="{color}">{label}</text>'
        f'<text x="{PAD_X + 108}" y="{y}" class="value">{value}</text>'
        f'</g>'
    )

bars = ""
bar_colors = ["#f14e32","#f2b807","#3ddc84","#3aa6ff","#a371f7","#ff7b9c","#5ee6c9","#f28b30"]
bar_y = HEIGHT - 26
for i, c in enumerate(bar_colors):
    bars += f'<rect x="{PAD_X + i*14}" y="{bar_y}" width="11" height="11" rx="2" fill="{c}"/>'

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">
  <style>
    .bg {{ fill: #0d1117; }}
    .titlebar {{ fill: #161b22; }}
    .dot {{ }}
    .path {{ fill: #8b949e; font: 12px 'Fira Code', monospace; }}
    .label {{ font: 700 13px 'Fira Code', monospace; }}
    .value {{ fill: #c9d1d9; font: 13px 'Fira Code', monospace; }}
    .row {{ opacity: 0; animation: fadeSlide 0.5s ease-out forwards; }}
    .row.static {{ opacity: 1; }}
    @keyframes fadeSlide {{
      0% {{ opacity: 0; transform: translateX(-8px); }}
      100% {{ opacity: 1; transform: translateX(0); }}
    }}
  </style>
  <rect class="bg" x="0" y="0" width="{WIDTH}" height="{HEIGHT}" rx="8"/>
  <rect class="titlebar" x="0" y="0" width="{WIDTH}" height="{TITLE_H}" rx="8"/>
  <rect x="0" y="{TITLE_H-8}" width="{WIDTH}" height="8" fill="#161b22"/>
  <circle cx="20" cy="17" r="6" fill="#ff5f56"/>
  <circle cx="40" cy="17" r="6" fill="#ffbd2e"/>
  <circle cx="60" cy="17" r="6" fill="#27c93f"/>
  <text x="{WIDTH/2}" y="21" text-anchor="middle" class="path">mrpandeyshubham@github ~ %</text>
  {''.join(rows_svg)}
  {bars}
</svg>'''

out = "info-card-static.svg" if STATIC else "info-card.svg"
with open(out, "w") as f:
    f.write(svg)
print("wrote", out, WIDTH, HEIGHT)
