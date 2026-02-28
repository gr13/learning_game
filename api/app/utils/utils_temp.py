from abc import ABC, abstractmethod
from app.utils.chatgpt import ChatGPT


class Utils(ABC):

    def __utils__(self):
        self.chat = ChatGPT()

    @abstractmethod
    def create_new_chat(self):
        """
        must start a comleletly fresh GPT conversation
        """
        pass
