# -*- coding: utf-8 -*-
"""
Studio Revision & Fact Manager
Quản lý các bản sửa đổi (revisions), bản ghi sự thật (facts), so sánh diff, chấp nhận có giao dịch và rollback toàn diện (Full Projections Rollback), từ chối (reject), chống rò rỉ đường dẫn (Path Traversal Guard) và an toàn đa luồng (StudioLock).
"""

import os
import re
import difflib
import shutil
import uuid
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple

from studio.store import (
    read_json, write_json, read_file, write_file, append_jsonl, ensure_dir, StudioLock
)
from studio.schemas import create_fact_schema, create_decision_record, validate_facts
from studio.projector import rebuild_all_projections, get_accepted_revision_for_chapter

def resolve_content(content_or_file: str) -> str:
    """Hỗ trợ nạp nội dung từ chuỗi trực tiếp, qua tiền tố @file: hoặc đường dẫn file."""
    if not content_or_file:
        return ""
    if content_or_file.startswith("@"):
        path_str = content_or_file[1:]
        p = Path(path_str)
        if p.exists():
            return read_file(p)
    p = Path(content_or_file)
    if p.exists() and p.is_file() and not "\n" in content_or_file and len(content_or_file) < 260:
        return read_file(p)
    return content_or_file

def sanitize_branch_name(branch: str) -> str:
    """Khử khuẩn và kiểm tra whitelist cho branch name (Chống Path Traversal - Sửa P0)."""
    if not branch:
        return "branch"
    clean = re.sub(r'[^a-zA-Z0-9_-]', '_', branch.strip())
    clean = clean.strip('_')
    if not clean:
        clean = "branch"
    return clean

def get_next_revision_id(base_dir: Path, chapter: int, branch: Optional[str] = None) -> str:
    """Tự động tính toán mã revision tiếp theo (r001, r002, r003... hoặc r002_branch_A)."""
    rev_dir = base_dir / "revisions" / f"{chapter:02d}"
    if not rev_dir.exists():
        base_id = "r001"
    else:
        existing = []
        for f in rev_dir.glob("r*.md"):
            stem = f.stem
            try:
                num = int(stem.replace("r", "").split("_")[0])
                existing.append(num)
            except ValueError:
                pass
        next_num = max(existing) + 1 if existing else 1
        base_id = f"r{next_num:03d}"
        
    if branch:
        clean_branch = sanitize_branch_name(branch)
        return f"{base_id}_branch_{clean_branch}"
    return base_id

def list_revisions_for_chapter(base_dir: Path, chapter: int) -> List[Dict[str, Any]]:
    """Liệt kê tất cả các revision của một chương kèm trạng thái hợp lệ."""
    rev_dir = base_dir / "revisions" / f"{chapter:02d}"
    if not rev_dir.exists():
        return []
        
    prog = read_json(base_dir / "meta" / "progress.json", {})
    accepted_rev = prog.get("accepted_revisions", {}).get(str(chapter))
    
    results = []
    for meta_file in sorted(rev_dir.glob("*.meta.json")):
        meta = read_json(meta_file, {})
        rev_id = meta.get("revision", meta_file.stem.replace(".meta", ""))
        is_accepted = (rev_id == accepted_rev)
        results.append({
            "revision": rev_id,
            "created_at": meta.get("created_at"),
            "author": meta.get("author", "agent"),
            "status": "accepted" if is_accepted else meta.get("status", "pending"),
            "note": meta.get("note", ""),
            "branch": meta.get("branch"),
            "word_count": meta.get("word_count", 0)
        })
    return results

