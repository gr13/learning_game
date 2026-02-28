from flask_restful import Resource
from app.utils.module_utils import ModuleUtils


class Module(Resource):
    """ The Module view """
    class_id = "Module"

    def __init__(self):
        self.module_utils = ModuleUtils()

    def get(self, module_id):
        result = self.module_utils.handle_module(module_id)
        return result
