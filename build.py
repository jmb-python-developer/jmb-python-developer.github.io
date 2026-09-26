"""Builds the ML Quest outputs from levels.json.

    python3 build.py

Writes:
  index.html                                  GitHub Pages site (interactive map)
  ../jmb-python-developer/assets/ml-quest-map.svg   README image (static, animated)
  build/readme-snippet.md                     <details> blocks to paste into the profile README

To add or update a level, edit levels.json and run this again.
"""

import base64
import math
import html
import json
from pathlib import Path

ROOT = Path(__file__).parent
PROFILE = ROOT.parent / "jmb-python-developer"
SITE_URL = "https://jmb-python-developer.github.io/"

W, H = 960, 400

C = {
    "sky": "#0E1726", "land": "#15233A", "land2": "#1B2D48", "star": "#C9D6EA",
    "trail": "#F2D492", "trail_dim": "#34455F",
    "cleared": "#34C98B", "cleared_dk": "#0F4A33",
    "current": "#FFC247", "current_dk": "#5C3F00",
    "locked": "#3A4A63", "locked_ink": "#8E9CB3",
    "text": "#EEF3FA", "soft": "#9AA9C0", "fog": "#0B1220",
}

STATUS_WORD = {"cleared": "Cleared", "current": "In progress", "locked": "Locked"}


def esc(s):
    return html.escape(s, quote=True)


def font_face(embed):
    if not embed:
        return ""
    faces = []
    for w in (500, 700):
        b64 = base64.b64encode((ROOT / "build" / f"pixelify-{w}.woff2").read_bytes()).decode()
        faces.append(
            f"@font-face{{font-family:'Pixelify Sans';font-weight:{w};"
            f"src:url(data:font/woff2;base64,{b64}) format('woff2');}}"
        )
    return "".join(faces)


def trail_path(points):
    """Smooth path through points (Catmull-Rom converted to cubic Béziers), one segment per pair."""
    segs = []
    for i in range(len(points) - 1):
        p0 = points[i - 1] if i > 0 else points[i]
        p1, p2 = points[i], points[i + 1]
        p3 = points[i + 2] if i + 2 < len(points) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        segs.append(f"M{p1[0]},{p1[1]} C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]},{p2[1]}")
    return segs


