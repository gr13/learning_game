from typing import Dict
from app.utils.chatgpt import ChatGPT
from app.utils.session_store import SessionStore

SIMPLE_PLAN = """
Module 1 – Core Vocabulary Practice

- Review introduced words.
- Introduce one new word.
- Create 5 short tasks.
- Mix translation and simple grammar.
- Keep exercises short.
"""

INTRODUCED_WORDS = """
gehen
kommen
lernen
arbeiten
wohnen
essen
trinken
lesen
schreiben
sehen
"""

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

    def initiate_module1(
            self, session_id: int
                        ) -> Dict:
        """
        Creates session
        Send System_prompt and user_prompt to chatGPT
        """
        system_prompt = """
            You are a German language teacher.

            Return ONLY valid JSON.
            Do not add explanations outside JSON.
            No markdown.
            No extra text.
        """

        user_prompt = """
            Explain the word 'gehen' at A1 level.

            Return ONLY valid JSON.
            No markdown.
            No text outside JSON.
            Do not rename keys.
            Do not translate keys.
            Keys must remain exactly as written below in English.
            Only translate or explain content, not key names.
            Always include all fields.
            Do not add extra fields.
            Do not remove fields.

            {
                "word": "",
                "partOfSpeech": "",
                "pronunciation": "",
                "definition": "",
                "meaning": "",
                "examples": [
                    {"de": "", "en": ""}
                ],
                "forms": {
                    "praesens": "",
                    "praeteritum": "",
                    "perfekt": ""
                }
            }
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
        # Add NEW system instruction BEFORE calling GPT
        # Only add exercise system instruction if not already added
        messages = SessionStore.get_messages(session_id)

        SessionStore.ensure_exercise_mode(session_id, system_prompt)

        # Get full message history
        messages = SessionStore.get_messages(session_id)
        # Call GPT
        response = self.chat.send_messages(messages)

        assistant_reply = response.choices[0].message.content
        # Store assistant reply
        SessionStore.append_message(session_id, "assistant", assistant_reply)

        return {"message": assistant_reply}
