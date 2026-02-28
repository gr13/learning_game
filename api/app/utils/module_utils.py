import json
from typing import Dict
from app.utils.chatgpt import ChatGPT


class ModuleUtils:
    """
    Handles module preparation logic.
    Talks to DB (later) and ChatGPT.
    """

    def __init__(self):
        self.chat = ChatGPT()

    def handle_module(self, module_id: int) -> Dict:
        """
        Entry point for module logic.
        """
        if module_id == 1:
            return self._handle_module_1()
        return {"message": f"Module {module_id} not implemented yet"}

    def _handle_module_1(self) -> Dict:
        """
        Simulate Module 1 basic logic.
        Later: load words from DB.
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
        user_prompt = "Explain the word 'gehen' in simple terms."

        response = self.chat.send_message(system_prompt, user_prompt)

        return {
            "module": 1,
            "message": json.loads(response)
        }
