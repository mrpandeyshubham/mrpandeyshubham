FALLBACK_ASCII = [
    "  _|_|_|  _|    _|  _|_|_|    ",
    "_|        _|  _|    _|    _|  ",
    "  _|_|    _|_|      _|_|_|    ",
    "      _|  _|  _|    _|        ",
    "_|_|_|    _|    _|  _|        ",
]

try:
    import pyfiglet
    raw = pyfiglet.Figlet(font="block", width=200).renderText("SKP")
    lines = [l for l in raw.split("\n") if l.strip()]
    if not lines:
        lines = FALLBACK_ASCII
except Exception:
    lines = FALLBACK_ASCII

WIDTH = 330
HEIGHT = 350
PAD_X = 24
TITLE_H = 36
LINE_H = 22
ASCII_TOP = TITLE_H + 46

rows = []
for i, line in enumerate(lines):
    y = ASCII_TOP + i * LINE_H
    text = line.replace(" ", "&#160;")
    width_px = max(260, len(line) * 9.4 + 8)
    delay = i * 0.12
    rows.append(f'''
  <clipPath id="clip{i}">
    <rect x="0" y="{y - LINE_H + 4}" width="0" height="{LINE_H}">
      <animate attributeName="width" from="0" to="{width_px}" begin="{delay:.2f}s" dur="0.35s" fill="freeze" calcMode="linear"/>
    </rect>
  </clipPath>
  <g clip-path="url(#clip{i})">
    <text x="{PAD_X}" y="{y}" class="ascii">{text}</text>
    <rect class="cursor" x="{PAD_X}" y="{y - LINE_H + 6}" width="7" height="{LINE_H - 6}">
      <animate attributeName="x" from="{PAD_X}" to="{PAD_X + width_px}" begin="{delay:.2f}s" dur="0.35s" fill="freeze" calcMode="linear"/>
      <animate attributeName="opacity" from="1" to="0" begin="{delay + 0.35:.2f}s" dur="0.01s" fill="freeze"/>
    </rect>
  </g>''')

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">
  <defs>
    <linearGradient id="asciiGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#58a6ff"/>
      <stop offset="55%" stop-color="#a371f7"/>
      <stop offset="100%" stop-color="#3fb950"/>
    </linearGradient>
  </defs>
  <style>
    .bg {{ fill: #0d1117; stroke: #30363d; stroke-width: 1; }}
    .titlebar {{ fill: #161b22; }}
    .path {{ fill: #8b949e; font: 12px 'JetBrains Mono', 'Fira Code', ui-monospace, monospace; }}
    .ascii {{ fill: url(#asciiGrad); font: 700 15px 'JetBrains Mono', 'Fira Code', 'Courier New', monospace; white-space: pre; }}
    .cursor {{ fill: #58a6ff; }}
    .term-k {{ fill: #7ee787; font: 600 12px 'JetBrains Mono', 'Fira Code', ui-monospace, monospace; }}
    .term-v {{ fill: #c9d1d9; font: 12px 'JetBrains Mono', 'Fira Code', ui-monospace, monospace; }}
    .term-m {{ fill: #8b949e; font: 11.5px 'JetBrains Mono', 'Fira Code', ui-monospace, monospace; }}
    .fade {{ opacity: 0; animation: fadeIn 0.5s ease-out 0.8s forwards; }}
    @keyframes fadeIn {{ to {{ opacity: 1; }} }}
  </style>
  <rect class="bg" x="0.5" y="0.5" width="{WIDTH-1}" height="{HEIGHT-1}" rx="10"/>
  <rect class="titlebar" x="1" y="1" width="{WIDTH-2}" height="{TITLE_H}" rx="10"/>
  <rect x="1" y="{TITLE_H - 7}" width="{WIDTH-2}" height="8" fill="#161b22"/>
  <line x1="1" y1="{TITLE_H + 1}" x2="{WIDTH-1}" y2="{TITLE_H + 1}" stroke="#21262d"/>
  <circle cx="20" cy="19" r="5.5" fill="#ff5f56"/>
  <circle cx="38" cy="19" r="5.5" fill="#ffbd2e"/>
  <circle cx="56" cy="19" r="5.5" fill="#27c93f"/>
  <text x="{WIDTH/2 + 16}" y="23" text-anchor="middle" class="path">skp@github ~ % banner</text>

  {''.join(rows)}

  <line x1="{PAD_X}" y1="212" x2="{WIDTH - PAD_X}" y2="212" stroke="#21262d"/>
  <g class="fade">
    <text x="{PAD_X}" y="240" class="term-k">$ whoami</text>
    <text x="{PAD_X}" y="260" class="term-v">Shubham Kumar Pandey (SKP)</text>
    <text x="{PAD_X}" y="286" class="term-k">$ focus --current</text>
    <text x="{PAD_X}" y="306" class="term-v">MERN · Computer Vision · RAG AI</text>
    <text x="{PAD_X}" y="330" class="term-m">India  ·  Open to SDE Opportunities</text>
  </g>
</svg>
'''

with open("skp-ascii.svg", "w", encoding="utf-8") as f:
    f.write(svg)
print("wrote skp-ascii.svg", WIDTH, HEIGHT)
