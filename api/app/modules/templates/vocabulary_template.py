from typing import Dict, Any, Type

from app.modules.base.base_module import BaseModule
from app.modules.shared.exercise_runner import ExerciseRunner
from app.modules.lifecycle.module_analyzer import ModuleAnalyzer


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

        exercise_index = self.get_current_exercise()

        exercise_class = self.get_exercise_class(exercise_index)

        runner = ExerciseRunner(self.module, self.session)

        return runner.run(exercise_class, user_input)

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
    def load_plan(self) -> Dict[str, Any]:
        """
        Load vocabulary plan configuration.
        """

        return self.get_plan()

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

        if hasattr(self.session, "current_exercise"):
            self.session.current_exercise += 1

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

        return {
            "module_id": self.module.id,
            "module_type": self.module.module_type.value,
            "exercise": self.get_current_exercise(),
        }
