"""Compute confidence scores from sources and agreement."""
from typing import Dict, List

SOURCE_TRUST = {
    'ats_json': 0.9,
    'recruiter_csv': 0.7,
    'text': 0.4,
}


def field_confidence(field: str, record: Dict) -> float:
    srcs: List[str] = record.get('sources', [])
    if not srcs:
        return 0.2
    # max trust among sources that provided the field
    best = 0.0
    for s in srcs:
        trust = SOURCE_TRUST.get(s, 0.2)
        best = max(best, trust)
    # if normalized flag present, boost slightly
    norm = record.get(f"{field}_normalized", False)
    conf = best + (0.05 if norm else 0.0)
    return min(conf, 1.0)


def record_confidence(record: Dict) -> float:
    # average of important fields
    fields = ['name', 'email', 'phone', 'skills']
    vals = []
    for f in fields:
        vals.append(field_confidence(f, record))
    return sum(vals) / max(1, len(vals))
