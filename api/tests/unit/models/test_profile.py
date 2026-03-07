from typing import Dict
from app.models.profile import ProfileModel
from app.enums import LevelEnum


class TestProfile:

    def test_profile_json(self, db_session):
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

    def test_profile_find_by_id_not_found(self, db_session):
        """
        Ensure None is returned if profile does not exist
        """
        result = ProfileModel.find_by_id(9999)
        assert result is None

    def test_profile_find_all(self, db_session):
        """
        Ensure multiple profiles can be retrieved
        """
        p1 = ProfileModel(user_level=LevelEnum.A1)
        p2 = ProfileModel(user_level=LevelEnum.B1)

        p1.save_to_db()
        p2.save_to_db()

        profiles = ProfileModel.find_all()

        assert len(profiles) == 2

    def test_profile_get_user_level(self, db_session):
        """
        Ensure get_user_level returns correct enum
        """
        model = ProfileModel(user_level=LevelEnum.B2)
        model.save_to_db()

        saved = ProfileModel.find_by_id(model.id)

        assert saved.get_user_level() == LevelEnum.B2.value

    def test_profile_preferences(self, db_session):
        """
        Ensure preferences field is saved correctly
        """
        model = ProfileModel(
            user_level=LevelEnum.A2,
            preferences="dark_mode=true"
        )

        model.save_to_db()

        saved = ProfileModel.find_by_id(model.id)

        assert saved.preferences == "dark_mode=true"
