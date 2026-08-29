# -*- coding: utf-8 -*-
"""
Studio CLI & Interactive Controller
Cung cấp 15+ thao tác tương tác tự nhiên cho Agent và Tác giả theo mô hình Agent-led, Engine-guarded.
"""

import sys
import os
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

from studio.store import (
    get_base_dir, init_novel_store, list_all_novels, read_json, write_json,
    read_file, write_file, get_config, set_config
)
from studio.schemas import (
    DEFAULT_CONFIG, create_decision_record, validate_config,
    validate_chapter_plan, validate_facts, validate_review_scorecard
)
from studio.projector import rebuild_all_projections, get_accepted_revision_for_chapter
from studio.revision import (
    save_draft_revision, diff_revisions, accept_revision, reject_revision,
    impact_analysis, list_revisions_for_chapter, resolve_content
)
from studio.context import (
    get_full_context, get_open_threads, get_summaries_hierarchy, get_missing_foundation
)
from studio.quality import style_lint, save_review_scorecard
from studio.snapshot import snapshot_create, snapshot_list, snapshot_restore
from studio.importer import import_novel

def load_payload(raw_value: Optional[str], file_flag_val: Optional[str] = None) -> Any:
    """Đọc dữ liệu từ string, file path hoặc JSON."""
    target_val = file_flag_val if file_flag_val else raw_value
    if not target_val:
        return None
    content = resolve_content(target_val)
    try:
        return json.loads(content)
    except Exception:
        return content

def suggest_next_options(base_dir: Path) -> List[Dict[str, Any]]:
    """Đề xuất 2-3 hướng đi tiếp theo cho Agent và Tác giả dựa trên trạng thái thực tế và chế độ tương tác."""
    cfg = get_config(base_dir)
    mode = cfg.get("interaction_mode", "guided")
    
    missing = get_missing_foundation(base_dir)
    if missing:
        return [
            {
                "action": "foundation",
                "title": f"Bổ sung thiết lập nền tảng còn thiếu: {', '.join(missing)}",
                "reason": "Chưa hoàn thiện thiết lập thế giới/nhân vật/dàn ý",
                "mode_policy": mode,
                "requires_approval": (mode != "auto"),
                "recommended": True
            },
            {
                "action": "import",
                "title": "Nhập tiểu thuyết có sẵn bằng lệnh import-novel",
                "reason": "Nếu bạn đã có bản thảo viết dở từ trước"
            }
        ]
        
    prog = read_json(base_dir / "meta" / "progress.json", {})
    completed = prog.get("completed_chapters", [])
    next_ch = max(completed) + 1 if completed else 1
    pending_rewrites = prog.get("pending_rewrites", [])
    
    options = []
    
    # 1. Hàng đợi viết lại
    if pending_rewrites:
        target_ch = pending_rewrites[0]
        options.append({
            "action": "rewrite",
            "chapter": target_ch,
            "title": f"Viết lại chương {target_ch} theo yêu cầu biên tập",
            "reason": prog.get("rewrite_reason", "Yêu cầu chỉnh sửa"),
            "mode_policy": mode,
            "requires_approval": (mode != "auto"),
            "recommended": True
        })
        options.append({
            "action": "override_rewrite",
            "chapter": target_ch,
            "title": f"Bỏ qua yêu cầu viết lại chương {target_ch} và tiếp tục viết chương {next_ch}",
            "reason": "Tác giả quyết định giữ nguyên bản hiện tại",
            "mode_policy": mode,
            "requires_approval": True
        })
        return options
        
    # 2. Bản nháp đang chờ duyệt
    cur_revs = list_revisions_for_chapter(base_dir, next_ch)
    pending_revs = [r for r in cur_revs if r.get("status") == "pending"]
    if pending_revs:
        p_rev = pending_revs[-1]["revision"]
        if mode == "auto":
            options.append({
                "action": "auto_accept",
                "chapter": next_ch,
                "revision": p_rev,
                "title": f"Tự động chấp nhận revision {p_rev} chương {next_ch} (Chế độ Auto)",
                "reason": "Chế độ Auto tự động đẩy nhanh tiến độ",
                "mode_policy": "auto",
                "recommended": True
            })
        else:
            options.append({
                "action": "review_draft",
                "chapter": next_ch,
                "revision": p_rev,
                "title": f"Xem diff và duyệt bản nháp {p_rev} của chương {next_ch}",
                "reason": "Bản nháp đã được soạn nhưng chưa commit",
                "mode_policy": mode,
                "requires_approval": True,
                "recommended": True
            })
        options.append({
            "action": "branch_draft",
            "chapter": next_ch,
            "title": f"Tạo nhánh rẽ A/B thử nghiệm cho chương {next_ch}",
            "reason": "Thử nghiệm phương án diễn biến khác",
            "mode_policy": mode
        })
        return options

    # 3. Ranh giới Arc
    if prog.get("layered", True) and completed and len(completed) % 5 == 0:
        arc_num = len(completed) // 5
        options.append({
            "action": "review_arc",
            "arc": arc_num,
            "title": f"Đánh giá tổng kết Cung {arc_num} (Chương {len(completed)-4}–{len(completed)})",
            "reason": "Đã hoàn thành 5 chương của Cung truyện",
            "mode_policy": mode,
            "recommended": True
        })
        options.append({
            "action": "write_chapter",
            "chapter": next_ch,
            "title": f"Viết tiếp chương {next_ch} (Mở đầu Cung {arc_num+1})",
            "reason": "Tiếp tục mạch truyện không cần dừng lại",
            "mode_policy": mode
        })
        return options

    # 4. Viết chương mới
    action_title = f"Lên kế hoạch và viết chương {next_ch}"
    if mode == "manual":
        action_title = f"[Thủ công] Bạn chỉ đạo kế hoạch và Agent viết nháp chương {next_ch}"
    elif mode == "auto":
        action_title = f"[Tự động] Tự lập kế hoạch và viết nháp chương {next_ch}"
        
    options.append({
        "action": "write_chapter",
        "chapter": next_ch,
        "title": action_title,
        "reason": "Tiếp tục phát triển cốt truyện",
        "mode_policy": mode,
        "requires_approval": (mode == "manual"),
        "recommended": True
    })
    if completed:
        options.append({
            "action": "edit_previous",
            "chapter": completed[-1],
            "title": f"Xem lại hoặc chỉnh sửa chương {completed[-1]} vừa viết",
            "reason": "Tinh chỉnh câu chữ hoặc nhịp điệu",
            "mode_policy": mode
        })
        options.append({
            "action": "snapshot",
            "title": f"Tạo điểm lưu checkpoint an toàn tại chương {len(completed)}",
            "reason": "Lưu mốc trước khi bước vào tình tiết quan trọng",
            "mode_policy": mode
        })
    return options

