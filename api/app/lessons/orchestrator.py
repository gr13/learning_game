from __future__ import annotations

import json
from openai.types.chat import ChatCompletion

# from app.api_helpers.schemas import EXPLANATION_SCHEMA
from app.lessons.chat_loop import ChatLoopService
from app.lessons.contracts import (
    EventType,
    LessonEnvelope,
    LessonEvent,
    LessonState,
)

from app.lessons.registry import LessonRegistry
from app.lessons.state_machine import LessonStateMachine
from app.sessions.session_store import SessionStore
from app.models.core_vocabulary import CoreVocabularyModel
from app.lessons.plan_loader import load_plan
from app.models.profile import ProfileModel
from app.models.modules import ModulesModel
from app.models.sessions import SessionsModel
from app.ai.chatgpt import ChatGPT
from app.models.exercises import ExercisesModel


class LessonOrchestrator:
    def __init__(self) -> None:
        self.registry = LessonRegistry()
        self.state_machine = LessonStateMachine()
        self.chat_loop = ChatLoopService()

    def start(
            self,
            module_type_id: int,
            module: ModulesModel,
            session: SessionsModel,
            exercise: ExercisesModel,
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
        return self._start_exercise(
            module_type_id=module_type_id,
            session=session,
            exercise=exercise)

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
            module_name = self._module_folder_from_id(module_type_id)
            if not module_name:
                return {
                    "mode": "error",
                    "message": f"Module type {module_type_id} "
                               "not implemented.",
                }
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

        return self._load_json_safely(response, session)

    def _start_exercise(
        self,
        module_type_id: int,
        session: SessionsModel,
        exercise: ExercisesModel,
    ) -> LessonEnvelope:

        module_name = self._module_folder_from_id(module_type_id)
        if not module_name:
            return {
                "mode": "error",
                "message": f"Module type {module_type_id} not implemented.",
            }

        practice_list = []
        if module_type_id == 1:
            rows = CoreVocabularyModel.find_introduced()
            if not rows:
                return {
                    "mode": "error",
                    "message": "No new core vocabulary word found.",
                }

            practice_list = [row.word for row in rows]

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

        # load plans
        general_plan = self._get_general_plan(module_name)

        exercise_name = self._get_plan_name(
            exercise=exercise,
            module_folder=module_name)
        exercise_plan = load_plan(module_name, exercise_name)

        # placeholders
        general_plan.setdefault("input", {})
        general_plan["input"]["practice_list"] = practice_list
        general_plan["input"]["practice_level"] = practice_level

        # combine plans into one package for GPT
        exercise_package = {
            "general": general_plan,
            "drill": exercise_plan,
        }
        system_content = json.dumps(
            exercise_package,
            ensure_ascii=True,
            indent=4
        )
        user_content = "Start the drill from this package. Return JSON only."

        # TODO:THE REST SHOULD BE THE SAME WITH _run_step_0_intro -> FUN

        # persist messages
        SessionStore.append_message(session.id, "system", system_content)
        SessionStore.append_message(session.id, "user", user_content)

        # one direct GPT call (no retry loop)
        response = ChatGPT().send_messages([
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content},
        ])

        return self._load_json_safely(response, session)

    @staticmethod
    def _get_plan_name(
            exercise: ExercisesModel,
            module_folder: str
    ):
        key = str(exercise.exercise_index)
        manifest = load_plan(module_folder, "manifest.json")
        if key not in manifest:
            raise KeyError(
                f"Exercise index {key} not found "
                f"in {module_folder}/manifest.json")
        return manifest[key]

    @staticmethod
    def _get_general_plan(module_folder: str):
        return load_plan(module_folder, "general_plan.json")

    @staticmethod
    def _load_json_safely(
            response: ChatCompletion,
            session: SessionsModel
            ):
        if not response.choices:
            return {"mode": "error", "message": "Empty model response."}
        assistant_reply = response.choices[0].message.content or ""

        if not assistant_reply:
            return {"mode": "error", "message": "Empty model response."}

        SessionStore.append_message(session.id, "assistant", assistant_reply)

        try:
            parsed = json.loads(assistant_reply)
        except json.JSONDecodeError:
            return {
                "mode": "error",
                "message": "Model returned non-JSON response.",
            }

        return {"mode": "json", "message": parsed}

    @staticmethod
    def _module_folder_from_id(module_type_id: int) -> str | None:
        module_name_map = {
            1: "core",
            2: "domain",
            3: "reading",
            4: "writing",
            5: "speaking",
        }
        return module_name_map.get(module_type_id)
