from typing import Dict, Any, Type

from app.modules.base.base_module import BaseModule
from app.modules.shared.exercise_runner import ExerciseRunner
from app.modules.lifecycle.module_analyzer import ModuleAnalyzer
from app.modules.shared.plan_loader import load_plan


class VocabularyTemplate(BaseModule):
    """
    Base template for vocabulary modules
    (core vocabulary, domain vocabulary).
    """

    TOTAL_EXERCISES = 5

    # -------------------------------------------------------
    # Main execution
    # -------------------------------------------------------
    def run_exercise(self, user_input: str | None) -> Dict[str, Any]:
        """
        Execute current vocabulary exercise.
        """

        # Intro
        if self.is_intro():
            result = self.run_intro()
            self.advance_exercise()
            return result

        # Closing
        if self.is_closing():
            return self.run_closing()

        # Normal exercise
        exercise_index = self.get_current_exercise()
        exercise_class = self.get_exercise_class(exercise_index)
        runner = ExerciseRunner(self.module, self.session)
        result = runner.run(exercise_class, user_input)

        return result

    # -------------------------------------------------------
    # Exercise selection
    # -------------------------------------------------------
    def get_exercise_class(self, index: int) -> Type:
        """
        Return exercise class for given index.
        Must be implemented by concrete module.
        """

        raise NotImplementedError

    # -------------------------------------------------------
    # Plan loading
    # -------------------------------------------------------
    def load_plan(self, plan_name: str) -> Dict[str, Any]:
        """
        Load vocabulary plan configuration.
        """
        return load_plan(plan_name)

    def get_plan(self) -> Dict[str, Any]:
        """
        Retrieve vocabulary plan.
        """

        raise NotImplementedError

    # -------------------------------------------------------
    # Exercise progression
    # -------------------------------------------------------
    def get_current_exercise(self) -> int:
        """
        Determine current exercise number.
        """

        analyzer = ModuleAnalyzer(self.module, self.session)

        return analyzer.get_current_exercise()

    def advance_exercise(self) -> None:
        """
        Move to next exercise.
        """
        self.session.advance_exercise()

    # -------------------------------------------------------
    # Completion
    # -------------------------------------------------------
    def is_module_complete(self) -> bool:
        """
        Determine if vocabulary module is finished.
        """
        return self.get_current_exercise() > self.TOTAL_EXERCISES

    # -------------------------------------------------------
    # Context builder
    # -------------------------------------------------------
    def build_context(self) -> Dict[str, Any]:
        """
        Build vocabulary module context.
        """
        # TODO: check value
        return {
            "module_id": self.module.id,
            "module_type": self.module.module_type.value,
            "exercise": self.get_current_exercise(),
        }

    # -------------------------------------------------------
    # Intro
    # -------------------------------------------------------
    def is_intro(self):
        return self.session.exercise_index == 0

    def run_intro(self) -> Dict[str, Any]:
        """
        Run word introduction.
        """
        return {
            "general_plan": self.load_plan("general_plan.json"),
            "exercise_plan": self.load_plan("word_intro_plan.json"),
            "context": self.build_context(),
        }

    # -------------------------------------------------------
    # Closing
    # -------------------------------------------------------
    def is_closing(self):
        return self.session.exercise_index >= 6

    def run_closing(self):
        return {
            "closing": [
                self.load_plan("closing_show_introduced.json"),
                self.load_plan("closing_show_learned.json"),
                self.load_plan("closing_session_summary.json"),
            ]
        }
