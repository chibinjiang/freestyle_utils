import json


def is_json(text):
    try:
        json.loads(text)
        return True
    except Exception:
        return False

