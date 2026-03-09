from __future__ import annotations

import json
from typing import Any

from app.lessons.adapters.base import BaseLessonAdapter
from app.lessons.contracts import LessonEvent, LessonState
from app.lessons.plan_loader import load_plan_bundle
from app.lessons.schemas import LESSON_JSON_SCHEMA
from app.models.profile import ProfileModel


class CoreLessonAdapter(BaseLessonAdapter):
    """CORE module adapter skeleton."""

    module_id = 1

    def build_start_package(self, state: LessonState) -> dict[str, Any]:
        plans = load_plan_bundle()
        profile = ProfileModel.find_by_id(1)

        return {
            "plans": plans,
            "runtime": {
                "session_id": state.session_id,
                "practice_level": (
                    profile.get_user_level() if profile else "A2"
                ),
                "exercise_index": state.exercise_index,
                "phase": state.phase.value,
            },
            "task": "introduce new word and prepare first exercise",
        }

    def build_continue_package(
        self,
        state: LessonState,
        event: LessonEvent,
    ) -> dict[str, Any]:
        return {
            "runtime": {
                "session_id": state.session_id,
                "exercise_index": state.exercise_index,
                "phase": state.phase.value,
                "task_round": state.task_round,
                "micro_drill_active": state.micro_drill_active,
            },
            "event": {
                "type": event.event_type.value,
                "user_input": event.user_input,
            },
        }

    def expected_schema_for_phase(
        self,
        _state: LessonState,
    ) -> dict[str, Any] | None:
        return LESSON_JSON_SCHEMA

    def parse_reply(self, raw_reply: str) -> dict[str, Any] | str:
        try:
            return json.loads(raw_reply)
        except json.JSONDecodeError:
            return raw_reply