def save_draft_revision(
    base_dir: Path,
    chapter: int,
    content: str,
    facts_data: Optional[Dict[str, Any]] = None,
    mode: str = "write",
    note: str = "",
    author: str = "agent",
    branch: Optional[str] = None
) -> Dict[str, Any]:
    """Lưu bản thảo mới dưới khóa StudioLock, kiểm tra path traversal an toàn tuyệt đối."""
    with StudioLock(base_dir):
        content_resolved = resolve_content(content)
        
        rev_dir = base_dir / "revisions" / f"{chapter:02d}"
        facts_dir = base_dir / "facts" / f"{chapter:02d}"
        ensure_dir(rev_dir)
        ensure_dir(facts_dir)
        
        if mode == "append":
            existing_revs = list_revisions_for_chapter(base_dir, chapter)
            if existing_revs:
                latest_rev_id = existing_revs[-1]["revision"]
                base_content = read_file(rev_dir / f"{latest_rev_id}.md")
            elif (base_dir / "chapters" / f"{chapter:02d}.md").exists():
                base_content = read_file(base_dir / "chapters" / f"{chapter:02d}.md")
            else:
                base_content = ""
            content_resolved = base_content.rstrip() + "\n\n" + content_resolved.lstrip() if base_content else content_resolved
            
        rev_id = get_next_revision_id(base_dir, chapter, branch=branch)
        target_md = rev_dir / f"{rev_id}.md"
        
        target_resolved_str = str(target_md.resolve())
        expected_dir_str = str(rev_dir.resolve())
        if not target_resolved_str.startswith(expected_dir_str):
            raise ValueError(f"Tên branch hoặc revision '{rev_id}' không hợp lệ vì vượt khỏi thư mục {expected_dir_str}")
            
        write_file(target_md, content_resolved)
        write_file(base_dir / "drafts" / f"{chapter:02d}.draft.md", content_resolved)
        
        words_count = len(content_resolved.split())
        if not isinstance(facts_data, dict):
            facts_data = {}
        facts_data["chapter"] = chapter
        facts_data["revision"] = rev_id
        valid_facts = validate_facts(facts_data)
        write_json(facts_dir / f"{rev_id}.json", valid_facts)
        
        meta_obj = {
            "chapter": chapter,
            "revision": rev_id,
            "created_at": datetime.now().isoformat(),
            "author": author,
            "status": "pending",
            "note": note,
            "branch": branch,
            "word_count": words_count
        }
        write_json(rev_dir / f"{rev_id}.meta.json", meta_obj)
        
        dec = create_decision_record(
            action="draft_created" if not branch else "branch_created",
            actor=author,
            chapter=chapter,
            revision=rev_id,
            reason=note or f"Tạo bản thảo revision {rev_id}"
        )
        append_jsonl(base_dir / "decisions.jsonl", dec)
        
        prog = read_json(base_dir / "meta" / "progress.json", {})
        prog["in_progress_chapter"] = chapter
        write_json(base_dir / "meta" / "progress.json", prog)
        
        return {
            "status": "draft_revision_created",
            "chapter": chapter,
            "revision": rev_id,
            "branch": branch,
            "word_count": words_count,
            "file": str(target_md),
            "note": "Bản thảo đã được tạo an toàn dưới dạng revision. Chưa ghi đè vào chapters/."
        }

