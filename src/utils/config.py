"""Typed-light YAML configuration loading with dotted overrides."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml


def load_config(path: str | Path) -> dict[str, Any]:
    """Load a YAML mapping, rejecting ambiguous non-mapping documents."""
    value = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("configuration root must be a mapping")
    return value


def parse_value(raw: str) -> Any:
    """Parse a CLI override using YAML scalar/list/dict semantics."""
    return yaml.safe_load(raw)


def apply_overrides(config: dict[str, Any], overrides: list[str]) -> dict[str, Any]:
    """Apply ``section.key=value`` overrides to a deep copy."""
    result = json.loads(json.dumps(config))
    for item in overrides:
        if "=" not in item:
            raise ValueError(f"override must be KEY=VALUE: {item}")
        path, raw = item.split("=", 1)
        keys = path.split(".")
        cursor = result
        for key in keys[:-1]:
            if key not in cursor or not isinstance(cursor[key], dict):
                cursor[key] = {}
            cursor = cursor[key]
        cursor[keys[-1]] = parse_value(raw)
    return result
