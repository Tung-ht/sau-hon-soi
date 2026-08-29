# -*- coding: utf-8 -*-
"""
Studio Store & Path Management
Quản lý I/O tệp, cấu trúc thư mục dự án, atomic write, StudioLock đa tác nhân liveness-aware và định tuyến đường dẫn.
"""

import sys
import os
import json
import re
import unicodedata
import time
import uuid
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional
from studio.schemas import DEFAULT_CONFIG

DEFAULT_NOVELS_ROOT = "novels"

def is_process_alive(pid: int) -> bool:
    """Kiểm tra tiến trình sở hữu lock còn sống hay đã chết để dọn lock treo ngay lập tức."""
    if pid <= 0 or pid == os.getpid():
        return True
    if os.name == 'nt':
        try:
            import ctypes
            PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
            SYNCHRONIZE = 0x00100000
            handle = ctypes.windll.kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION | SYNCHRONIZE, False, pid)
            if handle:
                ctypes.windll.kernel32.CloseHandle(handle)
                return True
            return False
        except Exception:
            return True
    else:
        try:
            os.kill(pid, 0)
            return True
        except OSError:
            return False

def slugify(text: str) -> str:
    """Chuyển đổi tên truyện tiếng Việt thành slug thư mục sạch sẽ (ví dụ: 'Lời Trăn Trối' -> 'loi-tran-troi')"""
    if not text:
        return "unnamed-novel"
    text = text.replace('Đ', 'D').replace('đ', 'd')
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')
    text = re.sub(r'[^\w\s-]', '', text.lower())
    slug = re.sub(r'[-\s]+', '-', text).strip('-')
    return slug or "unnamed-novel"

def get_base_dir(custom_path: Optional[str] = None, novel_name: Optional[str] = None) -> Path:
    """Xác định đường dẫn thư mục của tiểu thuyết trong novels/<slug>."""
    if custom_path:
        p = Path(custom_path)
        if not p.is_absolute():
            p = Path(os.getcwd()) / p
        return p
    if novel_name:
        return Path(os.getcwd()) / DEFAULT_NOVELS_ROOT / slugify(novel_name)
        
    # Tự động nhận diện nếu chỉ có 1 bộ tiểu thuyết duy nhất trong thư mục novels/
    novels_folder = Path(os.getcwd()) / DEFAULT_NOVELS_ROOT
    if novels_folder.exists() and novels_folder.is_dir():
        valid_novels = [d for d in novels_folder.iterdir() if d.is_dir() and (d / "meta" / "progress.json").exists()]
        if len(valid_novels) == 1:
            return valid_novels[0]
            
    return Path(os.getcwd()) / DEFAULT_NOVELS_ROOT / "unnamed-novel"

def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path

import threading

_local_lock = threading.local()

