"""Two draft slides in standard notation: a UML use-case diagram and a crow's foot ERD."""
import math
import sys

out = sys.argv[1]
F = "font-family:Inter, Arial, sans-serif"
SG = "font-family:'Space Grotesk', Arial, sans-serif"
INK, BG, W, H = "#14261c", "#f6f5ef", 1664, 640


def head(eyebrow, title):
    return f'''  <div style="display:flex; flex-direction:column; gap:12px">
    <p style="{F}; font-size:24px; font-weight:600; letter-spacing:3px; text-transform:uppercase; color:#2e7d32">{eyebrow}</p>
    <h2 style="{SG}; font-size:64px; font-weight:700; line-height:1.1; color:{INK}">{title}</h2>
  </div>'''


def foot(t):
    return f'  <p style="position:absolute; bottom:64px; left:128px; width:1664px; {F}; font-size:24px; color:#5e6b63">{t}</p>'


def pin(x, y, w, h, html, st=""):
    return f'<div style="position:absolute; left:{x}px; top:{y}px; width:{w}px; height:{h}px; display:flex; flex-direction:column; align-items:center; justify-content:center; {st}">{html}</div>'


def label(t, weight=400, size=24, st=""):
    return f'<p style="{F}; font-size:{size}px; font-weight:{weight}; line-height:1.2; text-align:center; color:{INK}; {st}">{t}</p>'


# ---- UML use-case diagram: primary actors left, supporting actors right ----
RX, RY, C1, C2 = 190, 40, 560, 1100
cases = {  # name: (cx, cy, text)
    "map": (C1, 100, "View Field Map"),
    "details": (C1, 280, "View Field Details"),
    "run": (C1, 470, "Run Pipeline<br>for a Region"),
    "eval": (C1, 585, "Evaluate Models"),
    "date": (C2, 100, "Select a Date"),
    "crop": (C2, 195, "View Crop Type<br>and Confidence"),
    "health": (C2, 285, "View Health History"),
    "yield": (C2, 375, "View Indicative Yield"),
    "ingest": (C2, 500, "Ingest Open Data"),
}


def edge(a, b):
    """Point where the line from case a's centre towards b's centre leaves a's ellipse."""
    ax, ay = cases[a][:2]
    bx, by = cases[b][:2]
    dx, dy = bx - ax, by - ay
    t = 1 / math.sqrt((dx / RX) ** 2 + (dy / RY) ** 2)
    return ax + dx * t, ay + dy * t


def dep(frm, to):
    """Dashed dependency with an open arrowhead (UML include and extend)."""
    x1, y1 = edge(frm, to)
    x2, y2 = edge(to, frm)
    a = math.atan2(y2 - y1, x2 - x1)
    pts = [(x2 - 18 * math.cos(a + s), y2 - 18 * math.sin(a + s)) for s in (0.45, -0.45)]
    return (f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="{INK}" stroke-width="2.5" stroke-dasharray="10 7"/>'
            f'<path d="M{pts[0][0]:.0f} {pts[0][1]:.0f}L{x2:.0f} {y2:.0f}L{pts[1][0]:.0f} {pts[1][1]:.0f}" fill="none" stroke="{INK}" stroke-width="2.5"/>'), (x1 + x2) / 2, (y1 + y2) / 2


def person(cx, cy):
    return (f'<circle cx="{cx}" cy="{cy-58}" r="20" fill="#ffffff" stroke="{INK}" stroke-width="3"/>'
            f'<path d="M{cx} {cy-38}V{cy+20}M{cx-36} {cy-20}H{cx+36}M{cx} {cy+20}L{cx-30} {cy+62}M{cx} {cy+20}L{cx+30} {cy+62}" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>')


actors = [(130, 170, "Mill Officer /<br>Agronomist"), (130, 500, "Developer"),
          (1534, 230, "Sentinel-2<br>Catalogue"), (1534, 490, "USDA Data<br>Sources")]
assoc = [((166, 150), "map"), ((166, 150), "details"), ((166, 480), "run"), ((166, 480), "eval"),
         ((1498, 210), "ingest"), ((1498, 470), "ingest")]
