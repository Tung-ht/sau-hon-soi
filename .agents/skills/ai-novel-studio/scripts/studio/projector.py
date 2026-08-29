# -*- coding: utf-8 -*-
"""
Studio Projection Engine
Dựng lại toàn bộ bản chiếu (Timeline, Phục Bút, Nhân Vật, Dàn Ý, Tóm Tắt, Trạng Thái Thế Giới)
HOÀN TOÀN từ các Fact của những Revision đã được CHẤP NHẬN (Accepted Only).
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from studio.store import read_json, write_json, write_file, ensure_dir
from datetime import datetime

def get_accepted_revision_for_chapter(base_dir: Path, chapter: int) -> Optional[str]:
    """Lấy mã revision đang được chấp nhận cho chương. Tuyệt đối chỉ lấy bản có status='accepted'."""
    prog = read_json(base_dir / "meta" / "progress.json", {})
    accepted_map = prog.get("accepted_revisions", {})
    rev = accepted_map.get(str(chapter))
    if rev:
        return rev
        
    # Tìm trong metadata của revisions xem có revision nào có status="accepted" không
    rev_dir = base_dir / "revisions" / f"{chapter:02d}"
    if rev_dir.exists():
        for meta_file in sorted(rev_dir.glob("*.meta.json")):
            m = read_json(meta_file, {})
            if m.get("status") == "accepted":
                return m.get("revision", meta_file.stem.replace(".meta", ""))
                
    return None

def rebuild_all_projections(base_dir: Path) -> Dict[str, Any]:
    """Duyệt qua tất cả các chapter đã accept để dựng lại 100% projections từ trạng thái sạch."""
    prog = read_json(base_dir / "meta" / "progress.json", {})
    accepted_map = dict(prog.get("accepted_revisions", {}))
    
    # 1. Tìm tất cả các chương có file chương thực tế trong chapters/
    chapters_dir = base_dir / "chapters"
    completed_chapters = []
    chapter_words = {}
    
    if chapters_dir.exists():
        for f in chapters_dir.glob("*.md"):
            try:
                ch_num = int(f.stem)
                completed_chapters.append(ch_num)
                text = f.read_text(encoding="utf-8")
                chapter_words[str(ch_num)] = len(text.split())
            except ValueError:
                pass
                
    completed_chapters.sort()
    
    # 2. Dựng Projections từ trạng thái RỖNG SẠCH
    all_timeline_events = []
    foreshadow_map: Dict[str, Dict[str, Any]] = {}
    cast_map: Dict[str, Dict[str, Any]] = {}
    rel_map: Dict[str, Any] = {}
    state_map: Dict[str, Any] = {}
    chapter_summaries = []
    
    valid_completed = []
    
    for ch in completed_chapters:
        rev = get_accepted_revision_for_chapter(base_dir, ch)
        if not rev:
            # Nếu chương chưa có accepted revision hợp lệ, bỏ qua không project
            continue
            
        valid_completed.append(ch)
        accepted_map[str(ch)] = rev
        
        fact_file = base_dir / "facts" / f"{ch:02d}" / f"{rev}.json"
        fact_data = read_json(fact_file)
        
        # Nếu chưa có fact file (dữ liệu cũ/chưa migrate), thử đọc từ summaries
        if not fact_data:
            sum_file = base_dir / "summaries" / f"{ch:02d}.summary.json"
            sum_data = read_json(sum_file, {})
            fact_data = {
                "chapter": ch,
                "revision": rev,
                "summary": sum_data.get("summary", ""),
                "timeline_events": [],
                "foreshadow_updates": [],
                "cast": [{"name": c, "brief_role": "", "first_seen": ch, "last_seen": ch} for c in sum_data.get("characters", [])]
            }
            write_json(fact_file, fact_data)
            
        summary_text = fact_data.get("summary", "")
        chapter_summaries.append({
            "chapter": ch,
            "revision": rev,
            "summary": summary_text
        })
        
        # Ghi tóm tắt từng chương
        write_json(base_dir / "summaries" / f"{ch:02d}.summary.json", {
            "chapter": ch,
            "revision": rev,
            "summary": summary_text,
            "characters": [c.get("name") if isinstance(c, dict) else str(c) for c in fact_data.get("cast", [])]
        })
        
        # Cập nhật timeline
        for ev in fact_data.get("timeline_events", []):
            ev_copy = dict(ev)
            ev_copy["chapter"] = ch
            all_timeline_events.append(ev_copy)
            
        # Cập nhật foreshadows (hỗ trợ plant, advance, resolve)
        for fs in fact_data.get("foreshadow_updates", []):
            fs_id = fs.get("id")
            if not fs_id:
                continue
                
            action = fs.get("action", "")
            status = fs.get("status", "active")
            if action == "resolve" or status == "resolved":
                status = "resolved"
                
            if fs_id not in foreshadow_map:
                foreshadow_map[fs_id] = {
                    "id": fs_id,
                    "description": fs.get("description", ""),
                    "planted_at": ch,
                    "advanced_at": [],
                    "status": status,
                    "resolved_at": ch if status == "resolved" else None,
                    "notes": fs.get("notes", "")
                }
            else:
                entry = foreshadow_map[fs_id]
                if fs.get("description"):
                    entry["description"] = fs["description"]
                entry["status"] = status
                if status == "resolved" and not entry.get("resolved_at"):
                    entry["resolved_at"] = ch
                if fs.get("notes"):
                    entry["notes"] = fs["notes"]
                if ch != entry["planted_at"] and ch not in entry["advanced_at"]:
                    entry["advanced_at"].append(ch)
                
        # Cập nhật cast
        for c in fact_data.get("cast", []):
            c_name = c.get("name") if isinstance(c, dict) else str(c)
            if not c_name:
                continue
            if c_name not in cast_map:
                cast_map[c_name] = {
                    "name": c_name,
                    "brief_role": c.get("brief_role", "") if isinstance(c, dict) else "",
                    "first_seen": ch,
                    "last_seen": ch
                }
            else:
                cast_map[c_name]["last_seen"] = ch
                if isinstance(c, dict) and c.get("brief_role"):
                    cast_map[c_name]["brief_role"] = c["brief_role"]
                    
        # Cập nhật relationship changes (hỗ trợ update và delete)
        for rel in fact_data.get("relationship_changes", []):
            pair = rel.get("pair")
            status = rel.get("status")
            action = rel.get("action", "update")
            if pair:
                if action == "delete":
                    rel_map.pop(pair, None)
                elif status:
                    rel_map[pair] = status
                    
        # Cập nhật world state changes
        for st in fact_data.get("state_changes", []):
            k = st.get("key")
            if k:
                state_map[k] = {"value": st.get("value"), "updated_at_chapter": ch}

    # 3. Ghi ra các Projections một cách nguyên tử
    # Timeline
    timeline_path = base_dir / "world" / "timeline.jsonl"
    ensure_dir(timeline_path.parent)
    timeline_content = "".join([f"{json.dumps(ev, ensure_ascii=False)}\n" for ev in all_timeline_events])
    write_file(timeline_path, timeline_content)
            
    # Foreshadow ledger
    write_json(base_dir / "world" / "foreshadow_ledger.json", list(foreshadow_map.values()))
    
    # Cast ledger
    write_json(base_dir / "characters" / "cast_ledger.json", list(cast_map.values()))
    
    # Relationships
    write_json(base_dir / "world" / "relationships.json", rel_map)
    
    # World state changes
    write_json(base_dir / "world" / "state_changes.json", state_map)
    
    # Dựng lại Arc Summaries
    rebuild_arc_summaries_from_facts(base_dir, valid_completed)
    
    # Cập nhật progress.json
    prog["completed_chapters"] = valid_completed
    prog["total_chapters"] = max(prog.get("total_chapters", 0), len(valid_completed))
    # Cập nhật current_chapter chuẩn xác
    if len(valid_completed) >= prog["total_chapters"]:
        prog["current_chapter"] = max(valid_completed) if valid_completed else 1
        prog["phase"] = "completed"
    else:
        prog["current_chapter"] = (max(valid_completed) + 1) if valid_completed else 1
    prog["chapter_word_counts"] = {str(k): chapter_words.get(str(k), 0) for k in valid_completed}
    prog["total_word_count"] = sum(prog["chapter_word_counts"].values())
    prog["accepted_revisions"] = {str(k): accepted_map[str(k)] for k in valid_completed if str(k) in accepted_map}
    write_json(base_dir / "meta" / "progress.json", prog)
    
    return {
        "status": "projections_rebuilt",
        "completed_chapters": valid_completed,
        "current_chapter": prog["current_chapter"],
        "total_words": prog["total_word_count"],
        "timeline_events_count": len(all_timeline_events),
        "foreshadows_count": len(foreshadow_map),
        "cast_count": len(cast_map),
        "relationships_count": len(rel_map)
    }

def rebuild_arc_summaries_from_facts(base_dir: Path, completed_chapters: List[int]) -> None:
    """Tái tạo tóm tắt các Cung truyện và Tập truyện từ các facts chương."""
    layered_outline = read_json(base_dir / "outlines" / "layered_outline.json")
    if not layered_outline or not isinstance(layered_outline, list):
        return

    for vol in layered_outline:
        v_idx = vol.get("index", 1)
        for arc in vol.get("arcs", []):
            a_idx = arc.get("index", 1)
            arc_ch_list = [c.get("chapter") for c in arc.get("chapters", []) if isinstance(c, dict)]
            
            arc_completed = [c for c in arc_ch_list if c in completed_chapters]
            if not arc_completed:
                continue
                
            summaries = []
            for ch in arc_completed:
                s_file = base_dir / "summaries" / f"{ch:02d}.summary.json"
                s_data = read_json(s_file)
                if s_data and s_data.get("summary"):
                    summaries.append(f"Chương {ch}: {s_data['summary']}")
                    
            arc_summary_data = {
                "volume": v_idx,
                "arc": a_idx,
                "title": arc.get("title", f"Cung {a_idx}"),
                "chapters_included": arc_completed,
                "arc_summary": " | ".join(summaries),
                "updated_at": datetime.now().isoformat()
            }
            write_json(base_dir / "summaries" / "arcs" / f"v{v_idx}_a{a_idx}.json", arc_summary_data)
