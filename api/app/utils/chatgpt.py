import os
from openai import OpenAI


class ChatGPT:
    """
    Thin wrapper around OpenAI Chat API.

    IMPORTANT:
    - This class stores NO conversation history.
    - It does NOT manage sessions.
    - It only sends whatever messages it receives.
    - Session logic must be handled elsewhere.
    """

    def __init__(self):

        api_key = os.getenv("OPENAI_API_KEY")
        model = os.getenv("OPENAI_MODEL")

        if not api_key:
            raise ValueError("OPENAI_API_KEY not set")

        if not model:
            raise ValueError("OPENAI_MODEL not set")

        self.client = OpenAI(api_key=api_key)
        self.model: str = model

    # ----------------------------------------------------------
    # Session-based conversation call (main method)
    # ----------------------------------------------------------
    def send_messages(self, messages: list):
        """
        Sends full conversation history.

        `messages` must be a list of:
        [
            {"role": "system", "content": "..."},
            {"role": "user", "content": "..."},
            {"role": "assistant", "content": "..."},
            ...
        ]
        """

        return self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )
