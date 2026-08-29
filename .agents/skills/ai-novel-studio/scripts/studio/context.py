# -*- coding: utf-8 -*-
"""
Studio Context Assembler
Lắp ráp bộ nhớ 4 tầng: Working Memory, Episodic Memory, Selected Memory và Reference Pack.
"""

from pathlib import Path
from typing import Dict, Any, List, Optional
from studio.store import read_json, read_file, read_jsonl

FORESHADOW_AGING_CHAPTERS = 30
MAX_RECENT_CAST = 15
PREVIOUS_TAIL_CHARS = 800

def get_missing_foundation(base_dir: Path) -> List[str]:
    """Kiểm tra các tệp nền tảng (Foundation) còn thiếu."""
    missing = []
    if not (base_dir / "outlines" / "premise.md").exists():
        missing.append("premise")
    if not (base_dir / "characters" / "characters.json").exists():
        missing.append("characters")
    if not (base_dir / "world" / "world_rules.json").exists():
        missing.append("world_rules")
    if not (base_dir / "outlines" / "outline.json").exists() and not (base_dir / "outlines" / "layered_outline.json").exists():
        missing.append("outline")
    return missing

def get_full_context(base_dir: Path, chapter: int = 0) -> Dict[str, Any]:
    """Lắp ráp đầy đủ gói ngữ cảnh 4 tầng cho chương chỉ định."""
    progress = read_json(base_dir / "meta" / "progress.json", {})
    novel_name = progress.get("novel_name", "Tiểu Thuyết")
    scale = "long" if progress.get("layered", True) else "short"
    
    # 1. Foundation
    premise = read_file(base_dir / "outlines" / "premise.md")
    characters = read_json(base_dir / "characters" / "characters.json", [])
    world_rules = read_json(base_dir / "world" / "world_rules.json", [])
    directives = read_json(base_dir / "meta" / "directives.json", [])
    
    foundation = {
        "novel_name": novel_name,
        "scale": scale,
        "premise": premise,
        "characters": characters,
        "world_rules": world_rules,
        "directives": directives
    }
    
    if chapter <= 0:
        return {
            "tier": "foundation_only",
            "missing_foundation": get_missing_foundation(base_dir),
            "foundation": foundation
        }

    # 2. Working Memory
    plan = read_json(base_dir / "drafts" / f"{chapter:02d}.plan.json", {})
    layered_outline = read_json(base_dir / "outlines" / "layered_outline.json")
    outline = read_json(base_dir / "outlines" / "outline.json")
    
    prev_tail = ""
    if chapter > 1:
        prev_md = base_dir / "chapters" / f"{chapter-1:02d}.md"
        if prev_md.exists():
            full_prev = read_file(prev_md)
            prev_tail = full_prev[-PREVIOUS_TAIL_CHARS:] if len(full_prev) > PREVIOUS_TAIL_CHARS else full_prev

    working_memory = {
        "chapter": chapter,
        "current_plan": plan,
        "previous_chapter_tail": prev_tail,
        "layered_outline": layered_outline if scale == "long" else None,
        "outline": outline if scale != "long" else None,
        "pending_rewrites": progress.get("pending_rewrites", []),
        "rewrite_reason": progress.get("rewrite_reason", "")
    }

    # 3. Episodic Memory
    recent_summaries = []
    start_ch = max(1, chapter - 3)
    for c in range(start_ch, chapter):
        s_file = base_dir / "summaries" / f"{c:02d}.summary.json"
        if s_file.exists():
            s_data = read_json(s_file)
            recent_summaries.append(s_data)

    timeline_all = read_jsonl(base_dir / "world" / "timeline.jsonl")
    recent_timeline = [ev for ev in timeline_all if ev.get("chapter", 0) < chapter][-20:]
    cast_ledger = read_json(base_dir / "characters" / "cast_ledger.json", [])
    relationships = read_json(base_dir / "world" / "relationships.json", {})

    episodic_memory = {
        "recent_chapter_summaries": recent_summaries,
        "recent_timeline_events": recent_timeline,
        "cast_ledger": cast_ledger[:MAX_RECENT_CAST],
        "relationships": relationships
    }

    # 4. Selected Memory (Aging Foreshadows & Open Threads)
    foreshadow_ledger = read_json(base_dir / "world" / "foreshadow_ledger.json", [])
    active_foreshadows = []
    aging_foreshadows = []

    for fs in foreshadow_ledger:
        if fs.get("status") == "active":
            planted = fs.get("planted_at", 0)
            age = chapter - planted
            fs_copy = dict(fs)
            fs_copy["age_chapters"] = age
            active_foreshadows.append(fs_copy)
            if age >= FORESHADOW_AGING_CHAPTERS:
                aging_foreshadows.append(fs_copy)

    selected_memory = {
        "active_foreshadows": active_foreshadows,
        "aging_foreshadows_alert": aging_foreshadows
    }

    return {
        "tier": "full_chapter_context",
        "chapter": chapter,
        "foundation": foundation,
        "working_memory": working_memory,
        "episodic_memory": episodic_memory,
        "selected_memory": selected_memory
    }

def get_open_threads(base_dir: Path) -> List[Dict[str, Any]]:
    """Liệt kê toàn bộ các tuyến truyện và phục bút đang mở kèm số chương tuổi."""
    prog = read_json(base_dir / "meta" / "progress.json", {})
    cur_ch = prog.get("current_chapter", 1)
    
    foreshadow_ledger = read_json(base_dir / "world" / "foreshadow_ledger.json", [])
    open_threads = []
    for fs in foreshadow_ledger:
        if fs.get("status") == "active":
            planted = fs.get("planted_at", 1)
            age = max(0, cur_ch - planted)
            open_threads.append({
                "id": fs.get("id"),
                "description": fs.get("description"),
                "planted_at": planted,
                "advanced_at": fs.get("advanced_at", []),
                "age_chapters": age,
                "is_aging": (age >= FORESHADOW_AGING_CHAPTERS),
                "notes": fs.get("notes", "")
            })
    return open_threads

def get_summaries_hierarchy(base_dir: Path, chapter: Optional[int] = None) -> Dict[str, Any]:
    """Lấy tóm tắt phân cấp theo chương, cung và tập."""
    prog = read_json(base_dir / "meta" / "progress.json", {})
    completed = prog.get("completed_chapters", [])
    
    chapter_sums = []
    for c in completed:
        if chapter is None or c <= chapter:
            s_file = base_dir / "summaries" / f"{c:02d}.summary.json"
            if s_file.exists():
                chapter_sums.append(read_json(s_file))
                
    arcs_dir = base_dir / "summaries" / "arcs"
    arc_sums = []
    if arcs_dir.exists():
        for f in sorted(arcs_dir.glob("*.json")):
            arc_sums.append(read_json(f))
            
    return {
        "chapters_summaries": chapter_sums,
        "arcs_summaries": arc_sums
    }
