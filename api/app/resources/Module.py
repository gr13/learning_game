import os
import base64
import uuid
import json
from flask_restful import Resource
from flask import request
from typing import Dict


class Module(Resource):
    """ The Module view """
    class_id = "Module"

    def get(self, module_id):
        if module_id == 1:
            return {"message": "Module 1 is requested"}
        elif module_id == 2:
            return {"message": "Module 2 is requested"}
        elif module_id == 3:
            return {"message": "Module 3 is requested"}
        elif module_id == 4:
            return {"message": "Module 4 is requested"}
        elif module_id == 5:
            return {"message": "Module 5 is requested"}
        elif module_id == 6:
            return {"message": "Module 6 is requested"}
        else:
            return {"message": "Invalid module"}, 404