def diff_revisions(
    base_dir: Path,
    chapter: int,
    rev_a: Optional[str] = None,
    rev_b: Optional[str] = None
) -> Dict[str, Any]:
    """So sánh sự khác biệt (Text Diff và Fact Diff) giữa hai revision hoặc giữa bản chính và bản nháp."""
    rev_dir = base_dir / "revisions" / f"{chapter:02d}"
    facts_dir = base_dir / "facts" / f"{chapter:02d}"
    
    accepted_rev = get_accepted_revision_for_chapter(base_dir, chapter)
    
    if not rev_a:
        rev_a = accepted_rev or "r001"
        
    if not rev_b:
        existing_revs = list_revisions_for_chapter(base_dir, chapter)
        if existing_revs:
            rev_b = existing_revs[-1]["revision"]
        else:
            rev_b = rev_a
            
    text_a = read_file(rev_dir / f"{rev_a}.md")
    if not text_a and (base_dir / "chapters" / f"{chapter:02d}.md").exists():
        text_a = read_file(base_dir / "chapters" / f"{chapter:02d}.md")
        
    text_b = read_file(rev_dir / f"{rev_b}.md")
    
    lines_a = text_a.splitlines()
    lines_b = text_b.splitlines()
    text_diff_lines = list(difflib.unified_diff(
        lines_a, lines_b,
        fromfile=f"Chapter_{chapter}_{rev_a}",
        tofile=f"Chapter_{chapter}_{rev_b}",
        lineterm=""
    ))
    
    facts_a = read_json(facts_dir / f"{rev_a}.json", {})
    facts_b = read_json(facts_dir / f"{rev_b}.json", {})
    
    fact_diff = {
        "summary_changed": (facts_a.get("summary") != facts_b.get("summary")),
        "summary_before": facts_a.get("summary", ""),
        "summary_after": facts_b.get("summary", ""),
        "timeline_events_count": {
            rev_a: len(facts_a.get("timeline_events", [])),
            rev_b: len(facts_b.get("timeline_events", []))
        },
        "foreshadow_updates": {
            rev_a: facts_a.get("foreshadow_updates", []),
            rev_b: facts_b.get("foreshadow_updates", [])
        },
        "cast_introduced": {
            rev_a: [c.get("name") if isinstance(c, dict) else c for c in facts_a.get("cast", [])],
            rev_b: [c.get("name") if isinstance(c, dict) else c for c in facts_b.get("cast", [])]
        }
    }
    
    return {
        "chapter": chapter,
        "rev_a": rev_a,
        "rev_b": rev_b,
        "is_identical": (text_a == text_b and facts_a == facts_b),
        "text_diff": "\n".join(text_diff_lines[:100]),
        "fact_diff": fact_diff,
        "narrative_summary": f"So sánh Chapter {chapter}: '{rev_a}' ({len(text_a.split())} từ) vs '{rev_b}' ({len(text_b.split())} từ)."
    }

