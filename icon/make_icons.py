#!/usr/bin/env python3
"""Generate the Zehnerfreund home-screen / PWA icons.

Recreates the glossy white "7+9" app icon as an SVG and rasterises it to the
PNG sizes that iOS ("Add to Home Screen") and PWA installs expect. The artwork
is full-bleed (white background to the edges) so iOS can mask the corners
cleanly without clipping into the numbers.
"""
import os
import cairosvg

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)  # repo root

# Full-bleed icon. iOS masks the corners itself, so the white background runs
# edge to edge. A gentle vertical gradient + a glossy top sheen recreate the
# look of the reference logo; "7" and "9" are red, the "+" is near-black.
SVG = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="0 0 1024 1024">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0"   stop-color="#ffffff"/>
      <stop offset="0.55" stop-color="#fbfbfa"/>
      <stop offset="1"   stop-color="#eceae5"/>
    </linearGradient>
    <linearGradient id="redgloss" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0"    stop-color="#ff5a63"/>
      <stop offset="0.48" stop-color="#ec1722"/>
      <stop offset="1"    stop-color="#cf0009"/>
    </linearGradient>
    <linearGradient id="darkgloss" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0"    stop-color="#4a4a4a"/>
      <stop offset="0.5"  stop-color="#262626"/>
      <stop offset="1"    stop-color="#111111"/>
    </linearGradient>
    <linearGradient id="sheen" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0"   stop-color="#ffffff" stop-opacity="0.55"/>
      <stop offset="1"   stop-color="#ffffff" stop-opacity="0"/>
    </linearGradient>
  </defs>

  <!-- background -->
  <rect x="0" y="0" width="1024" height="1024" fill="url(#bg)"/>

  <!-- numbers: 7 + 9 -->
  <g font-family="Liberation Sans, Helvetica, Arial, sans-serif" font-weight="bold"
     text-anchor="middle" dominant-baseline="alphabetic">
    <text x="280" y="700" font-size="520" fill="url(#redgloss)">6</text>
    <text x="512" y="678" font-size="360" fill="url(#darkgloss)">+</text>
    <text x="752" y="700" font-size="520" fill="url(#redgloss)">7</text>
  </g>

  <!-- glossy sheen across the top, with a gentle curved lower edge -->
  <path d="M0 0 H1024 V470 Q512 560 0 470 Z" fill="url(#sheen)"/>
</svg>
'''

svg_path = os.path.join(HERE, "icon.svg")
with open(svg_path, "w") as f:
    f.write(SVG)

# Apple touch icon (primary) + extra iOS sizes + PWA manifest + favicons.
sizes = {
    "apple-touch-icon.png": 180,
    "icon-192.png": 192,
    "icon-512.png": 512,
    "favicon-32.png": 32,
}
for name, px in sizes.items():
    cairosvg.svg2png(bytestring=SVG.encode(), write_to=os.path.join(OUT, name),
                     output_width=px, output_height=px)
    print("wrote", name, px)

print("done")
