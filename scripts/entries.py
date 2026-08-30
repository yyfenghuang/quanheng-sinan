"""Shared entry loader for the 权衡司南 build scripts.

One job: read entry metadata off disk. Each build step imports this so the
definition of "an entry" and "published" lives in exactly one place.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENTRIES = ROOT / "entries"
SITE = ROOT / "_site"


def load_published():
    """Return published entry metadata dicts, newest first.

    Each dict carries the raw meta.json fields plus a "_slug" key resolved
    from the folder name. Drafts and unparseable meta.json files are skipped.
    """
    items = []
    if not ENTRIES.is_dir():
        return items
    for meta_path in sorted(ENTRIES.glob("*/meta.json")):
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if meta.get("status") != "published":
            continue
        meta["_slug"] = meta.get("slug") or meta_path.parent.name
        items.append(meta)
    items.sort(key=lambda m: m.get("date", ""), reverse=True)
    return items
