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

# ---- 5. why Louisiana: cane fields by state, and the crop mix around the cane ----
cane = pd.read_parquet(ROOT / "data/interim/csb/csb1825_cane_any_2021_2023_attrs.parquet")
c23 = cane[cane.CDL2023 == 45]
states = {"22": "Louisiana", "12": "Florida", "48": "Texas"}
by = c23.groupby("STATEFIPS").agg(fields=("CSBID", "size"), counties=("CNTYFIPS", "nunique")).loc[list(states)]
mix = pd.read_parquet(ROOT / "data/interim/csb/cane_counties_LA_FL_2023_attrs.parquet")
names = pd.read_csv(ROOT / "data/reference/cdl_codes.csv").set_index("code")["name"]
field_crops = {"Soybeans", "Rice", "Corn", "Cotton", "Sorghum", "Winter Wheat"}
orchards = {"Oranges", "Citrus", "Other Tree Crops", "Pecans"}
pasture = {"Grassland/Pasture", "Fallow/Idle Cropland", "Other Hay/Non Alfalfa", "Sod/Grass Seed"}
def group(n):
    if n == "Sugarcane": return "Sugarcane"
    if n in field_crops or str(n).startswith("Dbl Crop"): return "Other field crops"
    if n in orchards: return "Orchards"
    if n in pasture: return "Pasture or fallow"
    return "Other"
mix["g"] = mix.CDL2023.map(names).map(group)
order = ["Sugarcane", "Other field crops", "Orchards", "Pasture or fallow", "Other"]
colors = {"Sugarcane": "#2E7D32", "Other field crops": "#1F6FB0", "Orchards": "#C8742A",
          "Pasture or fallow": "#9C7AC4", "Other": "#C9CCC4"}
share = mix.groupby("STATEFIPS").g.value_counts(normalize=True).unstack().reindex(columns=order).fillna(0)
print("crop mix in cane counties:\n", (share * 100).round(1).to_string())

fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.6, 5.6), dpi=200, gridspec_kw={"height_ratios": [1, 1.05], "hspace": 0.75})
fig.patch.set_facecolor(SURF)
for ax in (a1, a2):
    ax.set_facecolor(SURF)
    for s in ["top", "right", "bottom"]:
        ax.spines[s].set_visible(False)
    ax.tick_params(length=0)
ylab = [states[s] for s in by.index][::-1]
vals = by.fields.values[::-1]
cols = ["#B9BDB4", "#B9BDB4", "#2E7D32"]
a1.barh(ylab, vals, 0.62, color=cols)
for i, (v, s) in enumerate(zip(vals, by.index[::-1])):
    a1.text(v + 600, i, f"{v:,} fields · {by.loc[s, 'counties']} {'parishes' if s == '22' else 'counties'}",
            va="center", fontsize=12, color=INK)
a1.set_xlim(0, 52000); a1.set_xticks([]); a1.tick_params(axis="y", labelsize=13)
a1.spines["left"].set_color("#B9BDB4")
a1.set_title("Sugarcane fields, 2023", loc="left", fontsize=14, color=INK, pad=8)
left = np.zeros(2)
rows_ = ["22", "12"]
for g in order:
    v = share.loc[rows_, g].values * 100
    a2.barh([states[r] for r in rows_], v, 0.62, left=left, color=colors[g], label=g, edgecolor=SURF, linewidth=2)
    for i, (l, w) in enumerate(zip(left, v)):
        if w >= 9:   # label only segments wide enough to read
            a2.text(l + w / 2, i, f"{w:.0f}%", ha="center", va="center", fontsize=11.5,
                    color="#FBFBF8" if g != "Other" else INK)
    left += v
a2.invert_yaxis(); a2.set_xlim(0, 100); a2.set_xticks([]); a2.tick_params(axis="y", labelsize=13)
a2.spines["left"].set_color("#B9BDB4")
a2.set_title("All fields in the main cane areas, by 2023 crop", loc="left", fontsize=14, color=INK, pad=8)
a2.legend(loc="upper center", bbox_to_anchor=(0.42, -0.08), ncol=3, fontsize=11, frameon=False, handlelength=1.2, columnspacing=1.0)
fig.savefig(OUT / "why_louisiana.png", bbox_inches="tight", pad_inches=0.05, facecolor=SURF)
plt.close(fig)
