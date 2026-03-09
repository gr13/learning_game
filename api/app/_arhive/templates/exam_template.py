from typing import Dict, Any

from app.modules.base.base_module import BaseModule
from app.modules.shared.exercise_runner import ExerciseRunner


class ExamTemplate(BaseModule):
    """
    Base template for exam modules
    (reading, writing, speaking).
    """

    # -------------------------------------------------------
    # Main execution
    # -------------------------------------------------------
    def run_exercise(self, user_input: str | None) -> Dict[str, Any]:
        """
        Run exam exercise.
        """

        exercise_class = self.get_exercise_class()

        runner = ExerciseRunner(self.module, self.session)

        return runner.run(exercise_class, user_input)

    # -------------------------------------------------------
    # Exercise selection
    # -------------------------------------------------------
    def get_exercise_class(self):
        """
        Return exercise class for the exam.
        Must be implemented by concrete module.
        """

        raise NotImplementedError

    # -------------------------------------------------------
    # Plan loading
    # -------------------------------------------------------
    def load_plan(self) -> Dict[str, Any]:
        """
        Load exam plan.
        """

        return self.get_plan()

    def get_plan(self) -> Dict[str, Any]:
        """
        Retrieve exam configuration.
        """

        raise NotImplementedError

    # -------------------------------------------------------
    # Context builder
    # -------------------------------------------------------
    def build_context(self) -> Dict[str, Any]:
        """
        Build context for exam prompt.
        """

        return {
            "module_id": self.module.id,
            "module_type": self.module.module_type.value,
        }

    # -------------------------------------------------------
    # Completion
    # -------------------------------------------------------
    def is_exam_complete(self) -> bool:
        """
        Determine if exam exercise is complete.
        """

        return self.module.done
