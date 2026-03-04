import os
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from app.db import db
from app.resources.helloworld import HelloWorld
from app.resources.module import Module


def create_app(config: dict | None = None):

    app = Flask(__name__)
    # to transfer images increase max context lenght
    app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10MB
    app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY", "dev-secret")
    app.config["DEBUG"] = True

    if config:
        app.config.update(config)

    CORS(app)  # adress Cross-Origin Resourse Aharing for Flask app
    api = Api(app)

    api.add_resource(HelloWorld, "/")
    api.add_resource(Module, "/modules/<int:module_id>")

    db.init_app(app)
    return app
