# -*- coding: utf-8 -*-
"""
Studio Schemas & Data Contracts
Định nghĩa cấu trúc dữ liệu và trình kiểm định schema (Validators) cho Fact, Revision, Config, Review, Plan và Decision.
Hoàn toàn đồng bộ với các tài liệu quy chuẩn (chapter-contract.md, quality-checklist.md).
"""

from typing import Dict, Any, List, Optional
from datetime import datetime

DEFAULT_CONFIG: Dict[str, Any] = {
    "interaction_mode": "guided",
    "approval_required": {
        "foundation": True,
        "chapter_plan": False,
        "chapter_commit": True,
        "rewrite": True,
        "downstream_rewrite": True
    },
    "quality_gate": "advisory"
}

def validate_config(cfg: Any) -> Dict[str, Any]:
    """Kiểm tra tính hợp lệ của cấu hình studio."""
    if not isinstance(cfg, dict):
        raise ValueError("Cấu hình phải là một JSON object.")
        
    mode = cfg.get("interaction_mode", "guided")
    if mode not in ["manual", "guided", "auto"]:
        raise ValueError(f"Chế độ interaction_mode không hợp lệ: '{mode}'. Chỉ chấp nhận: 'manual', 'guided', 'auto'.")
        
    qgate = cfg.get("quality_gate", "advisory")
    if qgate not in ["strict", "advisory"]:
        raise ValueError(f"Quality gate không hợp lệ: '{qgate}'. Chỉ chấp nhận: 'strict', 'advisory'.")
        
    app_req = cfg.get("approval_required", {})
    if not isinstance(app_req, dict):
        app_req = DEFAULT_CONFIG["approval_required"]
        
    return {
        "interaction_mode": mode,
        "approval_required": {
            "foundation": bool(app_req.get("foundation", True)),
            "chapter_plan": bool(app_req.get("chapter_plan", False)),
            "chapter_commit": bool(app_req.get("chapter_commit", True)),
            "rewrite": bool(app_req.get("rewrite", True)),
            "downstream_rewrite": bool(app_req.get("downstream_rewrite", True))
        },
        "quality_gate": qgate
    }

def validate_chapter_plan(plan: Any) -> Dict[str, Any]:
    """Kiểm tra tính hợp lệ của Hợp đồng chương (Chapter Contract). Hỗ trợ cả top-level lẫn nested contract."""
    if not isinstance(plan, dict) or not plan:
        raise ValueError("Chapter Plan không được để rỗng. Cần có tối thiểu 'goal' và 'required_beats'.")
        
    contract = plan.get("contract", {}) if isinstance(plan.get("contract"), dict) else {}
    
    # 1. Goal
    goal = str(plan.get("goal") or contract.get("goal") or "").strip()
    if not goal:
        raise ValueError("Chapter Plan thiếu mục tiêu chính 'goal'.")
        
    # 2. Scenes
    scenes = plan.get("scenes") or contract.get("scenes") or []
    if not isinstance(scenes, list) or len(scenes) == 0:
        raise ValueError("Chapter Plan cần có danh sách phân cảnh 'scenes' tối thiểu 1 cảnh.")
        
    # 3. Required Beats (hỗ trợ cả top-level lẫn contract.required_beats/contract.beats)
    required_beats = plan.get("required_beats") or contract.get("required_beats") or contract.get("beats") or []
    if not isinstance(required_beats, list) or len(required_beats) == 0:
        raise ValueError("Chapter Plan cần có danh sách 'required_beats' (các nhịp bắt buộc phải có).")
        
    forbidden_moves = plan.get("forbidden_moves") or contract.get("forbidden_moves") or []
    payoff_points = plan.get("payoff_points") or contract.get("payoff_points") or []
    hook_goal = str(plan.get("hook_goal") or contract.get("hook_goal") or "")

    return {
        "goal": goal,
        "scenes": scenes,
        "required_beats": required_beats,
        "forbidden_moves": forbidden_moves,
        "payoff_points": payoff_points,
        "hook_goal": hook_goal,
        "planned_at": plan.get("planned_at", datetime.now().isoformat())
    }

