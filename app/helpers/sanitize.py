"""Sanitize Helper"""
from app.constants.vocab import EXERCISE_VOCAB

def normalize_exercise_name(raw_name) -> str:
    """Normalize exercise name with vocabulary to receive cannonical by aliases"""
    raw = raw_name.lower().strip()

    for canonical, data in EXERCISE_VOCAB.items():
        if raw == canonical:
            return canonical

        for alias in data["aliases"]:
            if raw == alias.lower():
                return canonical

    return raw
