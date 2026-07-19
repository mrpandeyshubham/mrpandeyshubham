import pyfiglet

art = pyfiglet.Figlet(font="block", width=200).renderText("SKP")
lines = [l for l in art.split("\n") if l.strip("\n")]
# trim trailing all-blank lines but keep interior blank rows
while lines and lines[-1].strip() == "":
    lines.pop()

CHAR_W = 9.6
LINE_H = 20
PAD = 20
max_len = max(len(l) for l in lines)
WIDTH = int(PAD * 2 + max_len * CHAR_W)
HEIGHT = int(PAD * 2 + len(lines) * LINE_H + 26)

rows = []
for i, line in enumerate(lines):
    y = PAD + 20 + i * LINE_H
    text = line.replace(" ", "&#160;")
    width_px = len(line) * CHAR_W + 4
    delay = i * 0.12
    rows.append(f'''
  <clipPath id="clip{i}">
    <rect x="0" y="{y - LINE_H + 4}" width="0" height="{LINE_H}">
      <animate attributeName="width" from="0" to="{width_px}" begin="{delay:.2f}s" dur="0.35s" fill="freeze" calcMode="linear"/>
    </rect>
  </clipPath>
  <g clip-path="url(#clip{i})">
    <text x="{PAD}" y="{y}" class="ascii">{text}</text>
    <rect class="cursor" x="{PAD}" y="{y - LINE_H + 6}" width="7" height="{LINE_H - 6}">
      <animate attributeName="x" from="{PAD}" to="{PAD + width_px}" begin="{delay:.2f}s" dur="0.35s" fill="freeze" calcMode="linear"/>
      <animate attributeName="opacity" from="1" to="0" begin="{delay + 0.35:.2f}s" dur="0.01s" fill="freeze"/>
    </rect>
  </g>''')

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">
  <style>
    .bg {{ fill: #0d1117; }}
    .ascii {{ fill: #c9d1d9; font: 15px 'Fira Code', 'Courier New', monospace; white-space: pre; }}
    .cursor {{ fill: #58a6ff; }}
    .caption {{ fill: #8b949e; font: 12px 'Fira Code', monospace; }}
  </style>
  <rect class="bg" x="0" y="0" width="{WIDTH}" height="{HEIGHT}" rx="8"/>
  {''.join(rows)}
  <text x="{PAD}" y="{HEIGHT - 12}" class="caption">Shubham Kumar Pandey</text>
</svg>'''

with open("skp-ascii.svg", "w") as f:
    f.write(svg)
print("wrote skp-ascii.svg", WIDTH, HEIGHT, "lines:", len(lines))
