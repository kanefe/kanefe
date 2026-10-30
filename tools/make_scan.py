"""Generates assets/profile-scan.svg: an animated terminal-style profile panel.

Run: python3 tools/make_scan.py  (from the github-profile folder)
"""
import math
import random
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets" / "profile-scan.svg"

W, H = 900, 430
FONT = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"

# Pixel spaceship (VoidRun nod). # hull, o cockpit, * engine flame.
SHIP = [
    "......#......",
    ".....###.....",
    ".....###.....",
    "....##o##....",
    "....#ooo#....",
    "....##o##....",
    "...#######...",
    "..#########..",
    ".###.###.###.",
    "####.###.####",
    "###..###..###",
    "##...#.#...##",
    ".....#.#.....",
    "....*...*....",
    "...**...**...",
    "....*...*....",
]

INFO = [
    ("Subject", "Efe Kan"),
    ("Handle", "@kanefe"),
    ("Role", "Student · Game Dev · Developer"),
    ("Status", "Building | Learning | Shipping"),
    ("Engine", "Unity 6 · C#"),
    ("Also", "TypeScript · React Native · Python"),
    ("Projects", "VoidRun · Dream Dealer · Rota"),
    ("Art", "Pixel art with PixelLab"),
    ("Now", "Polishing VoidRun for iOS"),
    ("Contact", "github.com/kanefe"),
]


def dot_map():
    """Left panel: circular dot field with the ship in the middle."""
    rnd = random.Random(7)
    n, step = 29, 10.5
    cx, cy = 40 + 165, 70 + 165  # panel centre
    r = n // 2
    ship_h, ship_w = len(SHIP), len(SHIP[0])
    oy, ox = r - ship_h // 2, r - ship_w // 2
    out = []
    for gy in range(n):
        for gx in range(n):
            if math.hypot(gx - r, gy - r) > r + 0.3:
                continue
            x = cx + (gx - r) * step
            y = cy + (gy - r) * step
            sy, sx = gy - oy, gx - ox
            ch = SHIP[sy][sx] if 0 <= sy < ship_h and 0 <= sx < ship_w else "."
            if ch == "#":
                out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.6" fill="#5ee4ff"/>')
            elif ch == "o":
                out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.8" fill="#ffffff"/>')
            elif ch == "*":
                d = f"{0.35 + rnd.random() * 0.3:.2f}s"
                out.append(
                    f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.6" fill="#ff8a3d">'
                    f'<animate attributeName="opacity" values="1;0.35;1" dur="{d}" repeatCount="indefinite"/>'
                    f"</circle>"
                )
            else:
                o = 0.12 + rnd.random() * 0.33
                if rnd.random() < 0.05:  # twinkling stars
                    d = f"{1.5 + rnd.random() * 2:.1f}s"
                    out.append(
                        f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.6" fill="#3fa7d6" opacity="{o:.2f}">'
                        f'<animate attributeName="opacity" values="{o:.2f};0.95;{o:.2f}" dur="{d}" repeatCount="indefinite"/>'
                        f"</circle>"
                    )
                else:
                    out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.6" fill="#3fa7d6" opacity="{o:.2f}"/>')
    return "\n    ".join(out), cx, cy, r * step + 6


def info_rows():
    out = []
    x0, x1, y0, dy = 470, 580, 128, 26
    for i, (label, value) in enumerate(INFO):
        y = y0 + i * dy
        begin = f"{0.6 + i * 0.28:.2f}s"
        out.append(
            f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{begin}" dur="0.35s" fill="freeze"/>'
            f'<text x="{x0}" y="{y}" class="k">{label}</text>'
            f'<text x="{x1}" y="{y}" class="v">{value}</text></g>'
        )
    return "\n    ".join(out), y0 + len(INFO) * dy


def build():
    dots, cx, cy, rad = dot_map()
    rows, end_y = info_rows()
    cursor_begin = f"{0.6 + len(INFO) * 0.28:.2f}s"
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Efe Kan - profile scan">
  <style>
    .t {{ font-family: {FONT}; }}
    .k {{ font-family: {FONT}; font-size: 14px; fill: #5be3a8; }}
    .v {{ font-family: {FONT}; font-size: 14px; fill: #e6f1ff; }}
  </style>
  <defs>
    <clipPath id="disc"><circle cx="{cx}" cy="{cy}" r="{rad:.1f}"/></clipPath>
    <linearGradient id="scan" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#5ee4ff" stop-opacity="0"/>
      <stop offset="1" stop-color="#5ee4ff" stop-opacity="0.35"/>
    </linearGradient>
  </defs>

  <rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16" fill="#0b1a1f" stroke="#2de0b0" stroke-opacity="0.55" stroke-width="2"/>
  <circle cx="26" cy="24" r="6" fill="#ff5f57"/>
  <circle cx="46" cy="24" r="6" fill="#febc2e"/>
  <circle cx="66" cy="24" r="6" fill="#28c840"/>
  <text x="{W / 2}" y="29" text-anchor="middle" class="t" font-size="13" fill="#8fb3bf">efe@github ~ $ ./profile-scan --live</text>

  <!-- left: visual map -->
  <rect x="24" y="48" width="410" height="{H - 70}" rx="10" fill="#0e2329" stroke="#2de0b0" stroke-opacity="0.35"/>
  <text x="40" y="70" class="t" font-size="11" font-weight="700" fill="#8fb3bf" letter-spacing="1">VISUAL.MAP</text>
  <g transform="translate(24 10)">
    {dots}
    <g clip-path="url(#disc)">
      <rect x="{cx - rad:.1f}" y="{cy - rad:.1f}" width="{2 * rad:.1f}" height="36" fill="url(#scan)">
        <animate attributeName="y" from="{cy - rad - 36:.1f}" to="{cy + rad:.1f}" dur="3.2s" repeatCount="indefinite"/>
      </rect>
    </g>
  </g>

  <!-- right: system info -->
  <rect x="450" y="48" width="{W - 474}" height="{H - 70}" rx="10" fill="#0e2329" stroke="#2de0b0" stroke-opacity="0.35"/>
  <text x="466" y="70" class="t" font-size="11" font-weight="700" fill="#8fb3bf" letter-spacing="1">SYSTEM.INFO</text>
  <g>
    <circle cx="{W - 76}" cy="66" r="4" fill="#28c840"><animate attributeName="opacity" values="1;0.2;1" dur="1.4s" repeatCount="indefinite"/></circle>
    <text x="{W - 66}" y="70" class="t" font-size="11" font-weight="700" fill="#28c840">LIVE</text>
  </g>
  <line x1="466" y1="84" x2="{W - 40}" y2="84" stroke="#2de0b0" stroke-opacity="0.25"/>
  <text x="466" y="104" class="t" font-size="12" fill="#8fb3bf">&gt; scanning profile...<animate attributeName="opacity" values="1;0.4;1" dur="0.8s" repeatCount="2"/></text>
  <g>
    {rows}
  </g>
  <rect x="470" y="{end_y - 6}" width="9" height="16" fill="#5be3a8" opacity="0">
    <animate attributeName="opacity" values="0;1;0" dur="1s" begin="{cursor_begin}" repeatCount="indefinite"/>
  </rect>
</svg>
"""


if __name__ == "__main__":
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(build(), encoding="utf-8")
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")