deps = [("details", "crop", "«include»"), ("details", "health", "«include»"), ("yield", "details", "«extend»"),
        ("date", "map", "«extend»"), ("run", "ingest", "«include»")]

s = f'<svg aria-label="UML use-case diagram of the AgriMon system with primary actors on the left, supporting actors on the right, and include and extend relationships" width="{W}" height="{H}" viewBox="0 0 {W} {H}" style="position:absolute; left:0; top:0">'
s += f'<rect x="262" y="2" width="1100" height="{H-4}" fill="#ffffff" stroke="{INK}" stroke-width="3"/>'
for (x, y), c in assoc:
    cx, cy = cases[c][:2]
    dx, dy = x - cx, y - cy
    t = 1 / math.sqrt((dx / RX) ** 2 + (dy / RY) ** 2)
    s += f'<line x1="{x}" y1="{y}" x2="{cx+dx*t:.0f}" y2="{cy+dy*t:.0f}" stroke="{INK}" stroke-width="2.5"/>'
tags = []
for a, b, t in deps:
    d, mx, my = dep(a, b)
    s += d
    tags.append(pin(round(mx) - 58, round(my) - 17, 116, 34, label(t, 400, 24, "background:#ffffff")))
for cx, cy, _ in cases.values():
    s += f'<ellipse cx="{cx}" cy="{cy}" rx="{RX}" ry="{RY}" fill="#ffffff" stroke="{INK}" stroke-width="2.5"/>'
for cx, cy, _ in actors:
    s += person(cx, cy)
s += "</svg>"
parts = [s, pin(280, 10, 1064, 36, label("AgriMon Crop Monitoring System", 600, 26))]
parts += [pin(cx - RX + 20, cy - RY, 2 * RX - 40, 2 * RY, label(t)) for cx, cy, t in cases.values()]
parts += tags
parts += [pin(cx - 112 if cx < 800 else cx - 110, cy + 66, 224 if cx < 800 else 220, 64, label(t, 600)) for cx, cy, t in actors]
open(f"{out}/usecases.html", "w").write(f'''<section id="usecases" data-transition="fade" style="display:flex; flex-direction:column; gap:28px; padding:128px 128px 160px; background:{BG}">
{head("Use-case diagram", "Who uses AgriMon, and for what")}
  <div style="position:relative; width:{W}px; height:{H}px; display:flex; flex-direction:column; align-self:stretch">
    {"".join(parts)}
  </div>
{foot("UML notation · «include»: always part of the use case · «extend»: optional addition · 10 / 16")}
</section>
''')

# ---- ERD in crow's foot notation; text stays editable, svg draws only the relationships ----
HH, RH, CW = 52, 38, 480


def entity(x, y, name, rows):
    h = HH + RH * len(rows) + 8
    body = ""
    for key, col, typ in rows:
        body += (f'<div style="display:flex; flex-direction:row; height:{RH}px; align-items:center">'
                 f'<p style="flex:none; width:96px; {F}; font-size:24px; font-weight:600; color:#2e7d32">{key}</p>'
                 f'<p style="flex:none; width:216px; {F}; font-size:24px; font-weight:{600 if "PK" in key else 400}; color:{INK}">{col}</p>'
                 f'<p style="flex:none; width:128px; {F}; font-size:24px; color:#5e6b63">{typ}</p></div>')
    return (f'<div style="position:absolute; left:{x}px; top:{y}px; width:{CW}px; height:{h}px; display:flex; flex-direction:column; background:#ffffff; border:2px solid {INK}">'
            f'<div style="height:{HH}px; display:flex; flex-direction:column; justify-content:center; padding:0 18px; background:{INK}"><p style="{F}; font-size:24px; font-weight:600; letter-spacing:1px; color:{BG}">{name}</p></div>'
            f'<div style="display:flex; flex-direction:column; padding:2px 18px">{body}</div></div>')


def bar(x, y, ux, uy, d):
    return f'<line x1="{x+ux*d-uy*13}" y1="{y+uy*d-ux*13}" x2="{x+ux*d+uy*13}" y2="{y+uy*d+ux*13}" stroke="{INK}" stroke-width="2.5"/>'


def one_only(x, y, ux, uy):
    return bar(x, y, ux, uy, 12) + bar(x, y, ux, uy, 22)


