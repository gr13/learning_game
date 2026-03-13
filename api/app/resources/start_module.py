from flask_restful import Resource
from flask import request
from flask import current_app

from app.lessons.engine import LessonEngine
from app.models.modules import ModulesModel
from app.models.training_lesson import TrainingLessonModel
from app.sessions.session_store import SessionStore
from app.models.profile import ProfileModel
from app.models.exercises import ExercisesModel

from app.monitoring.performance import time_register


class StartModule(Resource):
    def __init__(self):
        self.module_engine = LessonEngine()

    @time_register("Module GET")
    def post(self, module_type_id: int):
        """
        Start module:
        - new session/module when no session_id
        - resume existing session/module when session_id provided
        """
        session_id = request.args.get("session_id", type=int)

        requested_type = ModulesModel.module_type_from_module_id(
            module_type_id)
        if requested_type is None:
            return {
                "mode": "error",
                "message": f"Unsupported module_type_id: {module_type_id}",
            }, 400

        if session_id:
            """
            training_lesson exists: e.g. module 2
            The logic: session exists, so we can get the current module
            and exercise.
            - mark the module connected to session as done
            """
            self._mark_module_and_session_as_done(session_id)

        else:
            """
            New traning day
            Create training_lesson
            """
            profile = ProfileModel.find_by_id()
            lesson = TrainingLessonModel(
                user_level=profile.get_user_level() if profile else "A2")
            lesson.save_to_db()
        # standard flow for both cases: create new module and exercise,
        # connect to session
        # create module
        module = ModulesModel(
            training_lesson_id=lesson.id,
            module_type=requested_type,
            done=False
        )
        module.save_to_db()
        # always create session
        session = SessionStore.create_session()
        session.set_module_id(module.id)

        # create exercises # 1
        exercise = ExercisesModel(
            module_id=module.id,
            session_id=session.id,
            exercise_index=1
        )
        exercise.save_to_db()

        current_app.logger.info(
            f"module_start | module_type_id={module_type_id} | session_id={session.id}"  # noqa: E501
        )

        result = self.module_engine.start(
            module_type_id=module_type_id,
            module=module,
            session=session,
            exercise=exercise
        )
        result["session_id"] = session.id
        return result

    @staticmethod
    def _mark_module_and_session_as_done(session_id: int):
        """
        Mark old module as done.
        We don't care about error here, just return None
        TODO: add logging about failed session id
        """
        session = SessionStore.get_session(session_id)
        if not session:
            return

        if not session.module_id:
            return

        module = ModulesModel.find_by_id(session.module_id)
        if not module:
            return
        module.mark_done()
