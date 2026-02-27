import os
import base64
import uuid
import json
from flask_restful import Resource
from flask import request
from typing import Dict


class Module(Resource):
    """ The HelloWorld view """
    class_id = "ImageUtility"

    
