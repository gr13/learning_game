from typing import Dict
from app.models.profile import ProfileModel, LevelEnum


class TestProfile:

    def test_profile_json(self, app):
        """
        Creates profile model and checks the returned json
        """
        model = ProfileModel(user_level=LevelEnum.A2)
        model.save_to_db()

        saved = ProfileModel.find_by_id(model.id)
        assert saved is not None

        expected = {
            "id": saved.id,
            "user_level": "A2",
            "preferences": "",
        }
        actual: Dict = saved.json()
        assert actual == expected
