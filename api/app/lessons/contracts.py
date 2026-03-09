from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, TypedDict


class ResponseMode(str, Enum):
    TEXT = "text"
    JSON = "json"
    ERROR = "error"


class Phase(str, Enum):
    INTRO = "intro"
    EXERCISE = "exercise"
    FEEDBACK = "feedback"
    MICRO_DRILL = "micro_drill"
    CLOSING = "closing"


class EventType(str, Enum):
    START = "start"
    USER_ANSWER = "user_answer"
    REQUEST_DRILL = "request_drill"
    NEXT_EXERCISE = "next_exercise"
    FINISH_MODULE = "finish_module"


class LessonEnvelope(TypedDict):
    mode: str
    message: Any


@dataclass
class LessonEvent:
    event_type: EventType
    user_input: str | None = None


@dataclass
class LessonState:
    module_id: int
    session_id: int
    phase: Phase = Phase.INTRO
    exercise_index: int = 1
    task_round: int = 1
    micro_drill_active: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)
