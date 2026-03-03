"""
BaseTest
This class should be parent to each test.
It allows for instantiation of the database dynamically,
and make sure that it is a new, blank database each time.
"""
import os
import sys
from unittest import TestCase

# adding src to the system path
from pathlib import Path
sys.path.append(str(Path(sys.path[0]).parent))
from dotenv import load_dotenv  # noqa:E402
load_dotenv()
os.environ["LOG_FILENAME"] = "api.log"

from app import app  # noqa:E402
from app.db import db  # noqa:E402


class BaseTest(TestCase):
    # SQLALCHEMY_DATABASE_URI = "sqlite:///data_test.db"
    SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{os.environ['MYSQL_USER']}:{os.environ['MYSQL_ROOT_PASSWORD']}@{os.environ['MYSQL_HOST']}:3306/{os.environ['TEST_DATABASE_NAME']}"  # noqa: E501

    @classmethod
    def setUpClass(cls):
        """
        A class method called before tests in an individual class are run.
        setUpClass is called with the class as the only argument and must
        be decorated as a classmethod()
        """
        app.config["SQLALCHEMY_DATABASE_URI"] = BaseTest.SQLALCHEMY_DATABASE_URI  # noqa: E501
        app.config["DEBUG"] = True
        with app.app_context():
            db.init_app(app)

    def setUp(self):
        """
        Method called to prepare the test fixture. This is called immediately
        before calling the test method; other than AssertionError or SkipTest,
        any exception raised by this method will be considered an error rather
        than a test failure. The default implementation does nothing.
        """
        with app.app_context():
            db.create_all()
        self.app = app.test_client
        self.app_context = app.app_context

    def tearDown(self):
        """
        Method called immediately after the test method has been called and
        the result recorded. This is called even if the test method raised an
        exception, so the implementation in subclasses may need to be
        particularly careful about checking internal state. Any exception,
        other than AssertionError or SkipTest, raised by this method will be
        considered an additional error rather than a test failure (thus
        increasing the total number of reported errors).
        This method will only be called if the setUp() succeeds, regardless of
        the outcome of the test method. The default implementation does
        nothing.
        """
        with app.app_context():
            db.session.remove()
            db.drop_all()
