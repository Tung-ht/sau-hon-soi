# -*- coding: utf-8 -*-
"""
Studio Quality Linter & Editorial Scorecard
Phân tích văn phong tĩnh (chống văn mẫu AI, lặp từ, nhịp điệu) và quản trị đánh giá biên tập 7 chiều có kiểm định Quality Gate.
"""

import re
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional

from studio.store import read_json, write_json, read_file, append_jsonl, ensure_dir, get_config
from studio.schemas import create_decision_record, validate_review_scorecard

BANNED_AI_CLICHES = [
    {"pattern": r'khóe miệng.*?(?:câu lên|nở nụ cười|nhàn nhạt|tà mị)', "name": "Văn convert: khóe miệng câu lên / tà mị"},
    {"pattern": r'trong (?:đáy )?mắt (?:thoáng qua|xẹt qua|lóe lên).*?(?:tia|vệt)', "name": "Văn convert: trong mắt thoáng qua tia..."},
    {"pattern": r'không khỏi (?:hít|cảm thấy|rùng mình|kinh hãi|bàng hoàng|thán phục)', "name": "Sáo rỗng: không khỏi..."},
    {"pattern": r'bầu không khí.*?(?:đông đặc|ngưng kết|đọng lại)', "name": "Văn convert: bầu không khí đông đặc"},
    {"pattern": r'đồng tử.*?(?:co rút|co lại)', "name": "Văn convert: đồng tử co rút"},
    {"pattern": r'như một minh chứng', "name": "Văn mẫu AI: như một minh chứng"},
    {"pattern": r'bức tranh toàn cảnh', "name": "Văn mẫu AI: bức tranh toàn cảnh"},
    {"pattern": r'chìa khóa then chốt', "name": "Văn mẫu AI: chìa khóa then chốt"},
    {"pattern": r'không thể phủ nhận', "name": "Văn mẫu AI: không thể phủ nhận"},
    {"pattern": r'nâng tầm trải nghiệm', "name": "Văn mẫu AI: nâng tầm trải nghiệm"},
    {"pattern": r'hành trình (?:khám phá|đắm chìm)', "name": "Văn mẫu AI: hành trình đắm chìm/khám phá"},
    {"pattern": r'khí tức.*?(?:khủng bố|lạnh lẽo|áp bức)', "name": "Văn convert: khí tức khủng bố"},
    {"pattern": r'chẳng biết từ lúc nào', "name": "Sáo rỗng: chẳng biết từ lúc nào"},
    {"pattern": r'được (?:xem như|coi như) là', "name": "Cấu trúc dịch: được xem như là"},
    {"pattern": r'đóng vai trò quan trọng', "name": "Cấu trúc dịch: đóng vai trò quan trọng"}
]

