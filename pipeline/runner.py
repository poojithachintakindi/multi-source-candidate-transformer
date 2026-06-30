"""Orchestrate pipeline: detect -> extract -> normalize -> merge -> confidence -> project -> validate"""
import os
from typing import List, Dict
from . import detect, extract, normalize, merge, confidence, schema, project


EXTRACTOR_MAP = {
    'recruiter_csv': extract.extract_recruiter_csv,
    'ats_json': extract.extract_ats_json,
    'text': extract.extract_text,
}


def run(paths: List[str], config: Dict) -> List[Dict]:
    raw = []
    for p in paths:
        content = None
        try:
            with open(p, 'rb') as fh:
                content = fh.read()
        except Exception:
            content = None
        src = detect.detect_source(p, content)
        extractor = EXTRACTOR_MAP.get(src)
        if extractor:
            records = extractor(p)
            raw.extend(records)
        else:
            # unknown, treat as text
            raw.extend(extract.extract_text(p))

    # normalize in-place mild mapping
    for r in raw:
        # phones
        r_phone = r.get('phone') or r.get('Phone')
        if r_phone:
            r['phone'] = normalize.normalize_phone(r_phone)
            r['phone_normalized'] = True
        # skills
        skills = r.get('skills') or r.get('Skills') or r.get('skill')
        r['skills'] = normalize.normalize_skills(skills)
        # country/location
        loc = r.get('location') or r.get('country')
        if loc:
            r['location'] = normalize.normalize_country(loc)

    merged = merge.merge_records(raw)
    # compute confidence
    out = []
    for rec in merged:
        rec['confidence'] = confidence.record_confidence(rec)
        ok, msg = schema.validate(rec)
        rec['valid'] = ok
        rec['validation_msg'] = msg
        out.append(rec)

    # projection
    projected = [project.project_record(r, config) for r in out]
    return projected
