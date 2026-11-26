WIDTH = 360
HEIGHT = 360
TITLE_H = 38

LETTERS = {
    "S": [
        "01111",
        "10000",
        "10000",
        "01110",
        "00001",
        "00001",
        "11110",
    ],
    "K": [
        "10001",
        "10010",
        "10100",
        "11000",
        "10100",
        "10010",
        "10001",
    ],
    "P": [
        "11110",
        "10001",
        "10001",
        "11110",
        "10000",
        "10000",
        "10000",
    ],
}

LETTER_COLORS = {
    "S": "#38bdf8",  # cyan
    "K": "#a371f7",  # violet
    "P": "#3fb950",  # emerald
}

CELL = 13
GAP = 3
STEP = CELL + GAP
LETTER_GAP_COLS = 2
TOTAL_COLS = 5 * 3 + LETTER_GAP_COLS * 2  # 19 cols
GRID_W = TOTAL_COLS * CELL + (TOTAL_COLS - 1) * GAP  # 301px
START_X = (WIDTH - GRID_W) / 2
START_Y = TITLE_H + 26

blocks = []
col_offset = 0
for idx, ch in enumerate(("S", "K", "P")):
    bitmap = LETTERS[ch]
    color = LETTER_COLORS[ch]
    for r, row in enumerate(bitmap):
        for c, bit in enumerate(row):
            x = START_X + (col_offset + c) * STEP
            y = START_Y + r * STEP
            if bit == "1":
                delay = (col_offset + c) * 0.035 + r * 0.02
                blocks.append(
                    f'<rect class="blk" x="{x:.1f}" y="{y:.1f}" width="{CELL}" height="{CELL}" '
                    f'rx="3" fill="{color}" style="animation-delay:{delay:.2f}s"/>'
                )
            else:
                blocks.append(
                    f'<rect x="{x:.1f}" y="{y:.1f}" width="{CELL}" height="{CELL}" '
                    f'rx="3" fill="#161b22" opacity="0.55"/>'
                )
    col_offset += 5 + LETTER_GAP_COLS

NAME_Y = START_Y + 7 * STEP + 32

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">
  <style>
    .bg {{ fill: #0d1117; stroke: #30363d; stroke-width: 1; }}
    .titlebar {{ fill: #161b22; }}
    .path {{ fill: #8b949e; font: 12px 'JetBrains Mono', 'Fira Code', ui-monospace, monospace; }}
    .blk {{ opacity: 0; transform-box: fill-box; transform-origin: center; animation: popIn 0.35s ease-out forwards; }}
    @keyframes popIn {{
      0% {{ opacity: 0; transform: scale(0.75); }}
      100% {{ opacity: 1; transform: scale(1); }}
    }}
    .name {{
      fill: #f0f6fc;
      font: 700 19px 'Segoe UI', -apple-system, BlinkMacSystemFont, Helvetica, Arial, sans-serif;
      letter-spacing: -0.2px;
    }}
    .handle {{
      fill: #58a6ff;
      font: 600 13px 'JetBrains Mono', 'Fira Code', ui-monospace, monospace;
    }}
    .cmd {{
      fill: #3fb950;
      font: 700 13px 'JetBrains Mono', 'Fira Code', ui-monospace, monospace;
    }}
    .out {{
      fill: #e6edf3;
      font: 500 13px 'JetBrains Mono', 'Fira Code', ui-monospace, monospace;
    }}
  </style>
  <rect class="bg" x="0.5" y="0.5" width="{WIDTH-1}" height="{HEIGHT-1}" rx="10"/>
  <rect class="titlebar" x="1" y="1" width="{WIDTH-2}" height="{TITLE_H}" rx="10"/>
  <rect x="1" y="{TITLE_H - 7}" width="{WIDTH-2}" height="8" fill="#161b22"/>
  <line x1="1" y1="{TITLE_H + 1}" x2="{WIDTH-1}" y2="{TITLE_H + 1}" stroke="#21262d"/>
  <circle cx="20" cy="19" r="5.5" fill="#ff5f56"/>
  <circle cx="38" cy="19" r="5.5" fill="#ffbd2e"/>
  <circle cx="56" cy="19" r="5.5" fill="#27c93f"/>
  <text x="{WIDTH/2 + 16}" y="23" text-anchor="middle" class="path">skp@github ~ % id</text>

  {''.join(blocks)}

  <text x="{WIDTH/2}" y="{NAME_Y}" text-anchor="middle" class="name">Shubham Kumar Pandey</text>
  <text x="{WIDTH/2}" y="{NAME_Y + 22}" text-anchor="middle" class="handle">@mrpandeyshubham</text>

  <line x1="26" y1="{NAME_Y + 38}" x2="{WIDTH - 26}" y2="{NAME_Y + 38}" stroke="#21262d"/>

  <text x="28" y="{NAME_Y + 62}" class="cmd">$ focus</text>
  <text x="98" y="{NAME_Y + 62}" class="out">MERN · CV · RAG AI</text>
  <text x="28" y="{NAME_Y + 86}" class="cmd">$ status</text>
  <text x="98" y="{NAME_Y + 86}" class="out">Open to SDE Roles</text>
</svg>
'''

with open("skp-monogram.svg", "w", encoding="utf-8") as f:
    f.write(svg)
print("wrote skp-monogram.svg", WIDTH, HEIGHT)
