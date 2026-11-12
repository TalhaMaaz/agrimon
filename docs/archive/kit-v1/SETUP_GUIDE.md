# SETUP GUIDE: from zero to your first Claude Code session

For: Talha, Ubuntu, first time with Claude Code and Obsidian. Read Part 1 first (10 minutes). Then follow Part 2 in order. Each step says what it does, the command, and how to check that it worked.

Assumptions I made (correct me if wrong): you use a normal Ubuntu desktop with a terminal; you have a GitHub account (if not, create one at github.com first); you have the Claude Pro plan; you have sudo rights; you will work on the laptop (the lab PC comes later). Everything marked UNTESTED was not run by me in a real Claude Code session.

---

## Part 1: How the pieces fit together

```
  YOU
   |  talk to
   v
 +-------------+   reads/writes files     +---------------------------+
 | Claude Code |------------------------->|  ~/agrimon  (git repo)    |
 | (terminal)  |<-------------------------|   CLAUDE.md  .claude/     |
 +-------------+   runs git, gh, python   |   .github/  src/  docs/   |
        |                                  +------+-------------+------+
        | uses your                               |             |
        v logged-in tools                         |             | you open docs/
 +-------------+      push / pull         +-------v-----+  +----v----------+
 | git + gh    |<------------------------>|  GitHub     |  |  Obsidian     |
 | (on laptop) |   issues, PRs, CI        |  (cloud)    |  |  vault = docs/|
 +-------------+                          +-------------+  +---------------+
```

- **The repository** (`~/agrimon`) is just a folder of files tracked by Git. Everything lives in it: code, notes, the kit.
- **Claude Code** is a program you start in a terminal inside that folder. It reads `CLAUDE.md` (the rules) automatically, edits files, and runs commands such as `git` and `gh` on your behalf. It asks permission for risky actions.
- **Git** records every change as a commit. **GitHub** stores a copy online and adds issues, pull requests (PRs), automated checks (CI) and releases.
- **Obsidian** is a notes app that opens a folder of Markdown files. There is NO special link between Obsidian and Claude Code. They share the same files: Claude Code writes notes into `docs/`, and you read and navigate them in Obsidian. Git is the history and the sync.
- **The kit** is a set of instruction files and settings (rules, commands, hooks, templates) that tell Claude Code how to work with you. You copy it into the repository once.

What the kit's files do:

| File or folder | What it does | When it matters |
|---|---|---|
| `CLAUDE.md` | Short always-on rules Claude Code reads every session | Every session |
| `docs/agent/*.md` | Detailed protocols (teaching, research, GitHub, modules) Claude reads when needed | Claude reads them; you rarely need to |
| `.claude/commands/` | Slash commands you type: `/session-start`, `/lit-review`, `/phase-brief`, ... | Daily |
| `.claude/agents/` | Specialist helpers (reviewer, dataset-scout, examiner) Claude can call | Claude uses them |
| `.claude/hooks/` + `settings.json` | Safety guards: stop pushes to `main`, merges, commits of data or secrets | Automatic |
| `.github/` | Issue forms, PR template, automated checks, Dependabot | Once the repo is on GitHub |
| `docs/` | Your Obsidian vault: MAP, notes, ADRs, thesis drafts | Daily |
| `scripts/bootstrap_github.sh` | Creates labels, milestones, rules, first issues on GitHub | Once |

---

## Part 2: Setup, step by step

### Step 1. Install basic tools

```bash
sudo apt update
sudo apt install -y git curl unzip gnupg
git --version
```
Check: `git --version` prints a version.

### Step 2. Tell Git who you are

