# -*- coding: utf-8 -*-
"""
Permanent Automated Core Studio Tests
"""

import sys
import unittest
import tempfile
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from studio.store import init_novel_store, read_json
from studio.revision import save_draft_revision, accept_revision, reject_revision, diff_revisions
from studio.projector import rebuild_all_projections
from studio.quality import save_review_scorecard

class TestCoreStudio(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp_dir.name) / "test_novel"
        init_novel_store(self.base, "Test Novel", "long", premise="Premise test")

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_workflow_cycle(self):
        d1 = save_draft_revision(self.base, 1, "Nội dung chương 1", {
            "summary": "Tóm tắt chương 1",
            "cast": [{"name": "Nam", "brief_role": "NV chính"}],
            "foreshadow_updates": [{"id": "fs_1", "description": "Phục bút 1", "status": "active"}]
        })
        self.assertEqual(d1["revision"], "r001")
        
        acc = accept_revision(self.base, 1, "r001")
        self.assertEqual(acc["status"], "revision_accepted")
        self.assertEqual(acc["projections"]["current_chapter"], 2)
        
        fs_list = read_json(self.base / "world" / "foreshadow_ledger.json", [])
        self.assertEqual(len(fs_list), 1)
        self.assertEqual(fs_list[0]["id"], "fs_1")
        
        rev_res = save_review_scorecard(self.base, 1, {
            "dimensions": [
                {"dimension": "consistency", "score": 85},
                {"dimension": "character", "score": 90},
                {"dimension": "continuity", "score": 85},
                {"dimension": "pacing", "score": 80},
                {"dimension": "foreshadow", "score": 85},
                {"dimension": "hook", "score": 80},
                {"dimension": "aesthetic", "score": 85}
            ],
            "contract_status": "met",
            "verdict": "accept"
        })
        self.assertEqual(rev_res["status"], "review_saved")
        self.assertGreaterEqual(rev_res["average_score"], 80.0)

if __name__ == "__main__":
    unittest.main()
