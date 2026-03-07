from typing import Any, Dict

from app.models.modules import ModulesModel
from app.enums import ModuleTypeEnum

# module engines
from app.modules.vocabulary.core.engine import run as run_core
from app.modules.vocabulary.domain.engine import run as run_domain
from app.modules.exam.reading.engine import run as run_reading
from app.modules.exam.writing.engine import run as run_writing
from app.modules.exam.speaking.engine import run as run_speaking


MODULE_REGISTRY = {
    ModuleTypeEnum.CORE: run_core,
    ModuleTypeEnum.DOMAIN: run_domain,
    ModuleTypeEnum.READING: run_reading,
    ModuleTypeEnum.WRITING: run_writing,
    ModuleTypeEnum.SPEAKING: run_speaking,
}


# -------------------------------------------------------
# Public API
# -------------------------------------------------------
def run_module(
        module: ModulesModel, session, user_input: str | None = None
        ) -> Dict[str, Any]:
    """
    Main entrypoint for executing a module.

    Parameters
    ----------
    module : ModulesModel
        Current module instance

    session :
        Current learning session

    user_input : str | None
        User response if applicable

    Returns
    -------
    Dict
        Response payload for API
    """

    engine = get_module_engine(module)

    return engine(module, session, user_input)


# -------------------------------------------------------
# Engine resolution
# -------------------------------------------------------
def get_module_engine(module: ModulesModel):
    """
    Resolve the correct module engine
    based on module type.
    """

    module_type = module.module_type

    if module_type not in MODULE_REGISTRY:
        raise ValueError(f"Unsupported module type: {module_type}")

    return MODULE_REGISTRY[module_type]


# -------------------------------------------------------
# Module lifecycle helpers
# -------------------------------------------------------
def initialize_module(module: ModulesModel):
    """
    Run module initialization logic.
    """

    from app.modules.lifecycle.module_initializer import initialize

    return initialize(module)


def finalize_module(module: ModulesModel):
    """
    Run module finalization logic.
    """

    from app.modules.lifecycle.module_finalizer import finalize

    return finalize(module)


# -------------------------------------------------------
# Progress helpers
# -------------------------------------------------------
def is_module_completed(module: ModulesModel) -> bool:
    """
    Determine if module is completed.
    """

    return module.done


def mark_module_completed(module: ModulesModel):
    """
    Mark module as completed.
    """

    module.mark_done()
