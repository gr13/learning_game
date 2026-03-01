import json
import copy
from typing import Dict
from app.utils.chatgpt import ChatGPT
from app.utils.session_store import SessionStore
from app.utils.plans import MODULE_1_PLAN

# TODO:
# •	Add automatic schema validation guard (very powerful)
# (Add JSON Schema Validation Guard)
# •	Define strict schemas
# •	Validate GPT responses
# •	Add auto-retry mechanism
# •	Prevent malformed output from reaching frontend

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
        return {"message": f"Module {module_id} not implemented yet"}

    @staticmethod
    def _get_module_1_instance():
        return copy.deepcopy(MODULE_1_PLAN)

    def initiate_module1(
            self, session_id: int
                        ) -> Dict:
        """
        Creates session
        Send System_prompt and user_prompt to chatGPT
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

        user_prompt = """
            show the new word
        """

        SessionStore.append_message(session_id, "system", system_prompt)
        SessionStore.append_message(session_id, "user", user_prompt)

        messages = SessionStore.get_messages(session_id)

        response = self.chat.send_messages(messages)

        assistant_reply = response.choices[0].message.content

        SessionStore.append_message(session_id, "assistant", assistant_reply)

        print("SESSION STATE:", SessionStore.get_messages(session_id))

        return {"message": assistant_reply}

    def continue_module1(self, session_id, user_input) -> Dict:
        """
        Prepares list of messages
        receives the answer
        """
        system_prompt = """
            Now continue the exercise.
            Do not repeat the explanation.
            Show only the next task or feedback.
            No JSON. Just plain text.
        """
        # Add user answer to session
        SessionStore.append_message(session_id, "user", user_input)
        SessionStore.ensure_exercise_mode(session_id, system_prompt)
        messages = SessionStore.get_messages(session_id)

        # Call GPT
        response = self.chat.send_messages(messages)

        assistant_reply = response.choices[0].message.content
        # Store assistant reply
        SessionStore.append_message(session_id, "assistant", assistant_reply)

        return {"message": assistant_reply}
