# 🔄 Backdate Commits Generator

This script creates **backdated empty commits** in any Git repository. It’s meant for personal/private use — for example, to test contribution graphs or keep an internal log of work done across specific dates.

---

## 🚀 How to Use

### 1. Open Your Private Repo
Use [GitHub Codespaces](https://github.com/features/codespaces) or clone your private repo locally and open a terminal in the project folder.

### 2. Configure Git Identity
Your commits must use the same name and a **verified email** from your GitHub account:

git config user.name "Your Name"  
git config user.email "your-verified-email@example.com"

### 3. Adjust Script Settings
Edit the top of `backdate_commits.py` to set your desired date range and commit frequency:

START_DATE = datetime(2024, 10, 1)  
END_DATE   = datetime(2024, 11, 30)  
MIN_COMMITS_PER_DAY = 5  
MAX_COMMITS_PER_DAY = 7  
DAY_START_HOUR = 10  
DAY_END_HOUR   = 23  
PUSH = True  

- **START_DATE / END_DATE** → first and last day of commits  
- **MIN/MAX_COMMITS_PER_DAY** → number of commits per day  
- **DAY_START/END_HOUR** → hours between which commits will be timestamped  
- **PUSH** → set `True` to push automatically when done  

### 4. Run the Script
Run the Python file from the repo root:

python backdate_commits.py

The script will:
- Create commits for each day in the chosen range
- Randomize commit times daily
- Push them to the default branch (usually `main`)

When it finishes you’ll see:

✅ Done. Created X commits between YYYY-MM-DD and YYYY-MM-DD.

---

## ✨ Features

- Creates backdated commits automatically  
- Randomizes commit times to look natural  
- Resumes if interrupted (checkpoint file)  
- Pushes everything at the end  
- Keeps repo lightweight with empty commits  

---

## ⚡ After Running

- Wait ~30 minutes for GitHub’s graph to refresh.  
- Make sure “Include private contributions on my profile” is enabled:
  GitHub → Settings → Profile → Contributions & activity → turn ON **Include private contributions**.

---

## ⚠️ Note

This tool is for your own private repositories. Don’t use it to mislead about your public contribution history. GitHub discourages creating artificial activity.
