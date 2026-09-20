# GitHub Codespaces — Complete Python + Git + GitHub Workflow

This guide covers both ways to work in GitHub Codespaces:
1. Create a Codespace from an existing GitHub repository (already cloned).
2. Clone a repository manually inside a Codespace.

It includes environment setup, code, commits, branches, push/pull, and Pull Request creation.

---

## 0. Prerequisites

You need:
- A GitHub account
- A repository on GitHub (or permission to create one)
- GitHub Codespaces access

Codespaces terminals are generally Linux-based. Commands below use Bash.

---

# PATH A — Start from an Existing GitHub Repository

## 1. Create the Codespace

1. Open your repository on GitHub.
2. Click **Code → Codespaces → Create codespace on main**.
3. Wait for the browser-based VS Code environment to load.
4. Open **Terminal → New Terminal**.

**Important:** The repository is already cloned into the Codespace. Do not run `git clone` or `git init` again for this repository.

Verify:

```bash
pwd
git status
git remote -v
git branch --show-current
```

---

# PATH B — Clone a Repository Manually in a Codespace

Use this if you are in a blank Codespace or need a different repository.

## 2. Clone the Repository

```bash
git clone https://github.com/USERNAME/REPOSITORY.git
cd REPOSITORY
```

Replace `USERNAME` and `REPOSITORY` with the actual GitHub username/organization and repository name.

Verify:

```bash
git status
git remote -v
```

If the repository is private, make sure your GitHub account has access and authenticate when prompted. In a Codespace associated with your GitHub account, authentication is often already available.

---

# 3. Create a Python Virtual Environment

Run from the repository/project folder:

```bash
python --version
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

Your terminal should show `(.venv)` after activation.

If the environment already exists, just activate it:

```bash
source .venv/bin/activate
```

Add this to `.gitignore`:

```gitignore
.venv/
__pycache__/
*.py[cod]
.env
.pytest_cache/
```

Never commit secrets or your real `.env` file.

---

# 4. Create a Simple Python Project

Create files:

```bash
touch main.py requirements.txt README.md .gitignore
```

Put this in `main.py`:

```python
def main():
    print("Hello from GitHub Codespaces!")

if __name__ == "__main__":
    main()
```

Put this in `requirements.txt` if you need a sample dependency:

```text
requests
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Run the program:

```bash
python main.py
```

Expected output:

```text
Hello from GitHub Codespaces!
```

If the project already has a `requirements.txt`, use that file instead of replacing it.

---

# 5. Check Git Configuration

Codespaces usually has Git and repository authentication configured. Check:

```bash
git --version
git config user.name
git config user.email
git remote -v
```

If name/email are missing, set them:

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

Use the email you want associated with your commits.

---

# 6. Make Changes, Commit, and Push

Check current changes:

```bash
git status
git diff
```

Stage and commit:

```bash
git add .
git commit -m "Update project"
```

Push the current branch:

```bash
git push
```

For a newly created branch whose upstream is not set, use:

```bash
git push -u origin BRANCH_NAME
```

Replace `BRANCH_NAME` with the actual branch name.

---

# 7. Recommended Workflow — Feature Branch → Push → Pull Request

Avoid committing directly to `main` when using a branch-based workflow.

## Create a feature branch

```bash
git switch -c feature/my-change
```

Make code changes, then:

```bash
git status
git add .
git commit -m "Add my change"
git push -u origin feature/my-change
```

## Create the Pull Request

### Option A — GitHub website
1. Open the repository on GitHub.
2. Go to **Pull requests → New pull request**.
3. Set **base** to `main`.
4. Set **compare** to `feature/my-change`.
5. Add a title and description.
6. Click **Create pull request**.

### Option B — GitHub CLI (`gh`)

Check whether it is installed:

```bash
gh --version
```

Authenticate if required:

```bash
gh auth login
```

Create the PR:

```bash
gh pr create \
  --base main \
  --head feature/my-change \
  --title "Add my change" \
  --body "Summary of the changes"
```

View it:

```bash
gh pr view --web
```

**A push does not automatically create a Pull Request.** You must create the PR using GitHub or `gh`.

---

# 8. Pull the Latest Changes

Update your local `main` branch:

```bash
git switch main
git pull origin main
```

Update your feature branch with the latest `main`:

```bash
git switch feature/my-change
git fetch origin
git merge origin/main
```

After your Pull Request is merged, sync `main`:

```bash
git switch main
git pull origin main
```

If you have uncommitted changes, commit them or stash them before switching branches/pulling:

```bash
git stash
git pull origin main
git stash pop
```

---

# 9. If You Created a New Local Project in a Blank Codespace

If you started in an empty folder and want to connect it to a new GitHub repository:

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/USERNAME/REPOSITORY.git
git push -u origin main
```

Before running this:
1. Create an **empty** repository on GitHub.
2. Replace the example URL with your repository URL.
3. Do not run `git init` if you cloned a repository or opened a Codespace from an existing repository.

---

# 10. Troubleshooting Commands

## Check branch, status, and remote

```bash
git status
git branch --show-current
git branch -a
git remote -v
```

## `origin` already exists

```bash
git remote set-url origin https://github.com/USERNAME/REPOSITORY.git
```

## Push rejected because remote has newer commits

```bash
git pull --rebase origin main
git push
```

Resolve conflicts if Git reports them, then:

```bash
git add <resolved-file>
git rebase --continue
```

Cancel the rebase if needed:

```bash
git rebase --abort
```

## `gh` command not found

Create the PR using the GitHub website, or install/authenticate GitHub CLI according to GitHub's official Codespaces instructions.

## Python package missing

Make sure the virtual environment is active, then:

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
```

---

# 11. Quick Reference

## Existing repository → Codespace → commit → push

```bash
# Create Codespace from GitHub repository in browser
# Repository is already cloned

git status
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt

git switch -c feature/my-change
# Edit files

git add .
git commit -m "Describe change"
git push -u origin feature/my-change

# Create PR on GitHub website or with gh pr create
```

## Manual clone inside a Codespace

```bash
git clone https://github.com/USERNAME/REPOSITORY.git
cd REPOSITORY

python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt

git switch -c feature/my-change
# Edit files

git add .
git commit -m "Describe change"
git push -u origin feature/my-change
```

## After PR merge

```bash
git switch main
git pull origin main
```

---

## Key Terms

| Command / Term | Purpose |
|---|---|
| `git clone` | Copies a remote repository to your environment |
| `git init` | Starts Git tracking in a new local folder |
| `git add` | Stages changes for a commit |
| `git commit` | Saves a snapshot in local Git history |
| `git push` | Uploads commits to GitHub |
| `git pull` | Fetches and integrates remote changes |
| Branch | Separate line of development |
| Pull Request (PR) | Requests review/merge of a branch on GitHub |
| `.venv` | Isolated Python package environment |

**Remember:** Codespace created from a repository = already cloned. Blank Codespace = clone manually (or initialize a new project).