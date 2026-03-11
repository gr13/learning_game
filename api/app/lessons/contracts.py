from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, TypedDict


class ResponseMode(str, Enum):
    TEXT = "text"
    JSON = "json"
    ERROR = "error"


class Phase(str, Enum):
    INTRO = "intro"          # start: word explanation + exercise 1 bootstrap
    EXERCISE = "exercise"    # user<->gpt loop
    CLOSING = "closing"      # introduced / learned / teacher status


class EventType(str, Enum):
    START = "start"
    USER_ANSWER = "user_answer"
    NEXT_EXERCISE = "next_exercise"
    END_MODULE = "end_module"


class LessonEnvelope(TypedDict):
    mode: str
    message: Any


@dataclass
class LessonEvent:
    event_type: EventType
    user_input: str | None = None


@dataclass
class LessonState:
    module_type_id: int
    session_id: int
    phase: Phase = Phase.INTRO
    exercise_index: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)
