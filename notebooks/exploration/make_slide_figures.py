"""Slide figures: a crisp field map (slide 1), a dataset coverage matrix and the CDL accuracy chart."""
from pathlib import Path
import sys
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

ROOT = Path(sys.argv[1])
OUT = ROOT / "docs/presentation/figures"
OUT.mkdir(parents=True, exist_ok=True)
INK, MUTED, SURF = "#14261C", "#3D4A42", "#FBFBF8"
plt.rcParams.update({"font.family": "DejaVu Sans", "text.color": INK, "axes.labelcolor": MUTED,
                     "xtick.color": MUTED, "ytick.color": MUTED})

# ---- 1. field map for the cover: a 4 km window, crisp outlines, 4 classes ----
la = gpd.read_parquet(ROOT / "data/interim/csb/csb1825_louisiana.parquet")
p = la[la.CNTY == "Iberia"].copy()
cx = p.loc[p.CDL2023 == 45, "INSIDE_X"].median() + 1500
cy = p.loc[p.CDL2023 == 45, "INSIDE_Y"].median() - 800
half_w, half_h = 2200, 2000                        # metres; matches the 620 x 560 slot
win = p.cx[cx - half_w:cx + half_w, cy - half_h:cy + half_h].copy()
cls = {45: ("Sugarcane", "#2E7D32"), 61: ("Fallow", "#D8C27A"), 5: ("Soybeans", "#2F7FC1")}
win["col"] = win.CDL2023.map(lambda v: cls.get(v, ("Other", "#B9BDB4"))[1])
fig, ax = plt.subplots(figsize=(6.2, 5.6), dpi=220)
fig.patch.set_facecolor(SURF); ax.set_facecolor(SURF)
win.plot(ax=ax, color=win.col, edgecolor=SURF, linewidth=1.1)
ax.set_xlim(cx - half_w, cx + half_w); ax.set_ylim(cy - half_h, cy + half_h); ax.set_axis_off()
counts = win.CDL2023.map(lambda v: cls.get(v, ("Other",))[0]).value_counts()
handles = [Patch(facecolor=c, label=f"{n} ({counts.get(n, 0)})") for n, c in
           [v for v in cls.values()] + [("Other", "#B9BDB4")]]
fig.legend(handles=handles, loc="lower center", ncol=4, fontsize=12, frameon=False, bbox_to_anchor=(0.5, -0.06),
           handlelength=1.4, columnspacing=1.2)
fig.savefig(OUT / "cover_field_map.png", bbox_inches="tight", pad_inches=0.05, facecolor=SURF)
plt.close(fig)
print("map fields:", len(win), counts.to_dict())

# ---- 2. coverage matrix: which candidate covers every need? ----
needs = ["Field\npolygons", "Cane\nlabels", "Many\nyears", "Recent\nfields", "Yield\nstats", "Open\nlicence"]
rows = {
    "US: CSB + CDL\n(Louisiana)": ["Yes", "Yes", "Yes", "Yes", "Partly", "Yes"],
    "La Réunion\n(RPG)":          ["No", "Yes", "Yes", "No", "No", "Yes"],
    "Brazil-Crop":                ["Yes", "Yes", "No", "No", "No", "Yes"],
    "EuroCrops /\nFrance":        ["Yes", "No", "Yes", "Yes", "No", "No"],
}
style = {"Yes": ("#2E7D32", "#FBFBF8"), "Partly": ("#E3C56B", INK), "No": ("#C8553D", "#FBFBF8"),
         "Not\nverified": ("#E4E6E1", MUTED)}
fig, ax = plt.subplots(figsize=(9.6, 5.2), dpi=200)
fig.patch.set_facecolor(SURF); ax.set_facecolor(SURF)
for i, (name, vals) in enumerate(rows.items()):
    for j, v in enumerate(vals):
        bg, fg = style[v]
        ax.add_patch(plt.Rectangle((j + 0.04, -i - 0.92), 0.92, 0.84, facecolor=bg, edgecolor="none"))
        ax.text(j + 0.5, -i - 0.5, v, ha="center", va="center", fontsize=15, color=fg,
                fontweight="bold" if v == "Yes" else "normal")
    ax.text(-0.1, -i - 0.5, name, ha="right", va="center", fontsize=15, color=INK,
            fontweight="bold" if i == 0 else "normal")
