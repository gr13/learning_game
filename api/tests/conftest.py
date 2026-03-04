import os
import pytest
from app import create_app
from app.db import db

SQLALCHEMY_DATABASE_URI = (
    f"mysql+mysqlconnector://{os.environ['MYSQL_USER']}:"
    f"{os.environ['MYSQL_ROOT_PASSWORD']}@"
    f"{os.environ['MYSQL_HOST']}:3306/"
    f"{os.environ['TEST_DATABASE_NAME']}"
)


@pytest.fixture(scope="function")
def app():
    app = create_app({
        "SQLALCHEMY_DATABASE_URI": SQLALCHEMY_DATABASE_URI,
        "TESTING": True,
    })

    ctx = app.app_context()
    ctx.push()

    db.create_all()

    yield app   # ← test runs here

    db.session.remove()
    db.drop_all()
    ctx.pop()


@pytest.fixture(scope="function")
def client(app):
    return app.test_client()
