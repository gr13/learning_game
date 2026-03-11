from flask_restful import Resource
from flask import request
from flask import current_app

from app.lessons.engine import LessonEngine
from app.models.modules import ModulesModel
from app.models.training_lesson import TrainingLessonModel
from app.sessions.session_store import SessionStore
from app.monitoring.performance import time_register
from app.models.profile import ProfileModel

# TODO:
# •	Add response-type detector (JSON vs plain text auto handler)
# •	Detect JSON vs plain text
# •	Prevent rendering crashes
# •	Clean separation of modes

# •	refactor into a PromptBuilder class for cleaner scaling
# •	Centralized prompt generation
# •	Clean separation of concerns
# •	Scalable for Modules 2–5


class Module(Resource):
    """ The Module view """
    class_id = "Module"

    def __init__(self):
        self.module_engine = LessonEngine()

    @time_register("Module GET")
    def get(self, module_type_id):
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

        if session_id:  # training day exists: e.g. module 2
            session = SessionStore.get_session(session_id)
            if not session:
                return {"mode": "error", "message": "Invalid session"}, 404

            if not session.module_id:
                return {
                    "mode": "error",
                    "message": "Session has no module_id"}, 400

            module = ModulesModel.find_by_id(session.module_id)
            if not module:
                return {"mode": "error", "message": "Module not found"}, 404

            if module.module_type != requested_type:
                return {
                    "mode": "error",
                    "message": "Session/module type mismatch",
                }, 409

        else:  # new training day
            # create session
            session = SessionStore.create_session()
            # create lesson
            profile = ProfileModel.find_by_id(1)
            lesson = TrainingLessonModel(
                user_level=profile.get_user_level() if profile else "A2")
            lesson.save_to_db()
            # create module
            module = ModulesModel(
                training_lesson_id=lesson.id,
                module_type=requested_type,
                done=False
            )
            module.save_to_db()
            session.set_module_id(module.id)

        current_app.logger.info(
            f"module_start | module_type_id={module_type_id} | session_id={session.id}"  # noqa: E501
        )

        result = self.module_engine.start(
            module_type_id=module_type_id,
            module=module,
            session=session,
        )
        result["session_id"] = session.id
        return result

    @time_register("Module POST")
    def post(self, module_type_id):
        """
        extablish countious learning

        Expects JSON:
        {
            "session_id": 123,
            "button": "answer" | "next_exercise" | "end_module",
            "user_input": "..."   # required only when button == "answer"
        }
        """
        data = request.get_json(silent=True) or {}

        session_id = data.get("session_id")
        button = data.get("button", "answer")
        user_input = data.get("user_input")

        current_app.logger.info(
            f"module_continue | module_type_id={module_type_id} | session_id={session_id}"  # noqa: E501
        )

        if not session_id:
            return {"mode": "error", "message": "Missing session_id"}, 400

        if button == "answer" and not user_input:
            return {"mode": "error", "message": "Missing user_input"}, 400

        session = SessionStore.get_session(session_id)
        if not session:
            return {"mode": "error", "message": "Invalid session"}, 404

        if not session.module_id:
            return {
                "mode": "error", "message": "Session has no module_id"
            }, 400

        module = ModulesModel.find_by_id(session.module_id)

        if not module:
            return {"mode": "error", "message": "Module not found"}, 404

        requested_type = ModulesModel.module_type_from_module_id(
            module_type_id)
        if requested_type is None or module.module_type != requested_type:
            return {
                "mode": "error", "message": "Session/module type mismatch"
            }, 409

        current_app.logger.info(
            f"module_continue | module_type_id={module_type_id} | session_id={session_id}",  # noqa: E501
        )

        if button == "next_exercise":
            return self.module_engine.next_exercise(
                module_type_id=module_type_id,
                module=module,
                session=session,
            )

        if button == "end_module":
            return self.module_engine.end_module(
                module_type_id=module_type_id,
                module=module,
                session=session,
            )

        if button != "answer":
            return {
                "mode": "error",
                "message": f"Unsupported button: {button}"
            }, 400

        return self.module_engine.answer(
                module_type_id=module_type_id,
                module=module,
                session=session,
                user_input=user_input,
            )
