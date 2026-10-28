---
type: briefing
status: final
tags: [briefing, spike, csb, louisiana, phase-r, python, statistics]
phase: R
date: 2026-10-28
---

# B02: Spike S01, explained line by line

This is a snapshot from 2026-10-28, covering the notebook `notebooks/exploration/01_csb_fields.ipynb` (PR #31, issue #30). Reading time is about 60 to 75 minutes. Read it with the notebook open in Jupyter next to it:

```
~/miniforge3/envs/agrimon-spikes/bin/jupyter lab
```

Then open `notebooks/exploration/01_csb_fields.ipynb`. Questions you ask go in section 12.

How this document is ordered:

```
 1. why this spike exists          (the question, and why we set rules before looking)
 2. the dataset                    (what CSB is, how NASS makes it, every column)
 3. getting the data               (download, unzip, cut out Louisiana: code explained)
 4. the crop-code dictionary       (why we didn't type crop names from memory)
 5. the notebook, cell by cell     (every line of code and why)
 6. the statistics we used         (count, median, percentile, log scale, ...)
 7. what we found, and why it matters
 8. corrections and limits         (what I got wrong or assumed)
 9. Python and pandas idioms used
10. glossary
11. check yourself
12. questions and answers
```

---

## 1. Why this spike exists

### 1a. Where it sits in the plan

```
 Phase R (research and architecture)
   step 1 design questions ......... done
   step 2 literature ............... started
   step 5 SPIKES (small experiments) <-- we are here: S01 is the first
   step 6 architecture dossier
   step 7 Checkpoint R (you approve) --> then we build modules A, B, C
```

A **spike** is a small experiment that answers one design question with evidence. The code is throwaway, which is why it lives in `notebooks/exploration/`. What we learn is not throwaway: it goes into `docs/research/spikes/S01_csb_fields.md` and, later, into the thesis.

### 1b. The question

> Are the USDA Crop Sequence Boundaries usable as the **field polygons** (P-1) and the **per-year crop labels** (P-2) of our app, in our study area?

Why we needed to ask this, rather than assume it:

- Our app's first screen (product spec, P-1) is a map of field polygons. If the polygons are bad (too small, missing, wrong), every later module is built on sand.
- Module A learns from labels. If the labels are missing in some years, or there are too few cane fields, we can't train or test honestly.
- At the defence, "why did you trust this dataset?" must have an answer with numbers. This spike produces those numbers.

### 1c. Why we wrote decision rules *before* looking at the data

```
 1. at least 1,000 sugarcane fields in each year 2018-2025
 2. median cane field covers at least 50 Sentinel-2 pixels (0.5 ha)
 3. every field carries a crop code for all eight years
```

If you look at the data first and decide afterwards what "good enough" means, you will (without meaning to) pick thresholds that make the data look good. Writing the rule first is a guard against fooling ourselves. In science this is called **pre-registration**; in software it's like writing the test before the code.

Where each threshold comes from:

| Rule | Why that number | Honest status |
|---|---|---|
| ≥ 1,000 cane fields per year | Enough to train on one set of years and still have hundreds to test on held-out years and areas. Too few test fields make an accuracy score jumpy | Our judgment, not from a paper |
| ≥ 0.5 ha (50 pixels) | A Sentinel-2 pixel is 10 m × 10 m = 100 m² = 0.01 ha. Pixels on a field's edge mix two fields. With 50+ pixels, most pixels are inside the field, so the field's average is meaningful | Rule of thumb, not from a paper. Phase R literature should confirm or replace it |
| Code in all 8 years | Without a label for a year, that year can't be used for training or testing | Practical requirement |

---

## 2. The dataset: Crop Sequence Boundaries (CSB)

### 2a. What it is, in NASS's own words

From the metadata file inside the zip (`NationalCSB_2018-2025_rev23_metadata.htm`):

> *"Crop Sequence Boundaries (CSB) is a vector-based geospatial dataset which are fully synthetic representations of agricultural fields, their acreage, and cropping rotation history. These new data are primarily derived from a historical stack of Cropland Data Layers ..."*

Key word: **synthetic**. Nobody walked these fields or drew them by hand. The metadata says: *"The creation process is python-based with no manual drawing of field boundaries."*

### 2b. How NASS makes it (from the metadata's process description)

```
 8 years of CDL crop maps (2018 ... 2025), one raster per year
        |
        | 1. simplify crop categories (fewer classes)
        | 2. filter noise (remove isolated odd pixels)
        | 3. resample to 10 m pixels
        | 4. burn in road and rail lines (they split fields)
        | 5. stack the 8 years: each pixel now has an 8-year "crop sequence"
        v
 neighbouring pixels with the same sequence  ->  one polygon
        |
        | 6. small polygons (< 1 ha) with 2+ crop years are merged into
        |    their biggest neighbour (removes "islands" inside fields)
        |    polygons > 1 ha are kept if they have at least 1 crop year
        | 7. simplify outlines (Wang-Müller algorithm, 60 m tolerance)
        v
 national database, attribute table filled in  ->  CSB 2018-2025
```

Why this matters to us:

- **Step 6 explains a finding:** we found no field under 0.5 ha. NASS deliberately removes most tiny polygons.
- **Step 7 explains why fields look like smooth blobs:** outlines are simplified with a 60 m tolerance. Small bends and straight corners are lost.
- **Step 5 is why a "field" means "same crop history":** two real fields that always grew the same crops can become one CSB polygon.

### 2c. The "edition" idea

NASS makes a new CSB for every 8-year **window**: 2008-2015, 2009-2016, ... up to 2018-2025 (11 editions). Each edition has its own polygons. We downloaded the newest one, **2018-2025**, because it reaches the most recent year (2025), which matters for the "present-day" health layer (P-3, and the Tier 2 demo).

### 2d. The file

| Fact | Value |
|---|---|
| Download | `NationalCSB_2018-2025_rev23.zip`, 3,758,027,335 bytes (3.76 GB) |
| Inside | an Esri **File Geodatabase** `CSB1825.gdb` (a folder of binary files Esri's ArcGIS uses; GDAL can read it with its `OpenFileGDB` driver) plus the metadata page |
| Unzipped | 5.4 GB |
| Layers | one: `national1825` |
| Rows | 15,973,095 fields (whole contiguous US) |
| Geometry type | MultiPolygon (a field can be several separate pieces, e.g. split by a ditch) |
| CRS | Albers Conic Equal Area on the NAD83 datum, in metres |
| Licence | *"provided to the public as is and are considered public domain and free to redistribute"* |

### 2e. Every column

Official definitions from the metadata, plus what we observed.

| Column | Official definition | What it looks like / what we use it for |
|---|---|---|
| `CSBID` | "CSB Identifier" | e.g. `221825000004158`. Observed (not documented): starts with the state code `22` and the edition `1825`, then a running number. Our unique id per field |
| `CSBYEARS` | (not in the list) | `1825` for every row = the edition 2018-2025 |
| `CSBACRES` | "Area of polygon in acres" | field size. 1 acre = 0.404686 ha. We convert to hectares |
| `CDL2018` … `CDL2025` | "Majority crop type within the CSB polygon as identified in [year] Cropland Data Layer" | an integer code per year. 45 = Sugarcane, 61 = Fallow/Idle, 5 = Soybeans … These are **our labels** |
| `STATEFIPS` | "US State FIPS code" | `22` = Louisiana. FIPS is the US Census code system for states and counties |
| `STATEASD` | "US State FIPS code plus USDA NASS Agricultural Statistics District" | e.g. `2250` |
| `ASD` | "USDA NASS Agricultural Statistics District" | a group of neighbouring counties that NASS reports statistics for. Will matter for yield statistics (S04) |
| `CNTY` | "US County names" | in Louisiana counties are called **parishes**: "Iberia", "Rapides" … |
| `CNTYFIPS` | "US County FIPS code" | e.g. `079` |
| `INSIDE_X`, `INSIDE_Y` | "The center X / Y coordinate of a CSB polygon" | in the file's CRS (metres). Handy to place a label or find a field quickly |
| `ORIG_FID` | (not in the list) | empty (NaN) in our rows. Ignored |
| `Shape_Length` | "Calculated shape length in meters" | the perimeter |
| `Shape_Area` | (computed by ArcGIS) | area in m². We used it to double-check `CSBACRES` |
| `geometry` | "Feature geometry" | the polygon itself |

**"Majority" is a key word.** `CDL2023 = 45` means "more CDL pixels inside this polygon were sugarcane than any other single class in 2023". It does *not* mean the whole field is cane. A field could be 51 % cane and 49 % soybeans and still say 45. Spike S02 measures how pure fields really are.

### 2f. One more fact from the metadata that matters a lot

> *"The CDL uses Landsat 8 and 9 OLI/TIRS imagery … The CDL also uses Sentinel 2A and 2B imagery …"*

So the CDL, and therefore the CSB labels, were themselves made by a classifier that looked at **Sentinel-2**, the same satellite our model will look at. If our model learns "Sentinel-2 → CDL label", it is partly learning to copy another Sentinel-2 classifier. This is the **circularity** issue from B01, now confirmed at the source. It doesn't make the project invalid: a well-made copy of the CDL that works in-season, per field and on a new region is still useful. But the thesis must say it plainly, and S02 and the split design must keep it in view.

---

## 3. Getting the data (before the notebook)

These steps ran in the terminal, not in the notebook, because they run once.

### 3a. Download

```bash
curl -L -C - --retry 20 --retry-delay 10 --retry-all-errors \
     -o NationalCSB_2018-2025_rev23.zip "https://www.nass.usda.gov/Research_and_Science/Crop-Sequence-Boundaries/datasets/NationalCSB_2018-2025_rev23.zip"
```

| Flag | Why |
|---|---|
| `-L` | follow redirects (servers often send you to the real file location) |
| `-C -` | **resume**: if the connection drops, continue from where it stopped instead of restarting 3.76 GB |
| `--retry 20 --retry-delay 10 --retry-all-errors` | your network drops sometimes (we saw it last session), so retry automatically |

It ran **in the background** so we could keep working. Afterwards I compared the file size with the size the server announced (`content-length: 3758027335`) to be sure nothing was cut off.

### 3b. Look before reading: what's inside?

```python
import pyogrio
p = 'NationalCSB_2018-2025_rev23/CSB1825.gdb'
print(pyogrio.list_layers(p))   # -> [['national1825', 'MultiPolygon']]
i = pyogrio.read_info(p)        # metadata only, no rows loaded
print(i['crs'], i['features'], i['fields'])
```

`read_info` reads only the header: CRS, row count and column names. It's like `SELECT` on a table's schema before running a big query. With 16 million rows you don't load blindly.

### 3c. The PROJ error, and its fix

The first run printed `PROJ: proj_create_from_database: Open of .../share/proj failed`.

- **What PROJ is:** the library that converts between coordinate systems. It needs a database file, `proj.db`, which says what "EPSG:4326" or "Albers" mean.
- **Why it failed:** I ran the environment's Python directly, without *activating* the environment. Activation sets an environment variable, `PROJ_DATA`, that tells PROJ where `proj.db` is.
- **The fix:** the Jupyter kernel now sets `PROJ_DATA` and `GDAL_DATA` itself (in `~/.local/share/jupyter/kernels/agrimon-spikes/kernel.json`). In the terminal, use `mamba activate agrimon-spikes`.
- The pitfall is recorded in `notebooks/exploration/README.md`.

### 3d. Cut out Louisiana

```python
import pyogrio
src = 'data/raw/csb/NationalCSB_2018-2025_rev23/CSB1825.gdb'
la = pyogrio.read_dataframe(src, layer='national1825',
                            where="STATEFIPS = '22'",   # SQL filter, applied while reading
                            use_arrow=True)              # faster bulk transfer into pandas
la.to_parquet('data/interim/csb/csb1825_louisiana.parquet')
```

Why each part:

- **`where="STATEFIPS = '22'"`** is an SQL condition. GDAL applies it while reading, so only Louisiana's rows are turned into Python objects. Loading all 16 million and then filtering would need far more memory than your 16 GB laptop has. `'22'` is in quotes because the column is text, not a number.
- **`use_arrow=True`** moves data in big columnar blocks (Apache Arrow) instead of row by row, which is much faster.
- **GeoParquet output.** Parquet is a columnar, compressed, typed file format, like a CSV that remembers types and is 10–50× faster to read. GeoParquet adds the geometry and the CRS. Result: 88 MB that loads in seconds, versus 2 minutes to scan the geodatabase.
- **Folders:** `data/raw/` holds data exactly as downloaded (never edited); `data/interim/` holds derived files we can always rebuild from raw. This separation is a standard data-project layout. If an interim file is wrong, delete it and regenerate; raw is the source of truth. All of `data/` is git-ignored (rule 10).
- **The warning:** `organizePolygons() received a polygon with more than 100 parts`. Some fields have more than 100 pieces, and GDAL has to work out which rings are outer edges and which are holes. It's slow, not wrong.

Result: **206,389 fields in Louisiana**, in 1 minute 59 seconds.

---

## 4. The crop-code dictionary

The CSB stores crops as numbers (`45`), and we need names ("Sugarcane"). I could have typed a table from memory, but rule 6 says never invent facts; a wrong name would quietly spread through every figure. Instead, the code reads the official list from the NASS CDL metadata page:

```python
import re, html, requests, pandas as pd
t = requests.get('https://data.nass.usda.gov/Research_and_Science/Cropland/metadata/metadata_la23.htm', timeout=60).text
t = html.unescape(re.sub(r'<[^>]+>', '', t))         # strip HTML tags, turn &quot; into "
rows = re.findall(r'^\s*"(\d+)"\s+(.+?)\s*$', t, flags=re.M)
codes = pd.DataFrame(rows, columns=['code', 'name']).astype({'code': int}).drop_duplicates('code')
codes = codes[codes.name.str.strip() != '']           # drop codes with no name
codes.to_csv('data/reference/cdl_codes.csv', index=False)
```

- `re.sub(r'<[^>]+>', '', t)` deletes everything that looks like an HTML tag, leaving plain text.
- On the page, the code list looks like `"45"   Sugarcane`. The regular expression `^\s*"(\d+)"\s+(.+?)\s*$` means: at a line start, optional spaces, a quoted number (captured), spaces, then the rest of the line (captured) as the name.
- `re.M` makes `^` and `$` match at every line, not just the start and end of the whole text.
- `drop_duplicates('code')`: the page lists some codes more than once.

Result: 134 code-name pairs. I checked a sample against the page: 0 Background, 1 Corn, 3 Rice, 5 Soybeans, 45 Sugarcane, 61 Fallow/Idle Cropland, 111 Open Water, 176 Grassland/Pasture, 190 Woody Wetlands, 195 Herbaceous Wetlands.

---

## 5. The notebook, cell by cell

Section numbers below match the notebook's headings.

### Section 1: Load Louisiana

```python
from pathlib import Path
import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path.cwd().parents[1] if Path.cwd().name == "exploration" else Path.cwd()
FIG = ROOT / "docs/research/spikes/figures"
FIG.mkdir(parents=True, exist_ok=True)

la = gpd.read_parquet(ROOT / "data/interim/csb/csb1825_louisiana.parquet")
codes = pd.read_csv(ROOT / "data/reference/cdl_codes.csv").set_index("code")["name"]
print(f"{len(la):,} fields in Louisiana")
la.head(3)
```

| Line | What and why |
|---|---|
| imports | `geopandas` (tables with shapes), `pandas` (tables), `numpy` (arrays and maths), `matplotlib` (plots) |
| `ROOT = ...` | Jupyter runs with the notebook's folder (`notebooks/exploration`) as the current directory. `.parents[1]` goes two folders up to the repo root. That way paths like `data/...` work wherever you start Jupyter. `Path` objects join with `/`, which is safer than gluing strings |
| `FIG.mkdir(parents=True, exist_ok=True)` | create the figures folder; no error if it exists |
| `gpd.read_parquet` | load the 88 MB GeoParquet → a `GeoDataFrame` |
| `.set_index("code")["name"]` | turn the two-column table into a **lookup**: a pandas `Series` where `codes[45]` gives `"Sugarcane"`. Like a Python dict, but it works on whole columns at once (`.map(codes)`) |
| `f"{len(la):,}"` | the `:,` adds thousands separators: `206,389` |
| `la.head(3)` | show the first 3 rows. Always look at real rows before computing anything |

**Output:** 206,389 fields; the first rows are in Rapides parish.

### Section 2: The attribute table

```python
la[["CSBID", "CSBACRES"] + [f"CDL{y}" for y in range(2018, 2026)] + ["CNTY"]].sample(5, random_state=0)
```

- `[f"CDL{y}" for y in range(2018, 2026)]` is a **list comprehension** that builds `["CDL2018", ..., "CDL2025"]`. `range(2018, 2026)` stops *before* 2026, so it ends at 2025.
- `la[[...]]` with a list selects those columns.
- `.sample(5, random_state=0)` picks 5 random rows. Why random and not `head`? The first rows come from one place (Rapides); random rows show the variety. `random_state=0` fixes the randomness, so the same 5 rows appear every time you run it (rule 8, reproducibility).

What the output taught us:
- A row like `45 45 45 61 61 5 5 5` (St. James) reads: cane for three years, fallow for two, then soybeans.
- So one row is one field with its whole history.

### Section 3: Coordinate reference systems

```python
print("CSB CRS:", la.crs.name, "| units:", la.crs.axis_info[0].unit_name)
one = la.iloc[[0]]
print("first corner, Albers (m):", np.round(<first vertex of the first polygon>, 1))
g = one.to_crs(4326).geometry.iloc[0]
g = g if g.geom_type == "Polygon" else list(g.geoms)[0]
print("same corner, lon/lat (degrees):", np.round(g.exterior.coords[0], 5))

ratio = (la["Shape_Area"] / 4046.856) / la["CSBACRES"]
print(f"area check, Shape_Area/CSBACRES: median {ratio.median():.4f} (1.0 means consistent)")
```

**The concept.** A coordinate is just two numbers; the CRS says what they mean:

```
 Albers (CSB):   (312592.9, 929571.7)   metres east and north of a chosen origin, on a flat map
 EPSG:4326:      (-92.70035, 31.39261)  degrees of longitude and latitude, on the round Earth
```

How the code works:
- **`la.crs`** is the CRS stored with the data.
- **`la.iloc[[0]]`** takes the first row. The double brackets keep it a GeoDataFrame instead of a single row.
- **The first vertex.** A MultiPolygon is a list of polygons, a polygon has an `exterior` ring, and the ring has `coords` (the corner points). So the code goes MultiPolygon → first polygon → exterior → first coordinate. The notebook's line for this is long and awkward; it would be written more cleanly in real code.
- **`.to_crs(4326)`** re-projects the field into longitude and latitude. EPSG:4326 is the code for "WGS 84 lon/lat", the system GPS and web maps use.

**Why I printed both:** to make the idea visible. The *same* point, with two very different pairs of numbers. If you mix systems by accident, your field lands in the ocean.

**The area check, and why:**
- `Shape_Area` is in m², and 1 acre = 4,046.856 m², so `Shape_Area / 4046.856` should equal `CSBACRES`.
- The ratio's median is **1.0000**: the two agree.
- This is a **sanity check**: a cheap test that the data is self-consistent before you trust it. If it had come out at 0.0001, we'd know a unit was wrong.
- Using the median, rather than checking every row, tells us the typical row agrees. (Section 6 explains medians.)

**Why it matters:**
- **Areas are only correct in an equal-area projection.** Albers keeps areas true; lon/lat degrees aren't even a unit of area.
- **Sentinel-2 uses UTM zone 15N** (EPSG:32615), a different metre-based CRS. In S03 we must re-project one onto the other before combining them.

### Section 4: Choose the study parish

```python
cane23 = la[la["CDL2023"] == 45]
rank = (cane23.groupby("CNTY")
        .agg(cane_fields=("CSBID", "size"),
             cane_acres=("CSBACRES", "sum"),
             median_acres=("CSBACRES", "median"))
        .sort_values("cane_acres", ascending=False))
rank.head(10).round(1)
```

- **`la[la["CDL2023"] == 45]`** is **boolean filtering**. `la["CDL2023"] == 45` makes a True/False column, and `la[...]` keeps the True rows. That leaves the fields that were cane in 2023.
- **`groupby("CNTY")`** splits the rows into one group per parish, like SQL `GROUP BY`.
- **`.agg(name=(column, function))`** is "named aggregation": for each group, compute these and call them these names:
  - `size`: number of rows (cane fields);
  - `sum` of acres (total cane area);
  - `median` of acres (typical field size).
- **`.sort_values(..., ascending=False)`** puts the biggest cane area first.

Why 2023? It's a recent year with full CDL metadata. We checked its CDL sugarcane accuracy last session: producer's accuracy 95.0 %, user's accuracy 96.4 %.

The output (top 5):

| Parish | Cane fields | Cane acres | Median acres |
|---|---|---|---|
| Pointe Coupee | 3,107 | 81,538.5 | 15.3 |
| Iberia | 4,213 | 64,020.4 | 11.5 |
| Vermilion | 2,609 | 54,009.8 | 14.9 |
| St. Mary | 2,644 | 51,332.8 | 13.6 |
| Assumption | 3,048 | 47,011.9 | 12.0 |

Louisiana in total: 32,373 cane fields and 604,492 cane acres in 2023.

**Why Iberia and not Pointe Coupee:** Iberia has the most cane **fields**, and its fields are **smaller** (median 11.5 acres vs 15.3).
- More fields means more training and test examples.
- Smaller fields are a harder test for 10 m pixels and a little closer to Pakistan.

This was a judgment call, not a rule. Section 7 explains why a second, more mixed parish is probably needed later.

```python
PARISH = "Iberia"
p = la[la["CNTY"] == PARISH].copy()
p["ha"] = p["CSBACRES"] * 0.404686
p["crop23"] = p["CDL2023"].map(codes)
p["crop23"].value_counts().head(10)
```

- **`PARISH = "Iberia"`** is a constant at the top, so changing the parish is a one-line edit.
- **`.copy()`** makes a real copy. Without it, pandas may treat `p` as a *view* of `la`, and adding columns triggers a `SettingWithCopyWarning`, because it's ambiguous whether you meant to change `la` too.
- **`p["ha"]`** converts acres to hectares. We think in hectares because Sentinel-2 pixels are naturally measured that way: one pixel is 0.01 ha.
- **`.map(codes)`** replaces each number with its name using our lookup: 45 becomes "Sugarcane".
- **`.value_counts()`** counts how many fields have each value, sorted from most to least.

**Output:** Iberia has 5,632 fields (34,241 ha). In 2023:

| Crop | Fields |
|---|---|
| Sugarcane | 4,213 |
| Fallow/Idle Cropland | 829 |
| Soybeans | 221 |
| Aquaculture | 172 |
| Grassland/Pasture | 107 |
| Herbaceous Wetlands | 26 |
| Rice | 22 |

Aquaculture is mostly crawfish ponds, which Louisiana is known for.

### Section 5: The maps

```python
top = p["crop23"].value_counts().index[:6].tolist()
p["crop_map"] = np.where(p["crop23"].isin(top), p["crop23"], "Other")
palette = {"Sugarcane": "#2e7d32"}
...
for cat, col in palette.items():
    sub = p[p["crop_map"] == cat]
    sub.plot(ax=ax, color=col, linewidth=0, label=f"{cat} ({len(sub):,})")
fig.savefig(FIG / "S01_iberia_crop2023.png", dpi=130, bbox_inches="tight")
```

- **`top`** holds the 6 most common crops.
- **`np.where(condition, a, b)`** is a vectorised if/else: if the crop is in the top 6, keep its name, otherwise write "Other". Why? A legend with 25 colours is unreadable. Keep the main classes and lump the rest.
- **`palette`:** sugarcane gets a strong green; everything else gets muted colours. This is a deliberate design choice: the eye should go to the class the product cares about.
- **The loop plots one class at a time** with its own colour and label, so the legend shows a count per class.
- **`fig.savefig(...)`** writes a PNG into `docs/`, so the figure shows in Obsidian and can go on slides.

What to see in the map:
- Iberia is **dominated** by cane, with fallow fields scattered among it.
- The pink blocks to the east are aquaculture.
- The long strips follow the bayous.

**The 5 km zoom:**

```python
cx = p.loc[p.CDL2023 == 45, "INSIDE_X"].median()
cy = p.loc[p.CDL2023 == 45, "INSIDE_Y"].median()
win = p.cx[cx - 2500:cx + 2500, cy - 2500:cy + 2500]
```

- **The centre of the window** is the median x and median y of all cane-field centres: the middle of the parish's cane area. Median rather than mean, so a few far-off fields don't pull it away.
- **`p.cx[xmin:xmax, ymin:ymax]`** is geopandas' **coordinate indexer**: keep the fields that touch this box.
- **±2,500 m** works only because the CRS is in metres, giving a 5 km × 5 km window.
- **Result:** 262 fields, drawn with black outlines so individual fields are visible.

What to see in the zoom: outlines are **smooth, rounded blobs**, not the sharp rectangles of real fields. That's NASS's 60 m simplification (section 2b, step 7).

### Section 6: Field sizes against Sentinel-2 pixels

```python
cane_p = p[p.CDL2023 == 45]
bins = np.logspace(-2, 3, 60)
ax.hist(p["ha"], bins=bins, ...)
ax.hist(cane_p["ha"], bins=bins, ...)
ax.axvline(0.5, ...)
ax.set_xscale("log")
for name, d in [("all fields", p), ("sugarcane 2023", cane_p)]:
    q = d["ha"].quantile([0.1, 0.5, 0.9])
    print(... q[0.5], q[0.5] / 0.01, q[0.1], q[0.9], (d.ha < 0.5).mean())
```

**Why we wanted this number:** whether satellite pixels can "see" a field depends on how many pixels fall inside it. A 0.3 ha field is about 30 pixels, and many of them sit on the edge, half in the neighbour's field. A 5 ha field is about 500 pixels, mostly clean.

How the code works:
- **`np.logspace(-2, 3, 60)`** makes 60 histogram bins spaced evenly on a log scale, from 10⁻² = 0.01 ha to 10³ = 1,000 ha. Section 6 explains why a log scale.
- **Two histograms on the same bins:** all fields in grey, cane fields in green on top, so you can compare them.
- **`axvline(0.5)`** draws the decision-rule line at 0.5 ha.
- **`quantile([0.1, 0.5, 0.9])`** gives the 10th percentile, the median and the 90th percentile (section 6).
- **`(d.ha < 0.5).mean()`:** the mean of a True/False column is the *share* that is True, because True counts as 1 and False as 0. A handy pandas trick.

Output:

| | Median | ≈ pixels | 10th pct | 90th pct | Share under 0.5 ha |
|---|---|---|---|---|---|
| All fields | 4.55 ha | ~455 | 1.83 ha | 11.67 ha | 0.0 % |
| Sugarcane 2023 | 4.65 ha | ~465 | 1.97 ha | 11.77 ha | 0.0 % |

Reading it:
- **The typical cane field is about 4.65 ha, roughly 465 Sentinel-2 pixels.** That's large enough that per-field averages will be stable.
- **90 % of cane fields are bigger than 1.97 ha** (about 200 pixels).
- **No field under 0.5 ha.** That's partly NASS's rule of merging small polygons into neighbours (section 2b), not a fact about Louisiana farms.

### Section 7: The crop history

```python
years = list(range(2018, 2026))
cols = [f"CDL{y}" for y in years]
print({y: int((p[f'CDL{y}'] == 45).sum()) for y in years})
missing = (p[cols] <= 0).sum()
n_cane = (p[cols] == 45).sum(axis=1)
ever = p[n_cane > 0]
(n_cane[n_cane > 0]).value_counts().sort_index()
```

- **`(p['CDL2023'] == 45).sum()`:** summing True/False counts the Trues, so this counts the cane fields in that year. The dict comprehension does it for every year.
- **`missing`:** code 0 means "Background", i.e. no class. `(p[cols] <= 0).sum()` counts the missing labels per year. This checks decision rule 3.
- **`(p[cols] == 45).sum(axis=1)`:** `axis=1` sums **across a row** (over the 8 years), not down a column. So `n_cane` is, for each field, how many of the 8 years it was cane.
- **`ever`** holds the fields that were cane at least once.
- **`value_counts().sort_index()`** makes a distribution: how many fields had 1 cane year, 2, … 8.

Outputs:

- Cane fields per year in Iberia:

  | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
  |---|---|---|---|---|---|---|---|
  | 4,165 | 4,187 | 4,100 | 4,143 | 4,204 | 4,213 | 4,019 | 3,963 |

  The lowest is 3,963, so rule 1 (≥ 1,000) passes with a wide margin.
- Missing labels: 0 in every year, so rule 3 passes.
- 5,372 fields were cane at least once. Of those:

  | Cane years out of 8 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
  |---|---|---|---|---|---|---|---|---|
  | Fields | 71 | 54 | 50 | 92 | 306 | **2,925** | **1,775** | 99 |

**Why we wanted this:** sugarcane isn't planted every year like wheat. The industry cycle (well known in sugarcane agronomy; we still need a paper to cite it for Louisiana) is:

```
 year:      1          2           3           4          5
         plant cane  1st ratoon  2nd ratoon  (3rd ratoon) fallow -> replant
         (planted)   (regrows from the stubble after harvest)
```

If the CSB labels are realistic, most cane fields should be cane 6 or 7 years out of 8, with one or two fallow years. That's exactly what we see (2,925 + 1,775 fields). If we had seen random patterns, like cane, soy, cane, rice, we'd distrust the labels.

**The sequences:**

```python
short = {45: "C", 5: "S", 61: "F", 1: "M", 3: "R", 176: "G"}
seq = ever[cols].apply(lambda r: "".join(short.get(v, ".") for v in r), axis=1)
seq.value_counts().head(15)
```

- **`.apply(func, axis=1)`** runs `func` once per **row**.
- **The function** turns each code into a letter, using `.get(v, ".")` so unknown codes become ".". Then it joins the 8 letters into one string, like `CCCFCCCC`.
- **`value_counts()`** counts how many fields share each 8-year story.

Top results:

| Sequence | Fields | Reading |
|---|---|---|
| `CCCCFCCC` | 429 | 4 cane years, fallow in 2022, replanted |
| `CCCFCCCC` | 425 | fallow in 2021 |
| `CCFCCCCF` | 324 | fallow 2020 and 2025 |
| `CCCFCCCF` | 285 | fallow 2021 and 2025 |
| `CCFCCCFC` | 284 | fallow 2020 and 2024 |
| `CCCCSCCC` | 112 | soybeans instead of fallow in 2022 |
| `CCCCCCCC` | 99 | cane all 8 years (a long ratoon run, or labelling noise) |

The pattern is clear: about 3–4 cane years, one break year (usually fallow, sometimes soybeans), then cane again.

**The picture:**

```python
samp = ever.sample(min(300, len(ever)), random_state=1)
lut = {45: 0, 5: 1, 61: 2}
arr = samp[cols].apply(lambda col: col.map(lambda v: lut.get(v, 3))).to_numpy()
arr = arr[np.lexsort(arr.T[::-1])]
ax.imshow(arr, aspect="auto", cmap=ListedColormap([...]), interpolation="nearest")
```

- **Only 300 random fields:** 5,372 rows would be too thin to see in a figure.
- **Recoding:** each code becomes 0 (cane), 1 (soy), 2 (fallow) or 3 (other), and `imshow` draws the matrix as coloured cells (300 rows × 8 columns).
- **`np.lexsort(arr.T[::-1])`** sorts the rows like words in a dictionary: by the 2018 value, then 2019, and so on. Similar histories end up next to each other, making the diagonal "staircase" of fallow years visible.
- **`interpolation="nearest"`** keeps the cells sharp instead of blurred.

What to see: the staircase. Each block of rows takes its fallow break in a different year, and cane returns afterwards. Farms rotate their fallow fields, so roughly the same number of fields are cane every year (around 4,100–4,200).

### Section 8: The interactive map

```python
win.to_crs(4326)[["CSBID", "CSBACRES"] + cols + ["crop23", "geometry"]].explore(
    column="crop23", categorical=True, cmap="tab10", tiles="Esri.WorldImagery",
    style_kwds={"fillOpacity": 0.45, "weight": 0.6})
```

- **`.explore()`** creates a Leaflet web map, the same technology our final app will use. You can pan, zoom, and click a field to see its attributes.
- **`.to_crs(4326)`:** web maps expect lon/lat (they convert internally to Web Mercator). This is the CRS lesson in action.
- **`tiles="Esri.WorldImagery"`** puts satellite photos underneath. Zoom in and compare the smooth CSB outlines with the real field edges in the photo. That's the clearest way to see the 60 m simplification.
- **Only the 5 km window,** so the notebook stays small: 262 fields, not 5,632.

This is a mini preview of our product's map screen (P-1 and P-2).

### Section 9: Decision rule check

```python
r1 = min(per_year.values()) >= 1000
r2 = med_ha >= 0.5
r3 = bool((p[cols] > 0).all(axis=None))
```

- `(p[cols] > 0).all(axis=None)` asks: is *every* cell in the 8 label columns a real code? `axis=None` means all rows and all columns at once.

Output: all three are True.
- Minimum 3,963 cane fields in a year.
- Median cane field 4.65 ha (~465 pixels).
- Labels in all 8 years.

So CSB is **provisionally adopted** for Iberia. "Provisional" because the final decision is an ADR at Checkpoint R, and S02 still has to check label purity.

---

## 6. The statistics we used

### 6a. Count, sum, share

- **Count:** how many (`len`, `.size`, `.sum()` on True/False).
- **Sum:** a total (cane acres).
- **Share:** count ÷ total. For example, 4,213 cane fields ÷ 5,632 fields = 74.8 % of Iberia's fields were cane in 2023.

### 6b. Mean vs median, and why we used the median

The **mean** is the sum divided by the count. The **median** is the middle value once everything is sorted.

Worked example with 5 fields: 2, 3, 4, 5 and 100 ha (one giant field).

```
 mean   = (2 + 3 + 4 + 5 + 100) / 5 = 22.8 ha   <- pulled up by the giant
 median = middle of [2, 3, 4, 5, 100] = 4 ha    <- the "typical" field
```

Field sizes are **skewed**: many medium fields and a few huge ones. The mean is dragged towards the huge ones; the median isn't. So "typical field size" means the median. The same reasoning applied when we centred the zoom window on the median position.

In formula form, for sorted values $x_{(1)} \le \dots \le x_{(n)}$: the median is $x_{((n+1)/2)}$ for odd $n$, or the average of the two middle values for even $n$.

In code: `series.median()`.

### 6c. Percentiles (quantiles)

The **p-th percentile** is the value below which p % of the data falls. The median is the 50th percentile.

```
 10th percentile of cane field size = 1.97 ha  -> 10 % of cane fields are smaller than 1.97 ha
 90th percentile                    = 11.77 ha -> 90 % are smaller, 10 % are bigger
```

Why report the 10th and 90th as well as the median? The median tells you the middle; the percentiles tell you the **spread**. For us, the small end matters most: the 10th percentile says even small cane fields have about 200 pixels.

In code: `series.quantile([0.1, 0.5, 0.9])`.

### 6d. Histograms and the log scale

A **histogram** splits values into ranges (bins) and counts how many fall in each. It shows the shape of a distribution.

Why a **log scale** on the x-axis? Field sizes run from under 1 ha to hundreds of hectares. On a normal axis, everything below 20 ha squashes into one thin bar at the left. On a log axis, each step is ×10:

```
 linear:  0    250   500   750   1000 ha      (small fields invisible)
 log:     0.01  0.1   1    10   100  1000 ha  (each decade gets equal room)
```

`np.logspace(-2, 3, 60)` makes bins that look equally wide on that log axis.

### 6e. Distributions over a row

`n_cane` (cane years per field, 0–8) is a distribution over fields. Its peak at 6 and 7 is the evidence for the cane cycle. Reading the *shape* of a distribution, rather than one number, is often where the insight is.

### 6f. Sanity checks

The area ratio (median 1.0000) and the missing-label count (0) aren't findings about farming. They are **data-quality checks**. Real projects run many of these before trusting any result. A failed sanity check found early saves a wrong thesis chapter later.

---

## 7. What we found, and why each finding matters

| # | Finding (observation) | Why it matters (interpretation) | Feeds into |
|---|---|---|---|
| 1 | 206,389 fields in Louisiana; 32,373 cane fields in 2023 | The state has plenty of data; we're not data-starved | DQ-01 |
| 2 | Iberia: 3,963–4,213 cane fields every year; labels in all 8 years | Enough to train on some years and test on others (held-out years are the honest test) | DQ-10 splits, Module A |
| 3 | Median cane field 4.65 ha ≈ 465 pixels; none under 0.5 ha | Per-field Sentinel-2 averages will be stable; field size is not a risk here. Pakistan's fields are much smaller, so this is a Stage 2 risk to note | DQ-05, Stage 2 |
| 4 | Area check ratio 1.0000; CRS is equal-area metres | We can trust `CSBACRES` and measure areas directly | all modules |
| 5 | Cane histories peak at 6–7 cane years out of 8; top sequences are 3–4 cane years, then a fallow year | The labels behave like real sugarcane farming, which raises our trust in them. And sugarcane must be modelled as a **multi-year cycle**: the health baseline must ask "which ratoon year is this?", not just "which calendar month?" | DQ-21, H-20 (expected to fail), Module B |
| 6 | The year after a fallow year is (usually) newly planted cane | A **free label**: we can tell plant cane from ratoon cane using the history alone, without extra data. Useful for health baselines and maybe for yield (ratoon yields usually fall each year, still to confirm in the literature) | DQ-21, Module B, Module C |
| 7 | In Iberia's 2023, non-cane is 1,419 fields, and 829 of those are fallow | A cane vs non-cane classifier here mostly learns "growing cane vs bare field", an easy problem. A high score here could **overstate** how good the model is. A harder second parish (Pointe Coupee or St. Landry, with more soybeans and rice) is needed for an honest test | DQ-14, DQ-10, the thesis's honesty |
| 8 | Field outlines are smooth blobs (60 m simplification); fields are "same crop history" areas, not real fields | Our map will show approximate fields. Fine for a prototype; must be stated. Edge pixels may include a neighbour, so S03 should shrink fields slightly inward (a "negative buffer") before averaging pixels | P-1, S03 |
| 9 | The CDL (source of the labels) was made from Landsat **and Sentinel-2** | Circularity confirmed at the source: we'd partly be teaching a model to copy another Sentinel-2 model. Must be in the thesis; makes an independent check (e.g. Di Tommaso 2024's map) more valuable | H-24, rubric criterion 2 |

---

## 8. Corrections and limits (honest list)

1. **`INSIDE_X`/`INSIDE_Y`:** the notebook's column table says "a point guaranteed to lie inside the field". The official definition is **"the center X/Y coordinate of a CSB polygon"**. I'd guessed from the name. For our use (centring a window) it makes no difference, but the notebook text will be corrected.
2. **The `CSBID` structure** (state + edition + number) is my observation from the data, not documented by NASS.
3. **The 0.5 ha / 50-pixel threshold is our own rule of thumb.** Phase R literature should confirm or replace it.
4. **"Majority" labels.** A field labelled cane might be only just over half cane. Not yet measured; that's S02.
5. **The heatmap shows 300 random fields,** not all 5,372. The counts in the tables use all fields.
6. **The parish filter uses the name** (`CNTY == "Iberia"`). Using the code `CNTYFIPS` would be more robust (names can be spelled differently across datasets). Fine here; the real pipeline should use codes.
7. **Iberia was chosen by judgment** (most cane fields, smaller fields), not by a formal rule. Finding 7 suggests adding a second, more mixed parish.
8. **The cane cycle** (plant cane, ratoons, fallow) is standard sugarcane agronomy, but we haven't yet cited a source for Louisiana practice. That's a literature task.

---

## 9. Python and pandas idioms used (quick reference)

| Idiom | Meaning | Example from S01 |
|---|---|---|
| `df[df[col] == x]` | keep rows where the condition is True | cane fields in 2023 |
| `df[[c1, c2]]` | select columns | the attribute preview |
| `series.map(lookup)` | replace values using a dict or Series | code 45 → "Sugarcane" |
| `series.value_counts()` | count each distinct value | crops in Iberia |
| `df.groupby(k).agg(name=(col, fn))` | per-group summaries | cane per parish |
| `(cond).sum()` / `(cond).mean()` | count / share of True | fields under 0.5 ha |
| `df.sum(axis=1)` | sum across a row | cane years per field |
| `df.apply(f, axis=1)` | run `f` on each row | build `CCCFCCCC` strings |
| `np.where(c, a, b)` | vectorised if/else | lump small classes into "Other" |
| `gdf.to_crs(epsg)` | re-project | Albers → lon/lat |
| `gdf.cx[x0:x1, y0:y1]` | select by bounding box | the 5 km window |
| `gdf.explore()` | interactive web map | section 8 |
| `random_state=…` | reproducible randomness | `.sample(..., random_state=0)` |
| `[f"CDL{y}" for y in range(...)]` | list comprehension | the 8 label columns |

---

## 10. Glossary

| Term | Plain meaning |
|---|---|
| CSB | Crop Sequence Boundaries: synthetic field polygons with 8 years of crop history, made by NASS from CDL maps |
| CDL | Cropland Data Layer: a 30 m crop map of the US for each year, made by a classifier from Landsat and Sentinel-2 |
| NASS | National Agricultural Statistics Service (part of USDA) |
| FIPS | US Census codes for states (`22` = Louisiana) and counties |
| Parish | Louisiana's name for a county |
| ASD | Agricultural Statistics District: a group of parishes NASS reports statistics for |
| Edition / window | the 8 years a CSB covers (ours: 2018-2025) |
| Majority label | the class with the most pixels inside a polygon |
| File Geodatabase (`.gdb`) | Esri's folder-based format for GIS data |
| GeoParquet | a fast, compressed, columnar file format for tables with geometry |
| CRS | coordinate reference system: what coordinate numbers mean |
| EPSG code | a standard id for a CRS (4326 = lon/lat; 32615 = UTM zone 15N) |
| Equal-area projection | a flat map where areas stay correct (Albers) |
| MultiPolygon | one feature made of several polygon pieces |
| Plant cane / ratoon | first crop after planting / regrowth from stubble after harvest |
| Fallow | land left unplanted for a season |
| Median / percentile | middle value / value below which p % of the data falls |
| Sanity check | a cheap test that data is self-consistent |
| Spike | a small experiment answering one design question |
| Pre-registration | writing the decision rule before looking at results |
| Circularity | training on labels that came from a similar model on similar data |

---

## 11. Check yourself

1. Why does the CSB have no fields under 0.5 ha? Is that a fact about Louisiana farms?
2. `CDL2023 = 45` for a field. Does that mean the whole field was sugarcane?
3. Why did we read only Louisiana with a `where=` filter instead of loading the national file and then filtering?
4. Why is the median a better "typical field size" than the mean here?
5. What does the 10th percentile of 1.97 ha tell us that the median doesn't?
6. Why did we convert to EPSG:4326 for the interactive map but compute areas in Albers?
7. A field reads `FCCCFCCC`. Which years were plant cane, and which were ratoons?
8. Why might a cane vs non-cane model score very well in Iberia, and why is that a problem for the thesis?
9. The metadata says the CDL uses Sentinel-2. Why does that matter for how we describe our model's accuracy?

---

## 12. Questions and answers

(Your questions go here, with answers, as in B01.)
