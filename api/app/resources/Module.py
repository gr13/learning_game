from flask_restful import Resource
from flask import request
from flask import current_app

from app.lessons.orchestrator import LessonOrchestrator
from app.models.modules import ModulesModel
from app.sessions.session_store import SessionStore
from app.monitoring.performance import time_register
# from app.models.profile import ProfileModel
# from app.models.exercises import ExercisesModel

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
        self.orchestrator = LessonOrchestrator()

    @time_register("Module POST")
    def post(self, module_type_id):
        """
        extablish countious learning

        Expects JSON:
        {
            "session_id": 123,
            "user_input": "Ich gehe zur Schule"
        }
        """
        data = request.get_json(silent=True) or {}

        session_id = data.get("session_id")
        raw_user_input = data.get("user_input")
        user_input = raw_user_input if isinstance(raw_user_input, str) else ""
        user_input = user_input.strip()

        if not session_id:
            return {"mode": "error", "message": "Missing session_id"}, 400

        if not user_input:
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

        return self.orchestrator.continue_turn(
                module_type_id=module_type_id,
                module=module,
                session=session,
                user_input=user_input,
            )
