import json
from pathlib import Path
from typing import Dict, Any

# TODO: do we really need this?
# -------------------------------------------------------
# Plan cache
# -------------------------------------------------------
_PLAN_CACHE: Dict[str, Dict[str, Any]] = {}

# -------------------------------------------------------
# Base plan directory
# -------------------------------------------------------
PLAN_BASE_PATH = Path(__file__).resolve().parents[2]


# -------------------------------------------------------
# Public API
# -------------------------------------------------------
def load_plan(plan_name: str) -> Dict[str, Any]:
    """
    Load a plan JSON file.

    Plans are cached in memory to avoid repeated
    disk reads during module execution.

    Parameters
    ----------
    plan_name : str
        Name of the JSON plan file

    Returns
    -------
    Dict[str, Any]
        Parsed plan
    """

    # Return cached plan if already loaded
    if plan_name in _PLAN_CACHE:
        return _PLAN_CACHE[plan_name]

    plan_path = resolve_plan_path(plan_name)

    with open(plan_path, "r", encoding="utf-8") as f:
        plan = json.load(f)

    _PLAN_CACHE[plan_name] = plan

    return plan


# -------------------------------------------------------
# Path resolution
# -------------------------------------------------------

def resolve_plan_path(plan_name: str) -> Path:
    """
    Resolve absolute path to plan file.
    """

    possible_paths = [

        # vocabulary core plans
        PLAN_BASE_PATH / "modules" / "vocabulary" / "core" / "plans" / plan_name,  # noqa: E501

        # vocabulary domain plans
        PLAN_BASE_PATH / "modules" / "vocabulary" / "domain" / "plans" / plan_name,  # noqa: E501

        # exam plans
        PLAN_BASE_PATH / "modules" / "exam" / "plans" / plan_name,
    ]

    for path in possible_paths:
        if path.exists():
            return path

    raise FileNotFoundError(
        f"Plan file not found: {plan_name}"
    )