def get_status_dashboard(base_dir: Path) -> Dict[str, Any]:
    """Tạo báo cáo Dashboard trực quan theo đúng thiết kế Studio."""
    prog = read_json(base_dir / "meta" / "progress.json", {})
    cfg = get_config(base_dir)
    completed = prog.get("completed_chapters", [])
    total_words = prog.get("total_word_count", 0)
    novel_name = prog.get("novel_name", "Tiểu Thuyết")
    scale = "long" if prog.get("layered", True) else "short"
    
    vol_num = (len(completed) // 10) + 1 if scale == "long" else 1
    arc_num = ((len(completed) % 10) // 5) + 1 if scale == "long" else 1
    position = f"Tập {vol_num} · Cung {arc_num}" if scale == "long" else "Toàn tập"
    
    next_ch = max(completed) + 1 if completed else 1
    pending_drafts = []
    for c in range(1, next_ch + 2):
        revs = list_revisions_for_chapter(base_dir, c)
        for r in revs:
            if r.get("status") == "pending":
                pending_drafts.append(f"Chương {c} ({r['revision']})")
                
    open_threads = get_open_threads(base_dir)
    
    warnings = []
    missing_foundation = get_missing_foundation(base_dir)
    if missing_foundation:
        warnings.append(f"Thiếu thiết lập nền tảng: {', '.join(missing_foundation)}")
    if prog.get("pending_rewrites"):
        warnings.append(f"Có chương trong hàng đợi viết lại: {prog['pending_rewrites']}")
        
    suggestions = suggest_next_options(base_dir)
    
    return {
        "novel_name": novel_name,
        "interaction_mode": cfg.get("interaction_mode", "guided"),
        "progress": {
            "current_chapter": prog.get("current_chapter", next_ch),
            "completed_chapters_count": len(completed),
            "completed_chapters": completed,
            "total_words": total_words,
            "position": position
        },
        "pending_drafts": pending_drafts,
        "pending_rewrites": prog.get("pending_rewrites", []),
        "open_threads_count": len(open_threads),
        "open_threads": open_threads[:5],
        "warnings": warnings,
        "suggestions": suggestions
    }

def export_novel(base_dir: Path, output_file: Optional[str] = None) -> str:
    progress = read_json(base_dir / "meta" / "progress.json", {})
    name = progress.get("novel_name", "TieuThuyet")
    completed = progress.get("completed_chapters", [])
    completed.sort()

    lines = [f"# {name}\n\n"]
    premise = read_file(base_dir / "outlines" / "premise.md")
    if premise:
        lines.append(f"## Giới Thiệu Tác Phẩm\n\n{premise}\n\n---\n\n")

    for ch in completed:
        text = read_file(base_dir / "chapters" / f"{ch:02d}.md")
        lines.append(f"## Chương {ch}\n\n{text}\n\n")

    full_text = "".join(lines)
    out_path = Path(output_file) if output_file else base_dir / f"{name}.md"
    write_file(out_path, full_text)
    return str(out_path)

def save_foundation(base_dir: Path, f_type: str, data: Any, scale: str = "long") -> Dict[str, Any]:
    """Lưu trữ các tệp Foundation đầy đủ bao gồm compass, expand_arc, complete_book."""
    if f_type == "premise":
        write_file(base_dir / "outlines" / "premise.md", str(data))
    elif f_type == "characters":
        write_json(base_dir / "characters" / "characters.json", data)
    elif f_type == "world_rules":
        write_json(base_dir / "world" / "world_rules.json", data)
    elif f_type == "outline":
        write_json(base_dir / "outlines" / "outline.json", data)
    elif f_type == "layered_outline":
        write_json(base_dir / "outlines" / "layered_outline.json", data)
    elif f_type == "compass":
        write_json(base_dir / "outlines" / "compass.json", data)
    elif f_type == "expand_arc":
        layered = read_json(base_dir / "outlines" / "layered_outline.json", [])
        if isinstance(layered, list):
            if isinstance(data, list):
                layered.extend(data)
            elif isinstance(data, dict):
                layered.append(data)
            write_json(base_dir / "outlines" / "layered_outline.json", layered)
    elif f_type == "complete_book":
        prog = read_json(base_dir / "meta" / "progress.json", {})
        prog["phase"] = "completed"
        write_json(base_dir / "meta" / "progress.json", prog)
        
    missing = get_missing_foundation(base_dir)
    if not missing:
        prog = read_json(base_dir / "meta" / "progress.json", {})
        if prog.get("phase") == "init":
            prog["phase"] = "writing"
        write_json(base_dir / "meta" / "progress.json", prog)
        
    return {"status": "saved", "type": f_type, "missing_foundation": missing}

def plan_chapter(base_dir: Path, chapter: int, plan_data: Dict[str, Any]) -> Dict[str, Any]:
    valid_plan = validate_chapter_plan(plan_data)
    plan_file = base_dir / "drafts" / f"{chapter:02d}.plan.json"
    write_json(plan_file, valid_plan)
    return {"status": "planned", "chapter": chapter, "file": str(plan_file), "plan": valid_plan}

def reopen_chapters(base_dir: Path, chapters: List[int], reason: str) -> Dict[str, Any]:
    prog = read_json(base_dir / "meta" / "progress.json", {})
    if "pending_rewrites" not in prog:
        prog["pending_rewrites"] = []
    for ch in chapters:
        if ch not in prog["pending_rewrites"]:
            prog["pending_rewrites"].append(ch)
    prog["pending_rewrites"].sort()
    prog["flow"] = "rewriting"
    prog["rewrite_reason"] = reason
    write_json(base_dir / "meta" / "progress.json", prog)
    return {"status": "reopened", "pending_rewrites": prog["pending_rewrites"], "reason": reason}

# ----------------------------------------------------------------------
# CLI Entry Point
# ----------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="AI Novel Studio 2.0 (Agent-Led, Engine-Guarded)")
    parser.add_argument("--dir", default=None, help="Thư mục tiểu thuyết")

    subparsers = parser.add_subparsers(dest="command", required=True)

    # status
    subparsers.add_parser("status")

    # suggest-next & route-next
    subparsers.add_parser("suggest-next")
    subparsers.add_parser("route-next")

    # set-mode
    p_sm = subparsers.add_parser("set-mode")
    p_sm.add_argument("--mode", required=True, choices=["manual", "guided", "auto"])

    # summary
    p_sum = subparsers.add_parser("summary")
    p_sum.add_argument("--chapter", type=int, default=None)

    # threads
    subparsers.add_parser("threads")

    # context & get-context
    p_ctx = subparsers.add_parser("context")
    p_ctx.add_argument("--chapter", type=int, default=0)
    p_get_ctx = subparsers.add_parser("get-context")
    p_get_ctx.add_argument("--chapter", type=int, default=0)

    # plan & plan-chapter
    p_plan = subparsers.add_parser("plan")
    p_plan.add_argument("--chapter", type=int, required=True)
    p_plan.add_argument("--data", default=None)
    p_plan.add_argument("--file", default=None)
    
    p_plan_ch = subparsers.add_parser("plan-chapter")
    p_plan_ch.add_argument("--chapter", type=int, required=True)
    p_plan_ch.add_argument("--data", default=None)
    p_plan_ch.add_argument("--file", default=None)

    # draft & draft-chapter
    p_draft = subparsers.add_parser("draft")
    p_draft.add_argument("--chapter", type=int, required=True)
    p_draft.add_argument("--content", default=None)
    p_draft.add_argument("--content-file", default=None)
    p_draft.add_argument("--facts", default=None)
    p_draft.add_argument("--facts-file", default=None)
    p_draft.add_argument("--mode", choices=["write", "append"], default="write")
    p_draft.add_argument("--note", default="")
    
    p_draft_ch = subparsers.add_parser("draft-chapter")
    p_draft_ch.add_argument("--chapter", type=int, required=True)
    p_draft_ch.add_argument("--content", default=None)
    p_draft_ch.add_argument("--content-file", default=None)
    p_draft_ch.add_argument("--facts", default=None)
    p_draft_ch.add_argument("--facts-file", default=None)
    p_draft_ch.add_argument("--mode", choices=["write", "append"], default="write")
    p_draft_ch.add_argument("--note", default="")

    # branch
    p_br = subparsers.add_parser("branch")
    p_br.add_argument("--chapter", type=int, required=True)
    p_br.add_argument("--name", required=True, help="Tên nhánh A/B (ví dụ: phuong_an_A)")
    p_br.add_argument("--content", default=None)
    p_br.add_argument("--content-file", default=None)
    p_br.add_argument("--facts", default=None)
    p_br.add_argument("--note", default="")

    # diff
    p_diff = subparsers.add_parser("diff")
    p_diff.add_argument("--chapter", type=int, required=True)
    p_diff.add_argument("--rev-a", default=None)
    p_diff.add_argument("--rev-b", default=None)

    # accept
    p_accept = subparsers.add_parser("accept")
    p_accept.add_argument("--chapter", type=int, required=True)
    p_accept.add_argument("--rev", default=None)
    p_accept.add_argument("--reason", default="")
    p_accept.add_argument("--force", action="store_true")

    # reject
    p_reject = subparsers.add_parser("reject")
    p_reject.add_argument("--chapter", type=int, required=True)
    p_reject.add_argument("--rev", default=None)
    p_reject.add_argument("--reason", default="")
    p_reject.add_argument("--force", action="store_true")

    # impact & impact-check
    p_impact = subparsers.add_parser("impact")
    p_impact.add_argument("--chapter", type=int, required=True)
    p_imp_chk = subparsers.add_parser("impact-check")
    p_imp_chk.add_argument("--chapter", type=int, required=True)

    # rebuild & sync-context
    subparsers.add_parser("rebuild")
    subparsers.add_parser("sync-context")

    # init
    p_init = subparsers.add_parser("init")
    p_init.add_argument("--name", required=True)
    p_init.add_argument("--scale", choices=["short", "mid", "long"], default="long")
    p_init.add_argument("--premise", default="")
    p_init.add_argument("--force", action="store_true", help="Khởi tạo đè lên store đã có")
    p_init.add_argument("--resume", action="store_true", help="Tiếp tục sử dụng store đã có")

    # list-novels
    p_list = subparsers.add_parser("list-novels")
    p_list.add_argument("--root", default=None)

    # import-novel
    p_imp_nov = subparsers.add_parser("import-novel")
    p_imp_nov.add_argument("--file", required=True)
    p_imp_nov.add_argument("--name", required=True)
    p_imp_nov.add_argument("--scale", choices=["short", "mid", "long"], default="long")

    # style-lint
    p_lint = subparsers.add_parser("style-lint")
    p_lint.add_argument("--chapter", type=int, default=None)

    # snapshot
    p_snap = subparsers.add_parser("snapshot")
    snap_sub = p_snap.add_subparsers(dest="snap_action", required=True)
    p_sc = snap_sub.add_parser("create")
    p_sc.add_argument("--name", required=True)
    p_sc.add_argument("--note", default="")
    snap_sub.add_parser("list")
    p_sr = snap_sub.add_parser("restore")
    p_sr.add_argument("--name", required=True)

    # export
    p_exp = subparsers.add_parser("export")
    p_exp.add_argument("--output", default=None)

    # save-foundation
    p_found = subparsers.add_parser("save-foundation")
    p_found.add_argument("--type", required=True, choices=["premise", "characters", "world_rules", "outline", "layered_outline", "compass", "expand_arc", "complete_book"])
    p_found.add_argument("--data", required=True)
    p_found.add_argument("--scale", default="long")

    # save-review
    p_rev_save = subparsers.add_parser("save-review")
    p_rev_save.add_argument("--chapter", type=int, required=True)
    p_rev_save.add_argument("--data", default=None)
    p_rev_save.add_argument("--file", default=None)

    # reopen
    p_reopen = subparsers.add_parser("reopen")
    p_reopen.add_argument("--chapter", type=int, nargs="+", required=True)
    p_reopen.add_argument("--reason", required=True)

    # commit-chapter (Legacy backward-compatible handler)
    p_commit = subparsers.add_parser("commit-chapter")
    p_commit.add_argument("--chapter", type=int, required=True)
    p_commit.add_argument("--data", default=None)
    p_commit.add_argument("--file", default=None)

    args = parser.parse_args()

    try:
        if args.command == "list-novels":
            root = Path(args.root) if args.root else Path(os.getcwd())
            res = list_all_novels(root)
            print(json.dumps(res, ensure_ascii=False, indent=2))
            return

        novel_name = getattr(args, "name", None)
        base_dir = get_base_dir(args.dir, novel_name=novel_name)

        if args.command == "init":
            res = init_novel_store(base_dir, args.name, args.scale, args.premise, force=args.force, resume=args.resume)
            print(json.dumps(res, ensure_ascii=False, indent=2))
        elif args.command == "set-mode":
            cfg = get_config(base_dir)
            cfg["interaction_mode"] = args.mode
            valid_cfg = set_config(base_dir, cfg)
            print(json.dumps({"status": "mode_updated", "config": valid_cfg}, ensure_ascii=False, indent=2))
        elif args.command == "status":
            res = get_status_dashboard(base_dir)
            print(json.dumps(res, ensure_ascii=False, indent=2))
        elif args.command in ["suggest-next", "route-next"]:
            opts = suggest_next_options(base_dir)
            if args.command == "route-next":
                first_opt = opts[0] if opts else {}
                print(json.dumps({
                    "agent": "writer" if "write" in first_opt.get("action", "") else "architect_short",
                    "task": first_opt.get("title", ""),
                    "reason": first_opt.get("reason", ""),
                    "chapter": first_opt.get("chapter", 1),
                    "options": opts
                }, ensure_ascii=False, indent=2))
            else:
                print(json.dumps(opts, ensure_ascii=False, indent=2))
        elif args.command == "summary":
            res = get_summaries_hierarchy(base_dir, args.chapter)
            print(json.dumps(res, ensure_ascii=False, indent=2))
        elif args.command == "threads":
            res = get_open_threads(base_dir)
            print(json.dumps(res, ensure_ascii=False, indent=2))
        elif args.command in ["context", "get-context"]:
            res = get_full_context(base_dir, args.chapter)
            print(json.dumps(res, ensure_ascii=False, indent=2))
        elif args.command in ["plan", "plan-chapter"]:
            raw_data = load_payload(getattr(args, "data", None), getattr(args, "file", None))
            if not isinstance(raw_data, dict):
                raise ValueError("Dữ liệu plan phải là một JSON object.")
            res = plan_chapter(base_dir, args.chapter, raw_data)
            print(json.dumps(res, ensure_ascii=False, indent=2))
        elif args.command in ["draft", "draft-chapter"]:
            content = resolve_content(getattr(args, "content_file", None) or getattr(args, "content", ""))
            facts_val = load_payload(getattr(args, "facts", None), getattr(args, "facts_file", None))
            if facts_val and not isinstance(facts_val, dict):
                facts_val = None
            res = save_draft_revision(base_dir, args.chapter, content, facts_val, args.mode, args.note)
            print(json.dumps(res, ensure_ascii=False, indent=2))
        elif args.command == "branch":
            content = resolve_content(getattr(args, "content_file", None) or getattr(args, "content", ""))
            facts_val = load_payload(getattr(args, "facts", None), None)
            if facts_val and not isinstance(facts_val, dict):
                facts_val = None
            res = save_draft_revision(base_dir, args.chapter, content, facts_val, note=args.note, branch=args.name)
            print(json.dumps(res, ensure_ascii=False, indent=2))
        elif args.command == "diff":
            res = diff_revisions(base_dir, args.chapter, args.rev_a, args.rev_b)
            print(json.dumps(res, ensure_ascii=False, indent=2))
        elif args.command == "accept":
            res = accept_revision(base_dir, args.chapter, args.rev, reason=args.reason, force=args.force)
            print(json.dumps(res, ensure_ascii=False, indent=2))
        elif args.command == "reject":
            res = reject_revision(base_dir, args.chapter, args.rev, reason=args.reason, force=args.force)
            print(json.dumps(res, ensure_ascii=False, indent=2))
        elif args.command in ["impact", "impact-check"]:
            res = impact_analysis(base_dir, args.chapter)
            print(json.dumps(res, ensure_ascii=False, indent=2))
        elif args.command in ["rebuild", "sync-context"]:
            res = rebuild_all_projections(base_dir)
            print(json.dumps(res, ensure_ascii=False, indent=2))
        elif args.command == "commit-chapter":
            facts_data = load_payload(getattr(args, "data", None), getattr(args, "file", None))
            draft_path = base_dir / "drafts" / f"{args.chapter:02d}.draft.md"
            content = read_file(draft_path)
            if not content:
                content = read_file(base_dir / "chapters" / f"{args.chapter:02d}.md")
            draft_res = save_draft_revision(base_dir, args.chapter, content, facts_data, note="Auto commit")
            accept_res = accept_revision(base_dir, args.chapter, draft_res["revision"])
            print(json.dumps(accept_res, ensure_ascii=False, indent=2))
        elif args.command == "save-review":
            review_data = load_payload(getattr(args, "data", None), getattr(args, "file", None))
            if not isinstance(review_data, dict):
                raise ValueError("Review data phải là JSON object.")
            res = save_review_scorecard(base_dir, args.chapter, review_data)
            print(json.dumps(res, ensure_ascii=False, indent=2))
        elif args.command == "save-foundation":
            try:
                data = json.loads(args.data)
            except Exception:
                data = args.data
            res = save_foundation(base_dir, args.type, data, args.scale)
            print(json.dumps(res, ensure_ascii=False, indent=2))
        elif args.command == "reopen":
            res = reopen_chapters(base_dir, args.chapter, args.reason)
            print(json.dumps(res, ensure_ascii=False, indent=2))
        elif args.command == "style-lint":
            res = style_lint(base_dir, args.chapter)
            print(json.dumps(res, ensure_ascii=False, indent=2))
        elif args.command == "snapshot":
            if args.snap_action == "create":
                res = snapshot_create(base_dir, args.name, args.note)
            elif args.snap_action == "list":
                res = snapshot_list(base_dir)
            elif args.snap_action == "restore":
                res = snapshot_restore(base_dir, args.name)
            print(json.dumps(res, ensure_ascii=False, indent=2))
        elif args.command == "import-novel":
            res = import_novel(args.file, args.name, args.scale, base_dir)
            print(json.dumps(res, ensure_ascii=False, indent=2))
        elif args.command == "export":
            path = export_novel(base_dir, args.output)
            print(json.dumps({"status": "exported", "file": path}, ensure_ascii=False, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False, indent=2), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
