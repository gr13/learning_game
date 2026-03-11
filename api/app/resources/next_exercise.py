from flask_restful import Resource
from flask import request


class NextExercise(Resource):
    def post(self):
        data = request.get_json(silent=True) or {}
        session_id = data.get("session_id")
        # validate session -> module from session.module_id
        # call engine.next_exercise(module, session)
        return session_id
