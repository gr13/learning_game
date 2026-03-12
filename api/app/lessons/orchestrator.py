from __future__ import annotations

import json
from typing import Any

# from app.api_helpers.schemas import EXPLANATION_SCHEMA
from app.lessons.chat_loop import ChatLoopService
from app.lessons.contracts import (
    EventType,
    LessonEnvelope,
    LessonEvent,
    LessonState,
    Phase,
)

from app.lessons.registry import LessonRegistry
from app.lessons.schemas import EXERCISE_SCHEMA
from app.lessons.state_machine import LessonStateMachine
from app.sessions.session_store import SessionStore
from app.models.core_vocabulary import CoreVocabularyModel
from app.lessons.plan_loader import load_plan
from app.models.profile import ProfileModel
from app.models.modules import ModulesModel
from app.models.sessions import SessionsModel
from app.ai.chatgpt import ChatGPT


class LessonOrchestrator:
    def __init__(self) -> None:
        self.registry = LessonRegistry()
        self.state_machine = LessonStateMachine()
        self.chat_loop = ChatLoopService()

    def start(
            self,
            module_type_id: int,
            module: ModulesModel,
            session: SessionsModel
            ) -> LessonEnvelope:
        adapter = self.registry.get_adapter(module_type_id)
        if not adapter:
            return {"mode": "error", "message": f"Module type {module_type_id} not implemented."}  # noqa: E501

        state = LessonState(
            module_type_id=module_type_id,
            session_id=session.id
        )
        state = self.state_machine.apply(state, LessonEvent(EventType.START))
        state.exercise_index = 1

        # -------- Step 0: intro only --------
        if module_type_id in (1, 2):
            return self._run_step_0_intro(
                module_type_id=module_type_id,
                session=session)

        # -------- Step 1: general + drill 1 --------
        return self._do_exercise(
            module_type_id=module_type_id,
            session_id=session.id,
            state=state)

    def continue_turn(
        self,
        module_type_id: int,
        module_id: int,
        session_id: int,
        user_input: str,
    ) -> LessonEnvelope:
        adapter = self.registry.get_adapter(module_type_id)
        if not adapter:
            return {
                "mode": "error", "message": f"Module type {module_type_id} not implemented."  # noqa: E501
            }
        if not user_input.strip():
            return {
                "mode": "error", "message": "User input cannot be empty."
            }

        current_ex = SessionStore.get_current_exercise_index(
            session_id, module_id)
        state = LessonState(
            module_type_id=module_type_id,
            session_id=session_id,
            exercise_index=max(1, current_ex),
        )

        event = LessonEvent(EventType.USER_ANSWER, user_input=user_input)
        state = self.state_machine.apply(state, event)

        package = adapter.build_continue_package(state, event)
        SessionStore.append_message(
            session_id, "system", self._build_system_prompt(package))
        SessionStore.append_message(session_id, "user", user_input)

        return self.chat_loop.call(
            session_id, expected_schema=None, expect_json=None)

    def next_exercise(
            self, module_type_id: int, module_id: int, session_id: int
            ) -> LessonEnvelope:
        pass

    # TODO: redo correctly
    def end_module(
            self, module_type_id: int, module_id: int, session_id: int
            ) -> LessonEnvelope:
        _ = module_type_id, module_id
        messages = SessionStore.get_messages(session_id)
        transcript = "\n".join(
            f"{m.role}: {m.content}" for m in messages
        )

        SessionStore.append_message(
            session_id,
            "system",
            (
                "Analyze full transcript and return plain text with 3 sections:\n"  # noqa: E501
                "1) Introduced words\n"
                "2) Learned words\n"
                "3) Teacher status"
            ),
        )
        SessionStore.append_message(
            session_id,
            "user",
            f"Session transcript:\n{transcript}",
        )

        return self.chat_loop.call(
            session_id, expected_schema=None, expect_json=False)

    # TODO: remove it complitely
    @staticmethod
    def _build_system_prompt(package: dict[str, Any]) -> str:
        return (
            "You are a German language teacher. Follow the package exactly. "
            "Return JSON when structured response is required.\n\n"
            f"Package:\n{json.dumps(package, ensure_ascii=True, indent=2)}"
        )

    def _run_step_0_intro(
        self,
        module_type_id: int,
        session: SessionsModel,
    ) -> LessonEnvelope:
        # 1) Select word by module
        # get new word
        if module_type_id == 1:
            row = CoreVocabularyModel.find_new()
            if not row:
                return {
                    "mode": "error",
                    "message": "No new core vocabulary word found.",
                }
            row.mark_introduced()
            the_new_word = row.word
            module_name = "core"
        elif module_type_id == 2:
            return {
                "mode": "error",
                "message": "Domain step 0 not implemented.",
            }
        else:
            return {
                "mode": "error",
                "message": "Step 0 not supported for module "
                           f"type {module_type_id}."
            }

        # 2) Runtime for intro only
        profile = ProfileModel.find_by_id()
        practice_level = profile.get_user_level() if profile else "A2"
        intro_plan = load_plan(module_name, "0_word_intro_plan.json")
        # placeholders
        intro_plan.setdefault("input", {})
        intro_plan["input"]["the_new_word"] = the_new_word
        intro_plan["input"]["practice_level"] = practice_level

        # 3) append package to sessions
        # SessionStore.append_message(
        #     session.id,
        #     "system",
        #     json.dumps(intro_plan, ensure_ascii=True, indent=4),
        # )

        system_content = json.dumps(intro_plan, ensure_ascii=True, indent=4)
        user_content = f"Introduce this exact word: {the_new_word}"

        # persist messages
        SessionStore.append_message(session.id, "system", system_content)
        SessionStore.append_message(session.id, "user", user_content)

        # 4) Ask model for intro JSON
        # return self.chat_loop.call(session.id, EXPLANATION_SCHEMA, True)

        # one direct GPT call (no retry loop)
        response = ChatGPT().send_messages([
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content},
        ])

        assistant_reply = response.choices[0].message.content or ""

        if not assistant_reply:
            return {"mode": "error", "message": "Empty model response."}

        SessionStore.append_message(
            session.id, "assistant", assistant_reply)

        parsed = json.loads(assistant_reply)
        return {"mode": "json", "message": parsed}

    def _do_exercise(
        self,
        module_type_id: int,
        session: SessionsModel,
        module: ModulesModel,
    ) -> LessonEnvelope:

        # runtime payload for both calls
        # profile = ProfileModel.find_by_id()
        # runtime = {
        #     "session_id": session.id,
        #     "practice_level": profile.get_user_level() if profile else "A2",
        #     "exercise_index": 1,
        #     "phase": state.phase.value,
        #     "max_exercises": adapter.max_exercises,
        #     "the_new_word": state.metadata.get("the_new_word"),
        #     "practice_list": state.metadata.get("practice_list", []),
        # }

        adapter = self.registry.get_adapter(module_type_id)
        if not adapter:
            return {
                "mode": "error", "message": f"Module type {module_type_id} not implemented."  # noqa: E501
            }

        current_ex = SessionStore.get_current_exercise_index(
            session.id, module.id)
        if current_ex >= adapter.max_exercises:
            return {
                "mode": "error",
                "message": "No more exercises. Press End Module.",
            }

        state = LessonState(
            module_type_id=module_type_id,
            session_id=session.id,
            phase=Phase.EXERCISE,
            exercise_index=current_ex,
        )
        state = self.state_machine.apply(
            state, LessonEvent(EventType.NEXT_EXERCISE))

        if module_type_id == 1:
            state.metadata["practice_list"] = [
                w.word for w in CoreVocabularyModel.find_introduced()
            ]

        package = adapter.build_continue_package(state, LessonEvent(
            EventType.NEXT_EXERCISE))
        SessionStore.append_message(
            session.id, "system", self._build_system_prompt(package))
        SessionStore.append_message(
            session.id,
            "user",
            f"Start exercise {state.exercise_index}. Return mode='exercise' JSON.",  # noqa: E501
        )

        exercise = self.chat_loop.call(session.id, EXERCISE_SCHEMA, True)
        if exercise["mode"] != "json":
            return exercise

        SessionStore.create_exercise_marker(
            session.id, module.id, state.exercise_index)
        return exercise

        # exercise_package = {
        #     "general": load_plan(module_name, "general_plan.json"),
        #     "drill": load_plan(module_name, drill_file),
        #     "runtime": runtime,
        #     "intent": intent,
        # }

        # SessionStore.append_message(
        #     session_id, "system", self._build_system_prompt(exercise_package)
        # )
        # SessionStore.append_message(session_id, "user", user_prompt)

        # exercise = self.chat_loop.call(session_id, EXERCISE_SCHEMA, True)
        # if exercise["mode"] != "json":
        #     return exercise

        # SessionStore.create_exercise_marker(
        #     session_id, module_id, exercise_index)
        # return exercise
        # exercise1_package = {
        #     "general": load_plan("core", "general_plan.json"),
        #     "drill": load_plan("core", "1_new_word_drill.json"),
        #     "runtime": runtime,
        #     "intent": "start_exercise_1",
        # }

        # SessionStore.append_message(
        #     session_id, "system", self._build_system_prompt(
        #                           exercise1_package)
        # )
        # SessionStore.append_message(session_id, "user", "Start exercise 1.")

        # exercise = self.chat_loop.call(session_id, EXERCISE_SCHEMA, True)
        # if exercise["mode"] != "json":
        #     return exercise

        # SessionStore.create_exercise_marker(session_id, module_id, 1)

        # return {
        #     "mode": "json",
        #     "message": [explanation["message"], exercise["message"]],
        # }
