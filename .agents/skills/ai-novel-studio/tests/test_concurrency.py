# -*- coding: utf-8 -*-
"""
Permanent Automated Concurrency Tests
"""

import sys
import unittest
import tempfile
import concurrent.futures
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from studio.store import init_novel_store
from studio.revision import save_draft_revision

def worker_draft(base_dir_str, worker_id):
    base = Path(base_dir_str)
    return save_draft_revision(
        base, 1, f"Nội dung từ worker {worker_id}",
        {"summary": f"Tóm tắt {worker_id}", "timeline_events": [{"time": "12:00", "event": f"Event {worker_id}"}]}
    )

class TestConcurrency(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp_dir.name) / "test_novel"
        init_novel_store(self.base, "Test Concurrency Novel", "long")

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_concurrent_drafts(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            futures = [executor.submit(worker_draft, str(self.base), i) for i in range(1, 9)]
            results = [f.result() for f in futures]
            
        self.assertEqual(len(results), 8)
        rev_ids = [r["revision"] for r in results]
        self.assertEqual(len(set(rev_ids)), 8, f"Revision IDs collided: {rev_ids}")

if __name__ == "__main__":
    unittest.main()
