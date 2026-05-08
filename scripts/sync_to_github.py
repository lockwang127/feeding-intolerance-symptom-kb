#!/usr/bin/env python3
"""sync_to_github.py — 自动 commit + push 到 GitHub"""
import os, sys, subprocess, json
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT  = os.path.dirname(SCRIPT_DIR)
REMOTE     = os.environ.get("KB_REMOTE", "origin")
BRANCH     = os.environ.get("KB_BRANCH", "main")

def run(cmd, check=True):
    r = subprocess.run(cmd, shell=True, cwd=REPO_ROOT,
                       capture_output=True, text=True)
    if check and r.returncode != 0:
        print(f"❌ {cmd}\n{r.stderr}"); sys.exit(1)
    return r

def main():
    status = run("git status --porcelain", check=False)
    if not status.stdout.strip():
        print("✅ 没有变更需要同步"); return

    meta_path = os.path.join(REPO_ROOT, "data/kb_meta.json")
    if os.path.exists(meta_path):
        meta = json.load(open(meta_path, encoding="utf-8"))
        total = meta.get("total_entries", "?")
        ver   = meta.get("version", "?")
        msg   = f"feat: 喂养不耐受FI知识库更新至 {total} 条 v{ver}"
    else:
        msg = f"chore: FI知识库同步 ({datetime.now().strftime('%Y-%m-%d')})"

    run("git add -A")
    run(f'git commit -m "{msg}"')
    result = run(f"git push {REMOTE} {BRANCH}", check=False)
    if result.returncode == 0:
        print(f"✅ 已同步到 GitHub: {msg}")
    else:
        print(f"⚠️ Push 失败（可能无网络），本地 commit 已创建，可稍后手动 push")

if __name__ == "__main__":
    main()
