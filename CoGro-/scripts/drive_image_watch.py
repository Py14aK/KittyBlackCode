#!/usr/bin/env python3
"""Watch a Google Drive folder for new or changed images.

FA use: screenshot drops of T24, Jira, or VoP screens.
Does not upload secrets. Prints a manifest the Grok Drive connector can consume.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

IMAGE_EXT = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".tif", ".tiff", ".bmp"}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def scan(root: Path) -> list[dict]:
    rows = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in IMAGE_EXT:
            continue
        stat = path.stat()
        rows.append(
            {
                "path": str(path),
                "name": path.name,
                "bytes": stat.st_size,
                "mtime_utc": datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat(),
                "sha256": sha256_file(path),
            }
        )
    return rows


def diff(old: list[dict], new: list[dict]) -> dict:
    old_map = {r["path"]: r for r in old}
    new_map = {r["path"]: r for r in new}
    added = [r for p, r in new_map.items() if p not in old_map]
    removed = [r for p, r in old_map.items() if p not in new_map]
    changed = [
        r
        for p, r in new_map.items()
        if p in old_map and r["sha256"] != old_map[p]["sha256"]
    ]
    return {"added": added, "removed": removed, "changed": changed}


def main() -> None:
    parser = argparse.ArgumentParser(description="Hash image files and report live changes.")
    parser.add_argument("root", type=Path, help="Local folder synced from Google Drive")
    parser.add_argument(
        "--state",
        type=Path,
        default=Path("drive_image_state.json"),
        help="Previous scan JSON",
    )
    args = parser.parse_args()
    current = scan(args.root)
    previous = []
    if args.state.exists():
        previous = json.loads(args.state.read_text(encoding="utf-8")).get("files", [])
    report = {
        "scanned_utc": datetime.now(timezone.utc).isoformat(),
        "root": str(args.root.resolve()),
        "count": len(current),
        "delta": diff(previous, current),
        "files": current,
    }
    args.state.write_text(json.dumps({"files": current}, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
