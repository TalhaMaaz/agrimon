# WORKING ON MORE THAN ONE MACHINE (laptop, lab PC, cloud)

Fact (Claude Code docs, read Oct 2026): a Claude Code conversation is saved only on the machine where it ran, as a plaintext JSONL file under `~/.claude/projects/`, and is tied to the directory it ran in. Each new session starts with a fresh context window. Auto memory (`~/.claude/projects/<project>/memory/`) is machine-local and is not shared across machines. So two machines can never share one live session. What can be shared is the repository. The design rule is therefore:

**The repository is the memory. A chat is disposable.**

Anything a future session must know goes into a file in Git (STATUS, HANDOFF, lab notebook, ADRs, notes, CLAUDE.md), never only into a conversation or auto memory. If a fresh session on another machine reads those files, it knows everything the old session knew that matters.

## 1. What travels and what does not

| Travels through Git | Stays on each machine (rebuild or copy) |
|---|---|
| Code, configs, docs, Obsidian vault (`docs/`), `CLAUDE.md`, `.claude/` commands, agents, hooks, project `settings.json`, templates, lockfile | Claude Code login and session history (`~/.claude/`), auto memory, `.env` and tokens, `gh` and SSH logins, Python environment (rebuilt from the lockfile), raw and processed data, downloaded imagery caches, model weights |
| `docs/STATUS.md`, `docs/HANDOFF.md`, lab notebook entries, ADRs, experiment records | `.claude/settings.local.json`, `CLAUDE.local.md`, `docs/.obsidian/workspace*.json` (ignored by Git on purpose) |

Large artefacts (per-parcel feature tables, trained weights) are not in Git. They are reproducible from the code, config and a data manifest, and you move them deliberately: `rsync` over SSH between your machines, a Kaggle dataset for GPU notebooks, or a release asset if small and licence-clean. The experiment record says where the artefact lives and its checksum.

## 2. The handoff routine (every time you switch machines)

On the machine you are leaving:
1. Run `/handoff` (it updates `docs/HANDOFF.md`, the lab notebook and STATUS, commits to the current feature branch, and pushes it). Work-in-progress commits on a feature branch are fine; `main` is only changed by PR merges.
2. Check: `git status` is clean and `git log origin/<branch>..HEAD` is empty.

On the machine you are arriving at:
1. `cd ~/agrimon && git fetch --all --prune && git switch <branch> && git pull --ff-only`.
2. If dependencies changed: rebuild the environment from the lockfile (command in README / Makefile).
3. Start `claude`, run `/session-start`. It reads STATUS, HANDOFF and the latest notebook, so the new session knows what the old one knew.
4. Open `docs/` in Obsidian on that machine (same vault, same files).

One machine is "active" at a time. Do not edit the same files on both without pushing between them; Git conflicts are recoverable but waste time.

## 3. Machine-specific settings

- Paths and hardware differ. Keep them out of code: a git-ignored `configs/local.yaml` (data root, cache root, number of workers, GPU yes/no) read by the code, and a committed `configs/local.example.yaml` showing the keys.
- Record in each lab notebook entry and experiment: machine name, CPU/GPU/RAM, data root. The hardware report command output goes into `docs/machines/<name>.md` once per machine.
- Secrets: create `.env` separately on each machine from `.env.example`. Never copy tokens through Git or chat.
- Personal Claude preferences that should apply on every machine and every project belong in `~/.claude/CLAUDE.md` (copy it by hand once). Project rules belong in the repo's `CLAUDE.md`.

## 4. Running Claude Code on the lab PC: options

| Option | How | Pros | Cons |
|---|---|---|---|
| A. Claude Code on the laptop only; the lab PC just runs jobs | Laptop's Claude Code runs `ssh labpc "cd ~/agrimon && make features"` (asks permission); results rsynced back | One session, no duplication; nothing to install on the lab PC except Python and Git | Needs working SSH from the laptop; the laptop must stay on for interactive work; a long job needs `tmux` on the lab PC |
| B. Claude Code installed on the lab PC too | Clone the repo there; use the handoff routine | Works at the lab with local speed; fully independent | Two logins, two histories; only works if installation and internet are allowed there (unknown) |
| C. Claude Code on the lab PC via SSH from the laptop | `ssh labpc`, then `tmux`, then `claude` on the remote | Sessions survive disconnects with `tmux`; one terminal | Needs Claude Code on the lab PC (as B) |
| D. Cloud session (claude.ai/code) | Claude Code in the cloud clones the GitHub repo | Runs while your computers are off | Cannot see lab data or your GPU; counts toward Pro limits; separate from local sessions |

Recommendation (hypothesis; confirm when you know the lab rules): start with A (cheap, safe), add B or C only if the lab allows installing Claude Code and you really need it there.

## 5. Remote Control and teleport (what they do and do not do)

- **Remote Control** lets a browser or the Claude phone app steer a session that keeps running on your own machine. It does not move a session to another computer.
- **Cloud sessions and `--teleport`** pull a cloud session into a terminal. Teleport needs a clean git state, the same repository, and the branch pushed. It does not pull sessions from your other computer.
- Copying `~/.claude/projects/...` JSONL files between machines to `--resume` there is not documented and not recommended here; use the handoff files instead.

## 6. Rules for the agent

1. At the end of every session, and whenever the user says they are switching machines, run the handoff routine. Never leave important state only in the conversation.
2. At the start of every session, `git fetch`, report if the branch is behind or ahead, then read STATUS, HANDOFF and the latest notebook.
3. Do not rely on auto memory for project facts. If something is worth remembering, write it to a repo file in the right place.
4. Ask the user which machine they are on if it is not obvious; record it in the notebook.
5. Never copy secrets, data or weights between machines through Git.
