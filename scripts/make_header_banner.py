import math

WIDTH, HEIGHT = 1200, 200
TITLE = "Shubham Kumar Pandey"
SUBTITLE = "Final-Year CSE Student | Full-Stack Developer | AI &amp; Cloud Enthusiast"

# Build a smooth wave path across the bottom of the band (same idea as
# capsule-render's "waving" type, but generated locally so it never 404s).
points = []
amplitude = 14
wavelength = 300
base_y = HEIGHT - 24
for x in range(0, WIDTH + 20, 20):
    y = base_y + amplitude * math.sin((x / wavelength) * 2 * math.pi)
    points.append((x, round(y, 1)))

path_d = f"M0,{HEIGHT} L0,{points[0][1]} "
path_d += " ".join(f"L{x},{y}" for x, y in points)
path_d += f" L{WIDTH},{HEIGHT} Z"

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#2196F3"/>
      <stop offset="100%" stop-color="#9C27B0"/>
    </linearGradient>
    <linearGradient id="wave" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.12"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0.05"/>
    </linearGradient>
  </defs>
  <style>
    .band {{ fill: url(#bg); }}
    .wave {{ fill: url(#wave); }}
    .title {{
      fill: #ffffff; font: 700 46px 'Segoe UI', Helvetica, Arial, sans-serif;
      opacity: 0; animation: fadeIn 1s ease-out 0.2s forwards;
    }}
    .subtitle {{
      fill: #eef3ff; font: 400 18px 'Segoe UI', Helvetica, Arial, sans-serif;
      opacity: 0; animation: fadeIn 1s ease-out 0.6s forwards;
    }}
    @keyframes fadeIn {{
      0% {{ opacity: 0; transform: translateY(8px); }}
      100% {{ opacity: 1; transform: translateY(0); }}
    }}
  </style>
  <rect class="band" x="0" y="0" width="{WIDTH}" height="{HEIGHT}"/>
  <path class="wave" d="{path_d}"/>
  <text x="50%" y="42%" text-anchor="middle" class="title">{TITLE}</text>
  <text x="50%" y="58%" text-anchor="middle" class="subtitle">{SUBTITLE}</text>
</svg>'''

with open("header-banner.svg", "w") as f:
    f.write(svg)
print("wrote header-banner.svg")