def node_shape(lv):
    x, y, st, kind = lv["x"], lv["y"], lv["status"], lv.get("kind", "tile")
    fill = C[st]
    ink = {"cleared": C["cleared_dk"], "current": C["current_dk"], "locked": C["locked_ink"]}[st]
    out = []
    if kind == "tile":
        if st == "current":
            out.append(
                f'<rect class="pulse" x="{x-31}" y="{y-31}" width="62" height="62" rx="6" '
                f'fill="none" stroke="{C["current"]}" stroke-width="3"/>'
            )
        # pixel-style tile: square with notched corners
        s = 22
        n = 6
        pts = [(x-s+n, y-s), (x+s-n, y-s), (x+s, y-s+n), (x+s, y+s-n), (x+s-n, y+s),
               (x-s+n, y+s), (x-s, y+s-n), (x-s, y-s+n)]
        out.append(f'<polygon points="{" ".join(f"{a},{b}" for a, b in pts)}" fill="{fill}" '
                   f'stroke="{C["sky"]}" stroke-width="3"/>')
        if st == "cleared":
            out.append(f'<polyline points="{x-10},{y+1} {x-3},{y+8} {x+11},{y-8}" fill="none" '
                       f'stroke="{ink}" stroke-width="5" stroke-linecap="square"/>')
        elif st == "current":
            star = []
            for k in range(10):
                r = 12 if k % 2 == 0 else 5
                a = -math.pi / 2 + k * math.pi / 5
                star.append(f"{x + r*math.cos(a):.1f},{y + r*math.sin(a):.1f}")
            out.append(f'<polygon points="{" ".join(star)}" fill="{ink}"/>')
        else:
            out.append(f'<rect x="{x-8}" y="{y-2}" width="16" height="12" fill="{ink}"/>'
                       f'<path d="M{x-5},{y-2} v-4 a5,5 0 0 1 10,0 v4" fill="none" stroke="{ink}" stroke-width="3"/>')
    elif kind == "gate":
        out.append(f'<path d="M{x-26},{y+22} v-26 a26,26 0 0 1 52,0 v26 z" fill="{fill}" stroke="{C["sky"]}" stroke-width="3"/>'
                   f'<path d="M{x-12},{y+22} v-14 a12,12 0 0 1 24,0 v14 z" fill="{C["fog"]}"/>'
                   f'<text x="{x}" y="{y-10}" text-anchor="middle" class="px" font-size="12" fill="{ink}">?</text>')
    elif kind == "flag":
        out.append(f'<rect x="{x-2}" y="{y-28}" width="4" height="50" fill="{C["locked_ink"]}"/>'
                   f'<polygon points="{x+2},{y-28} {x+28},{y-19} {x+2},{y-10}" fill="{fill}" stroke="{C["locked_ink"]}" stroke-width="2"/>'
                   f'<rect x="{x-12}" y="{y+20}" width="24" height="6" fill="{fill}"/>')
    elif kind == "trophy":
        g = f'<g fill="{fill}" stroke="{C["sky"]}" stroke-width="2">'
        g += f'<path d="M{x-18},{y-26} h36 v10 a18,18 0 0 1 -36,0 z"/>'
        g += f'<path d="M{x-18},{y-22} h-8 v6 a8,8 0 0 0 8,8" fill="none" stroke="{fill}" stroke-width="4"/>'
        g += f'<path d="M{x+18},{y-22} h8 v6 a8,8 0 0 1 -8,8" fill="none" stroke="{fill}" stroke-width="4"/>'
        g += f'<rect x="{x-4}" y="{y+2}" width="8" height="10"/><rect x="{x-14}" y="{y+12}" width="28" height="10"/>'
        g += '</g>'
        g += f'<path d="M{x},{y-22} l3,6 6,1 -4.5,4 1,6 -5.5,-3 -5.5,3 1,-6 -4.5,-4 6,-1 z" fill="{C["fog"]}"/>'
        out.append(g)
    elif kind == "castle":
        b = f'<g fill="{fill}" stroke="{C["sky"]}" stroke-width="2">'
        b += f'<rect x="{x-34}" y="{y-10}" width="68" height="34"/>'
        b += f'<rect x="{x-40}" y="{y-30}" width="18" height="54"/><rect x="{x+22}" y="{y-30}" width="18" height="54"/>'
        b += f'<rect x="{x-11}" y="{y-40}" width="22" height="30"/>'
        for bx in (x-40, x-31, x+22, x+31):
            b += f'<rect x="{bx}" y="{y-38}" width="6" height="8"/>'
        b += '</g>'
        b += f'<path d="M{x-8},{y+24} v-14 a8,8 0 0 1 16,0 v14 z" fill="{C["fog"]}"/>'
        b += f'<rect x="{x-5}" y="{y-32}" width="10" height="12" fill="{C["fog"]}"/>'
        out.append(b)
    return "".join(out)


