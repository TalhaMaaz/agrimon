"""Cover map: real Iberia CSB fields on the dark slide, full height, fading into the slide on the left."""
import sys
import numpy as np, geopandas as gpd, matplotlib.pyplot as plt
ROOT, OUT = sys.argv[1], sys.argv[2]
W, H = 2900, 4000     # metres; same shape as the 784 x 1080 px slot, so 4 km tall
BG = "#14261C"
COL = {61: "#D8C27A", 5: "#4A9BD9"}; OTHER = "#6F7D74"
la = gpd.read_parquet(f"{ROOT}/data/interim/csb/csb1825_louisiana.parquet", columns=["CNTY","CDL2023","INSIDE_X","INSIDE_Y","geometry"])
p = la[la.CNTY == "Iberia"].copy(); print("crs", p.crs.name, "fields", len(p))
p["a"] = p.area
# densest window: slide over a 100 m grid of field area by centroid, keeping a real crop mix
step = 100
x0, y0 = p.INSIDE_X.min(), p.INSIDE_Y.min()
nx, ny = int((p.INSIDE_X.max()-x0)/step)+2, int((p.INSIDE_Y.max()-y0)/step)+2
ix, iy = ((p.INSIDE_X-x0)/step).astype(int).values, ((p.INSIDE_Y-y0)/step).astype(int).values
def box(mask):
    g = np.zeros((nx, ny)); np.add.at(g, (ix[mask], iy[mask]), p.a.values[mask])
    c = np.zeros((nx+1, ny+1)); c[1:,1:] = g.cumsum(0).cumsum(1)
    a, b = W//step, H//step
    return c[a:,b:]-c[:-a,b:]-c[a:,:-b]+c[:-a,:-b]
tot, cane = box(np.ones(len(p),bool)), box((p.CDL2023==45).values)
# most fields wins (finer pattern), provided the window is well filled and mostly cane
g = np.zeros((nx, ny)); np.add.at(g, (ix, iy), 1); c = np.zeros((nx+1, ny+1)); c[1:,1:] = g.cumsum(0).cumsum(1)
a, b = W//step, H//step; num = c[a:,b:]-c[:-a,b:]-c[a:,:-b]+c[:-a,:-b]
score = num.copy(); score[(tot < .8*W*H) | (cane > .88*tot) | (cane < .6*tot)] = 0
i, j = np.unravel_index(score.argmax(), score.shape)
xa, ya = x0+i*step, y0+j*step
win = p.cx[xa:xa+W, ya:ya+H].copy()
counts = win.CDL2023.map(lambda v: {45:"Sugarcane",61:"Fallow",5:"Soybeans"}.get(v,"Other")).value_counts().to_dict()
print("window", xa, ya, "fields", len(win), counts, "cover %.0f%%" % (100*win.clip((xa,ya,xa+W,ya+H)).area.sum()/(W*H)))
fig = plt.figure(figsize=(7.84,10.8), dpi=200); ax = fig.add_axes([0,0,1,1]); ax.set_axis_off()
fig.patch.set_alpha(0)
# cane gets one of three close greens at random (fixed seed): decoration so single fields read, not data
rng = np.random.default_rng(7); greens = ["#2E7D32", "#388E3C", "#43A047"]
win["col"] = [greens[rng.integers(3)] if v == 45 else COL.get(v, OTHER) for v in win.CDL2023]
win.plot(ax=ax, color=win.col, edgecolor=BG, linewidth=1.8)
ax.set_xlim(xa,xa+W); ax.set_ylim(ya,ya+H)
fig.savefig(f"{OUT}/cover_map_tmp.png", transparent=True); plt.close(fig)
# fade the left edge into the slide so the map has no hard border
im = plt.imread(f"{OUT}/cover_map_tmp.png"); w = im.shape[1]
im[...,3] *= np.clip(np.arange(w)/(0.22*w),0,1)[None,:]
plt.imsave(f"{OUT}/cover_map_dark.png", im)
