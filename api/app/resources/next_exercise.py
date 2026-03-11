from flask_restful import Resource
from flask import request
from app.lessons.engine import LessonEngine
from app.models.modules import ModulesModel
from app.sessions.session_store import SessionStore


class NextExercise(Resource):
    def __init__(self):
        self.module_engine = LessonEngine()

    def post(self):
        data = request.get_json(silent=True) or {}
        session_id = data.get("session_id")
        if not session_id:
            return {"mode": "error", "message": "Missing session_id"}, 400

        session = SessionStore.get_session(session_id)
        if not session:
            return {"mode": "error", "message": "Invalid session"}, 404

        module = ModulesModel.find_by_id(session.module_id)
        if not module:
            return {"mode": "error", "message": "Module not found"}, 404

        return self.module_engine.next_exercise(
                module_type_id=ModulesModel.module_id_from_module_type(
                    module.module_type),
                module=module,
                session=session,
            )