def render_map(data, interactive):
    lv = data["levels"]
    pts = [(l["x"], l["y"]) for l in lv]
    segs = trail_path(pts)
    parts = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
                 f'role="img" aria-labelledby="mapTitle" class="map">')
    parts.append('<title id="mapTitle">ML Quest world map: levels 1.0 and 1.2 cleared, level 1.3 in progress, '
                 'then level 1.4, a World 1 achievement, World 2 and Deep Learning ahead.</title>')
    parts.append("<style>" + font_face(not interactive) + f"""
      .px{{font-family:'Pixelify Sans',ui-monospace,'SFMono-Regular',Menlo,monospace;font-weight:700;}}
      .px5{{font-family:'Pixelify Sans',ui-monospace,'SFMono-Regular',Menlo,monospace;font-weight:500;}}
      .pulse{{transform-box:fill-box;transform-origin:center;animation:pulse 1.6s ease-out infinite;}}
      @keyframes pulse{{0%{{opacity:.9;transform:scale(.85)}}100%{{opacity:0;transform:scale(1.35)}}}}
      .you{{animation:bob 1.2s ease-in-out infinite alternate;}}
      @keyframes bob{{from{{transform:translateY(0)}}to{{transform:translateY(-5px)}}}}
      .twinkle{{animation:tw 3s ease-in-out infinite alternate;}}
      @keyframes tw{{from{{opacity:.25}}to{{opacity:.9}}}}
      @media (prefers-reduced-motion:reduce){{.pulse,.you,.twinkle{{animation:none}}}}
    </style>""")
    # sky and stars
    parts.append(f'<rect width="{W}" height="{H}" rx="14" fill="{C["sky"]}"/>')
    stars = [(40, 40), (130, 70), (210, 30), (330, 55), (420, 25), (520, 60), (640, 35), (700, 80),
             (790, 40), (900, 65), (60, 120), (380, 110), (560, 120), (930, 130), (270, 100), (860, 110)]
    for i, (sx, sy) in enumerate(stars):
        cls = ' class="twinkle"' if i % 3 == 0 else ""
        style = f' style="animation-delay:{(i % 5) * 0.4:.1f}s"' if i % 3 == 0 else ""
        parts.append(f'<rect{cls}{style} x="{sx}" y="{sy}" width="3" height="3" fill="{C["star"]}" opacity=".6"/>')
    # land: layered hills
    parts.append(f'<path d="M0,250 C120,210 220,240 330,225 C450,205 560,240 680,220 C800,200 890,230 960,215 V386 a14,14 0 0 1 -14,14 H14 a14,14 0 0 1 -14,-14 Z" fill="{C["land"]}"/>')
    parts.append(f'<path d="M0,320 C150,300 260,330 400,315 C540,300 660,330 800,310 C880,300 930,310 960,305 V386 a14,14 0 0 1 -14,14 H14 a14,14 0 0 1 -14,-14 Z" fill="{C["land2"]}"/>')
    # fog over locked worlds
    last_w1 = max(i for i, l in enumerate(lv) if l.get("world") == 1)
    fog_x = (lv[last_w1]["x"] + lv[last_w1 + 1]["x"]) / 2
    parts.append(f'<rect x="{fog_x}" y="0" width="{W-fog_x}" height="{H}" fill="{C["fog"]}" opacity=".45"/>')
    parts.append(f'<line x1="{fog_x}" y1="24" x2="{fog_x}" y2="{H-24}" stroke="{C["soft"]}" stroke-width="2" stroke-dasharray="4 8" opacity=".5"/>')
    # world banners
    parts.append(f'<text x="28" y="40" class="px" font-size="18" fill="{C["text"]}" letter-spacing="1">WORLD 1</text>'
                 f'<text x="28" y="60" class="px5" font-size="12" fill="{C["soft"]}" letter-spacing="1">CLASSIC MACHINE LEARNING</text>')
    parts.append(f'<text x="{fog_x+20}" y="40" class="px" font-size="18" fill="{C["soft"]}" letter-spacing="1">BEYOND</text>'
                 f'<text x="{fog_x+20}" y="60" class="px5" font-size="12" fill="{C["soft"]}" letter-spacing="1">COMING UP</text>')
    # trail
    for i, d in enumerate(segs):
        lit = lv[i + 1]["status"] in ("cleared", "current")
        if lit:
            parts.append(f'<path d="{d}" fill="none" stroke="{C["trail"]}" stroke-width="6" stroke-dasharray="2 10" stroke-linecap="square"/>')
        else:
            parts.append(f'<path d="{d}" fill="none" stroke="{C["trail_dim"]}" stroke-width="6" stroke-dasharray="2 10" stroke-linecap="square"/>')
    # nodes
    for l in lv:
        x, y = l["x"], l["y"]
        label_col = C["text"] if l["status"] != "locked" else C["soft"]
        attrs = ""
        if interactive:
            attrs = (f' class="node" data-id="{l["id"]}" tabindex="0" role="button" '
                     f'aria-label="Level {esc(l["num"])}: {esc(l["name"])}, {STATUS_WORD[l["status"]]}"')
        parts.append(f"<g{attrs}>")
        # generous invisible hit area
        parts.append(f'<rect class="hit" x="{x-48}" y="{y-46}" width="96" height="112" fill="transparent"/>')
        parts.append(node_shape(l))
        ly = y + 50
        fs = 15 if len(l["num"]) <= 5 else 12
        parts.append(f'<text x="{x}" y="{ly}" text-anchor="middle" class="px" font-size="{fs}" fill="{label_col}">{esc(l["num"])}</text>')
        parts.append(f'<text x="{x}" y="{ly+16}" text-anchor="middle" class="px5" font-size="12" fill="{C["soft"]}">{esc(l["short"])}</text>')
        parts.append("</g>")
    # player marker over current level
    cur = next(l for l in lv if l["status"] == "current")
    cx, cy = cur["x"], cur["y"] - 48
    parts.append(f'<g class="you"><rect x="{cx-20}" y="{cy-20}" width="40" height="18" fill="{C["current"]}"/>'
                 f'<polygon points="{cx-6},{cy-2} {cx+6},{cy-2} {cx},{cy+6}" fill="{C["current"]}"/>'
                 f'<text x="{cx}" y="{cy-6}" text-anchor="middle" class="px" font-size="12" fill="{C["current_dk"]}">YOU</text></g>')
    # legend
    lx, ly = W - 290, H - 22
    legend = [("cleared", "CLEARED"), ("current", "IN PROGRESS"), ("locked", "LOCKED")]
    for i, (k, t) in enumerate(legend):
        ox = lx + i * 95
        parts.append(f'<rect x="{ox}" y="{ly-10}" width="10" height="10" fill="{C[k]}"/>'
                     f'<text x="{ox+16}" y="{ly}" class="px5" font-size="11" fill="{C["soft"]}">{t}</text>')
    if not interactive:
        parts.append(f'<text x="28" y="{H-18}" class="px5" font-size="12" fill="{C["trail"]}">▶ CLICK THE MAP TO PLAY THE INTERACTIVE VERSION</text>')
    parts.append("</svg>")
    return "\n".join(parts)


