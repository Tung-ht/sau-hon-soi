# -*- coding: utf-8 -*-
"""
AI Novel Studio CLI Bridge
Tương thích ngược 100% với các lệnh novel_state.py và chuyển hướng sang studio.cli.
"""

import sys
import os
from pathlib import Path

# Đảm bảo đường dẫn scripts nằm trong sys.path
scripts_dir = Path(__file__).resolve().parent
if str(scripts_dir) not in sys.path:
    sys.path.insert(0, str(scripts_dir))

from studio.cli import main

if __name__ == "__main__":
    main()