def validate_facts(facts: Any) -> Dict[str, Any]:
    """Kiểm tra và chuẩn hóa cấu trúc Fact của một revision."""
    if not isinstance(facts, dict):
        raise ValueError("Facts phải là một JSON object.")
        
    chapter = facts.get("chapter")
    if not isinstance(chapter, int) or chapter <= 0:
        raise ValueError(f"Số chương trong facts không hợp lệ: {chapter}")
        
    summary = facts.get("summary", "")
    if not isinstance(summary, str):
        summary = str(summary)
        
    raw_ev = facts.get("timeline_events", [])
    events = []
    if isinstance(raw_ev, list):
        for ev in raw_ev:
            if isinstance(ev, dict) and ev.get("event"):
                events.append({
                    "time": str(ev.get("time", "")),
                    "event": str(ev.get("event")),
                    "chapter": chapter
                })
                
    raw_fs = facts.get("foreshadow_updates", [])
    foreshadows = []
    if isinstance(raw_fs, list):
        for fs in raw_fs:
            if isinstance(fs, dict) and fs.get("id"):
                action = fs.get("action", "plant")
                status = fs.get("status", "active")
                if action == "resolve" or status == "resolved":
                    status = "resolved"
                foreshadows.append({
                    "id": str(fs.get("id")),
                    "description": str(fs.get("description", "")),
                    "action": action,
                    "status": status,
                    "notes": str(fs.get("notes", ""))
                })
                
    raw_cast = facts.get("cast", [])
    cast = []
    if isinstance(raw_cast, list):
        for c in raw_cast:
            if isinstance(c, dict) and c.get("name"):
                cast.append({
                    "name": str(c.get("name")),
                    "brief_role": str(c.get("brief_role", "")),
                    "first_seen": c.get("first_seen", chapter),
                    "last_seen": c.get("last_seen", chapter)
                })
            elif isinstance(c, str) and c.strip():
                cast.append({
                    "name": c.strip(),
                    "brief_role": "",
                    "first_seen": chapter,
                    "last_seen": chapter
                })
                
    raw_rel = facts.get("relationship_changes", [])
    rels = []
    if isinstance(raw_rel, list):
        for r in raw_rel:
            if isinstance(r, dict) and r.get("pair"):
                rels.append({
                    "pair": str(r.get("pair")),
                    "status": str(r.get("status", "")),
                    "action": str(r.get("action", "update"))
                })
                
    raw_states = facts.get("state_changes", [])
    state_changes = []
    if isinstance(raw_states, list):
        for st in raw_states:
            if isinstance(st, dict) and st.get("key"):
                state_changes.append({
                    "key": str(st.get("key")),
                    "value": st.get("value"),
                    "chapter": chapter
                })
                
    raw_dep = facts.get("dependencies", [])
    dependencies = [str(d) for d in raw_dep if d] if isinstance(raw_dep, list) else []

    return {
        "chapter": chapter,
        "revision": str(facts.get("revision", "r001")),
        "created_at": facts.get("created_at", datetime.now().isoformat()),
        "summary": summary,
        "timeline_events": events,
        "foreshadow_updates": foreshadows,
        "cast": cast,
        "relationship_changes": rels,
        "state_changes": state_changes,
        "dependencies": dependencies
    }

