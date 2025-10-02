# backdate_commits.py
# Creates 5–10 backdated empty commits per day from 2024-10-02 to 2025-09-29.
# Run inside your PRIVATE repo (e.g., in GitHub Codespaces terminal):
#   python backdate_commits.py
# It will also push at the end (set PUSH=False to skip).

import os
import random
import subprocess
from datetime import datetime, timedelta

# -------------------- CONFIG --------------------
START_DATE = datetime(2024, 10, 1)   # <-- change to Oct 1, 2024
END_DATE   = datetime(2024, 11, 30)   # <-- change to May 23, 2025
MIN_COMMITS_PER_DAY = 5
MAX_COMMITS_PER_DAY = 7
DAY_START_HOUR = 10   # commits between 10:00...
DAY_END_HOUR   = 23   # ...and 18:00 (local time in Codespaces = UTC)
PUSH = True           # push to origin at the end
CHECKPOINT_FILE = ".backdate_checkpoint"  # for resume-safety
# ------------------------------------------------

def run(cmd, env=None, check=True):
    subprocess.run(cmd, check=check, env=env, text=True)

def ensure_git_identity():
    # Must match a verified GitHub email, otherwise contributions won't show
    name = subprocess.run(["git", "config", "--get", "user.name"], capture_output=True, text=True).stdout.strip()
    email = subprocess.run(["git", "config", "--get", "user.email"], capture_output=True, text=True).stdout.strip()
    if not name or not email:
        raise SystemExit("❌ Set git identity first:\n  git config user.name \"Your Name\"\n  git config user.email \"your-verified-email@example.com\"")

def read_checkpoint():
    if os.path.exists(CHECKPOINT_FILE):
        s = open(CHECKPOINT_FILE, "r", encoding="utf-8").read().strip()
        try:
            return datetime.strptime(s, "%Y-%m-%d")
        except Exception:
            return None
    return None

def write_checkpoint(d: datetime):
    with open(CHECKPOINT_FILE, "w", encoding="utf-8") as f:
        f.write(d.strftime("%Y-%m-%d"))

def daterange(start, end):
    cur = start
    while cur <= end:
        yield cur
        cur += timedelta(days=1)

def random_times_for_day(day, n):
    # pick n random seconds in [DAY_START_HOUR, DAY_END_HOUR)
    start_sec = DAY_START_HOUR * 3600
    end_sec   = DAY_END_HOUR   * 3600
    # if the window is small and n is large, allow duplicates then sort
    seconds = [random.randrange(start_sec, end_sec) for _ in range(n)]
    seconds.sort()
    for s in seconds:
        h = s // 3600
        m = (s % 3600) // 60
        sec = s % 60
        yield day.replace(hour=h, minute=m, second=sec, microsecond=0)

def iso(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%S")

def make_empty_commit_at(dtobj: datetime):
    env = os.environ.copy()
    ts = iso(dtobj)
    env["GIT_AUTHOR_DATE"] = ts
    env["GIT_COMMITTER_DATE"] = ts
    # --allow-empty so the repo stays tiny
    run(["git", "commit", "--allow-empty", "-m", f"Backdated commit {ts}"], env=env)

def main():
    ensure_git_identity()

    # Resume support
    resume_from = read_checkpoint()
    start = START_DATE
    if resume_from and resume_from >= START_DATE and resume_from <= END_DATE:
        # continue from the day AFTER the checkpoint
        start = resume_from + timedelta(days=1)

    total = 0
    for day in daterange(start, END_DATE):
        n = random.randint(MIN_COMMITS_PER_DAY, MAX_COMMITS_PER_DAY)
        for t in random_times_for_day(day, n):
            make_empty_commit_at(t)
            total += 1
        write_checkpoint(day)

    # Push once at the end
    if PUSH:
        try:
            # Rebase in case the remote moved (rare in a private solo repo)
            run(["git", "pull", "--rebase"])
        except subprocess.CalledProcessError:
            # If there's nothing to pull or rebase fails, continue to push anyway
            pass
        run(["git", "push", "origin", "HEAD"])

    # Cleanup checkpoint if finished
    if os.path.exists(CHECKPOINT_FILE):
        os.remove(CHECKPOINT_FILE)

    print(f"✅ Done. Created {total} commits between {START_DATE.date()} and {END_DATE.date()}.")
    print("   If some days are missing squares, give GitHub a few minutes to refresh your graph.")
    print("   Make sure 'Include private contributions' is enabled in your GitHub profile settings.")

if __name__ == "__main__":
    main()
