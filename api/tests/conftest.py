import os
import pytest
from app import create_app
from app.db import db
from sqlalchemy.orm import scoped_session, sessionmaker


SQLALCHEMY_DATABASE_URI = (
    f"mysql+mysqlconnector://{os.environ['MYSQL_USER']}:"
    f"{os.environ['MYSQL_ROOT_PASSWORD']}@"
    f"{os.environ['MYSQL_HOST']}:3306/"
    f"{os.environ['TEST_DATABASE_NAME']}"
)


@pytest.fixture(scope="session")
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
def db_session(app):
    connection = db.engine.connect()
    transaction = connection.begin()

    Session = scoped_session(sessionmaker(bind=connection))
    db.session = Session

    yield Session

    transaction.rollback()
    connection.close()
    Session.remove()
