# from flask_restful import Resource
# from flask import request
# from flask import current_app
# from app.models.modules import ModulesModel
# from app.modules.engine import ModuleEngine
# from app.sessions.session_store import SessionStore
# from app.monitoring.performance import time_register

# # TODO:
# # •	Add response-type detector (JSON vs plain text auto handler)
# # •	Detect JSON vs plain text
# # •	Prevent rendering crashes
# # •	Clean separation of modes

# # •	refactor into a PromptBuilder class for cleaner scaling
# # •	Centralized prompt generation
# # •	Clean separation of concerns
# # •	Scalable for Modules 2–5


# class Module(Resource):
#     """ The Module view """
#     class_id = "Module"

#     def __init__(self):
#         self.module_engine = ModuleEngine()

#     @time_register("Module GET")
#     def get(self, module_id):
#         """
#         initiates the module
#         """

#         module = ModulesModel.find_by_id(module_id)

#         if not module:
#             return {"error": "Module not found"}, 404

#         session = SessionStore.create_session(module_id=module_id)
#         current_app.logger.info(
#             f"module_start | module_id={module_id} | session_id={session.id}"  # noqa: E501
#         )
#         result = self.module_engine.run_module(
#             module=module,
#             session=session,
#             user_input=None
#         )
#         result["session_id"] = session.id
#         return result

#     @time_register("Module POST")
#     def post(self, module_id):
#         """
#         extablish countious learning

#         Expects JSON:
#         {
#         "module_id": 1,
#         "session_id": 123,
#         "user_input": "Ich gehe zur Schule"
#         }
#         """
#         data = request.get_json()

#         session_id = data.get("session_id")
#         current_app.logger.info(
#             f"module_continue | module_id={module_id} | session_id={session_id}"  # noqa: E501
#         )
#         user_input = data.get("user_input")

#         # Basic validation
#         if not session_id or not user_input:
#             return {"error": "Missing required fields"}, 400

#         module = ModulesModel.find_by_id(module_id)

#         if not module:
#             return {"error": "Module not found"}, 404

#         session = SessionStore.get_session(session_id)
#         if not session:
#             return {"error": "Invalid session"}, 404

#         result = self.module_engine.run_module(
#             module=module,
#             session=session,
#             user_input=user_input
#         )
#         return result
