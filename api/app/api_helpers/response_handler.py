import json
from jsonschema import validate, ValidationError


class ResponseHandler:

    @staticmethod
    def is_json(text: str) -> bool:
        try:
            json.loads(text)
            return True
        except json.JSONDecodeError:
            return False

    @staticmethod
    def validate_json(text: str, schema: dict) -> bool:
        try:
            data = json.loads(text)
            validate(instance=data, schema=schema)
            return True
        except (json.JSONDecodeError, ValidationError):
            return False
