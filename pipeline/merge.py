"""Merge raw/normalized records into canonical records with provenance."""
from typing import List, Dict
from difflib import SequenceMatcher


SOURCE_PRIORITY = {
    'ats_json': 3,
    'recruiter_csv': 2,
    'text': 1,
    'unknown': 0,
}


def similar(a: str, b: str) -> float:
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def merge_records(records: List[Dict]) -> List[Dict]:
    groups = []
    for r in records:
        placed = False
        for grp in groups:
            # match by normalized email first
            if r.get('email') and grp.get('email') and r['email'].lower() == grp['email'].lower():
                grp = resolve_conflicts(grp, r)
                placed = True
                break
            # else fuzzy name
            if similar(r.get('name', ''), grp.get('name', '')) > 0.85:
                grp = resolve_conflicts(grp, r)
                placed = True
                break
        if not placed:
            groups.append(r.copy())
    # ensure provenance list and basic normal form
    out = []
    for g in groups:
        g.setdefault('sources', [])
        if g.get('source') and g['source'] not in g['sources']:
            g['sources'].append(g['source'])
        out.append(g)
    return out


def resolve_conflicts(a: Dict, b: Dict) -> Dict:
    # prefer field value from higher priority source; keep provenance
    sa = a.get('source', 'unknown')
    sb = b.get('source', 'unknown')
    pa = SOURCE_PRIORITY.get(sa, 0)
    pb = SOURCE_PRIORITY.get(sb, 0)
    out = a.copy()
    for k, v in b.items():
        if k in ('source', 'sources'):
            continue
        if v is None or v == '':
            continue
        if k not in out or out.get(k) in (None, ''):
            out[k] = v
        else:
            # conflict
            if pb >= pa:
                out[k] = v
    # merge sources
    out.setdefault('sources', [])
    for s in (a.get('source'), b.get('source')):
        if s and s not in out['sources']:
            out['sources'].append(s)
    return out
