#!/usr/bin/env python3
"""
build_kb.py — 喂养不耐受（FI）症状知识库构建脚本
合并所有批次文件 → 去重 → 输出 kb.json + kb_meta.json
"""
import json, os
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(SCRIPT_DIR, "../data/knowledge-graph")
OUT_FILE = os.path.join(SCRIPT_DIR, "../data/kb.json")
VERSION   = "1.0.0"

DOMAIN_RULES = [
    (["定义", "诊断", "ICIF", "GRV", "喂养不耐受", "FI", "评分", "标准"], "定义与诊断标准"),
    (["危险", "风险因素", "上消化道", "腹部手术", "机械通气"], "危险因素"),
    (["I-FABP", "L-FABP", "瓜氨酸", "DAO", "乳酸", "白蛋白", "CRP", "IL", "PCT", "zonulin", "GLP", "标志物", "激素", "胆囊收缩素", "胃动素", "血清", "血浆"], "生物标志物"),
    (["EN", "肠内", "营养", "蛋白质", "热量", "脂肪", "碳水", "红霉素", "甲氧氯普胺", "促动力", "喂养", "输注", "滴注", "配方", "滋养", "补充"], "营养管理"),
    (["死亡率", "结局", "预后", "ICU", "住院", "感染", "谵妄", "器官", "机械通气撤机"], "临床结局"),
    (["ICU", "儿童", "老年", "脓毒", "急性胰腺炎", "恶液质", "克罗恩", "肿瘤", "术后", "创伤", "烧伤", "肥胖", "心衰", "移植", "COVID"], "特殊人群"),
    (["ESPEN", "ASPEN", "SCCM", "ERAS", "指南", "共识", "NCCN", "CSCO", "CSPEN", "NICE", "推荐", "GLIM", "IAP", "RTOG"], "指南推荐"),
    (["监测", "评估", "超声", "血糖", "腹部", "GRV监测", "耐受性"], "监测与评估"),
    (["误吸", "腹泻", "腹胀", "肠鸣音", "肠坏死", "反流", "呕吐", "细菌移位", "VAP", "SIRS", "脓毒", "并发症"], "并发症处理"),
    (["食管癌", "胃癌", "胰十二指肠", "肝切除", "全胃", "胰头", "壶腹", "HIPEC", "放化疗", "SBRT", "射频"], "肿瘤术后管理"),
    (["康复", "经口进食", "出院", "家庭", "随访", "运动", "下床", "过渡"], "康复与长期管理"),
    (["营养支持小组", "NST", "流程", "质量", "改进", "NUTRIC", "NRS", "SOFA", "APACHE", "mNUTRIC", "GLIM", "PG-SGA", "PNI", "评分", "预测"], "预后模型"),
    (["超声", "床旁", "电阻抗", "GLP-2", "电刺激", "针灸", "益生菌", "谷氨酰胺", "ω-3", "鱼油", "英夫利", "FMT", "人参", "中药", "电磁导航", "鼻空肠管", "基因", "微生物", "代谢组"], "新技术"),
    (["经济", "成本", "卫生", "HEN", "间接测热法"], "质量改进"),
    (["PubMed", "来源", "证据"], "证据体系"),
]

def infer_domain(head: str, existing: str) -> str:
    if existing and existing.strip():
        return existing.strip()
    for keywords, domain in DOMAIN_RULES:
        if any(kw in head or kw in str(existing) for kw in keywords):
            return domain
    return "临床治疗"

def normalize(entry: dict) -> dict:
    h = entry.get("head", entry.get("subject", ""))
    base = {
        "head": h,
        "relation": entry.get("relation", entry.get("predicate", "")),
        "tail": entry.get("tail", entry.get("object", "")),
        "source": entry.get("source", ""),
        "evidence": entry.get("evidence", entry.get("evidence_level", "")),
        "domain": infer_domain(h, entry.get("domain", "")),
        "confidence": float(entry.get("confidence", 0.5)),
        "update_date": entry.get("update_date", datetime.now().strftime("%Y-%m-%d")),
    }
    if entry.get("pmid"):
        base["pmid"] = str(entry["pmid"])
    if entry.get("conditions"):
        base["conditions"] = entry["conditions"]
    return base

def build():
    all_entries, seen = [], set()
    stats = {"total": 0, "duplicates": 0, "by_file": {}}

    for fname in sorted(os.listdir(SRC_DIR)):
        if not fname.endswith(".json"):
            continue
        with open(os.path.join(SRC_DIR, fname), encoding="utf-8") as f:
            data = json.load(f)
        added = 0
        for entry in data:
            norm = normalize(entry)
            key = (norm["head"], norm["relation"], norm["tail"])
            if key not in seen:
                seen.add(key); all_entries.append(norm); added += 1
            else:
                stats["duplicates"] += 1
        stats["by_file"][fname] = added
        print(f"  + [{fname}]: {added} 条")

    with open(OUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_entries, f, ensure_ascii=False, indent=2)

    domains = {}
    for e in all_entries:
        d = e.get("domain", "未分类")
        domains[d] = domains.get(d, 0) + 1

    meta = {
        "version": VERSION,
        "update_date": datetime.now().strftime("%Y-%m-%d"),
        "total_entries": len(all_entries),
        "duplicates_removed": stats["duplicates"],
        "source_files": stats["by_file"],
        "domains": domains,
    }
    meta_out = os.path.join(os.path.dirname(OUT_FILE), "kb_meta.json")
    with open(meta_out, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 构建完成: {len(all_entries)} 条 | 去重 {stats['duplicates']} 条")
    print(f"📊 Domain分布：")
    for d, c in sorted(domains.items(), key=lambda x: -x[1]):
        pct = c / len(all_entries) * 100
        bar = "█" * int(pct / 5)
        print(f"   {d:<18s} {c:>4d} ({pct:>5.1f}%) {bar}")

if __name__ == "__main__":
    build()
