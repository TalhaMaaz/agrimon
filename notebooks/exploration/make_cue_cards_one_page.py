"""All 16 cue cards on one A4 landscape PDF page. Text is laid out word by word so bold parts stay bold."""
import re, html, sys
import matplotlib; matplotlib.use("pdf")
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.textpath import TextToPath
from matplotlib.patches import FancyBboxPatch

src = open(sys.argv[1]).read()
cards = []
for m in re.finditer(r'<h2><span>(\d+)</span> (.*?)</h2><ul>(.*?)</ul>', src):
    cards.append((m.group(1), html.unescape(m.group(2)), re.findall(r'<li>(.*?)</li>', m.group(3))))
assert len(cards) == 16, len(cards)

REG = FontProperties(family="Liberation Sans"); BOLD = FontProperties(family="Liberation Sans", weight="bold")
t2p = TextToPath()
def width(s, bold, size):
    p = (BOLD if bold else REG).copy(); p.set_size(size)
    return t2p.get_text_width_height_descent(s, p, ismath=False)[0]

def tokens(li):
    """Words with a bold flag and whether a space came before them (keeps "surveys," and "(NDVI)" tight)."""
    out = []; space = True
    for i, part in enumerate(re.split(r'</?b>', li)):
        for piece in re.split(r'(\s+)', html.unescape(part)):
            if not piece: continue
            if piece.isspace(): space = True; continue
            out.append((piece, i % 2 == 1, space)); space = False
    return out

W, H = 842, 595; M = 16; G = 6
cw = (W - 2*M - 3*G) / 4; ch = (H - 2*M - 3*G - 14) / 4   # 14 pt kept for the page header
PAD = 6; LH = 1.18

def layout(card, size):
    """Return list of (x, y, word, bold, size) lines; y from top of card. None if it does not fit."""
    num, title, lis = card
    items = []; y = PAD + size * 1.15
    items.append((PAD, y, f"{num}  {title}", True, size * 1.15))
    y += size * 0.55
    bullet_w = width("• ", False, size); maxw = cw - 2*PAD
    for li in lis:
        y += size * LH; x = PAD + bullet_w; items.append((PAD, y, "•", False, size))
        first = True
        for w, b, sp_before in tokens(li):
            ww = width(w, b, size); sp = width(" ", False, size) if (sp_before and not first) else 0
            if x + sp + ww > PAD + maxw and x > PAD + bullet_w:
                y += size * LH; x = PAD + bullet_w; sp = 0
            items.append((x + sp, y, w, b, size)); x += sp + ww; first = False
        y += size * 0.25
    return items if y + PAD <= ch else None

def best(card):
    s = 14.0
    while s > 5 and layout(card, s) is None: s -= 0.1
    return round(s, 1)

sizes = [best(c) for c in cards]
size = None  # each card gets its own largest size, capped so the page stays even
print("per-card sizes:", [min(s, 11.0) for s in sizes])

fig = plt.figure(figsize=(W/72, H/72)); ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(H, 0); ax.axis("off")
ax.text(M, M + 8, "AgriMon mid-semester presentation: cue cards", fontproperties=BOLD, fontsize=10, va="baseline", color="#14261c")
ax.text(W - M, M + 8, "16 slides, about 10 minutes", fontproperties=REG, fontsize=8, va="baseline", ha="right", color="#5e6b63")
for i, card in enumerate(cards):
    r, c = divmod(i, 4); x0 = M + c*(cw + G); y0 = M + 14 + r*(ch + G)
    ax.add_patch(FancyBboxPatch((x0, y0), cw, ch, boxstyle="round,pad=0,rounding_size=5", fc="white", ec="#9aa59d", lw=0.8))
    size = min(sizes[i], 11.0)
    for x, y, w, b, s in layout(card, size):
        col = "#2e7d32" if (s > size and False) else "#111111"
        ax.text(x0 + x, y0 + y, w, fontproperties=BOLD if b else REG, fontsize=s, va="baseline", color="#14261c" if b else "#111111")
fig.savefig(sys.argv[2]); print("saved", sys.argv[2])
