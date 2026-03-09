from typing import Dict, Any


class PromptBuilder:
    """
    Builds prompts for AI-based exercises.
    """

    # -------------------------------------------------------
    # Public API
    # -------------------------------------------------------
    def build(
        self,
        instruction: str,
        tasks: list[str],
        context: Dict[str, Any]
    ) -> str:
        """
        Build final prompt.
        """

        prompt = ""

        prompt += self.build_instruction(instruction)
        prompt += self.build_context(context)
        prompt += self.build_tasks(tasks)

        return prompt

    # -------------------------------------------------------
    # Instruction section
    # -------------------------------------------------------
    def build_instruction(self, instruction: str) -> str:
        """
        Build instruction part of the prompt.
        """

        return f"Instruction:\n{instruction}\n\n"

    # -------------------------------------------------------
    # Context section
    # -------------------------------------------------------
    def build_context(self, context: Dict[str, Any]) -> str:
        """
        Add contextual information.
        """

        if not context:
            return ""

        text = "Context:\n"

        for key, value in context.items():
            text += f"{key}: {value}\n"

        text += "\n"

        return text

    # -------------------------------------------------------
    # Tasks section
    # -------------------------------------------------------
    def build_tasks(self, tasks: list[str]) -> str:
        """
        Build task list.
        """

        if not tasks:
            return ""

        text = "Tasks:\n"

        for i, task in enumerate(tasks, start=1):
            text += f"Task {i}: {task}\n"

        return text

    # -------------------------------------------------------
    # Helpers
    # -------------------------------------------------------
    def add_examples(self, examples: list[Dict[str, str]]) -> str:
        """
        Add examples section to prompt.
        """

        if not examples:
            return ""

        text = "Examples:\n"

        for example in examples:
            text += f"{example}\n"

        text += "\n"

        return text

    def add_rules(self, rules: list[str]) -> str:
        """
        Add grammar or instruction rules.
        """

        if not rules:
            return ""

        text = "Rules:\n"

        for rule in rules:
            text += f"- {rule}\n"

        text += "\n"

        return text