class StudioLock:
    """Khóa tiến trình tái nhập (Re-entrant Process Lock) có liveness-checking và heartbeat."""
    def __init__(self, base_dir: Path, timeout: float = 30.0, retry_interval: float = 0.05):
        self.base_dir = base_dir.resolve()
        self.lock_dir = base_dir / "meta"
        self.lock_file = self.lock_dir / ".studio.lock"
        self.timeout = timeout
        self.retry_interval = retry_interval
        self.lock_token = str(uuid.uuid4())
        self.acquired = False

    def touch(self):
        """Làm mới thời gian heartbeat của lock cho các tác vụ dài."""
        if self.acquired and self.lock_file.exists():
            try:
                with open(self.lock_file, "w", encoding="utf-8") as f:
                    f.write(f"{self.lock_token}\n{os.getpid()}\n{time.time()}")
            except Exception:
                pass

    def __enter__(self):
        if not hasattr(_local_lock, "acquired_locks"):
            _local_lock.acquired_locks = {}
            
        store_key = str(self.base_dir)
        depth = _local_lock.acquired_locks.get(store_key, 0)
        if depth > 0:
            _local_lock.acquired_locks[store_key] = depth + 1
            self.acquired = True
            return self

        ensure_dir(self.lock_dir)
        start_time = time.time()
        while True:
            try:
                fd = os.open(str(self.lock_file), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                with os.fdopen(fd, "w", encoding="utf-8") as f:
                    f.write(f"{self.lock_token}\n{os.getpid()}\n{time.time()}")
                self.acquired = True
                _local_lock.acquired_locks[store_key] = 1
                return self
            except FileExistsError:
                try:
                    if self.lock_file.exists():
                        content = self.lock_file.read_text(encoding="utf-8").strip().splitlines()
                        if len(content) >= 2:
                            holder_pid = int(content[1])
                            holder_time = float(content[2]) if len(content) >= 3 else 0
                            if not is_process_alive(holder_pid) or (time.time() - holder_time > 120.0):
                                self.lock_file.unlink(missing_ok=True)
                                continue
                except Exception:
                    pass
                if time.time() - start_time > self.timeout:
                    raise TimeoutError(f"Không thể lấy khóa (lock) cho novel store tại '{self.lock_file}' sau {self.timeout}s.")
                time.sleep(self.retry_interval)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.acquired:
            store_key = str(self.base_dir)
            if hasattr(_local_lock, "acquired_locks") and store_key in _local_lock.acquired_locks:
                _local_lock.acquired_locks[store_key] -= 1
                if _local_lock.acquired_locks[store_key] <= 0:
                    del _local_lock.acquired_locks[store_key]
                    try:
                        if self.lock_file.exists():
                            self.lock_file.unlink(missing_ok=True)
                    except Exception:
                        pass
            self.acquired = False

def read_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default

def write_json(path: Path, data: Any) -> None:
    """Ghi JSON nguyên tử tuyệt đối (Unique Temp File + Flush + Fsync + Replace)."""
    ensure_dir(path.parent)
    unique_suffix = f"{os.getpid()}_{uuid.uuid4().hex}"
    temp_file = path.parent / f".tmp_{path.name}_{unique_suffix}"
    try:
        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.flush()
            os.fsync(f.fileno())
        temp_file.replace(path)
    except Exception:
        if temp_file.exists():
            temp_file.unlink(missing_ok=True)
        raise

def read_file(path: Path, default: str = "") -> str:
    if not path.exists():
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return default

def write_file(path: Path, content: str) -> None:
    """Ghi File nguyên tử tuyệt đối (Unique Temp File + Flush + Fsync + Replace)."""
    ensure_dir(path.parent)
    unique_suffix = f"{os.getpid()}_{uuid.uuid4().hex}"
    temp_file = path.parent / f".tmp_{path.name}_{unique_suffix}"
    try:
        with open(temp_file, "w", encoding="utf-8") as f:
            f.write(content)
            f.flush()
            os.fsync(f.fileno())
        temp_file.replace(path)
    except Exception:
        if temp_file.exists():
            temp_file.unlink(missing_ok=True)
        raise

def append_jsonl(path: Path, data: Dict[str, Any]) -> None:
    ensure_dir(path.parent)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")

def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    records = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                try:
                    records.append(json.loads(line))
                except Exception:
                    pass
    return records

def init_novel_store(
    base_dir: Path,
    name: str,
    scale: str = "long",
    premise: str = "",
    force: bool = False,
    resume: bool = False
) -> Dict[str, Any]:
    """Khởi tạo toàn bộ cấu trúc thư mục cho tiểu thuyết với cơ chế bảo vệ dữ liệu sẵn có và dọn dẹp sạch khi force."""
    with StudioLock(base_dir):
        prog_file = base_dir / "meta" / "progress.json"
        chapters_dir = base_dir / "chapters"
        has_existing_data = prog_file.exists() or (chapters_dir.exists() and any(chapters_dir.glob("*.md")))

        if has_existing_data and not force:
            if resume:
                prog = read_json(prog_file, {})
                return {
                    "status": "resumed",
                    "novel_name": prog.get("novel_name", name),
                    "completed_chapters": len(prog.get("completed_chapters", [])),
                    "dir": str(base_dir.resolve())
                }
            raise FileExistsError(
                f"Tiểu thuyết tại '{base_dir}' đã có dữ liệu. Hãy sử dụng cờ --resume để tiếp tục hoặc --force để khởi tạo lại từ đầu."
            )

        if force and base_dir.exists():
            clean_dirs = ["chapters", "drafts", "revisions", "facts", "outlines", "characters", "world", "summaries"]
            for d in clean_dirs:
                target_dir = base_dir / d
                if target_dir.exists():
                    shutil.rmtree(target_dir, ignore_errors=True)
            dec_file = base_dir / "decisions.jsonl"
            if dec_file.exists():
                dec_file.unlink(missing_ok=True)

        ensure_dir(base_dir / "outlines")
        ensure_dir(base_dir / "characters" / "snapshots")
        ensure_dir(base_dir / "world" / "reviews")
        ensure_dir(base_dir / "drafts")
        ensure_dir(base_dir / "revisions")
        ensure_dir(base_dir / "facts")
        ensure_dir(base_dir / "chapters")
        ensure_dir(base_dir / "summaries" / "arcs")
        ensure_dir(base_dir / "summaries" / "volumes")
        ensure_dir(base_dir / "meta" / "checkpoints")

        progress = {
            "novel_name": name,
            "phase": "init",
            "flow": "writing",
            "current_chapter": 1,
            "total_chapters": 0,
            "completed_chapters": [],
            "accepted_revisions": {},
            "chapter_word_counts": {},
            "total_word_count": 0,
            "in_progress_chapter": 0,
            "pending_rewrites": [],
            "rewrite_reason": "",
            "layered": (scale == "long"),
            "current_volume": 1 if scale == "long" else 0,
            "current_arc": 1 if scale == "long" else 0,
            "strand_history": [],
            "hook_history": []
        }
        write_json(base_dir / "meta" / "progress.json", progress)

        run_meta = {
            "planning_tier": scale,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        write_json(base_dir / "meta" / "run_meta.json", run_meta)
        write_json(base_dir / "meta" / "config.json", DEFAULT_CONFIG)
        write_json(base_dir / "meta" / "directives.json", [])
        write_json(base_dir / "characters" / "cast_ledger.json", [])
        write_json(base_dir / "world" / "foreshadow_ledger.json", [])
        write_json(base_dir / "world" / "relationships.json", {})
        write_json(base_dir / "world" / "state_changes.json", {})

        if premise:
            write_file(base_dir / "outlines" / "premise.md", premise)

        return {"status": "initialized", "novel_name": name, "scale": scale, "dir": str(base_dir.resolve())}

def get_config(base_dir: Path) -> Dict[str, Any]:
    cfg = read_json(base_dir / "meta" / "config.json")
    if not cfg:
        cfg = DEFAULT_CONFIG
        write_json(base_dir / "meta" / "config.json", cfg)
    return cfg

def set_config(base_dir: Path, config: Dict[str, Any]) -> Dict[str, Any]:
    with StudioLock(base_dir):
        from studio.schemas import validate_config
        valid_cfg = validate_config(config)
        write_json(base_dir / "meta" / "config.json", valid_cfg)
        return valid_cfg

def list_all_novels(root_dir: Optional[Path] = None) -> List[Dict[str, Any]]:
    """Quét toàn bộ workspace để liệt kê tất cả các tiểu thuyết hiện có trong novels/<slug>/."""
    if root_dir is None:
        root_dir = Path(os.getcwd())
    
    novels = []
    candidates = []
    
    novels_folder = root_dir / DEFAULT_NOVELS_ROOT
    if novels_folder.exists() and novels_folder.is_dir():
        for item in sorted(novels_folder.iterdir()):
            if item.is_dir():
                candidates.append(item)
                
    if (root_dir / "meta" / "progress.json").exists():
        candidates.append(root_dir)
    
    seen_dirs = set()
    for folder in candidates:
        prog_file = folder / "meta" / "progress.json"
            
        if prog_file.exists():
            base = folder
            base_resolved = str(base.resolve())
            if base_resolved in seen_dirs:
                continue
            seen_dirs.add(base_resolved)
            
            prog = read_json(prog_file)
            if prog:
                cfg = get_config(base)
                novels.append({
                    "name": prog.get("novel_name", folder.name),
                    "dir": base_resolved,
                    "relative_dir": os.path.relpath(base, root_dir),
                    "phase": prog.get("phase", "init"),
                    "flow": prog.get("flow", "writing"),
                    "interaction_mode": cfg.get("interaction_mode", "guided"),
                    "completed_chapters": len(prog.get("completed_chapters", [])),
                    "total_chapters": prog.get("total_chapters", 0),
                    "total_words": prog.get("total_word_count", 0),
                    "pending_rewrites": prog.get("pending_rewrites", [])
                })
                
    return novels
