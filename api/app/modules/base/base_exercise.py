from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseExercise(ABC):
    """
    Base class for all exercises.

    Every exercise must implement the same interface so that
    exercise_engine can execute them generically.
    """

    def __init__(self, module, session):
        self.module = module
        self.session = session

    # -------------------------------------------------------
    # Core execution
    # -------------------------------------------------------

    def run(self, user_input: str | None = None) -> Dict[str, Any]:
        """
        Main execution entrypoint.

        This is called by the exercise_engine.
        """

        if user_input is None:
            return self.start()

        return self.process(user_input)

    # -------------------------------------------------------
    # Exercise lifecycle
    # -------------------------------------------------------

    @abstractmethod
    def start(self) -> Dict[str, Any]:
        """
        Start the exercise.

        Usually builds the prompt and sends it to the user.
        """
        pass

    @abstractmethod
    def process(self, user_input: str) -> Dict[str, Any]:
        """
        Process user input and return evaluation.
        """
        pass

    # -------------------------------------------------------
    # Prompt generation
    # -------------------------------------------------------

    def build_prompt(self) -> str:
        """
        Build prompt for AI model.
        Optional override in subclasses.
        """
        raise NotImplementedError

    # -------------------------------------------------------
    # Evaluation
    # -------------------------------------------------------

    def evaluate(self, user_input: str) -> Dict[str, Any]:
        """
        Evaluate user answer.

        Typically delegates to shared evaluation logic.
        """
        raise NotImplementedError

    # -------------------------------------------------------
    # Helpers
    # -------------------------------------------------------

    def next_exercise(self) -> None:
        """
        Advance exercise pointer in session.
        """

        if hasattr(self.session, "current_exercise"):
            self.session.current_exercise += 1

    def complete_module(self) -> None:
        """
        Mark module as completed.
        """

        if hasattr(self.module, "mark_done"):
            self.module.mark_done()