"""Assemble Intent | Pattern from the five files. Git author is observed attribution."""

from __future__ import annotations

import datetime
import subprocess
from pathlib import Path

from .ast import Check, Door, Envelope, RV
from .types import typecheck


# A root's four required files, and provenance as something a root may HAVE
# rather than a filename the language dictates.
#
# This constant read ("Intent", "Pattern", "Glimpse", "README.md",
# "IMG_3790.jpeg") until 2026-09-10 -- one photograph in one repository, named
# in the language itself, so every YA|RA root anywhere on earth failed to
# measure without a copy of it. Discovering the attachment instead keeps that
# root passing (it has one) without requiring every other root to hold it.
REQUIRED_FILES = ("Intent", "Pattern", "Glimpse", "README.md")
PROVENANCE_SUFFIXES = (".jpeg", ".jpg", ".png", ".pdf", ".heic", ".webp")


def provenance(root: Path) -> str | None:
    """The root's attachment, if it has one. Name is the root's business."""
    for p in sorted(Path(root).iterdir()):
        if p.is_file() and p.suffix.lower() in PROVENANCE_SUFFIXES:
            return p.name
    return None


class RootError(Exception):
    pass


def from_root(root: Path) -> Door:
    root = Path(root).resolve()
    missing = [n for n in ("Intent", "Pattern", "Glimpse") if not (root / n).is_file()]
    if missing:
        raise RootError(f"YA|RA root needs {', '.join(missing)} at {root}")

    intent = (root / "Intent").read_text(encoding="utf-8").strip()
    pattern = (root / "Pattern").read_text(encoding="utf-8").strip()
    glimpse = (root / "Glimpse").read_text(encoding="utf-8")
    readme = (root / "README.md").read_text(encoding="utf-8") if (root / "README.md").is_file() else ""

    env = _envelope(root)
    checks = [
        Check("words", ["intent", "17"]),
        Check("words", ["pattern", "17"]),
    ]
    for name in REQUIRED_FILES:
        checks.append(Check("exists", [name]))
    attached = provenance(root)
    if attached:
        checks.append(Check("exists", [attached]))
    checks.append(Check("contains", ["Glimpse", "glimpse"]))
    door = Door(
        intent=intent,
        pattern=pattern,
        envelope=env,
        rv=RV,
        measure="all",
        zero=("00" in readme) or ("      0" in readme),
        glimpse="glimpse" in glimpse.lower(),
        source=str(root),
        checks=checks,
    )
    return typecheck(door)


def _envelope(root: Path) -> Envelope:
    try:
        r = subprocess.run(
            ["git", "log", "-1", "--format=%an%n%ad", "--date=short", "--", "Intent"],
            cwd=root,
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError:
        r = None
    if r is not None and r.returncode == 0:
        lines = [ln.strip() for ln in r.stdout.splitlines() if ln.strip()]
        if len(lines) >= 2:
            return Envelope(
                kind="git-author",
                actor=lines[0],
                timestamp=lines[1],
                note="git log of Intent is observed attribution, not a cryptographic signature",
            )
    intent = root / "Intent"
    ts = datetime.datetime.utcfromtimestamp(intent.stat().st_mtime).strftime("%Y-%m-%d")
    return Envelope(kind="mtime", actor="root", timestamp=ts, note="filesystem mtime fallback")
