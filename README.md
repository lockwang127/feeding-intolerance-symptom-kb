# Feeding Intolerance Symptom Knowledge Base
# 喂养不耐受（Feeding Intolerance）症状知识库

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-orange.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
[![Total Entries](https://img.shields.io/badge/Triplets-296-blue.svg)](data/kb.json)
[![Last Updated](https://img.shields.io/badge/Updated-2026--05--08-green.svg)](data/kb_meta.json)

> **领域定位**：Feeding Intolerance（FI）是重症医学、外科营养和肿瘤学交叉的核心临床综合征。本知识库系统整理FI的定义诊断、危险因素、生物标志物、营养管理策略、临床结局、特殊人群管理及最新指南推荐，为RAG-LLM医疗问答、临床决策支持和医学教育提供结构化知识支撑。

---

## 简介

喂养不耐受（Feeding Intolerance, FI）是重症监护、外科手术和肿瘤患者肠内营养（Enteral Nutrition, EN）治疗中最常见的临床挑战之一。FI不仅导致营养摄入不足、延长ICU住院时间，还与感染并发症、器官功能障碍甚至死亡密切相关。

本知识库旨在：

- 📚 **结构化FI医学知识**：将散在的指南、文献、专家共识整合为机器可读的**知识三元组**（head-relation-tail）
- 🤖 **赋能AI应用**：为RAG-LLM医疗问答系统、多智能体患者管理系统提供可检索、可溯源的知识支撑
- 🔬 **促进科研协作**：系统梳理FI领域的研究空白和前沿方向

---

## 仓库结构

```
feeding-intolerance-symptom-kb/
├── data/
│   ├── kb.json                   # ✅ 合并后的完整知识库（构建产物）
│   ├── kb_meta.json              # 元数据统计
│   └── knowledge-graph/          # 源批次文件
│       ├── literature_batch_20260508.json              # 批次1：核心三元组（220条）
│       └── literature_batch_20260508_supplement.json   # 批次2：补充扩展（76条）
├── scripts/
│   ├── build_kb.py              # 构建脚本
│   ├── sync_to_github.py         # GitHub同步脚本
│   ├── generate_fi_triplets.py   # 三元组生成器（批次1）
│   ├── generate_fi_triplets_2.py# 三元组生成器（批次2）
│   └── tests/
│       └── test_kb_format.py    # 格式校验脚本
├── schemas/
│   └── triplet_schema.json       # JSON Schema定义
├── docs/                         # 文档
├── UPDATE_POLICY.md              # 更新规范
├── CHANGELOG.md                  # 变更日志
└── README.md
```

---

## 知识域分布（15个Domain）

| Domain | 条数 | 占比 | 代表内容 |
|--------|:----:|:----:|---------|
| 营养管理 | 53 | 17.9% | EN启动时机、蛋白质目标、促动力药、配方选择 |
| 特殊人群 | 30 | 10.1% | ICU患者、肿瘤术后、儿童/老年、脓毒症 |
| 生物标志物 | 28 | 9.5% | I-FABP、瓜氨酸、DAO、乳酸、GLP-2 |
| 指南推荐 | 26 | 8.8% | ESPEN 2023、ASPEN-SCCM 2022、ERAS 2023 |
| 定义与诊断标准 | 24 | 8.1% | ESPEN 2012定义、Reintam评分、GRV阈值 |
| 危险因素 | 23 | 7.8% | 腹部手术、机械通气、血管活性药物 |
| 质量改进 | 17 | 5.7% | NST团队、FI流程SOP、EN达标率基准 |
| 新技术 | 17 | 5.7% | 床旁超声、GLP-2类似物、微生物组干预 |
| 监测与评估 | 15 | 5.1% | FI评分、腹部超声、间接测热 |
| 临床结局 | 12 | 4.1% | 死亡率、ICU住院、感染风险 |
| 并发症处理 | 12 | 4.1% | 误吸、腹泻、肠坏死、细菌移位 |
| 预后模型 | 12 | 4.1% | NUTRIC、NRS-2002、GLIM、SOFA |
| 肿瘤术后管理 | 12 | 4.1% | 食管癌/胃癌/胰十二指肠术后EN管理 |
| 康复与长期管理 | 10 | 3.4% | 经口进食过渡、家庭EN、营养随访 |
| 证据体系 | 5 | 1.7% | GRADE系统、ASPEN证据分级 |

---

## 核心内容摘要

### 定义与诊断
- **ESPEN 2012**标准：胃肠道功能紊乱导致EN无法满足机体需求
- **Reintam评分**（0-8分）：腹胀+呕吐+GRV+腹泻综合评估
- **GRV阈值**：传统≥200mL预警，新版指南强调综合判断

### 关键生物标志物
- 肠上皮损伤：**I-FABP**、**L-FABP**、**DAO**
- 肠功能评估：**瓜氨酸**（Cit<13μmol/L提示功能障碍）
- 肠屏障通透性：**D-乳酸**、**zonulin**、**尿L/M比值**

### 一线管理策略
1. **不因低-中度GRV停止EN**（ESPEN/ASPEN强烈推荐）
2. **促动力药**：红霉素（首选，≤7天）或甲氧氯普胺
3. **幽门后喂养**：GRV反复升高时转换鼻空肠管
4. **个体化EN配方**：整蛋白→短肽→氨基酸逐步升级

### 指南核心推荐
- **ESPEN 2023 EN指南**：危重患者24-48h内启动EN
- **ASPEN-SCCM 2022**：GRV>500mL才考虑暂停EN
- **ERAS Society 2023**：多模式围手术期策略减少术后FI
- **中国CSPEN 2022**：FI分级处置SOP

---

## 数据质量体系

### 证据等级标准

| 等级 | 说明 | 典型来源 |
|------|------|---------|
| `I级` | 大样本RCT/系统评价/Meta分析 | TARGET Trial, NUTRICE Trial |
| `I级专家共识` | 权威指南强烈推荐（A类） | ESPEN 2023, ASPEN-SCCM 2022 |
| `II级` | 队列研究、病例对照 | Reintam et al. Intens Care Med |
| `专家共识` | 专家意见/中文指南 | CSPEN 2022, 中国外科营养指南 |

### 知识来源覆盖

| 来源类型 | 代表内容 |
|----------|---------|
| ESPEN/ASPEN/SCCM指南 | 定义标准、EN/PN推荐 |
| ERAS Society指南 | 术后FI预防策略 |
| CSCO/CSPEN中国指南 | 中国实践规范 |
| PubMed临床文献 | 危险因素、生物标志物 |
| ClinicalTrials.gov | 新型干预研究 |

---

## 快速开始

### 本地构建知识库

```bash
# 克隆仓库
git clone git@github.com:lockwang127/feeding-intolerance-symptom-kb.git
cd feeding-intolerance-symptom-kb

# 构建知识库（合并批次文件）
python3 scripts/build_kb.py

# 校验格式
python3 scripts/tests/test_kb_format.py

# 同步到GitHub
python3 scripts/sync_to_github.py
```

### RAG向量数据库入库（示例）

```python
import json
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("BAAI/bge-large-zh-v1.5")
client = QdrantClient("localhost", port=6333)

with open("data/kb.json", encoding="utf-8") as f:
    kb = json.load(f)

texts = [f"{item['head']} {item['relation']} {item['tail']}" for item in kb]
vectors = model.encode(texts, batch_size=64, show_progress_bar=True)

client.upload_collection(
    collection_name="feeding_intolerance_symptom_kb",
    vectors=vectors.tolist(),
    payload=kb,
)
print(f"✅ 已入库 {len(kb)} 条FI知识三元组")
```

---

## 许可证

- **内容数据**（data/knowledge-graph/、data/kb.json）：[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)
- **代码脚本**（scripts/、schemas/）：[MIT License](./LICENSE)

> ⚠️ 本知识库仅供**学术研究和公益医学知识共享**，不可用于商业用途。

---

## 引用本知识库

```
胖子. 喂养不耐受（Feeding Intolerance）症状知识库 v1.4.0.
GitHub: https://github.com/lockwang127/feeding-intolerance-symptom-kb
更新日期: 2026-05-08
访问日期: [请填写]
```

---

*本知识库由胖子构建维护，2026-05-08 初始化。*
