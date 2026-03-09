from typing import Any, Dict

from app.models.modules import ModulesModel
from app.enums import ModuleTypeEnum
from app.models.sessions import SessionsModel

# module engines
from app.modules.vocabulary.core.engine import run as run_core


# from app.modules.exam.reading.engine import run as run_reading
# from app.modules.exam.writing.engine import run as run_writing
# from app.modules.exam.speaking.engine import run as run_speaking
# Maps module types to their execution entrypoints.
#
# Each module exposes a function with the same signature:
#     run(module, session, user_input)
# ModuleEngine dynamically resolves the correct engine
# and executes it through this registry.
# Example:
#     module.module_type == CORE
# results in:
#     run_core(module, session, user_input)
MODULE_REGISTRY = {
    ModuleTypeEnum.CORE: run_core,
    # ModuleTypeEnum.DOMAIN: run_domain,
    # ModuleTypeEnum.READING: run_reading,
    # ModuleTypeEnum.WRITING: run_writing,
    # ModuleTypeEnum.SPEAKING: run_speaking,
}


class ModuleEngine:
    # -------------------------------------------------------
    # Public API
    # -------------------------------------------------------
    def run_module(
            self,
            module: ModulesModel,
            session: SessionsModel,
            user_input: str | None = None
            ) -> Dict[str, Any]:
        """
        Execute a learning module.
        This is the main entrypoint used by the API layer.
        Execution flow
        --------------
        Flask API
            ↓
        ModuleEngine.run_module()
            ↓
        Resolve module engine from MODULE_REGISTRY
            ↓
        Call engine(module, session, user_input)
            ↓
        Module-specific engine handles the logic
        Example
        -------
        If module.module_type == CORE then:
            engine = run_core
        which means this line:
            engine(module, session, user_input)
        becomes:
            run_core(module, session, user_input)

        Parameters
        ----------
        module : ModulesModel
            Module database record
        session :
            Current learning session
        user_input : str | None
            User answer submitted from API.
            None means module is being started (GET request).

        Returns
        -------
        Dict
            API response payload produced by the module engine.
        """

        if not module.done and user_input is None:
            self.initialize_module(module)

        engine = self.get_module_engine(module)

        result = engine(module, session, user_input)

        if not module.done and self.is_module_completed(module):
            self.mark_module_completed(module)
            self.finalize_module(module, session)

        return result

    # -------------------------------------------------------
    # Engine resolution
    # -------------------------------------------------------
    def get_module_engine(self, module: ModulesModel):
        """
        Resolve the correct module execution function.
        The registry maps module types to engine entrypoints.
        Example
        -------
        MODULE_REGISTRY = {
            ModuleTypeEnum.CORE: run_core
        }
        So if:
            module.module_type == CORE
        this function returns:
            run_core
        which will later be executed as:
            run_core(module, session, user_input)
        """

        module_type = module.module_type

        if module_type not in MODULE_REGISTRY:
            raise ValueError(f"Unsupported module type: {module_type}")

        return MODULE_REGISTRY[module_type]

    # -------------------------------------------------------
    # Module lifecycle helpers
    # -------------------------------------------------------
    def initialize_module(self, module: ModulesModel):

        from app.modules.lifecycle.module_initializer import ModuleInitializer
        initializer = ModuleInitializer(module)

        return initializer.initialize()

    def finalize_module(
            self,
            module: ModulesModel,
            session: SessionsModel):
        """
        Run module finalization logic.
        """

        from app.modules.lifecycle.module_finalizer import ModuleFinalizer

        finalizer = ModuleFinalizer(module, session)
        return finalizer.finalize()

    # -------------------------------------------------------
    # Progress helpers
    # -------------------------------------------------------
    def is_module_completed(self, module: ModulesModel) -> bool:
        """
        Determine if module is completed.
        """
        return module.done

    def mark_module_completed(
            self, module: ModulesModel, session: SessionsModel
            ):
        """
        Mark module as completed.
        """
        module.mark_done()
