# PLATFORM AND COMPUTE

Facts here were read from official pages during kit preparation unless marked UNVERIFIED. Re-check anything that affects cost, licence or a startup, because terms change.

## 1. Machines

| Machine | Spec (as told by the user) | Use for | Not for |
|---|---|---|---|
| Laptop | RTX 3060 Laptop GPU, 6 GB VRAM, 16 GB RAM, Ubuntu | Development, tests, small and medium model training (LightGBM, TempCNN, small attention), notebooks, web app | Large parallel extraction, models needing more than about 5 GB VRAM |
| Lab PC | No GPU, large RAM, large SSD | Heavy ETL: STAC streaming, zonal statistics, large parquet work, CPU gradient boosting | Deep model training |
| Cloud notebooks (Kaggle, Colab) | Free tiers, limited sessions | GPU training when the laptop is slow; one-off experiments | Anything needing persistent disk or long unattended jobs. Exact current GPU types and weekly quotas: UNVERIFIED, check the Kaggle and Colab pages |
| Google Earth Engine | Server-side processing | Bulk extraction of time series across many fields | Final product code for a startup unless licensing is settled (section 2) |
| Google Cloud (user says allowed) | Pay-as-you-go or credits | Only if free options are not enough; costs money, so ask first | Default path |

Lab PC access (user: reachable remotely): use SSH with key authentication and `tmux` so long jobs survive disconnects; keep code in Git (clone on the lab PC, pull before runs); keep large data and caches on the lab PC and sync only small outputs (per-parcel feature parquet, metrics) back with `rsync`; put machine-specific paths in a git-ignored local config. Ask the user about the lab's network and security rules before opening any tunnel, and never store credentials in the repo. Whether Claude Code can be installed on the lab PC is unknown: ask.

Kaggle and Colab (user has both): Kaggle datasets are a convenient way to hand a feature table to a GPU notebook; sessions are time-limited and disk is ephemeral, so write results back as small files. Exact current GPU types and quotas remain unverified.

Claude plan: Claude Pro. Long agentic sessions use the allowance quickly; I did not verify current Pro limits for Claude Code (check support.claude.com). Keep sessions short and focused, use /session-end often, avoid running subagents needlessly, and do heavy compute outside Claude (the lab PC and Kaggle run the jobs; Claude writes and reviews code).

Rules: configs are hardware-agnostic; each experiment records where it ran; the agent runs a hardware report on the laptop and asks the user to run it on the lab PC; long jobs are chunked and resumable.

6 GB VRAM guidance: TempCNN and LightGBM fit comfortably; use mixed precision, modest batch sizes and gradient accumulation; a small Transformer on per-parcel series (hundreds of thousands of short sequences) is feasible; per-pixel image Transformers or large segmentation models are not the plan.

## 2. Google Earth Engine (read from developers.google.com/earth-engine/guides/noncommercial_tiers)

- Noncommercial projects use tiers, with quotas per month per project, reset on the first of each month: Community 150 EECU-hours (default), Contributor 1,000 EECU-hours (needs a billing account; noncommercial Earth Engine use not charged; intended for graduate students, nonprofits and researchers), Partner 100,000 EECU-hours (separate application, climate and nature focus).
- Beyond the quota a project enters restricted mode (lower concurrency and throughput), not a hard cutoff.
- Projects must be verified as noncommercial and re-verify every year. Using several accounts or projects to dodge limits violates the terms.
- A project can be registered as commercial and is then billed. The page I read did not define what counts as commercial; it linked to separate eligibility criteria which I could not read.
- User status (Oct 2026): the user already has a Google Earth Engine noncommercial account set up and uses it only for university work. The user intends to buy a commercial licence legally when the startup begins. Keep this boundary clean: FYP work only in the noncommercial project; no startup, client or paid work in it; do not reuse the noncommercial project for the startup; re-verify noncommercial status each year. Whether a given use is eligible is decided by Google's eligibility criteria, which the agent could not read; the user should read them once and the agent should not claim legal certainty.
- Design rule: GEE is an optional extraction backend behind an interface (STAC/Planetary Computer is the default), so moving to a commercial or STAC-only setup later is a configuration change, not a rewrite. Record this in an ADR.
- Implication for the student phase: an FYP is academic and the Community tier is probably enough for extraction at this scale. Implication for the later startup: do not build the product on the noncommercial tier. Treat GEE as a prototyping and learning tool, and make the production plan independent of it (STAC plus open code, or paid GEE). The agent writes this into an ADR.

## 3. Satellite data access

- Preferred: Sentinel-2 L2A through STAC. Microsoft Planetary Computer is the first choice; AWS Earth Search is the fallback. The Planetary Computer overview page I fetched was an empty app shell and said nothing about limits or terms, so its terms and any rate limits are UNVERIFIED. The agent must read the Planetary Computer data catalogue docs and terms, test an actual query, and record findings before relying on it.
- Stream imagery, cache only per-parcel features (CLAUDE.md rule 9).
- Sentinel-1 radar through the same catalogues (verify collection IDs by querying).

## 4. GitHub plan (read from docs.github.com plans page)

- GitHub Free for personal accounts: unlimited public repositories with the full feature set; unlimited private repositories with a limited feature set. The page I read listed protected branches only under Pro for private repositories, so rulesets and branch protection on a free private repo are UNVERIFIED and probably unavailable.
- Pages on Free: public repositories only.
- Actions: 2,000 minutes per month on Free; hosted runners are free in public repositories.
- Dependabot alerts included. Codespaces: 120 core-hours and 15 GB per month on Free. Packages: 500 MB.
- Projects, Discussions and code scanning were not covered by that page. For public repositories GitHub generally offers them (UNVERIFIED here; the agent checks the Settings page of the real repo).
- GitHub Student Developer Pack: the user does not have it. Plan on free features only.

Recommendation (flagged as a trade-off): make the repository PUBLIC if the university allows it, because it unlocks the full feature set for free and doubles as a portfolio. Cost: code and docs become visible; never commit data, credentials or personal information; check the university's rules about publishing FYP work and about plagiarism-detection. If it must be private, the workflow degrades gracefully (see GITHUB_WORKFLOW.md section 9).

## 5. Disk budget

The 60 GB default was lifted by the user on 2026-10-27: the laptop has plenty of space, downloaded datasets are kept (not deleted after clipping), and disk use is logged in STATUS. Streaming per-parcel features (rule 9) still applies to imagery. The lab PC may take larger caches (record paths in a config, never in code). Brazil-Crop is about 10 GB mostly photos: download only vector files unless photos are needed.
