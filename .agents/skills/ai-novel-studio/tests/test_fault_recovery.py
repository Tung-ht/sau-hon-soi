# -*- coding: utf-8 -*-
"""
Permanent Automated Fault Injection & Recovery Tests
"""

import sys
import unittest
import tempfile
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from studio.store import init_novel_store, read_file
from studio.revision import save_draft_revision, accept_revision
from studio.snapshot import snapshot_create, snapshot_restore

class TestFaultRecovery(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp_dir.name) / "test_novel"
        init_novel_store(self.base, "Test Fault Novel", "long")

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_corrupt_zip_recovery(self):
        ch1_text = "Nội dung chương 1 bất biến"
        d1 = save_draft_revision(self.base, 1, ch1_text, {"summary": "Tóm tắt"})
        accept_revision(self.base, 1, d1["revision"])
        
        snap = snapshot_create(self.base, "valid_snap")
        snap_path = Path(snap["file"])
        self.assertTrue(snap_path.exists())
        
        # Corrupt the ZIP
        with open(snap_path, "wb") as f:
            f.write(b"CORRUPT DATA GARBAGE")
            
        with self.assertRaises(Exception):
            snapshot_restore(self.base, "valid_snap")
            
        cur_ch1 = read_file(self.base / "chapters" / "01.md")
        self.assertEqual(cur_ch1, ch1_text, "Live chapter was lost during failed restore!")

if __name__ == "__main__":
    unittest.main()
