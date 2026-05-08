#!/usr/bin/env python3
"""test_kb_format.py — 快速校验 kb.json 格式完整性"""
import json, sys, os

KB_PATH = os.path.join(os.path.dirname(__file__), "../../data/kb.json")
REQUIRED = ["head", "relation", "tail", "source", "evidence", "domain"]

def test():
    if not os.path.exists(KB_PATH):
        print(f"❌ 文件不存在: {KB_PATH}")
        sys.exit(1)
    with open(KB_PATH, encoding="utf-8") as f:
        kb = json.load(f)

    errors = []
    for i, item in enumerate(kb):
        missing = [f for f in REQUIRED if not item.get(f)]
        if missing:
            errors.append(f"[{i}] {item.get('head','?')[:30]}: 缺少 {missing}")

    if errors:
        print(f"❌ 发现 {len(errors)} 条不合规记录:")
        for e in errors[:20]: print(f"   {e}")
        sys.exit(1)
    else:
        print(f"✅ 全部 {len(kb)} 条记录格式正确 ✓")

if __name__ == "__main__":
    test()
