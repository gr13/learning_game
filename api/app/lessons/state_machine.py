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
            state.phase = Phase.FEEDBACK
            return state

        if event.event_type == EventType.REQUEST_DRILL:
            state.phase = Phase.MICRO_DRILL
            state.micro_drill_active = True
            return state

        if event.event_type == EventType.NEXT_EXERCISE:
            state.exercise_index += 1
            state.task_round = 1
            state.micro_drill_active = False
            state.phase = Phase.EXERCISE
            return state

        if event.event_type == EventType.FINISH_MODULE:
            state.phase = Phase.CLOSING
            return state

        return state
