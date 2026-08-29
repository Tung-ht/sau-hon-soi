# -*- coding: utf-8 -*-
"""
Studio Novel Importer
Bóc tách chương từ file thô (.txt, .md) và nạp vào cấu trúc Revisions/Facts để tiếp tục viết.
"""

import re
from pathlib import Path
from typing import Dict, Any, List, Optional

from studio.store import read_file, write_file, write_json, ensure_dir, get_base_dir, init_novel_store
from studio.projector import rebuild_all_projections

CHAPTER_HEADER_REGEX = re.compile(
    r'^(?:#{1,3}\s*)?(?:Chương|Hồi|Tiết|Chapter|PHẦN)\s+([0-9IVXLCDMivxlcdm]+|[一二三四五六七八九十百千万]+)(?:[\s:.\-–—]+(.*))?$',
    re.IGNORECASE
)

def parse_raw_novel_text(content: str) -> List[Dict[str, Any]]:
    """Phân tích văn bản thô để tách các chương dựa trên biểu thức chính quy."""
    lines = content.splitlines()
    chapters = []
    current_ch = None
    current_lines = []
    
    for line in lines:
        match = CHAPTER_HEADER_REGEX.match(line.strip())
        if match:
            if current_ch is not None and current_lines:
                current_ch["content"] = "\n".join(current_lines).strip()
                chapters.append(current_ch)
                current_lines = []
            
            raw_num = match.group(1)
            title = match.group(2).strip() if match.group(2) else f"Chương {raw_num}"
            try:
                ch_idx = int(raw_num)
            except ValueError:
                ch_idx = len(chapters) + 1
                
            current_ch = {
                "index": ch_idx,
                "title": title,
                "header": line.strip(),
                "content": ""
            }
        else:
            if current_ch is not None:
                current_lines.append(line)
                
    if current_ch is not None and current_lines:
        current_ch["content"] = "\n".join(current_lines).strip()
        chapters.append(current_ch)
        
    return chapters

def import_novel(file_path: str, name: str, scale: str = "long", base_dir: Optional[Path] = None) -> Dict[str, Any]:
    """Nhập một tệp tiểu thuyết có sẵn và tự động xây dựng cơ sở dữ liệu để tiếp tục viết."""
    src_file = Path(file_path)
    if not src_file.exists():
        raise FileNotFoundError(f"Không tìm thấy file nguồn tại '{file_path}'")
        
    content = read_file(src_file)
    parsed_chapters = parse_raw_novel_text(content)
    if not parsed_chapters:
        raise ValueError("Không thể nhận diện được các chương từ file nguồn. Vui lòng đảm bảo có tiêu đề định dạng 'Chương 1: ...'")
        
    if base_dir is None:
        base_dir = get_base_dir(None, novel_name=name)
        
    init_novel_store(base_dir, name, scale, premise=f"Tác phẩm '{name}' được nhập từ tệp nguồn {src_file.name}.")
    
    outline_chapters = []
    accepted_revisions = {}
    
    for ch in parsed_chapters:
        ch_idx = ch["index"]
        ch_text = ch["content"]
        ch_title = ch["title"]
        rev_id = "r001"
        
        # 1. Lưu bản chính chapters/
        write_file(base_dir / "chapters" / f"{ch_idx:02d}.md", ch_text)
        
        # 2. Lưu revision & facts
        rev_dir = base_dir / "revisions" / f"{ch_idx:02d}"
        facts_dir = base_dir / "facts" / f"{ch_idx:02d}"
        ensure_dir(rev_dir)
        ensure_dir(facts_dir)
        
        write_file(rev_dir / f"{rev_id}.md", ch_text)
        write_json(rev_dir / f"{rev_id}.meta.json", {
            "chapter": ch_idx,
            "revision": rev_id,
            "status": "accepted",
            "author": "imported",
            "word_count": len(ch_text.split())
        })
        
        # Tóm tắt sơ bộ từ 200 chữ đầu
        preview_words = ch_text.split()[:150]
        preview_text = " ".join(preview_words) + ("..." if len(ch_text.split()) > 150 else "")
        fact_data = {
            "chapter": ch_idx,
            "revision": rev_id,
            "summary": f"[{ch_title}] " + preview_text,
            "timeline_events": [],
            "foreshadow_updates": [],
            "cast": [],
            "dependencies": []
        }
        write_json(facts_dir / f"{rev_id}.json", fact_data)
        
        outline_chapters.append({
            "chapter": ch_idx,
            "title": ch_title,
            "summary": fact_data["summary"]
        })
        accepted_revisions[str(ch_idx)] = rev_id
        
    # Tạo layered_outline hoặc outline
    if scale == "long":
        arcs = []
        for a_idx, i in enumerate(range(0, len(outline_chapters), 5), 1):
            arc_ch = outline_chapters[i:i+5]
            arcs.append({
                "index": a_idx,
                "title": f"Cung {a_idx} (Nhập tự động)",
                "chapters": arc_ch
            })
        layered = [{
            "index": 1,
            "title": "Tập 1",
            "arcs": arcs
        }]
        write_json(base_dir / "outlines" / "layered_outline.json", layered)
    else:
        write_json(base_dir / "outlines" / "outline.json", outline_chapters)
        
    if not (base_dir / "characters" / "characters.json").exists():
        write_json(base_dir / "characters" / "characters.json", [])
    if not (base_dir / "world" / "world_rules.json").exists():
        write_json(base_dir / "world" / "world_rules.json", [])
        
    rebuild_res = rebuild_all_projections(base_dir)
    
    return {
        "status": "imported",
        "novel_name": name,
        "dir": str(base_dir.resolve()),
        "imported_chapters": len(parsed_chapters),
        "total_words": rebuild_res["total_words"],
        "next_chapter": len(parsed_chapters) + 1,
        "next_action": f"Architect: Phân tích ngược nhân vật và bối cảnh từ {len(parsed_chapters)} chương đã nhập, sau đó tiếp tục viết chương {len(parsed_chapters) + 1}."
    }
