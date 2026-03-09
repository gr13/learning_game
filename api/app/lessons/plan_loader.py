from __future__ import annotations

import json
from pathlib import Path
from typing import Any

PLAN_ROOT = Path(__file__).parent / "plans"
DEFAULT_MODULE = "core"


def _module_dir(module_name: str) -> Path:
    path = PLAN_ROOT / module_name
    if not path.exists():
        raise FileNotFoundError(
            f"Module plan directory not found: {module_name}"
        )
    return path


def load_plan(module_name: str, plan_name: str) -> dict[str, Any]:
    plan_path = _module_dir(module_name) / plan_name
    with open(plan_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_plan_bundle(
    module_name: str = DEFAULT_MODULE,
) -> dict[str, dict[str, Any]]:
    manifest = load_plan(module_name, "manifest.json")
    return {
        key: load_plan(module_name, filename)
        for key, filename in manifest.items()
    }
