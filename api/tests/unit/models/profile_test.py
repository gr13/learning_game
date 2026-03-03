import sys
from typing import Dict
# adding src to the system path
from pathlib import Path
sys.path.append(str(Path(sys.path[0]).parent))
sys.path.append(str(Path(sys.path[0]).parent.parent))
sys.path.append(str(Path(sys.path[0]).parent.parent.parent))
from app.models.profile import ProfileModel  # noqa:E402
from tests.base_test import BaseTest  # noqa:E402


class ProfileTest(BaseTest):

    def test_user_json(self):
        """
        Creates user model and checks the returned json
        """
        with self.app_context():
            profile = ProfileModel()
            profile.save_to_db()

            saved = ProfileModel.find_by_id(profile.id)
            expected = {
                "id": profile.id,
                "user_level": "A2",
                "preferences": "",
            }
            actual: Dict = saved.json()
            self.assertDictEqual(
                actual, expected,
                f"Profile JSON is incorrect expected: {expected}, actual: "
                f"{actual}")
