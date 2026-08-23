"""Structured experiment logging helpers."""
from __future__ import annotations

import json
import logging
import os
import random
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def configure_logging(level: str = "INFO") -> logging.Logger:
    """Configure one consistent console logger."""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        force=True,
    )
    return logging.getLogger("wordle_small_llm")


def create_run_dir(root: str | Path, name: str, seed: int) -> Path:
    """Create a collision-resistant run directory."""
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run = Path(root) / f"{stamp}-{name}-s{seed}-{random.randrange(1_000_000):06d}"
    run.mkdir(parents=True, exist_ok=False)
    return run


def write_json(path: str | Path, value: Any) -> None:
    """Atomically write deterministic, human-readable JSON."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    tmp = destination.with_suffix(destination.suffix + f".{os.getpid()}.tmp")
    tmp.write_text(json.dumps(value, indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")
    tmp.replace(destination)