def accept_revision(
    base_dir: Path,
    chapter: int,
    revision: Optional[str] = None,
    actor: str = "user",
    reason: str = "",
    force: bool = False
) -> Dict[str, Any]:
    """Chấp nhận revision làm bản chính với Two-Phase Projections Rollback sạch sẽ 100% (Sửa P0)."""
    with StudioLock(base_dir) as lock:
        rev_dir = base_dir / "revisions" / f"{chapter:02d}"
        
        if not revision:
            rev_list = list_revisions_for_chapter(base_dir, chapter)
            if not rev_list:
                raise FileNotFoundError(f"Chương {chapter} chưa có bản revision nào để accept.")
            pending = [r for r in rev_list if r.get("status") == "pending"]
            revision = pending[-1]["revision"] if pending else rev_list[-1]["revision"]
            
        rev_md = rev_dir / f"{revision}.md"
        rev_meta_file = rev_dir / f"{revision}.meta.json"
        if not rev_md.exists() or not rev_meta_file.exists():
            raise FileNotFoundError(f"Không tìm thấy file revision '{revision}' tại {rev_md}")
            
        rev_meta = read_json(rev_meta_file, {})
        if rev_meta.get("status") == "rejected" and not force:
            raise ValueError(f"Revision '{revision}' đã bị rejected trước đó. Tạo revision mới hoặc dùng --force để chấp nhận lại.")

        prog = read_json(base_dir / "meta" / "progress.json", {})
        cur_accepted = prog.get("accepted_revisions", {}).get(str(chapter))
        ch_main_file = base_dir / "chapters" / f"{chapter:02d}.md"
        if cur_accepted == revision and ch_main_file.exists() and not force:
            return {
                "status": "already_accepted",
                "chapter": chapter,
                "accepted_revision": revision,
                "message": f"Revision '{revision}' đã là bản chính hiện tại của chương {chapter}."
            }

        # 1. Tạo cây thư mục Backup toàn bộ Projections & Chapters trước giao dịch
        bk_token = uuid.uuid4().hex
        bk_tree_dir = base_dir / f".tmp_accept_backup_{bk_token}"
        ensure_dir(bk_tree_dir)
        
        proj_dirs = ["world", "summaries", "characters", "chapters"]
        for d in proj_dirs:
            live_d = base_dir / d
            if live_d.exists():
                shutil.copytree(str(live_d), str(bk_tree_dir / d))
                
        backup_progress = read_json(base_dir / "meta" / "progress.json", {})
        backup_rev_metas = {f.name: read_json(f) for f in rev_dir.glob("*.meta.json")}
        
        content = read_file(rev_md)
        
        try:
            # 2. Cập nhật chapters/XX.md
            ensure_dir(base_dir / "chapters")
            write_file(ch_main_file, content)
            
            # 3. Cập nhật trạng thái revision meta
            for meta_file in rev_dir.glob("*.meta.json"):
                m = read_json(meta_file, {})
                if meta_file.name.startswith(revision):
                    m["status"] = "accepted"
                elif m.get("status") == "accepted":
                    m["status"] = "superseded"
                write_json(meta_file, m)
                
            # 4. Cập nhật progress accepted_revisions
            prog = read_json(base_dir / "meta" / "progress.json", {})
            if "accepted_revisions" not in prog:
                prog["accepted_revisions"] = {}
            prog["accepted_revisions"][str(chapter)] = revision
            
            if chapter in prog.get("pending_rewrites", []):
                prog["pending_rewrites"].remove(chapter)
            if not prog.get("pending_rewrites"):
                prog["flow"] = "writing"
                prog["rewrite_reason"] = ""
            write_json(base_dir / "meta" / "progress.json", prog)
            
            lock.touch()

            # 5. DỰNG LẠI TOÀN BỘ BẢN CHIẾU (PROJECTIONS)
            rebuild_res = rebuild_all_projections(base_dir)
            
            # 6. Ghi nhận vào decisions.jsonl
            dec = create_decision_record(
                action="revision_accepted",
                actor=actor,
                chapter=chapter,
                revision=revision,
                reason=reason or f"Chấp nhận {revision} làm bản chính chương {chapter}"
            )
            append_jsonl(base_dir / "decisions.jsonl", dec)
            
            # 7. Thành công: Xóa thư mục backup
            shutil.rmtree(bk_tree_dir, ignore_errors=True)
            
            return {
                "status": "revision_accepted",
                "chapter": chapter,
                "accepted_revision": revision,
                "word_count": len(content.split()),
                "projections": rebuild_res,
                "message": f"Chương {chapter} đã được cập nhật chính thức với revision '{revision}'."
            }
            
        except Exception as e:
            # ROLLBACK TOÀN DIỆN: Xóa sạch thư mục projections bị lỗi và khôi phục từ bk_tree_dir
            for d in proj_dirs:
                live_d = base_dir / d
                if live_d.exists():
                    shutil.rmtree(live_d, ignore_errors=True)
                bk_d = bk_tree_dir / d
                if bk_d.exists():
                    shutil.copytree(str(bk_d), str(live_d))
                    
            write_json(base_dir / "meta" / "progress.json", backup_progress)
            for fname, data in backup_rev_metas.items():
                write_json(rev_dir / fname, data)
                
            shutil.rmtree(bk_tree_dir, ignore_errors=True)
            raise RuntimeError(f"Lỗi khi accept revision '{revision}': {str(e)}. Toàn bộ dữ liệu & projections đã được Rollback 100% về trạng thái an toàn.")

