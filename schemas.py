pet = {
    "type": "object",
    "required": ["name", "type"],
    "properties": {
        "id": {
            "type": "integer"
        },
        "name": {
            "type": "string"
        },
        "type": {
            "type": "string",
            "enum": ["cat", "dog", "fish", "horse", "bird"]
        },
        "status": {
            "type": "string",
            "enum": ["available", "sold", "pending"]
        },
    }
}

order = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "pet_id": {"type": "number"},
        "message": {"type": "string"},
    },
    "required": ["id", "pet_id"]
}
