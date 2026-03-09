from __future__ import annotations

from app.api_helpers.schemas import EXPLANATION_SCHEMA

EXERCISE_SCHEMA = {
    "type": "object",
    "required": [
        "mode",
        "exerciseNumber",
        "exerciseType",
        "tasks",
    ],
    "properties": {
        "mode": {"const": "exercise"},
        "exerciseNumber": {"type": ["integer", "string"]},
        "exerciseType": {"type": "string"},
        "tasks": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["instruction"],
                "properties": {
                    "instruction": {"type": "string"},
                },
            },
        },
    },
}

MICRO_DRILL_SCHEMA = {
    "type": "object",
    "required": ["mode"],
    "properties": {
        "mode": {"const": "micro_drill"},
    },
}

LESSON_JSON_SCHEMA = {
    "oneOf": [
        EXPLANATION_SCHEMA,
        EXERCISE_SCHEMA,
        MICRO_DRILL_SCHEMA,
    ]
}