for j, n in enumerate(needs):
    ax.text(j + 0.5, 0.15, n, ha="center", va="bottom", fontsize=14, color=MUTED)
ax.add_patch(plt.Rectangle((-2.75, -0.98), 8.8, 0.96, facecolor="none", edgecolor=INK, linewidth=2.5))
ax.set_xlim(-2.8, 6.05); ax.set_ylim(-4.05, 1.25); ax.set_axis_off()
fig.savefig(OUT / "dataset_coverage_matrix.png", bbox_inches="tight", pad_inches=0.05, facecolor=SURF)
plt.close(fig)

# ---- 3. CDL sugarcane accuracy, Louisiana (NASS metadata) ----
years = ["2020", "2022", "2023"]
prod = [94.3, 94.1, 95.0]   # producer's accuracy: share of real cane the CDL finds
user = [96.2, 95.8, 96.4]   # user's accuracy: share of CDL 'cane' that really is cane
x = np.arange(len(years)); w = 0.32
fig, ax = plt.subplots(figsize=(6.6, 5.2), dpi=200)
fig.patch.set_facecolor(SURF); ax.set_facecolor(SURF)
b1 = ax.bar(x - w / 2 - 0.03, prod, w, color="#2E7D32", label="Producer’s accuracy (cane found)")
b2 = ax.bar(x + w / 2 + 0.03, user, w, color="#1F6FB0", label="User’s accuracy (cane label correct)")
for bars in (b1, b2):
    for b in bars:
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 1.2, f"{b.get_height():.1f}%",
                ha="center", va="bottom", fontsize=12.5, color=INK)
ax.set_ylim(0, 115); ax.set_yticks([0, 25, 50, 75, 100]); ax.set_yticklabels(["0", "25", "50", "75", "100%"], fontsize=13)
ax.set_xticks(x); ax.set_xticklabels(years, fontsize=15)
ax.grid(axis="y", color="#E4E6E1", linewidth=1); ax.set_axisbelow(True)
for s in ["top", "right", "left"]:
    ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color("#B9BDB4"); ax.tick_params(length=0)
ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.3), ncol=1, fontsize=13, frameon=False)
fig.savefig(OUT / "cdl_cane_accuracy.png", bbox_inches="tight", pad_inches=0.05, facecolor=SURF)
plt.close(fig)
print("written:", sorted(f.name for f in OUT.iterdir()))

# ---- 4. sugarcane fields per year, Iberia (CSB 2018-2025, S01) ----
yrs = list(range(2018, 2026))
n = [int((p[f"CDL{y}"] == 45).sum()) for y in yrs]
fig, ax = plt.subplots(figsize=(6.6, 5.2), dpi=200)
fig.patch.set_facecolor(SURF); ax.set_facecolor(SURF)
ax.bar(range(len(yrs)), n, 0.72, color="#2E7D32")
ax.axhline(1000, color="#C8553D", lw=2, ls="--")
ax.text(len(yrs) - 0.6, 1000, "pass rule: at least 1,000", ha="right", va="center", fontsize=13, color="#9E3B26",
        bbox=dict(facecolor=SURF, edgecolor="#C8553D", boxstyle="round,pad=0.35"))
for i in (int(np.argmin(n)), int(np.argmax(n))):          # label only the extremes
    ax.text(i, n[i] + 70, f"{n[i]:,}", ha="center", va="bottom", fontsize=13, color=INK)
ax.set_xticks(range(len(yrs))); ax.set_xticklabels([f"’{y % 100:02d}" for y in yrs], fontsize=14)
ax.set_ylim(0, 4900); ax.set_yticks([0, 1000, 2000, 3000, 4000]); ax.set_yticklabels(["0", "1,000", "2,000", "3,000", "4,000"], fontsize=13)
ax.grid(axis="y", color="#E4E6E1", linewidth=1); ax.set_axisbelow(True)
for s in ["top", "right", "left"]:
    ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color("#B9BDB4"); ax.tick_params(length=0)
ax.set_xlabel("year (CSB 2018–2025 labels)", fontsize=13)
fig.savefig(OUT / "cane_fields_per_year.png", bbox_inches="tight", pad_inches=0.05, facecolor=SURF)
plt.close(fig)
print("cane fields per year:", dict(zip(yrs, n)))