def reject_revision(
    base_dir: Path,
    chapter: int,
    revision: Optional[str] = None,
    actor: str = "user",
    reason: str = "",
    force: bool = False
) -> Dict[str, Any]:
    """Từ chối một revision nháp có kiểm tra tính hợp lệ trạng thái."""
    with StudioLock(base_dir):
        rev_dir = base_dir / "revisions" / f"{chapter:02d}"
        
        if not revision:
            rev_list = list_revisions_for_chapter(base_dir, chapter)
            if not rev_list:
                raise FileNotFoundError(f"Chương {chapter} không có revision nào để reject.")
            pending = [r for r in rev_list if r.get("status") == "pending"]
            revision = pending[-1]["revision"] if pending else rev_list[-1]["revision"]
            
        prog = read_json(base_dir / "meta" / "progress.json", {})
        cur_accepted = prog.get("accepted_revisions", {}).get(str(chapter))
        
        if cur_accepted == revision and not force:
            raise ValueError(f"Không thể reject revision '{revision}' vì nó đang là bản chính (accepted). Hãy accept một revision khác trước hoặc dùng --force.")
            
        meta_file = rev_dir / f"{revision}.meta.json"
        if meta_file.exists():
            m = read_json(meta_file, {})
            m["status"] = "rejected"
            m["rejected_at"] = datetime.now().isoformat()
            m["rejection_reason"] = reason
            write_json(meta_file, m)
            
        dec = create_decision_record(
            action="revision_rejected",
            actor=actor,
            chapter=chapter,
            revision=revision,
            reason=reason or f"Từ chối revision {revision} chương {chapter}"
        )
        append_jsonl(base_dir / "decisions.jsonl", dec)
        
        return {
            "status": "revision_rejected",
            "chapter": chapter,
            "rejected_revision": revision,
            "message": f"Đã từ chối revision '{revision}'. Bản chính của chương {chapter} không bị thay đổi."
        }

def impact_analysis(base_dir: Path, chapter: int) -> Dict[str, Any]:
    """Phân tích toàn diện các chương phía sau, dependencies, state changes, và phục bút bị ảnh hưởng."""
    prog = read_json(base_dir / "meta" / "progress.json", {})
    completed = prog.get("completed_chapters", [])
    downstream = [c for c in completed if c > chapter]
    
    foreshadows = read_json(base_dir / "world" / "foreshadow_ledger.json", [])
    affected_fs = []
    if isinstance(foreshadows, list):
        for fs in foreshadows:
            planted = fs.get("planted_at")
            advanced = fs.get("advanced_at", [])
            resolved = fs.get("resolved_at")
            if planted == chapter or chapter in advanced or resolved == chapter:
                affected_fs.append(fs)
                
    cast = read_json(base_dir / "characters" / "cast_ledger.json", [])
    affected_cast = []
    if isinstance(cast, list):
        for c in cast:
            if c.get("first_seen") == chapter or c.get("last_seen") == chapter:
                affected_cast.append(c)
                
    affected_downstream_chapters = []
    for dch in downstream:
        rev = get_accepted_revision_for_chapter(base_dir, dch)
        if rev:
            facts = read_json(base_dir / "facts" / f"{dch:02d}" / f"{rev}.json", {})
            deps = facts.get("dependencies", [])
            if any(f"chapter-{chapter}" in str(dep) or f"ch-{chapter}" in str(dep) for dep in deps):
                affected_downstream_chapters.append(dch)
                
    return {
        "target_chapter": chapter,
        "downstream_completed_chapters": downstream,
        "requires_downstream_review": len(downstream) > 0,
        "affected_foreshadows": affected_fs,
        "affected_cast": affected_cast,
        "dependent_chapters_detected": affected_downstream_chapters,
        "recommendation": f"Sửa chương {chapter} có thể làm thay đổi tiền đề cho {len(downstream)} chương sau ({downstream}). Hãy kiểm tra tính liên tục sau khi commit bản mới." if downstream else "Chương này không có chương sau phụ thuộc."
    }
