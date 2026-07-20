import math

WIDTH, HEIGHT = 1200, 100
amplitude = 10
wavelength = 260
base_y = 20

points = []
for x in range(0, WIDTH + 20, 20):
    y = base_y + amplitude * math.sin((x / wavelength) * 2 * math.pi)
    points.append((x, round(y, 1)))

path_d = f"M0,0 L0,{points[0][1]} "
path_d += " ".join(f"L{x},{y}" for x, y in points)
path_d += f" L{WIDTH},0 Z"

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#9C27B0"/>
      <stop offset="100%" stop-color="#2196F3"/>
    </linearGradient>
  </defs>
  <path fill="url(#bg)" d="{path_d}"/>
</svg>'''

with open("footer-banner.svg", "w") as f:
    f.write(svg)
print("wrote footer-banner.svg")
