import os
from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from app.db import db
from app.monitoring.logging import configure_logging
from app.monitoring.request_logger import register_request_logging
from app.models.exercises import ExercisesModel  # noqa: F401
from app.resources.helloworld import HelloWorld
from app.resources.module import Module
from app.resources.next_exercise import NextExercise
from app.resources.end_module import EndModule


import app.models as app_models  # noqa: F401


def create_app(config: dict | None = None):
    app = Flask(__name__)

    # ------------------------------------------------
    # Base config
    # ------------------------------------------------
    app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10MB
    app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY", "dev-secret")
    app.config["DEBUG"] = os.environ.get("DEBUG", "0") == "1"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # ------------------------------------------------
    # Database configuration
    # ------------------------------------------------
    if config:
        app.config.update(config)
        configure_logging(app)
    else:
        user = os.environ.get("MYSQL_USER")
        password = os.environ.get("MYSQL_ROOT_PASSWORD")
        host = os.environ.get("MYSQL_HOST")
        db_name = os.environ.get("DATABASE_NAME")

        # ------------------------------------------------
        # Validate environment variables
        # ------------------------------------------------
        for key, value in {
            "MYSQL_USER": user,
            "MYSQL_HOST": host,
            "DATABASE_NAME": db_name,
        }.items():
            if not value:
                app.logger.warning(f"ENV VARIABLE MISSING: {key}")

        if not password:
            app.logger.warning("ENV VARIABLE MISSING: MYSQL_ROOT_PASSWORD")

        # ------------------------------------------------
        # Build database URI
        # ------------------------------------------------
        db_uri = (
            f"mysql+mysqlconnector://"
            f"{user}:{password}@"
            f"{host}:3306/"
            f"{db_name}"
        )

        # masked version for logs
        masked_uri = (
            f"mysql+mysqlconnector://"
            f"{user}:******@"
            f"{host}:3306/"
            f"{db_name}"
        )

        app.logger.info("Database configuration detected:")
        app.logger.info(f"MYSQL_USER={user}")
        app.logger.info(f"MYSQL_HOST={host}")
        app.logger.info(f"DATABASE_NAME={db_name}")
        app.logger.info(f"SQLALCHEMY_DATABASE_URI={masked_uri}")

        app.config["SQLALCHEMY_DATABASE_URI"] = db_uri

        # app.config["SQLALCHEMY_DATABASE_URI"] = (
        #     f"mysql+mysqlconnector://"
        #     f"{os.environ.get('MYSQL_USER')}:"
        #     f"{os.environ.get('MYSQL_ROOT_PASSWORD')}@"
        #     f"{os.environ.get('MYSQL_HOST')}:3306/"
        #     f"{os.environ.get('DATABASE_NAME')}"
        # )

    # ------------------------------------------------
    # Extensions
    # ------------------------------------------------
    CORS(app)  # adress Cross-Origin Resourse Aharing for Flask app
    api = Api(app)
    db.init_app(app)

    # ------------------------------------------------
    # Routes
    # ------------------------------------------------
    api.add_resource(HelloWorld, "/")
    api.add_resource(Module, "/modules/<int:module_type_id>")
    api.add_resource(
        NextExercise, "/modules/<int:module_type_id>/next-exercise"
    )
    api.add_resource(EndModule, "/modules/<int:module_type_id>/end-module")

    # ------------------------------------------------
    # Request logging
    # ------------------------------------------------
    register_request_logging(app)

    return app
