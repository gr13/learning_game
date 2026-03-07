from abc import ABC, abstractmethod
from typing import Dict, Any


class BasePlan(ABC):
    """
    Base class for exercise plans.

    A plan defines:
    - instructions
    - structure of the task
    - prompt template
    """

    def __init__(self, plan_data: Dict[str, Any]):
        self.plan_data = plan_data

    # -------------------------------------------------------
    # Plan lifecycle
    # -------------------------------------------------------

    def load(self) -> Dict[str, Any]:
        """
        Return raw plan data.
        """

        return self.plan_data

    # -------------------------------------------------------
    # Prompt generation
    # -------------------------------------------------------

    @abstractmethod
    def build_prompt(self, context: Dict[str, Any]) -> str:
        """
        Build the AI prompt using plan and context.
        """
        pass

    # -------------------------------------------------------
    # Task structure
    # -------------------------------------------------------

    def get_instruction(self) -> str:
        """
        Return instruction text.
        """

        return self.plan_data.get("instruction", "")

    def get_examples(self):
        """
        Return example tasks if defined.
        """

        return self.plan_data.get("examples", [])

    def get_rules(self):
        """
        Return grammar or logic rules.
        """

        return self.plan_data.get("rules", [])

    # -------------------------------------------------------
    # Metadata
    # -------------------------------------------------------

    def get_task_count(self) -> int:
        """
        Number of tasks in this exercise.
        """

        return self.plan_data.get("task_count", 5)

    def get_level(self) -> str:
        """
        Language level of the plan.
        """

        return self.plan_data.get("level", "A2")

    # -------------------------------------------------------
    # Validation
    # -------------------------------------------------------

    def validate(self) -> None:
        """
        Validate plan structure.
        """

        if "instruction" not in self.plan_data:
            raise ValueError("Plan missing instruction")

        if "task_count" not in self.plan_data:
            raise ValueError("Plan missing task_count")
