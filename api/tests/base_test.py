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

from app import create_app  # noqa:E402
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
        cls.app = create_app({
            "SQLALCHEMY_DATABASE_URI": cls.SQLALCHEMY_DATABASE_URI,
            "TESTING": True,
        })

    def setUp(self):
        """
        Method called to prepare the test fixture. This is called immediately
        before calling the test method; other than AssertionError or SkipTest,
        any exception raised by this method will be considered an error rather
        than a test failure. The default implementation does nothing.
        """
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

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
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
