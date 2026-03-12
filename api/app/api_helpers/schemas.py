EXPLANATION_SCHEMA = {
    "type": "object",
    "required": [
        "mode",
        "word",
        "partOfSpeech",
        "pronunciation",
        "definition",
        "translation",
        "examples",
        "forms"
    ],
    "properties": {
        "mode": {"type": "string"},
        "word": {"type": "string"},
        "partOfSpeech": {"type": "string"},
        "pronunciation": {"type": "string"},
        "definition": {"type": "string"},
        "translation": {"type": "string"},
        "examples": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["de", "en"],
                "properties": {
                    "de": {"type": "string"},
                    "en": {"type": "string"}
                }
            }
        },
        "forms": {
            "type": "object",
            "required": ["praesens", "praeteritum", "perfekt"],
            "properties": {
                "praesens": {"type": "string"},
                "praeteritum": {"type": "string"},
                "perfekt": {"type": "string"}
            }
        }
    }
}
