from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_v5_integrity.py"

spec = importlib.util.spec_from_file_location("check_v5_integrity_extra", SCRIPT)
assert spec and spec.loader
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)


def test_quoted_duplicate_top_level_key_is_rejected():
    text = '''---
name: anti-hallucination-protocol
version: 5.4.2
"version": 5.4.3
description: x
author: x
license: MIT
platforms: [linux]
metadata:
  hermes: {}
---
body
'''
    _, _, errors = mod.parse_frontmatter(text)
    assert any("duplicate top-level key: version" in error for error in errors)