def crow(x, y, ux, uy):
    tip = (x + ux * 22, y + uy * 22)
    return (f'<path d="M{x-uy*13} {y-ux*13}L{tip[0]} {tip[1]}L{x+uy*13} {y+ux*13}" fill="none" stroke="{INK}" stroke-width="2.5"/>')


def one_many(x, y, ux, uy):
    return crow(x, y, ux, uy) + bar(x, y, ux, uy, 30)


def zero_many(x, y, ux, uy):
    return crow(x, y, ux, uy) + f'<circle cx="{x+ux*31}" cy="{y+uy*31}" r="9" fill="{BG}" stroke="{INK}" stroke-width="2.5"/>'


X0, X1, X2, Y2 = 0, 592, 1184, 318
line = lambda d: f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="2.5"/>'
rel = line(f"M480 90H592") + one_many(480, 90, 1, 0) + one_only(592, 90, -1, 0)      # CROP_LABEL >|--|| FIELD
rel += line(f"M1072 90H1184") + one_many(1072, 90, 1, 0) + one_only(1184, 90, -1, 0)  # FIELD >|--|| REGION
rel += line(f"M832 214V{Y2}") + one_only(832, 214, 0, 1) + zero_many(832, Y2, 0, -1)  # FIELD ||--o< PREDICTION
rel += line(f"M592 170H536V430H480") + one_only(592, 170, -1, 0) + zero_many(480, 430, 1, 0)  # FIELD ||--o< INDEX_OBSERVATION
rel += line(f"M1424 176V{Y2}") + one_only(1424, 176, 0, 1) + zero_many(1424, Y2, 0, -1)  # REGION ||--o< YIELD_STATISTIC
svg = f'<svg aria-label="Crow\'s foot relationship lines between the six entities" width="{W}" height="{H}" viewBox="0 0 {W} {H}" style="position:absolute; left:0; top:0">{rel}</svg>'
PF = "PK, FK"
body = svg
body += entity(X0, 0, "CROP_LABEL", [(PF, "field_id", "STRING"), ("PK", "year", "INT"), ("", "crop_code", "INT")])
body += entity(X1, 0, "FIELD", [("PK", "field_id", "STRING"), ("FK", "region_id", "STRING"), ("", "geometry", "POLYGON"), ("", "area_acres", "FLOAT")])
body += entity(X2, 0, "REGION", [("PK", "region_id", "STRING"), ("", "name", "STRING"), ("", "level", "STRING")])
body += entity(X0, Y2, "INDEX_OBSERVATION", [(PF, "field_id", "STRING"), ("PK", "obs_date", "DATE"), ("PK", "index_name", "STRING"), ("", "value", "FLOAT"), ("", "cloud_flag", "BOOL")])
body += entity(X1, Y2, "PREDICTION", [(PF, "field_id", "STRING"), ("PK", "pred_date", "DATE"), ("", "crop_class", "STRING"), ("", "confidence", "FLOAT"), ("", "health_flag", "BOOL"), ("", "est_yield", "FLOAT")])
body += entity(X2, Y2, "YIELD_STATISTIC", [(PF, "region_id", "STRING"), ("PK", "year", "INT"), ("", "official_yield", "FLOAT")])
open(f"{out}/datamodel.html", "w").write(f'''<section id="datamodel" data-transition="fade" style="display:flex; flex-direction:column; gap:28px; padding:128px 128px 160px; background:{BG}">
{head("Database design: entity-relationship diagram", "Every result links back to one field")}
  <div style="position:relative; width:{W}px; height:{H}px; display:flex; flex-direction:column; align-self:stretch">
    {body}
  </div>
{foot("Crow’s foot notation · PK primary key, FK foreign key · logical design, stored as GeoParquet files joined on keys · 11 / 16")}
</section>
''')

for n in ("usecases", "datamodel"):
    sec = open(f"{out}/{n}.html").read()
    open(f"{out}/prev_{n}.html", "w").write('<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Space+Grotesk:wght@700&display=swap" rel="stylesheet"><style>*{margin:0;padding:0;box-sizing:border-box}section{position:relative;width:1920px;height:1080px;overflow:hidden}</style></head><body>' + sec + '</body></html>')
