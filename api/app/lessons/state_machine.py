from __future__ import annotations

from app.lessons.contracts import EventType, LessonEvent, LessonState, Phase


class LessonStateMachine:
    """Deterministic lesson state transitions.

    This is intentionally simple in skeleton stage.
    """

    def apply(self, state: LessonState, event: LessonEvent) -> LessonState:
        if event.event_type == EventType.START:
            state.phase = Phase.INTRO
            return state

        if event.event_type == EventType.USER_ANSWER:
            state.phase = Phase.EXERCISE
            return state

        if event.event_type == EventType.NEXT_EXERCISE:
            state.phase = Phase.EXERCISE
            state.exercise_index += 1
            return state

        if event.event_type == EventType.END_MODULE:
            state.phase = Phase.CLOSING
            return state

        return state