def readme_snippet(data):
    icon = {"cleared": "✅", "current": "⭐", "locked": "🔒"}
    out = [
        data["player"]["path_note"],
        "",
        f'<a href="{SITE_URL}"><img src="assets/ml-quest-map.svg" width="100%" '
        f'alt="ML Quest world map: my machine-learning projects shown as game levels. Click to open the interactive version."></a>',
        "",
        "<sub>Click a level below to see what it covered, or open the "
        f'<a href="{SITE_URL}">interactive map</a>.</sub>',
        "",
    ]
    for l in data["levels"]:
        if l.get("kind") and l["status"] == "locked":
            continue  # future worlds stay on the map only
        st = STATUS_WORD[l["status"]]
        out.append("<details>")
        out.append(f'<summary><b>{icon[l["status"]]} Level {l["num"]} · {l["name"]}</b> — {st}</summary>')
        out.append("")
        out.append(f'**Mission:** {l["mission"]}')
        out.append("")
        if l["status"] != "locked":
            out.append(f'**Result:** {l["result"]}')
            out.append("")
        verb = "Learned" if l["status"] == "cleared" else "Will learn"
        out.append(f"**{verb}:**")
        for x in l["learned"]:
            out.append(f"- {x}")
        out.append("")
        out.append("**Skills:** " + " · ".join(f"`{s}`" for s in l["skills"]))
        if l["repo"] and l.get("repo_private"):
            out.append("")
            out.append("🔒 *Repository private until this level is cleared.*")
        elif l["repo"]:
            out.append("")
            out.append(f'[Open the project ↗]({l["repo"]})')
        out.append("")
        out.append("</details>")
    out.append("")
    out.append(f'**How I use AI.** {data["player"]["ai_note"]}')
    return "\n".join(out) + "\n"


def main():
    data = json.loads((ROOT / "levels.json").read_text())
    tpl = (ROOT / "template.html").read_text()
    page = (tpl.replace("<!--MAP-->", render_map(data, interactive=True))
               .replace("/*LEVELS_JSON*/null", json.dumps(data, ensure_ascii=False)))
    (ROOT / "index.html").write_text(page)

    (PROFILE / "assets").mkdir(exist_ok=True)
    (PROFILE / "assets" / "ml-quest-map.svg").write_text(render_map(data, interactive=False))
    (ROOT / "build" / "readme-snippet.md").write_text(readme_snippet(data))
    print("built index.html, assets/ml-quest-map.svg, build/readme-snippet.md")


if __name__ == "__main__":
    main()
