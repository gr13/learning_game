from flask_restful import Resource
from flask import request


class EndModule(Resource):
    def post(self):
        data = request.get_json(silent=True) or {}
        session_id = data.get("session_id")
        # validate session -> module from session.module_id
        # call engine.end_module(module, session)
        return session_id
