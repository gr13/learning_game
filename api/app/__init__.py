import os
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from app.db import db
from app.resources.helloworld import HelloWorld
# from app.resources.module import Module


def create_app(config: dict | None = None):

    app = Flask(__name__)
    # to transfer images increase max context lenght
    app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10MB
    app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY", "dev-secret")
    app.config["DEBUG"] = os.environ.get("DEBUG", "0") == "1"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if config:
        app.config.update(config)
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = (
            f"mysql+mysqlconnector://"
            f"{os.environ.get('MYSQL_USER')}:"
            f"{os.environ.get('MYSQL_ROOT_PASSWORD')}@"
            f"{os.environ.get('MYSQL_HOST')}:3306/"
            f"{os.environ.get('DATABASE_NAME')}"
        )

    CORS(app)  # adress Cross-Origin Resourse Aharing for Flask app
    api = Api(app)
    db.init_app(app)

    api.add_resource(HelloWorld, "/")
    # api.add_resource(Module, "/modules/<int:module_id>")

    return app
