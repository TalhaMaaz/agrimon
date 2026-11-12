# Contributing

This is a solo final-year project that follows a professional workflow on purpose.

1. Every change starts as an issue with acceptance criteria.
2. Branch from `main` with the name `type/issue-slug`, for example `feat/42-tempcnn`.
3. Use Conventional Commits for commits and for the PR title.
4. Open a draft pull request early using the template; mark it ready when `make check` and CI pass.
5. The maintainer reviews and squash-merges. Nobody merges their own unreviewed work, including AI assistants.
6. Never commit data, rasters, model weights, credentials or `.env` files.
7. Update the lab notebook, `docs/STATUS.md` and any affected ADR in the same PR.

Setup and commands are in `README.md`. The full process is in `docs/agent/GITHUB_WORKFLOW.md`.
