# 更新规范 — Feeding Intolerance 症状知识库

## 核心原则

### 增量更新，只加不减
- ✅ **只新建批次文件**，不修改已入库的历史文件
- ✅ **按时间命名批次**：`literature_batch_YYYYMMDD.json`
- ✅ 每次更新只整理最近一段时间的新知识
- ❌ **禁止回补旧内容**（不针对过去的文献期间补录）

---

## 版本号递增规则

| 触发条件 | 版本号变更 |
|----------|-----------|
| 新增 <50 条三元组 | patch: x.x.Z+1 |
| 新增 ≥50 条三元组 | minor: x.Y.0 |
| 新增新的Domain分类 | minor: x.Y.0 |
| Schema/架构重构 | major: X.0.0 |

---

## 完整更新流程（约15-30分钟）

```bash
# 1. 新建批次文件（填入最近一段时间的新知识）
#    命名：literature_batch_YYYYMMDD.json 或
#          literature_batch_YYYYMMDD_{topic}.json
vim data/knowledge-graph/literature_batch_$(date +%Y%m%d).json

# 2. 构建知识库（合并所有批次）
python3 scripts/build_kb.py

# 3. 校验格式
python3 scripts/tests/test_kb_format.py

# 4. 同步 GitHub
python3 scripts/sync_to_github.py

# 5. 更新 CHANGELOG.md
```

---

## Domain扩展规范

新增Domain时需满足以下条件之一：
- 有 ≥10 条独立三元组支撑
- 有 ≥1 条I级证据支持的核心概念
- 有明确的临床应用场景

---

## 三元组质量要求

每条三元组必须包含：
- `head`: 实体/概念（主语）
- `relation`: 关系谓词（动词短语）
- `tail`: 实体/值/描述（宾语）
- `source`: 原始出处（PMID / 指南版本 / 试验编号）
- `evidence`: 证据等级
- `domain`: 所属Domain
- `confidence`: 置信度（0.0-1.0）
- `update_date`: YYYY-MM-DD

---

## 隐私与安全

- ❌ 禁止包含患者个人信息
- ❌ 禁止包含医院内部数据（除已脱敏的统计数据）
- ❌ 禁止包含内部项目代号或流水号
- ✅ 所有内容须为原创整理或公开发表文献解读
