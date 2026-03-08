from typing import Dict, Any

from app.modules.templates.vocabulary_template import VocabularyTemplate
from app.modules.vocabulary.core.exercise_engine import CoreExerciseEngine


def run(module, session, user_input: str | None = None) -> Dict[str, Any]:
    """
    Core Vocabulary module entrypoint.
    This function is registered in MODULE_REGISTRY and
    is called dynamically by ModuleEngine.
    Execution chain
    ---------------
    ModuleEngine.run_module()
        ↓
    MODULE_REGISTRY[module_type]
        ↓
    run(module, session, user_input)
        ↓
    CoreVocabularyModule
        ↓
    Exercise engine
        ↓
    Exercise logic

    Parameters
    ----------
    module : ModulesModel
        Module instance from database.

    session :
        Active learning session.

    user_input : str | None
        User answer submitted from the UI.
        If None, the exercise should start.

    Returns
    -------
    Dict
        Response payload sent back to the API.
    """

    module_runner = CoreVocabularyModule(module=module, session=session)
    return module_runner.run_exercise(user_input)


class CoreVocabularyModule(VocabularyTemplate):
    """
    Core Vocabulary learning module.

    Structure:
        5 exercises
        each exercise → 5 tasks
    """
    # -------------------------------------------------------
    # Main execution
    # -------------------------------------------------------
    def run_exercise(self, user_input: str | None) -> Dict[str, Any]:
        """
        Execute the current vocabulary exercise.
        This method determines which exercise is active
        and delegates execution to the exercise engine.
        Flow
        ----
        run()
            ↓
        CoreVocabularyModule.run_exercise()
            ↓
        CoreExerciseEngine.run()
            ↓
        Exercise implementation

        Parameters
        ----------
        user_input : str | None
            User answer. None indicates the exercise start.

        Returns
        -------
        Dict
            Exercise result payload.
        """
        exercise_index = self.get_current_exercise()

        engine = CoreExerciseEngine(
            module=self.module,
            session=self.session
        )

        return engine.run(exercise_index, user_input)

    # -------------------------------------------------------
    # Engine factory
    # -------------------------------------------------------
    def get_exercise_engine(self) -> CoreExerciseEngine:
        """
        Create exercise engine instance.
        """

        return CoreExerciseEngine(
            module=self.module,
            session=self.session
        )

    # -------------------------------------------------------
    # Context builder
    # -------------------------------------------------------
    def build_context(self) -> Dict[str, Any]:
        """
        Build context passed to exercises / prompts.
        """

        context = super().build_context()

        context.update({
            "module": "core_vocabulary",
            "exercise": self.get_current_exercise(),
        })

        return context

    # -------------------------------------------------------
    # Debug helpers
    # -------------------------------------------------------
    def debug_info(self) -> Dict[str, Any]:
        """
        Debug information for monitoring.
        """

        return {
            "module_id": self.module.id,
            "exercise": self.get_current_exercise(),
        }
