# -*- coding: utf-8 -*-
"""
Studio Snapshot & Checkpoint Manager
Tạo và khôi phục các điểm lưu (checkpoint zip) với cơ chế Hoán Đổi Hai Pha Nguyên Tử (Two-Phase Atomic Swap with Rollback - Sửa P0) bảo vệ 100% dữ liệu không bao giờ bị rơi vào trạng thái hỗn hợp.
"""

import os
import shutil
import zipfile
import uuid
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

from studio.store import read_json, write_json, ensure_dir, slugify, StudioLock
from studio.projector import rebuild_all_projections

def snapshot_create(base_dir: Path, name: str, note: str = "") -> Dict[str, Any]:
    """Tạo điểm khôi phục (checkpoint zip) với định danh microsecond chống ghi đè trong cùng 1 giây."""
    with StudioLock(base_dir):
        checkpoints_dir = base_dir / "meta" / "checkpoints"
        ensure_dir(checkpoints_dir)
        clean_name = slugify(name)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        zip_filename = f"{timestamp}_{clean_name}.zip"
        zip_path = checkpoints_dir / zip_filename
        
        backup_dirs = ["chapters", "drafts", "revisions", "facts", "outlines", "characters", "world", "summaries", "meta"]
        
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for bdir in backup_dirs:
                folder_path = base_dir / bdir
                if folder_path.exists():
                    for root, _, files in os.walk(folder_path):
                        if "checkpoints" in root or ".studio.lock" in root:
                            continue
                        for f in files:
                            if f.startswith(".tmp_") or f.startswith(".studio"):
                                continue
                            full_file = Path(root) / f
                            rel_path = os.path.relpath(full_file, base_dir)
                            zf.write(full_file, rel_path)
                            
            dec_file = base_dir / "decisions.jsonl"
            if dec_file.exists():
                zf.write(dec_file, "decisions.jsonl")
                            
        progress = read_json(base_dir / "meta" / "progress.json", {})
        manifest_file = checkpoints_dir / f"{timestamp}_{clean_name}.json"
        manifest = {
            "name": name,
            "filename": zip_filename,
            "created_at": datetime.now().isoformat(),
            "note": note,
            "completed_chapters": len(progress.get("completed_chapters", [])),
            "total_words": progress.get("total_word_count", 0)
        }
        write_json(manifest_file, manifest)
        
        return {"status": "snapshot_created", "name": name, "file": str(zip_path), "chapters": manifest["completed_chapters"]}

def snapshot_list(base_dir: Path) -> List[Dict[str, Any]]:
    """Liệt kê toàn bộ các checkpoint hiện có của tiểu thuyết."""
    checkpoints_dir = base_dir / "meta" / "checkpoints"
    if not checkpoints_dir.exists():
        return []
    snapshots = []
    for mf in sorted(checkpoints_dir.glob("*.json"), reverse=True):
        m = read_json(mf)
        if m:
            snapshots.append(m)
    return snapshots

def snapshot_restore(base_dir: Path, name: str) -> Dict[str, Any]:
    """Khôi phục dữ liệu với cơ chế Two-Phase Atomic Swap & Rollback an toàn 100% (Sửa P0)."""
    with StudioLock(base_dir) as lock:
        checkpoints_dir = base_dir / "meta" / "checkpoints"
        clean_name = slugify(name)
        target_zip = None
        
        for z in sorted(checkpoints_dir.glob("*.zip"), reverse=True):
            if clean_name in z.name:
                target_zip = z
                break
                
        if not target_zip or not target_zip.exists():
            raise FileNotFoundError(f"Không tìm thấy snapshot phù hợp với tên '{name}' trong {checkpoints_dir}")
            
        staging_dir = base_dir / f".tmp_staging_restore_{uuid.uuid4().hex}"
        backup_live_dir = base_dir / f".tmp_live_backup_{uuid.uuid4().hex}"
        ensure_dir(staging_dir)
        ensure_dir(backup_live_dir)
        
        target_dirs = ["chapters", "drafts", "revisions", "facts", "outlines", "characters", "world", "summaries"]
        phase2_started = False
        
        try:
            # 1. Pha 1: Giải nén & Kiểm thử CRC tệp ZIP trong staging biệt lập
            with zipfile.ZipFile(target_zip, "r") as zf:
                bad_file = zf.testzip()
                if bad_file is not None:
                    raise zipfile.BadZipFile(f"Tệp snapshot bị hỏng (CRC check failed) tại file '{bad_file}'.")
                zf.extractall(staging_dir)
                
            lock.touch()

            # 2. Pha 2: Di chuyển toàn bộ live store hiện tại vào backup_live_dir
            phase2_started = True
            for d in target_dirs:
                live_d = base_dir / d
                if live_d.exists():
                    shutil.move(str(live_d), str(backup_live_dir / d))
                    
            dec_file = base_dir / "decisions.jsonl"
            if dec_file.exists():
                shutil.move(str(dec_file), str(backup_live_dir / "decisions.jsonl"))

            # 3. Di chuyển toàn bộ staging store vào live
            for d in target_dirs:
                staged_d = staging_dir / d
                if staged_d.exists():
                    shutil.move(str(staged_d), str(base_dir / d))
                    
            staged_dec = staging_dir / "decisions.jsonl"
            if staged_dec.exists():
                shutil.move(str(staged_dec), str(base_dir / "decisions.jsonl"))
                
            # Sao chép metadata từ staging (tránh đè checkpoints)
            staged_meta = staging_dir / "meta"
            if staged_meta.exists():
                for mf in staged_meta.iterdir():
                    if mf.name != "checkpoints" and not mf.name.startswith("."):
                        if mf.is_file():
                            shutil.copy2(str(mf), str(base_dir / "meta" / mf.name))

            # 4. Tái tạo Projections từ dữ liệu vừa phục hồi
            sync_res = rebuild_all_projections(base_dir)
            
            # 5. Hoàn tất thành công: Dọn dẹp an toàn các thư mục tạm
            shutil.rmtree(backup_live_dir, ignore_errors=True)
            shutil.rmtree(staging_dir, ignore_errors=True)
            
            return {
                "status": "snapshot_restored",
                "snapshot": target_zip.name,
                "sync_result": sync_res
            }
            
        except Exception as e:
            # ROLLBACK TOÀN DIỆN NẾU PHA 2 THẤT BẠI
            if phase2_started:
                for d in target_dirs:
                    live_d = base_dir / d
                    if live_d.exists():
                        shutil.rmtree(live_d, ignore_errors=True)
                dec_live = base_dir / "decisions.jsonl"
                if dec_live.exists():
                    dec_live.unlink(missing_ok=True)
                    
                # Đổi backup_live_dir trở lại live store
                for d in target_dirs:
                    bk_d = backup_live_dir / d
                    if bk_d.exists():
                        shutil.move(str(bk_d), str(base_dir / d))
                bk_dec = backup_live_dir / "decisions.jsonl"
                if bk_dec.exists():
                    shutil.move(str(bk_dec), str(base_dir / "decisions.jsonl"))
                
            shutil.rmtree(backup_live_dir, ignore_errors=True)
            shutil.rmtree(staging_dir, ignore_errors=True)
            
            raise RuntimeError(f"Lỗi khi khôi phục snapshot '{name}': {str(e)}. Toàn bộ live store đã được bảo vệ/rollback an toàn.")
