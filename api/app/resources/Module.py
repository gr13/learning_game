from flask_restful import Resource
from flask import request
from app.utils.module_utils import ModuleUtils
from app.utils.session_store import SessionStore


class Module(Resource):
    """ The Module view """
    class_id = "Module"

    def __init__(self):
        self.module_utils = ModuleUtils()

    def get(self, module_id):
        """
        initiates the module
        """
        session_id = SessionStore.create_session(module_id=module_id)
        result = self.module_utils.handle_module(module_id, session_id)
        result["session_id"] = session_id
        return result

    def post(self, module_id):
        """
        extablish countious learning

        Expects JSON:
        {
        "module_id": 1,
        "session_id": 123,
        "user_input": "Ich gehe zur Schule"
        }
        """
        data = request.get_json()

        session_id = data.get("session_id")
        user_input = data.get("user_input")

        # Basic validation
        if not module_id or not session_id or not user_input:
            return {"error": "Missing required fields"}, 400

        # Route to correct module continuation
        if module_id == 1:
            result = self.module_utils.continue_module1(
                session_id=session_id,
                user_input=user_input
            )
            return result

        return {"error": "Module not implemented"}, 400
