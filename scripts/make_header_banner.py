import math

WIDTH, HEIGHT = 1200, 260
TITLE = "Shubham Kumar Pandey"
SUBTITLE = "Full-Stack Engineer (MERN / TypeScript)  ·  Computer Vision &amp; Applied AI  ·  Cloud &amp; DevOps"
META = "B.Tech CSE '27 (Parul University)   •   TrueEyeball · UniBill · BachatPay AI   •   IBM SkillsBuild AI Intern"

# Smooth layered sine waves for the bottom edge
def build_wave(amp: float, wl: float, phase: float, base_y: float) -> str:
    pts = []
    for x in range(0, WIDTH + 20, 20):
        y = base_y + amp * math.sin((x / wl) * 2 * math.pi + phase)
        pts.append((x, round(y, 1)))
    d = f"M0,{HEIGHT} L0,{pts[0][1]} "
    d += " ".join(f"L{x},{y}" for x, y in pts)
    d += f" L{WIDTH},{HEIGHT} Z"
    return d

wave1 = build_wave(12, 360, 0.0, HEIGHT - 28)
wave2 = build_wave(9, 280, 1.8, HEIGHT - 18)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0b101b"/>
      <stop offset="50%" stop-color="#0d1117"/>
      <stop offset="100%" stop-color="#111827"/>
    </linearGradient>
    <radialGradient id="orbCyan" cx="18%" cy="22%" r="48%">
      <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.24"/>
      <stop offset="100%" stop-color="#38bdf8" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="orbViolet" cx="84%" cy="24%" r="46%">
      <stop offset="0%" stop-color="#a855f7" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="#a855f7" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="orbEmerald" cx="52%" cy="88%" r="42%">
      <stop offset="0%" stop-color="#10b981" stop-opacity="0.16"/>
      <stop offset="100%" stop-color="#10b981" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="accentLine" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#38bdf8"/>
      <stop offset="50%" stop-color="#818cf8"/>
      <stop offset="100%" stop-color="#34d399"/>
    </linearGradient>
    <linearGradient id="waveGrad1" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.14"/>
      <stop offset="50%" stop-color="#818cf8" stop-opacity="0.14"/>
      <stop offset="100%" stop-color="#a855f7" stop-opacity="0.14"/>
    </linearGradient>
    <linearGradient id="waveGrad2" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#34d399" stop-opacity="0.10"/>
      <stop offset="100%" stop-color="#38bdf8" stop-opacity="0.12"/>
    </linearGradient>
    <pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="1" fill="#30363d" opacity="0.65"/>
    </pattern>
  </defs>

  <style>
    .title {{
      fill: #f0f6fc;
      font: 700 44px 'Segoe UI', -apple-system, BlinkMacSystemFont, Helvetica, Arial, sans-serif;
      letter-spacing: -0.5px;
      opacity: 0;
      animation: fadeUp 0.7s ease-out 0.15s forwards;
    }}
    .subtitle {{
      fill: #c9d1d9;
      font: 500 17px 'Segoe UI', -apple-system, BlinkMacSystemFont, Helvetica, Arial, sans-serif;
      opacity: 0;
      animation: fadeUp 0.7s ease-out 0.35s forwards;
    }}
    .meta {{
      fill: #8b949e;
      font: 500 13px 'JetBrains Mono', 'Fira Code', ui-monospace, Menlo, Consolas, monospace;
      opacity: 0;
      animation: fadeUp 0.7s ease-out 0.55s forwards;
    }}
    .pill-text {{
      fill: #c9d1d9;
      font: 600 11.5px 'JetBrains Mono', 'Fira Code', ui-monospace, Menlo, Consolas, monospace;
      letter-spacing: 0.6px;
    }}
    .pulse {{
      animation: pulseDot 2.2s ease-in-out infinite;
    }}
    @keyframes fadeUp {{
      0% {{ opacity: 0; transform: translateY(8px); }}
      100% {{ opacity: 1; transform: translateY(0); }}
    }}
    @keyframes pulseDot {{
      0%, 100% {{ opacity: 1; }}
      50% {{ opacity: 0.35; }}
    }}
  </style>

  <rect x="0.5" y="0.5" width="{WIDTH-1}" height="{HEIGHT-1}" rx="14" fill="url(#bgGrad)" stroke="#30363d"/>
  <rect x="1" y="1" width="{WIDTH-2}" height="{HEIGHT-2}" rx="14" fill="url(#dots)"/>
  <rect x="1" y="1" width="{WIDTH-2}" height="{HEIGHT-2}" rx="14" fill="url(#orbCyan)"/>
  <rect x="1" y="1" width="{WIDTH-2}" height="{HEIGHT-2}" rx="14" fill="url(#orbViolet)"/>
  <rect x="1" y="1" width="{WIDTH-2}" height="{HEIGHT-2}" rx="14" fill="url(#orbEmerald)"/>

  <rect x="120" y="1" width="960" height="2.5" rx="1.25" fill="url(#accentLine)" opacity="0.85"/>

  <g transform="translate(465, 34)">
    <rect x="0" y="0" width="270" height="28" rx="14" fill="#161b22" fill-opacity="0.9" stroke="#30363d"/>
    <circle class="pulse" cx="18" cy="14" r="4.5" fill="#3fb950"/>
    <text x="31" y="18" class="pill-text">OPEN TO SDE &amp; AI/ML ROLES</text>
  </g>

  <text x="50%" y="114" text-anchor="middle" class="title">{TITLE}</text>
  <text x="50%" y="150" text-anchor="middle" class="subtitle">{SUBTITLE}</text>
  <text x="50%" y="188" text-anchor="middle" class="meta">{META}</text>

  <path fill="url(#waveGrad1)" d="{wave1}"/>
  <path fill="url(#waveGrad2)" d="{wave2}"/>
</svg>
'''

with open("header-banner.svg", "w", encoding="utf-8") as f:
    f.write(svg)
print("wrote header-banner.svg")
