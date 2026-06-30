"""Canonical schema and simple validator."""
from typing import Dict, Any

CANONICAL_FIELDS = {
    "id": str,
    "name": str,
    "email": str,
    "phone": str,
    "company": str,
    "title": str,
    "skills": list,
    "location": str,
    "sources": list,  # provenance
    "confidence": float,
}


def validate(record: Dict[str, Any]) -> (bool, str):
    """Basic validation: required `name` or `email`, types for known fields."""
    if not record.get("email") and not record.get("name"):
        return False, "missing name and email"
    for k, t in CANONICAL_FIELDS.items():
        if k in record and record[k] is not None:
            if not isinstance(record[k], t):
                return False, f"field {k} expected {t.__name__} got {type(record[k]).__name__}"
    return True, "ok"
