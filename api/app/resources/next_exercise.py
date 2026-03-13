from flask_restful import Resource
from flask import request
from app.lessons.engine import LessonEngine
from app.models.modules import ModulesModel
from app.sessions.session_store import SessionStore
from app.models.exercises import ExercisesModel


class NextExercise(Resource):
    def __init__(self):
        self.module_engine = LessonEngine()

    def post(self):
        """
        Logic
        1. create old_session from session_id
        2. get module from old_session.module_id
        3. get old_exercise from exercises.session_id
        4. get old_exercise.exercise_index
        5. create session
        6. create exercise with session, module, exercise_index + 1
        7. return self.module_engine.start
        """
        data = request.get_json(silent=True) or {}
        session_id = data.get("session_id")
        if not session_id:
            return {"mode": "error", "message": "Missing session_id"}, 400

        old_session = SessionStore.get_session(session_id)
        if not old_session:
            return {"mode": "error", "message": "Invalid session"}, 404

        if not old_session.module_id:
            return {
                "mode": "error", "message": "Session has no module_id"}, 400

        module = ModulesModel.find_by_id(old_session.module_id)
        if not module:
            return {"mode": "error", "message": "Module not found"}, 404

        module_type_id = ModulesModel.module_id_from_module_type(
            module.module_type)
        if module_type_id is None:
            return {"mode": "error", "message": "Unsupported module type"}, 400

        old_exercise = ExercisesModel.find_by_session_id(session_id)
        if not old_exercise:
            return {
                "mode": "error",
                "message": f"Exercise is not found for session: {session_id}",
            }, 404

        old_exercise_index = old_exercise.exercise_index or 0

        session = SessionStore.create_session()
        session.set_module_id(module.id)

        exercise = ExercisesModel(
            module_id=module.id,
            session_id=session.id,
            exercise_index=old_exercise_index + 1,
        )
        exercise.save_to_db()

        return self.module_engine.start(
            module_type_id=module_type_id,
            module=module,
            session=session,
            exercise=exercise
        )
