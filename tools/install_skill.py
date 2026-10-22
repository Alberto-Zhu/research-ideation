#!/usr/bin/env python3
"""Install the bundled skill into a local agent's skills directory."""
import argparse
import os
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

NAME = "research-ideation"


def install(source, parent, force=False):
    source, parent = Path(source).resolve(), Path(parent).expanduser().resolve()
    if not (source / "SKILL.md").is_file():
        raise ValueError("Source does not contain SKILL.md.")
    target = parent / NAME
    if target.is_symlink():
        raise ValueError("Refusing to replace a symbolic-link destination.")
    if target.exists() and not force:
        raise ValueError("Already installed; --force preserves a backup before replacement.")
    if target == source or source in target.parents or target in source.parents:
        raise ValueError("Source and destination must be separate directory trees.")
    parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix="." + NAME + "-install-", dir=parent))
    backup = None
    try:
        shutil.copytree(source, staging, dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        if target.exists():
            suffix = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
            backup = target.with_name(NAME + ".backup-" + suffix)
            target.rename(backup)
        staging.rename(target)
    except Exception:
        shutil.rmtree(staging, ignore_errors=True)
        if backup is not None and backup.exists() and not target.exists():
            backup.rename(target)
        raise
    return target, backup


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agent", choices=("codex", "claude"), default="codex")
    parser.add_argument("--dest", help="Parent skills directory; the skill name is appended.")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args(argv)
    source = Path(__file__).resolve().parents[1] / "skills" / NAME
    if args.dest:
        parent = Path(args.dest)
    elif args.agent == "codex":
        parent = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))) / "skills"
    else:
        parent = Path.home() / ".claude" / "skills"
    try:
        target, backup = install(source, parent, args.force)
    except (OSError, ValueError) as exc:
        print("ERROR " + str(exc), file=sys.stderr)
        return 1
    print("Installed: " + str(target))
    if backup:
        print("Previous installation preserved: " + str(backup))
    print("Reload your client's skills or start a new session.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
