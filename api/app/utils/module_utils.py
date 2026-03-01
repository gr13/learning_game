import json
import copy
from typing import Dict
from app.utils.chatgpt import ChatGPT
from app.utils.session_store import SessionStore
from app.utils.plans import MODULE_1_PLAN
from app.utils.response_handler import ResponseHandler
from app.utils.schemas import EXPLANATION_SCHEMA

MAX_RETRIES = 2

# TODO:
# •	Add response-type detector (JSON vs plain text auto handler)
# •	Detect JSON vs plain text
# •	Prevent rendering crashes
# •	Clean separation of modes

# •	refactor into a PromptBuilder class for cleaner scaling
# •	Centralized prompt generation
# •	Clean separation of concerns
# •	Scalable for Modules 2–5

PRACTICE_LIST = [
    "gehen",
    "kommen",
    "lernen",
    "arbeiten",
    "wohnen",
    "essen",
    "trinken",
    "lesen",
    "schreiben",
    "sehen",
]

NEW_WORD = "Spiel"


class ModuleUtils:
    """
    Handles module preparation logic.
    Talks to DB (later) and ChatGPT.
    """

    def __init__(self):
        self.chat = ChatGPT()

    def handle_module(self,
                      module_id: int,
                      session_id: int
                      ) -> Dict:
        """
        Entry point for module logic.
        """
        if module_id == 1:
            return self.initiate_module1(session_id)
        return {
            "mode": "error",
            "message": f"Module {module_id} not implemented."
        }

    @staticmethod
    def _get_module_1_instance():
        return copy.deepcopy(MODULE_1_PLAN)

    def initiate_module1(
            self, session_id: int
                        ) -> Dict:
        """
        Creates session and sends initial explanation request.
        """

        plan_instance = self._get_module_1_instance()
        runtime_context = {
            "the_new_word": NEW_WORD,
            "practice_list": PRACTICE_LIST,
            "practice_level": "A2"
        }
        system_plan = json.dumps(
            {"plan": plan_instance, "runtime": runtime_context},
            indent=2
        )

        system_prompt = f"""You are a German language teacher.

You MUST strictly follow the configuration below.
Treat all constraints as binding rules.
Do not ignore any schema requirements.
Never modify the JSON structure.

Configuration:
{system_plan}
"""

        user_prompt = "show the new word"

        SessionStore.append_message(session_id, "system", system_prompt)
        SessionStore.append_message(session_id, "user", user_prompt)

        return self._guarded_call(
            session_id=session_id,
            expected_schema=EXPLANATION_SCHEMA,
            expect_json=True
        )

    def continue_module1(self, session_id, user_input) -> Dict:
        """
        Continues exercise flow.
        Can return JSON or plain text.
        """
        system_prompt = """
Now continue the exercise.
Do not repeat the explanation.
Return JSON if an exercise is required.
Return plain text if feedback is required.
Do not mix formats.
"""
        # Normalize input (can be JSON or string)
        if isinstance(user_input, dict):
            user_input = json.dumps(user_input)

        # Add user answer to session
        SessionStore.append_message(session_id, "user", user_input)
        SessionStore.ensure_exercise_mode(session_id, system_prompt)

        return self._guarded_call(
            session_id=session_id,
            expected_schema=None,      # Could validate later per type
            expect_json=None           # Auto detect
        )

    def _guarded_call(
        self,
        session_id: int,
        expected_schema=None,
        expect_json: bool | None = None
    ) -> Dict:

        for _ in range(MAX_RETRIES):

            messages = SessionStore.get_messages(session_id)
            response = self.chat.send_messages(messages)
            assistant_reply = response.choices[0].message.content

            is_json = ResponseHandler.is_json(assistant_reply)

            # If explicitly expecting JSON but received text
            if expect_json is True and not is_json:
                self._inject_retry_instruction(session_id)
                continue

            # JSON branch
            if is_json:
                try:
                    parsed = json.loads(assistant_reply)
                except json.JSONDecodeError:
                    self._inject_retry_instruction(session_id)
                    continue

                if expected_schema:
                    if not ResponseHandler.validate_json(
                            assistant_reply,
                            expected_schema
                    ):
                        self._inject_retry_instruction(session_id)
                        continue

                # Store ONLY validated output
                SessionStore.append_message(
                    session_id, "assistant", assistant_reply)

                return {
                    "mode": "json",
                    "message": parsed
                }

            # Plain text branch
            SessionStore.append_message(
                session_id, "assistant", assistant_reply)

            return {
                "mode": "text",
                "message": assistant_reply
            }

        return self._error("Invalid structured response after retries.")

    def _inject_retry_instruction(self, session_id: int):
        SessionStore.append_message(
            session_id,
            "system",
            "Your previous response was invalid. "
            "Return ONLY valid JSON matching required schema."
        )

    def _error(self, message: str) -> Dict:
        return {
            "mode": "error",
            "message": message
        }
