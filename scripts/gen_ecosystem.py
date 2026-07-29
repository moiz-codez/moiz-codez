#!/usr/bin/env python3
"""Generate the ecosystem network map SVG."""
import os
import sys
import math

HERE = os.path.dirname(os.path.abspath(__file__))

FG = "#6e7681"
FG_DARK = "#c9d1d9"
FG_EMP = "#424a53"
FG_EMP_DARK = "#f0f6fc"
FG_DIM = "#8c959f"
FG_DIM_DARK = "#8b949e"
RULE = "#d8dee4"
RULE_DARK = "#30363d"
SURFACE = "#ffffff"
SURFACE_DARK = "#0d1117"

CX, CY = 500, 330
CLUSTER_RADIUS = 140
NODE_RADIUS = 190
CORE_R = 50

clusters = [
    {"name": "BACKEND",  "angle": -120, "items": ["Flask", "Django", "FastAPI", "Node.js", "Express"]},
    {"name": "FRONTEND", "angle": -60,  "items": ["React", "Next.js", "HTML/CSS", "Tailwind"]},
    {"name": "DATABASES","angle": 0,    "items": ["MongoDB", "PostgreSQL", "MySQL", "SQLite", "Redis", "Firebase", "Supabase"]},
    {"name": "DEVOPS",   "angle": 60,   "items": ["Docker", "K8s", "AWS", "GCP", "Nginx", "GH Actions"]},
    {"name": "LANGUAGES","angle": 120,  "items": ["C", "C++", "Java", "Python", "JS", "TS"]},
    {"name": "TOOLS",    "angle": 180,  "items": ["Git", "Linux", "Arduino", "GraphQL", "Vercel", "Netlify"]},
]

def deg(angle):
    return angle * math.pi / 180

def point(cx, cy, r, angle):
    a = deg(angle)
    return (cx + r * math.cos(a), cy + r * math.sin(a))

parts = [
    '<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="660" viewBox="0 0 1000 660"',
    ' font-family="JBMono,ui-monospace,SFMono-Regular,Menlo,Consolas,monospace">',
    '<style>',
    f'.bg{{fill:{SURFACE}}}@media(prefers-color-scheme:dark){{.bg{{fill:{SURFACE_DARK}}}}}',
    f'.a{{fill:{FG}}}@media(prefers-color-scheme:dark){{.a{{fill:{FG_DARK}}}}}',
    f'.b{{fill:{FG_EMP}}}@media(prefers-color-scheme:dark){{.b{{fill:{FG_EMP_DARK}}}}}',
    f'.c{{fill:{FG_DIM}}}@media(prefers-color-scheme:dark){{.c{{fill:{FG_DIM_DARK}}}}}',
    f'.r{{stroke:{RULE}}}@media(prefers-color-scheme:dark){{.r{{stroke:{RULE_DARK}}}}}',
    '.w{stroke:#d29922;stroke-width:1.5;stroke-dasharray:6 4}',
    '@media(prefers-color-scheme:dark){.w{stroke:#d29922}}',
    '@media(prefers-reduced-motion){animate{display:none}set{display:none}}',
    '.core{animation:breathe 3s ease-in-out infinite}',
    '@keyframes breathe{0%,100%{opacity:0.4}50%{opacity:1}}',
    '</style>',
    f'<rect width="1000" height="660" class="bg"/>',
]

# Title
parts.append(f'<text x="30" y="40" class="b" font-size="16">ecosystem</text>')
parts.append(f'<text x="30" y="58" class="c" font-size="12">~/network-map  FIG. 01</text>')

# Draw connecting lines from clusters to core
delay_base = 0.3
for i, cl in enumerate(clusters):
    cx_c, cy_c = point(CX, CY, CLUSTER_RADIUS, cl["angle"])
    a = deg(cl["angle"] + 10)
    begin = delay_base + i * 0.15
    dx = cx_c - CX
    dy = cy_c - CY
    length = math.sqrt(dx*dx + dy*dy)
    parts.append(f'<line x1="{CX}" y1="{CY}" x2="{cx_c}" y2="{cy_c}" class="w" opacity="0">'
                 f'<set attributeName="opacity" to="1" begin="{begin:.2f}s"/>'
                 f'<animate attributeName="stroke-dashoffset" from="{length}" to="0" begin="{begin:.2f}s" dur="0.5s" fill="freeze"/>'
                 f'</line>')

# Core node
delay = delay_base + len(clusters) * 0.15 + 0.1
parts.append(f'<circle cx="{CX}" cy="{CY}" r="{CORE_R}" fill="#d29922" opacity="0" class="core">'
             f'<set attributeName="opacity" to="0.8" begin="{delay:.2f}s"/></circle>')
parts.append(f'<circle cx="{CX}" cy="{CY}" r="{CORE_R+4}" fill="none" stroke="#d29922" stroke-width="2" opacity="0">'
             f'<set attributeName="opacity" to="0.3" begin="{delay:.2f}s"/>'
             f'<animate attributeName="r" from="{CORE_R+4}" to="{CORE_R+14}" begin="{delay:.2f}s" dur="1.5s" fill="freeze"/></circle>')
parts.append(f'<text x="{CX-42}" y="{CY+5}" fill="#0d1117" font-size="14" font-weight="bold" opacity="0">'
             f'<set attributeName="opacity" to="1" begin="{delay+0.1:.2f}s"/>MOIZ.SYS</text>')

# Draw clusters
item_delay = delay + 0.2
for ci, cl in enumerate(clusters):
    cx_c, cy_c = point(CX, CY, CLUSTER_RADIUS, cl["angle"])
    
    # Cluster label
    lbl_angle = cl["angle"]
    lbl_x, lbl_y = point(CX, CY, CLUSTER_RADIUS - 40, cl["angle"])
    # Adjust label position based on angle
    ta = "middle"
    if -90 < lbl_angle < 90:
        ta = "start"
    elif lbl_angle > 90 or lbl_angle < -90:
        ta = "end"
    
    delay_c = item_delay + ci * 0.1
    parts.append(f'<text x="{lbl_x}" y="{lbl_y}" class="b" font-size="10" text-anchor="{ta}" opacity="0">'
                 f'<set attributeName="opacity" to="1" begin="{delay_c:.2f}s"/>{cl["name"]}</text>')
    
    # Items around cluster
    n = len(cl["items"])
    item_r = 55
    for ii, item in enumerate(cl["items"]):
        item_angle = cl["angle"] - 15 + (ii * (30 / max(n-1, 1)))
        ix, iy = point(cx_c, cy_c, item_r, item_angle)
        
        # line from cluster center to item
        dx = ix - cx_c
        dy = iy - cy_c
        length = math.sqrt(dx*dx + dy*dy)
        
        delay_i = delay_c + 0.1 + ii * 0.08
        
        # Item dot
        parts.append(f'<circle cx="{ix}" cy="{iy}" r="3" fill="#d29922" opacity="0">'
                     f'<set attributeName="opacity" to="1" begin="{delay_i:.2f}s"/></circle>')
        
        # Item text
        tx = ix + 8
        ty = iy + 4
        parts.append(f'<text x="{tx}" y="{ty}" class="a" font-size="10" opacity="0">'
                     f'<set attributeName="opacity" to="1" begin="{delay_i+0.1:.2f}s"/>{item}</text>')

parts.append('</svg>')
svg = "".join(parts)

out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "assets", "ecosystem.svg")
out = os.path.abspath(out)
with open(out, "w", encoding="utf-8") as f:
    f.write(svg)
print(f"wrote {out}")