Use the same email as your GitHub account (or the private "noreply" address GitHub shows in Settings, Emails, if you want to hide your real email).

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git config --global init.defaultBranch main
git config --global --list
```
Check: the list shows your name, email and `init.defaultBranch=main`.

### Step 3. Install the GitHub CLI (`gh`) and log in

`gh` lets Claude Code (and you) create repos, issues and PRs from the terminal. Use the official GitHub instructions for Debian/Ubuntu (the Ubuntu-packaged `gh` can be old and broken, per GitHub's own page): open https://github.com/cli/cli/blob/trunk/docs/install_linux.md, copy the command under "Debian ... Recommended (Official)", run it, then:

```bash
gh --version
gh auth login
```
Choose: GitHub.com, then HTTPS, then "Login with a web browser", and follow the code in the browser. Then:

```bash
gh auth status
```
Check: it says you are logged in to github.com as your username. This login is on YOUR laptop. Claude Code uses it, so there is nothing to "link" inside Claude Code. (The linking problem I hit earlier was only in my own cloud session.)

### Step 4. Install Claude Code and log in

```bash
curl -fsSL https://claude.ai/install.sh | bash
```
Open a NEW terminal window, then:

```bash
claude --version
claude doctor
```
Check: a version number prints; `claude doctor` reports no errors. If `claude` is "not found", the install folder (`~/.local/bin`) is not on your PATH; see https://code.claude.com/docs/en/troubleshoot-install. You log in the first time you run `claude` (Step 8) with your Claude Pro account. Native installs update themselves.

### Step 5. Install Obsidian

Download the `.deb` from https://obsidian.md/download (Linux, "Deb"). Then, from the folder where it downloaded:

```bash
sudo apt install ./obsidian_*_amd64.deb
```
(Alternatives listed on the download page: AppImage, Snap, Flatpak.) Start Obsidian from the application menu. You do not need an Obsidian account for local notes, as far as I know.

### Step 6. Create the GitHub repository and put the kit in it

Pick the repository name (suggestion: `agrimon`; it is a working name). Public is recommended: it unlocks the full free GitHub feature set.

```bash
cd ~
gh repo create agrimon --public --clone --description "Satellite crop intelligence: classification, health monitoring (FYP)"
cd agrimon
```
Now copy the kit in. Replace the path to the zip if it is elsewhere. The trailing `/.` matters: it also copies hidden folders like `.claude` and `.github`.

```bash
mkdir -p ~/kit_tmp && unzip -q ~/Downloads/agrimon_claude_code_kit_v2.zip -d ~/kit_tmp
cp -a ~/kit_tmp/claude_code_kit/. ~/agrimon/
ls -a ~/agrimon
```
Check: you see `.claude`, `.github`, `.devcontainer`, `docs`, `scripts`, `CLAUDE.md`, `START_HERE.md`, this guide.

Replace the placeholders with your GitHub username (example uses `yourname`):

```bash
cd ~/agrimon
sed -i 's#OWNER/REPO#yourname/agrimon#g; s#@OWNER#@yourname#g' .github/CODEOWNERS .github/ISSUE_TEMPLATE/config.yml
grep -rn "OWNER" .github || echo "placeholders replaced"
```

Make the hooks executable and make the first commit straight to `main` (an empty repo needs one; the protections come after):

```bash
chmod +x .claude/hooks/*.py scripts/bootstrap_github.sh
git add -A
git status
git commit -m "chore: import project kit"
git push -u origin main
```
Check: the files appear on github.com/yourname/agrimon. The hooks only guard Claude Code, not your own terminal, so this first push works. (Choose a code licence later with Claude Code; GitHub can add it through a PR.)

### Step 7. Open the vault in Obsidian

1. Start Obsidian, click "Open folder as vault", and choose `~/agrimon/docs`.
2. If Obsidian asks about trusting the vault's author or enabling plugins, only core plugins are used; you can say yes or "restricted mode".
3. Settings, Files and links: turn OFF "Use [[Wikilinks]]". Turn ON "Automatically update internal links". (My shipped config tries to set this; confirm it. UNTESTED.)
4. Open `learning/MAP.md` and pin the tab. Open `learning/MAP.canvas` to see the visual map. Read `learning/OBSIDIAN_GUIDE.md`.

Check: the file explorer on the left shows `agent`, `learning`, `_templates`; MAP.md displays; the canvas shows boxes with arrows.

Rule of thumb: Claude Code writes the notes; you read them in Obsidian and write your own only in `learning/my_understanding/`. Do not edit the same file in Obsidian and Claude Code at the same time. Before a session run `git pull`; at the end Claude commits on a branch.

### Step 8. First Claude Code session

```bash
cd ~/agrimon
claude
```
First time: it opens a browser to log in with your Claude Pro account, and asks whether you trust the folder (say yes: it is your project). Then inside Claude Code:

1. Type `/help` to see commands. Type `/` to see the kit's commands (`/session-start`, `/lit-review`, `/phase-brief`, `/session-end`, `/weekly-review`, `/teach-back`, `/viva-drill`, `/open-pr`).
2. Type `/hooks` and `/agents` to confirm the safety hooks and the three helpers (reviewer, dataset-scout, examiner) were loaded. If they are missing, exit (`/exit`) and run `claude` again once. UNTESTED.
3. Type `/permissions` to see what is allowed, asked, or denied. Do not use any "skip permissions" mode; it would defeat the safety rules.
4. Paste the first message from `START_HERE.md`:

> Read CLAUDE.md and every file in docs/agent/. Treat the architecture in the kit as hypotheses. Start with Phase R: give me a Phase R Brief (design questions, research plan, first papers to read, assumptions, clarifying questions).

Claude should answer with assumptions first and questions for you. Answer them. It will wait for your "go" before doing the work.

### Step 9. Apply the GitHub rules and seed issues

Do this after Claude Code has created the first real files, or right away if you prefer. In Claude Code, say:

> Read scripts/bootstrap_github.sh and explain each command to me. Then, after I say go, run it for yourname/agrimon.

What it creates: labels, milestones, the protection rules for `main` (PR required, no force pushes, linear history, a required check named `ci`), and a few starter issues. Notes:
- The `ci` check passes on an empty project because the Python steps are skipped until `pyproject.toml` exists.
- After this, direct pushes to `main` are blocked: all changes go through a branch and a PR. That is intended.
- Rulesets, Pages, CodeQL and secret scanning are free on public repos. Some Settings toggles (Discussions, secret scanning, push protection, Dependabot alerts, private vulnerability reporting, Pages source = GitHub Actions) are switched in the repository's Settings page; Claude Code can guide you or call `gh api` (it will ask permission first).
- CodeQL may report an error until the repo contains Python or JavaScript code. Dependabot may complain about a missing `/apps/web` folder until it exists. These are not required checks.

### Step 10. Your first pull request (practice the loop)

Ask Claude Code: "Create an issue for X, a branch, make the change, run `/open-pr`." Then in your browser: open the PR on GitHub, read "Files changed" line by line, wait for the green check, and click "Squash and merge" yourself. Claude Code is not allowed to merge. After the merge: `git switch main && git pull`.

---

## Part 3: Your daily loop

```
 1. cd ~/agrimon && git pull        (get the latest)
 2. open Obsidian on docs/          (read MAP.md: "Right now")
 3. claude                          then /session-start
 4. work with Claude Code           (it teaches, builds on a branch)
 5. /open-pr                        (draft PR with the template)
 6. you review + merge on GitHub    (read the diff!)
 7. /session-end                    (notebook, STATUS, ledger)
 8. weekly: /weekly-review          fortnightly: /viva-drill <topic>
```

Using Claude Pro well: Pro has usage limits (I did not verify the current numbers; see support.claude.com). Keep sessions focused on one task, end them with `/session-end`, start a new session for a new topic, and avoid asking for huge multi-hour jobs in one go. Heavy compute runs on your laptop, the lab PC or Kaggle, not inside Claude's own allowance. Use `/clear` between unrelated tasks and `/resume` to return to an old conversation.

## Part 3b: Working on two machines (laptop now, lab PC later)

Claude Code sessions do not sync between computers: a conversation is saved only on the machine where it ran. The fix is that the repository is the shared memory. Before leaving a machine run `/handoff`; on the other machine run `git fetch --all --prune`, `git switch <branch>`, `git pull --ff-only`, rebuild the environment from the lockfile, start `claude`, and run `/session-start`. Full details, what travels and what does not, and the options for the lab PC are in `docs/agent/MULTI_MACHINE.md`.

## Part 4: Troubleshooting

| Symptom | Likely cause and fix |
|---|---|
| `claude: command not found` | New terminal not opened, or PATH. See Claude Code troubleshooting page |
| Hooks seem inactive | Run `/hooks`; restart `claude`; check `python3` exists (`python3 --version`) |
| Slash commands missing | Are you inside `~/agrimon`? `ls .claude/commands` |
| `gh` says not logged in | `gh auth login` again |
| Push rejected to `main` | That is the protection rule. Use a branch and a PR |
| Commit blocked on `main` by a hook | Run `git switch -c feat/<issue>-<slug>` first |
| Hook blocked a commit with data files | Unstage them (`git restore --staged <file>`); data stays out of Git |
| Obsidian shows `[[` links or broken links | Turn off Wikilinks; check the vault is `docs/`, not the repo root |
| CI red on a PR | Open the PR, click Details, read the log; ask Claude Code to fix on the same branch |

## Part 5: What to prepare before Phase R ends

- Your thesis deadline, defence date, weekly hours, department rubric, Word template.
- Code licence choice (MIT or Apache-2.0 are common; ask Claude Code to explain the difference).
- Lab PC details (SSH access, hardware report, network rules).
- Whether Claude Code can be installed on the lab PC.

## Part 6: Safety rules to remember

1. Never paste passwords, tokens or API keys into the chat or into files. Use `.env` (ignored by Git).
2. Never commit data, satellite images or model weights.
3. You merge; Claude Code does not.
4. If a command Claude Code wants to run looks strange, say no and ask why.
5. The university requires that you understand everything built. If you cannot explain a diff, do not merge it; ask for a walkthrough or run `/teach-back`.