def style_lint(base_dir: Path, chapter: Optional[int] = None) -> Dict[str, Any]:
    """Phân tích tĩnh kiểm tra chất lượng văn phong, từ cấm AI, từ lặp và nhịp điệu câu."""
    target_files = []
    chapters_dir = base_dir / "chapters"
    if not chapters_dir.exists():
        return {"error": "Chưa có chương nào được viết để kiểm tra."}
        
    if chapter:
        f = chapters_dir / f"{chapter:02d}.md"
        if f.exists():
            target_files.append((chapter, f))
    else:
        for p in sorted(chapters_dir.glob("*.md")):
            m = re.match(r"^(\d+)\.md$", p.name)
            if m:
                target_files.append((int(m.group(1)), p))
                
    results = []
    total_issues = 0
    
    for ch_num, file_path in target_files:
        text = read_file(file_path)
        lines = text.splitlines()
        words = re.findall(r'\b\w+\b', text.lower())
        total_word_count = len(words)
        
        # 1. Quét từ cấm AI
        cliche_matches = []
        for idx, line in enumerate(lines, 1):
            for rule in BANNED_AI_CLICHES:
                if re.search(rule["pattern"], line, re.IGNORECASE):
                    cliche_matches.append({
                        "line": idx,
                        "rule": rule["name"],
                        "snippet": line.strip()
                    })
                    
        # 2. Thống kê N-gram Repetition (2-grams, 3-grams)
        ngrams = {}
        for i in range(len(words) - 2):
            trigram = " ".join(words[i:i+3])
            if len(trigram) > 8:
                ngrams[trigram] = ngrams.get(trigram, 0) + 1
        
        frequent_repetitions = [
            {"phrase": phrase, "count": count}
            for phrase, count in ngrams.items() if count >= 4
        ]
        
        # 3. Type-Token Ratio (TTR)
        unique_words = len(set(words))
        ttr = round(unique_words / max(1, total_word_count), 3)
        
        # 4. Phân tích độ dài câu (Sentence length)
        sentences = [s.strip() for s in re.split(r'[.!?…\n]+', text) if len(s.strip().split()) > 0]
        sent_lengths = [len(s.split()) for s in sentences]
        avg_sent_len = round(sum(sent_lengths) / max(1, len(sent_lengths)), 1)
        overlong_sentences = [
            {"sentence": s[:80] + "...", "words": len(s.split())}
            for s in sentences if len(s.split()) > 35
        ]
        
        # Tính điểm phong cách (0-100)
        score = 100 - (len(cliche_matches) * 10) - (len(frequent_repetitions) * 5) - (len(overlong_sentences) * 2)
        score = max(0, min(100, score))
        
        total_issues += len(cliche_matches) + len(frequent_repetitions)
        results.append({
            "chapter": ch_num,
            "word_count": total_word_count,
            "style_score": score,
            "metrics": {
                "ttr_vocabulary_variety": ttr,
                "avg_sentence_length": avg_sent_len,
                "total_sentences": len(sentences),
                "overlong_sentences_count": len(overlong_sentences)
            },
            "banned_ai_cliches": cliche_matches,
            "frequent_repetitions": frequent_repetitions[:5]
        })
        
    return {
        "status": "lint_completed",
        "total_chapters_checked": len(results),
        "total_issues_found": total_issues,
        "chapters": results
    }

def save_review_scorecard(
    base_dir: Path,
    chapter: int,
    review_data: Dict[str, Any],
    actor: str = "agent"
) -> Dict[str, Any]:
    """Lưu đánh giá 7 chiều có kiểm định Quality Gate thực tế (Sửa P1)."""
    cfg = get_config(base_dir)
    valid_review = validate_review_scorecard(review_data, quality_gate_mode=cfg.get("quality_gate", "advisory"))
    
    review_file = base_dir / "world" / "reviews" / f"{chapter:02d}.json"
    ensure_dir(review_file.parent)
    write_json(review_file, valid_review)
    
    verdict = valid_review.get("verdict", "accept")
    affected_chapters = valid_review.get("affected_chapters", [])
    
    prog = read_json(base_dir / "meta" / "progress.json", {})
    
    if verdict == "rewrite" or affected_chapters:
        targets = affected_chapters if affected_chapters else [chapter]
        for t in targets:
            if t not in prog.get("pending_rewrites", []):
                prog["pending_rewrites"].append(t)
        prog["pending_rewrites"].sort()
        prog["flow"] = "rewriting"
        prog["rewrite_reason"] = valid_review.get("reason", f"Review chương {chapter} yêu cầu viết lại.")
        write_json(base_dir / "meta" / "progress.json", prog)
        
        dec = create_decision_record(
            action="review_triggered_rewrite",
            actor=actor,
            chapter=chapter,
            reason=prog["rewrite_reason"],
            metadata={"verdict": verdict, "targets": targets, "warnings": valid_review.get("warnings", [])}
        )
        append_jsonl(base_dir / "decisions.jsonl", dec)
        
    return {
        "status": "review_saved",
        "chapter": chapter,
        "verdict": verdict,
        "scores": valid_review["scores"],
        "average_score": valid_review["average_score"],
        "contract_status": valid_review["contract_status"],
        "warnings": valid_review.get("warnings", []),
        "pending_rewrites": prog.get("pending_rewrites", [])
    }