def validate_review_scorecard(review: Any, quality_gate_mode: str = "advisory") -> Dict[str, Any]:
    """Kiểm tra và chấm điểm biên tập 7 chiều theo chuẩn quality-checklist.md."""
    if not isinstance(review, dict) or not review:
        raise ValueError("Review Scorecard không được để rỗng.")
        
    clean_scores = {}
    dimensions = ["consistency", "character", "continuity", "pacing", "foreshadow", "hook", "aesthetic"]
    
    # 1. Trích xuất chính xác điểm từ scores{} hoặc dimensions[]
    if isinstance(review.get("scores"), dict):
        raw_scores = review["scores"]
        for d in dimensions:
            if d in raw_scores:
                try:
                    clean_scores[d] = max(0, min(100, int(raw_scores[d])))
                except (ValueError, TypeError):
                    clean_scores[d] = 0
            else:
                clean_scores[d] = 0
    elif isinstance(review.get("dimensions"), list):
        for item in review["dimensions"]:
            if isinstance(item, dict):
                d_key = str(item.get("dimension") or item.get("name") or "").lower()
                if d_key in dimensions:
                    try:
                        clean_scores[d_key] = max(0, min(100, int(item.get("score", 0))))
                    except (ValueError, TypeError):
                        clean_scores[d_key] = 0
        for d in dimensions:
            if d not in clean_scores:
                clean_scores[d] = 0
    else:
        raise ValueError("Review Scorecard thiếu trường 'scores' hoặc 'dimensions'.")
            
    # 2. Chuẩn hóa contract_status (hỗ trợ 'met', 'fulfilled', 'partial', 'missed')
    raw_status = str(review.get("contract_status", "met")).lower()
    if raw_status in ["met", "fulfilled"]:
        contract_status = "fulfilled"
    elif raw_status in ["partial"]:
        contract_status = "partial"
    else:
        contract_status = "missed"
        
    verdict = str(review.get("verdict", "accept")).lower()
    if verdict not in ["accept", "polish", "rewrite"]:
        verdict = "accept"
        
    min_score = min(clean_scores.values()) if clean_scores else 0
    avg_score = sum(clean_scores.values()) / max(1, len(clean_scores))
    
    # 3. Quality Gate Rules Check:
    # Accept: tất cả các chiều >= 80 và contract fulfilled
    # Polish: bất kỳ chiều < 80 hoặc contract partial
    # Rewrite: bất kỳ chiều < 60 hoặc contract missed
    warnings = []
    failed_dimensions = [d for d, s in clean_scores.items() if s < 80]
    critical_dimensions = [d for d, s in clean_scores.items() if s < 60]
    
    requires_rewrite = len(critical_dimensions) > 0 or contract_status == "missed" or avg_score < 60
    requires_polish = len(failed_dimensions) > 0 or contract_status == "partial"
    
    if verdict == "accept" and (requires_rewrite or requires_polish):
        if quality_gate_mode == "strict":
            if requires_rewrite:
                raise ValueError(
                    f"Bản thảo không đạt Quality Gate Strict (Điểm thấp: {critical_dimensions}, contract={contract_status}). "
                    f"Verdict bắt buộc phải là 'rewrite'."
                )
            else:
                raise ValueError(
                    f"Bản thảo không đạt Quality Gate Strict (Chưa đạt chuẩn >= 80 tại: {failed_dimensions}, contract={contract_status}). "
                    f"Verdict bắt buộc phải là 'polish' hoặc 'rewrite'."
                )
        else:
            warnings.append(
                f"CẢNH BÁO QUALITY GATE: Bản thảo chưa đạt chuẩn chất lượng (min_score={min_score}, failed={failed_dimensions}, contract={contract_status}) nhưng được chấp nhận (Override)."
            )
            
    return {
        "scores": clean_scores,
        "average_score": round(avg_score, 1),
        "contract_status": contract_status,
        "verdict": verdict,
        "reason": review.get("reason", ""),
        "affected_chapters": review.get("affected_chapters", []),
        "warnings": warnings,
        "reviewed_at": review.get("reviewed_at", datetime.now().isoformat())
    }

def create_fact_schema(
    chapter: int,
    revision: str,
    summary: str = "",
    timeline_events: Optional[List[Dict[str, Any]]] = None,
    foreshadow_updates: Optional[List[Dict[str, Any]]] = None,
    relationship_changes: Optional[List[Dict[str, Any]]] = None,
    state_changes: Optional[List[Dict[str, Any]]] = None,
    cast: Optional[List[Dict[str, Any]]] = None,
    dependencies: Optional[List[str]] = None
) -> Dict[str, Any]:
    """Tạo đối tượng Fact chuẩn cho một revision chương."""
    raw = {
        "chapter": chapter,
        "revision": revision,
        "summary": summary,
        "timeline_events": timeline_events or [],
        "foreshadow_updates": foreshadow_updates or [],
        "relationship_changes": relationship_changes or [],
        "state_changes": state_changes or [],
        "cast": cast or [],
        "dependencies": dependencies or []
    }
    return validate_facts(raw)

def create_decision_record(
    action: str,
    actor: str,
    chapter: Optional[int] = None,
    revision: Optional[str] = None,
    reason: str = "",
    override: bool = False,
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Tạo bản ghi quyết định lưu vào decisions.jsonl."""
    return {
        "timestamp": datetime.now().isoformat(),
        "action": action,
        "actor": actor,
        "chapter": chapter,
        "revision": revision,
        "reason": reason,
        "override": override,
        "metadata": metadata or {}
    }
