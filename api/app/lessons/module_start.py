from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from app.models.exercises import ExercisesModel
from app.models.modules import ModulesModel
from app.models.profile import ProfileModel
from app.models.sessions import SessionsModel
from app.models.training_lesson import TrainingLessonModel
from app.sessions.session_store import SessionStore


class StartErrorCode(str, Enum):
    INVALID_SESSION = "invalid_session"
    SESSION_NO_MODULE = "session_no_module"
    MODULE_NOT_FOUND = "module_not_found"
    MODULE_MISMATCH = "module_mismatch"
    UNSUPPORTED_MODULE_TYPE = "unsupported_module_type"


# TODO: refactor (put to the proper place with exceptions)
class ModuleStartError(Exception):
    def __init__(self, code: StartErrorCode, message: str):
        self.code = code
        self.message = message
        super().__init__(message)


@dataclass
class ModuleStartContext:
    session: SessionsModel
    module: ModulesModel
    exercise: ExercisesModel


class ModuleStart:
    @staticmethod
    def start_or_resume(
        module_type_id: int,
        session_id: int | None,
    ) -> ModuleStartContext:
        requested_type = ModulesModel.module_type_from_module_id(
            module_type_id)
        if requested_type is None:
            raise ModuleStartError(
                StartErrorCode.UNSUPPORTED_MODULE_TYPE,
                f"Unsupported module_type_id: {module_type_id}",
            )

        if session_id:
            return ModuleStart._resume_training_day(session_id, requested_type)

        return ModuleStart._create_new_training_day(requested_type)

    @staticmethod
    def _resume_training_day(
            session_id: int,
            requested_type
            ) -> ModuleStartContext:
        session = SessionStore.get_session(session_id)
        if not session:
            raise ModuleStartError(
                StartErrorCode.INVALID_SESSION, "Invalid session")

        if not session.module_id:
            raise ModuleStartError(
                StartErrorCode.SESSION_NO_MODULE,
                "Session has no module_id",
            )

        module = ModulesModel.find_by_id(session.module_id)
        if not module:
            raise ModuleStartError(
                StartErrorCode.MODULE_NOT_FOUND,
                "Module not found",
            )

        if module.module_type != requested_type:
            raise ModuleStartError(
                StartErrorCode.MODULE_MISMATCH,
                "Session/module type mismatch",
            )

        rows = ExercisesModel.find_by_session_id(session.id)
        exercise = rows[-1] if rows else ExercisesModel(
            module_id=module.id,
            session_id=session.id,
            exercise_index=1,
        )
        if not rows:
            exercise.save_to_db()

        return ModuleStartContext(
            session=session,
            module=module,
            exercise=exercise,
        )

    @staticmethod
    def _create_new_training_day(requested_type) -> ModuleStartContext:
        session = SessionStore.create_session()

        profile = ProfileModel.find_by_id()
        lesson = TrainingLessonModel(
            user_level=profile.get_user_level() if profile else "A2",
        )
        lesson.save_to_db()

        module = ModulesModel(
            training_lesson_id=lesson.id,
            module_type=requested_type,
            done=False,
        )
        module.save_to_db()
        session.set_module_id(module.id)

        exercise = ExercisesModel(
            module_id=module.id,
            session_id=session.id,
            exercise_index=1,
        )
        exercise.save_to_db()

        return ModuleStartContext(
            session=session,
            module=module,
            exercise=exercise,
        )
