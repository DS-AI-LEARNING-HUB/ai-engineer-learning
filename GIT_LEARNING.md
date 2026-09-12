# Git Learning Path

A step-by-step companion for learning Git alongside [LEARNING_PATH.md](LEARNING_PATH.md). Work through the modules in order — each builds on the last. Check items off as you actually *do* them (not just read them).

---

## Module 1 — Core Concepts (Done ✅ — recap)

- [x] Git tracks files in three areas: **working directory** (your files) → **staging area** (`git add`) → **commit history** (`git commit`)
- [x] `git init` — turns a folder into a Git repository
- [x] `git config --global user.name` / `user.email` — sets your identity for commits
- [x] `git status` — shows what's changed, staged, or untracked
- [x] `git add <file>` — stages a file (or `git add .` for everything)
- [x] `git commit -m "message"` — saves a permanent snapshot of staged changes
- [x] `git log --oneline` — lists commits (short hash + message), with `HEAD -> branch` marking where you currently are
- [x] `git restore <file>` — discards uncommitted changes to a file, reverting it to the last commit
- [x] `git clean -fdx <files>` — deletes untracked files (careful: irreversible)
- [x] `.gitignore` — tells Git to never track certain files (e.g. `.env`, `.venv`)

**Gotcha learned:** `git log`, `git show`, `git diff` open a **pager** — press `q` to exit back to your normal prompt. It's not frozen, it's waiting for you.

---

## Module 2 — Branches

**Concept:** a branch is an independent line of work. `master` (or `main`) is your default branch. Creating a new branch lets you try things without touching your working code — if it goes wrong, you just delete the branch.

**Commands to practice, in order:**

- [ ] `git branch` — list all branches (the one with `*` is where you are)
- [ ] `git branch feature/test-branch` — create a new branch (doesn't switch to it yet)
- [ ] `git switch feature/test-branch` — move onto that branch (older Git tutorials use `git checkout feature/test-branch` — same effect, `switch` is the newer, clearer command)
- [ ] Make a small edit on this branch (e.g. add a line to README.md), then `git add` + `git commit -m "test commit on branch"`
- [ ] `git switch master` — move back to your main branch. Notice: your edit from the other branch is *not* here — it's isolated to `feature/test-branch`.
- [ ] `git branch -d feature/test-branch` — delete the branch once you're done experimenting (only works if it's already merged, `-D` force-deletes)

**Exercise:** create a branch, make a commit on it, switch back to `master`, confirm the change is "missing" on master (it's not lost, just isolated), then switch back to the branch and confirm it's still there.

---

## Module 3 — Merging

**Concept:** merging brings changes from one branch into another.

- [ ] From `master`, run: `git merge feature/test-branch` — this brings the branch's commits into `master`
- [ ] Run `git log --oneline --graph --all` to *see* the branch history visually (the `--graph` flag draws the branch lines with ASCII art)

**Two kinds of merges you'll encounter:**
1. **Fast-forward** — if `master` hasn't changed since you branched off, Git just moves the pointer forward. No conflict possible.
2. **Merge conflict** — if the *same lines* of the *same file* were changed differently on both branches, Git can't auto-decide and asks you to resolve it manually.

**Practice creating a real conflict (safe, low-stakes):**
- [ ] On `master`, edit line 1 of README.md, commit it.
- [ ] Create a branch from *before* that commit (or just edit the same line differently on another branch), commit there too.
- [ ] Try merging — Git will mark the conflicting file with `<<<<<<<`, `=======`, `>>>>>>>` markers. Open the file, manually decide what the final content should be, delete the markers, then `git add <file>` and `git commit` to complete the merge.
- [ ] `git merge --abort` — good to know: this cancels a merge mid-conflict and returns you to how things were before you started.

---

## Module 4 — Remotes & GitHub

**Concept:** so far everything has been local to your machine. A remote is a copy of the repo hosted elsewhere (GitHub) — this is what makes your work a shareable portfolio and gives you a backup.

- [ ] Create an empty repository on GitHub (no README/license — keep it empty since you already have local history)
- [ ] `git remote add origin <the URL GitHub gives you>` — links your local repo to that GitHub repo, naming it `origin`
- [ ] `git remote -v` — confirms the link, shows the URL for fetch/push
- [ ] `git push -u origin master` — uploads your commits to GitHub. The `-u` remembers this pairing so future pushes can just be `git push`
- [ ] Refresh the GitHub page in your browser — see your commits and files there
- [ ] Make a local change, commit it, `git push` again — confirm it appears on GitHub without needing `-u` this time
- [ ] `git pull` — downloads and merges any changes from GitHub you don't have locally (important once you're working from more than one machine, or collaborating)

**Pushing/pulling a branch other than master (the real-world workflow):**

In practice you rarely push straight to `master`. Instead you work on a feature branch, push *that*, and merge via a Pull Request on GitHub — this is how teams review changes before they land on `master`.

- [ ] Create and switch to a new branch: `git switch -c feature/my-change`
- [ ] Make an edit, `git add`, `git commit -m "..."`
- [ ] Push this branch (not master) to GitHub: `git push -u origin feature/my-change` — notice it's the branch *name* after `origin`, not `master`. This creates a matching branch on GitHub, separate from `master` there too.
- [ ] On GitHub, refresh the repo page — you'll see a prompt like "feature/my-change had recent pushes" with a **"Compare & pull request"** button. Click it, add a description, and open the Pull Request (PR).
- [ ] Merge the PR on GitHub (via the "Merge pull request" button) — this merges `feature/my-change` into `master` *on GitHub*.
- [ ] Back in your terminal: `git switch master` then `git pull` — this downloads the merge that just happened on GitHub, updating your local `master` to match.
- [ ] Optional cleanup: `git branch -d feature/my-change` locally, and delete the branch on GitHub too (there's a button for it right after merging the PR)

**Pulling a specific branch (not your current one):** `git pull origin <branch-name>` — fetches and merges just that branch, useful if you want to grab someone else's branch without switching to it first.

---

## Module 5 — Undoing Things (safely)

You've already used `git restore` for uncommitted changes. Here's the fuller picture:

| Situation | Command |
|---|---|
| Undo uncommitted changes to a file | `git restore <file>` |
| Unstage a file (keep the edit, just remove from staging) | `git restore --staged <file>` |
| See what changed but isn't staged yet | `git diff` |
| See what's staged, about to be committed | `git diff --staged` |
| Fix the message of your *last* commit (not yet pushed) | `git commit --amend -m "new message"` |
| Go back to an old commit, keeping history (safe) | `git revert <commit-hash>` — creates a *new* commit that undoes an old one |
| Move your branch pointer back, rewriting history (risky, avoid on shared/pushed branches) | `git reset --hard <commit-hash>` |

**Rule of thumb:** `restore` and `revert` are safe (non-destructive to history). `reset --hard` and `clean` are destructive — always run `git status`/`git log` first to see what you'd lose.

---

## Quick-Reference Cheat Sheet

```
git status                  # what's changed right now
git add <file>               # stage a file
git add .                    # stage everything
git commit -m "message"      # save a snapshot
git log --oneline            # list commits
git log --oneline --graph --all   # visualize branches
git branch                   # list branches
git switch <branch>          # move to a branch
git switch -c <branch>       # create + move to a branch in one step
git merge <branch>            # merge a branch into your current one
git restore <file>            # discard uncommitted changes
git push                     # upload commits to GitHub
git pull                     # download commits from GitHub
```

## Notes

*(Jot down anything confusing or any command that behaved differently than expected — we'll debug it together.)*
