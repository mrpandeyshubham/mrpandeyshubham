import math

WIDTH, HEIGHT = 1200, 110

pts = []
for x in range(0, WIDTH + 20, 20):
    y = 26 + 11 * math.sin((x / 300) * 2 * math.pi)
    pts.append((x, round(y, 1)))

wave_d = f"M0,{HEIGHT} L0,{pts[0][1]} "
wave_d += " ".join(f"L{x},{y}" for x, y in pts)
wave_d += f" L{WIDTH},{HEIGHT} Z"

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#0d1117"/>
      <stop offset="50%" stop-color="#111827"/>
      <stop offset="100%" stop-color="#0d1117"/>
    </linearGradient>
    <linearGradient id="wave" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.18"/>
      <stop offset="50%" stop-color="#818cf8" stop-opacity="0.20"/>
      <stop offset="100%" stop-color="#34d399" stop-opacity="0.18"/>
    </linearGradient>
    <linearGradient id="topLine" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#38bdf8" stop-opacity="0"/>
      <stop offset="50%" stop-color="#818cf8" stop-opacity="0.75"/>
      <stop offset="100%" stop-color="#34d399" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <rect x="0.5" y="0.5" width="{WIDTH-1}" height="{HEIGHT-1}" rx="12" fill="url(#bg)" stroke="#30363d"/>
  <path fill="url(#wave)" d="{wave_d}"/>
  <rect x="180" y="1" width="840" height="1.5" fill="url(#topLine)"/>
  <text x="50%" y="56" text-anchor="middle" fill="#c9d1d9" font-family="'Segoe UI', Helvetica, Arial, sans-serif" font-size="14" font-weight="600">Built with consistency, curiosity &amp; clean engineering  ·  Shubham Kumar Pandey</text>
  <text x="50%" y="78" text-anchor="middle" fill="#8b949e" font-family="'JetBrains Mono', 'Fira Code', ui-monospace, monospace" font-size="11.5">github.com/mrpandeyshubham   •   let's build something impactful</text>
</svg>
'''

with open("footer-banner.svg", "w", encoding="utf-8") as f:
    f.write(svg)
print("wrote footer-banner.svg")
