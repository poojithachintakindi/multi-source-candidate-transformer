"""Extract raw records from multiple source types.
Each extractor returns a list of raw dicts and attaches a `source` tag.
"""
import csv
import json
from typing import List, Dict


def extract_recruiter_csv(path: str) -> List[Dict]:
    out = []
    with open(path, newline='', encoding='utf-8') as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            row['source'] = 'recruiter_csv'
            out.append(row)
    return out


def extract_ats_json(path: str) -> List[Dict]:
    with open(path, encoding='utf-8') as fh:
        data = json.load(fh)
    out = []
    if isinstance(data, dict):
        # single record or envelope
        items = data.get('candidates') or [data]
    else:
        items = data
    for it in items:
        if isinstance(it, dict):
            it['source'] = 'ats_json'
            out.append(it)
    return out


def extract_text(path: str) -> List[Dict]:
    # naive key:value parsing falling back to whole text
    out = []
    with open(path, encoding='utf-8') as fh:
        txt = fh.read()
    rec = {'source': 'text', 'raw_text': txt}
    # try simple lines like 'Name: John Doe'
    for line in txt.splitlines():
        if ':' in line:
            k, v = line.split(':', 1)
            rec[k.strip().lower()] = v.strip()
    out.append(rec)
    return out
