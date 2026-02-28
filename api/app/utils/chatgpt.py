import os
from openai import OpenAI


class ChatGPT:
    """
    handles communication with OpenAI API.
    No business logic here.
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

    def send_message(
            self,
            system_promt: str,
            user_prompt: str
    ) -> str:
        """
        Sends a structured request to GPT and returns text response.
        """

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_promt},
                {"role": "user", "content": user_prompt},
            ]
        )
        return response.choices[0].message.content
